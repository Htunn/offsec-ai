# offsec-ai — Enterprise-Grade Features

This document covers the engineering features added in v2.2.0 that make offsec-ai suitable
for production and enterprise deployment: structured logging, centralised configuration,
exception hierarchy, CI/CD security gates, and supply-chain hardening.

---

## Exception Hierarchy

All package exceptions inherit from `OffsecError`, enabling broad-or-specific catch blocks:

```python
from offsec_ai.exceptions import (
    OffsecError,            # base class — catch everything
    ScanError,              # unexpected scan-operation failure
    ConfigError,            # invalid/missing configuration at startup
    NetworkError,           # DNS, connection, or timeout failure
    TargetUnreachableError, # target unreachable after retries (subclass of NetworkError)
    AuthorizationRequired,  # active attack attempted without authorization
)
```

### Usage pattern

```python
from offsec_ai.exceptions import ScanError, TargetUnreachableError, OffsecError

try:
    result = await scanner.scan("target.example.com")
except TargetUnreachableError as exc:
    logger.warning("host down — skipping: %s", exc)
except ScanError as exc:
    logger.error("scan error: %s", exc)
except OffsecError as exc:
    logger.error("offsec-ai error: %s", exc)
```

`AuthorizationRequired` is raised **before any network traffic** when an attack module is
instantiated without `authorized=True`, preventing accidental active testing.

---

## Configuration Management

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | OpenAI API key (SecretStr) |
| `ANTHROPIC_API_KEY` | — | Anthropic API key (SecretStr) |
| `GEMINI_API_KEY` | — | Google Gemini API key (SecretStr) |
| `OFFSEC_LLM_BASE_URL` | — | Custom OpenAI-compatible base URL |
| `OFFSEC_LLM_MODEL` | — | Model name override |
| `OFFSEC_DEFAULT_TIMEOUT` | `15.0` | Per-request timeout in seconds |
| `OFFSEC_DEFAULT_CONCURRENT` | `50` | Max concurrent requests |
| `OFFSEC_MAX_RETRIES` | `3` | Retry count on transient errors |
| `OFFSEC_RETRY_DELAY` | `1.0` | Base retry delay (seconds, exponential back-off) |
| `OFFSEC_LOG_LEVEL` | `INFO` | Logging level |
| `OFFSEC_LOG_FORMAT` | `text` | `text` or `json` |
| `OFFSEC_AUDIT_LOG_FILE` | — | Path for rotating audit log |

### `.env` file

Place a `.env` file in your working directory (or specify its path) — it is loaded
automatically by `pydantic-settings`:

```dotenv
OPENAI_API_KEY=sk-...
OFFSEC_DEFAULT_TIMEOUT=20.0
OFFSEC_LOG_FORMAT=json
OFFSEC_AUDIT_LOG_FILE=/var/log/offsec-ai/audit.log
```

### Accessing config in code

```python
from offsec_ai.config import get_config, reset_config

cfg = get_config()                         # cached singleton
print(cfg.default_timeout)                # 20.0 (from env/file)
print(cfg.openai_api_key)                 # SecretStr('**********')
print(cfg.openai_api_key.get_secret_value())  # actual key — only when needed

# In tests: reinitialise from a fresh environment
reset_config()
```

API keys are stored as `pydantic.SecretStr` — they are **never serialised, logged, or
included in exception messages** as plain text.

---

## Structured Logging

### Setup

```python
from offsec_ai.log_config import configure_logging

# Human-readable (default)
configure_logging(level="INFO", fmt="text")

# Machine-parseable JSON — recommended for production / SIEM ingestion
configure_logging(level="INFO", fmt="json")
```

JSON log lines look like:

```json
{
  "timestamp": "2026-06-30T12:34:56.789Z",
  "level": "INFO",
  "logger": "offsec_ai.core.mcp_scanner",
  "correlation_id": "a1b2c3d4-...",
  "message": "MCP scan completed",
  "target": "https://mcp.example.com/mcp",
  "tools_found": 8,
  "vuln_count": 6
}
```

### Correlation IDs

Every scan or attack invocation should call `new_correlation_id()` once. All log lines
emitted during that operation carry the same `correlation_id` field, enabling end-to-end
tracing across async tasks.

```python
from offsec_ai.log_config import new_correlation_id, get_correlation_id

cid = new_correlation_id()          # sets a new UUID in the current async context
result = await scanner.scan(...)    # all internal log calls include this cid

print(get_correlation_id())         # same UUID — read from current context
```

### Audit logging

The audit logger records every authorized attack invocation. It always emits JSON and
can be persisted to a rotating file via `OFFSEC_AUDIT_LOG_FILE`.

```python
from offsec_ai.log_config import audit_log

# Emitted automatically by attack modules; call manually for custom events:
audit_log(
    "custom_scan_completed",
    target="192.168.1.10",
    module="OpenClawScanner",
    findings=3,
)
```

Audit log entry example:

```json
{
  "timestamp": "2026-06-30T12:34:56.789Z",
  "level": "INFO",
  "logger": "offsec_ai.audit",
  "event": "attack_started",
  "target": "https://api.example.com/v1/chat/completions",
  "module": "LLMConversationAttacker",
  "mode": "crescendo",
  "correlation_id": "a1b2c3d4-..."
}
```

---

## CI/CD Security Gates

### What runs on every push / PR

| Step | Tool | Purpose |
|------|------|---------|
| Linting | `ruff` | Fast linting + format checking |
| Type checking | `mypy --strict` | Full static type analysis |
| Unit tests | `pytest` with coverage | Functional correctness |
| Dependency CVEs | `pip-audit` | Known vulnerabilities in dependencies |
| SAST | `bandit` | Python-specific security issues (hardcoded secrets, dangerous calls) |
| Secret detection | `detect-secrets` | Credential/API key scanning against baseline |
| CodeQL | GitHub CodeQL | Deep semantic security analysis (Python + Actions) |

### Coverage threshold

Tests are configured with `--cov-fail-under` — the build fails if coverage drops below
the defined threshold. Run locally:

```bash
make test-cov     # runs pytest with coverage report
make ci           # full CI sequence: ruff + mypy + test-cov + bandit + audit
```

### Pre-commit hooks

Install once:

```bash
pip install pre-commit
pre-commit install
```

Hooks run on every `git commit`: ruff, black, isort, mypy, bandit, detect-secrets.

### Dependabot

`.github/dependabot.yml` is configured to open PRs weekly for:
- Python dependency updates (`pip`)
- GitHub Actions version bumps

---

## Supply-Chain Security (v2.2.0+)

| Artefact | How |
|----------|-----|
| **SBOM** | CycloneDX SBOM generated on every release and attached to the GitHub release |
| **Signed package** | PyPI package signed via `cosign` keyless signing (sigstore OIDC) |
| **SLSA provenance** | Build provenance attestation generated by `publish.yml` |
| **Docker image scan** | Trivy scans the built image before push; blocks on HIGH/CRITICAL CVEs |

Verify the PyPI package signature:

```bash
pip install sigstore
sigstore verify pypi --bundle offsec_ai-2.2.0-py3-none-any.whl.bundle \
    offsec_ai-2.2.0-py3-none-any.whl
```

---

## Docker

### Running with JSON logging

```bash
docker run --rm \
  -e OFFSEC_LOG_FORMAT=json \
  -e OFFSEC_LOG_LEVEL=INFO \
  -e OFFSEC_AUDIT_LOG_FILE=/data/audit.log \
  -v "$(pwd)/data:/data" \
  htunnthuthu/offsec-ai:latest \
  mcp-scan https://mcp.example.com/mcp
```

### Environment variable injection

```bash
docker run --rm \
  --env-file .env \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge
```

The Docker image version is dynamically derived from `pyproject.toml` at build time via
`importlib.metadata` — no hardcoded version strings in the Dockerfile.

---

## Security Policy

See [SECURITY.md](../SECURITY.md) for:
- Supported versions and end-of-life dates
- Vulnerability reporting process (private disclosure)
- Expected response timeline
- Out-of-scope items (e.g. DoS via intentional payload abuse)
