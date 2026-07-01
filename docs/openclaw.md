# offsec-ai — OpenClaw Gateway Security

[OpenClaw](https://github.com/openclaw/openclaw) is a personal AI assistant gateway that bridges messaging platforms (Telegram, Discord, Slack, etc.) to LLM backends. Because OpenClaw instances are often self-hosted and internet-exposed, misconfigurations can lead to unauthenticated LLM access, conversation history disclosure, SSRF, and prompt injection attack surfaces.

`offsec-ai` ships a passive **scanner** and an authorization-gated **attacker** for assessing OpenClaw deployments.

---

## Quick Start

```bash
# Passive scan — fingerprint and report misconfigurations
offsec-ai openclaw-scan 192.168.1.10

# Custom port / TLS
offsec-ai openclaw-scan gateway.example.com --port 18789 --tls

# With bearer token (authenticated scan)
offsec-ai openclaw-scan gateway.example.com \
    --header "Authorization: Bearer <token>"

# With LLM judge for enriched finding triage
offsec-ai openclaw-scan 192.168.1.10 --llm-judge

# Export JSON report
offsec-ai openclaw-scan 192.168.1.10 --format json --output report.json

# Active attack (requires explicit authorization flag)
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization

# Deep mode — message injection + WebSocket + SSRF probes
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep

# Deep mode with LLM judge for attack-path narrative
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep --llm-judge

# Export attack report
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization \
    --mode deep --format json --output attack.json
```

---

## Scanner (`openclaw-scan`)

The scanner performs five sequential phases with no active exploitation:

```
Phase 1 — Fingerprint
    Probe well-known paths (/health, /status, /api/v1/status, ...)
    Match response headers and JSON body against OpenClaw signatures
    Identify gateway version and ID from /health body

Phase 2 — Endpoint Enumeration
    Probe all known API paths (/api/v1/*, /ws/*, /webhooks, ...)
    Record accessible (non-401/403/404) endpoints
    Flag response bodies containing API keys, tokens, or secrets

Phase 3 — Authentication Posture
    Detect unauthenticated REST API access (no auth required on /api/v1/*)
    Probe for unauthenticated WebSocket upgrade on /ws and /api/v1/ws

Phase 4 — Configuration Assessment
    Parse /api/v1/config for DM (direct message) policy
    Detect open DM policy: gateway accepts messages from any channel user
    Detect insecure sandbox modes: disabled, none, off, false

Phase 5 — CVE / Misconfiguration Matching
    Cross-reference accessible paths and config against advisory database
    Produce severity-ranked vulnerability list
```

### Advisory Database

| ID | Severity | Finding |
|----|----------|---------|
| OCL-ADV-001 | **Critical** | Unauthenticated REST API access |
| OCL-ADV-002 | **High** | Open DM policy — all channels accepted |
| OCL-ADV-003 | **High** | Sandbox mode disabled |
| OCL-ADV-004 | **High** | Unauthenticated WebSocket connection |
| OCL-ADV-005 | Medium | Health/status endpoint information disclosure |
| OCL-ADV-006 | Medium | Webhook automation SSRF risk |
| OCL-ADV-007 | Medium | Session history and message log exposure |
| OCL-ADV-008 | Medium | Model API key leakage via config endpoint |
| OCL-ADV-009 | Low | Gateway version fingerprinting |
| OCL-ADV-010 | Info | OpenClaw instance fingerprint |

### Sample Output

```
╔══════════════════════════════════════════════╗
║     OpenClaw Gateway Security Scan Report    ║
╚══════════════════════════════════════════════╝

Target        : 192.168.1.10:18789
Is OpenClaw   : ✓
Version       : 2026.6.10
Gateway ID    : gw-abc123
Channels      : telegram, discord
Scan duration : 1.23s

Accessible Endpoints (4)
  /health               200  [sensitive: openclaw_version]
  /api/v1/status        200
  /api/v1/config        200  [sensitive: apiKey]
  /api/v1/sessions/history  200

Authentication Posture
  API auth required    : No  ← CRITICAL
  WebSocket auth req.  : No  ← HIGH

Vulnerabilities (6)
  [CRITICAL] OCL-ADV-001  Unauthenticated REST API Access
  [HIGH]     OCL-ADV-002  Open DM Policy — All Channels Accepted
  [HIGH]     OCL-ADV-003  Sandbox Mode Disabled
  [HIGH]     OCL-ADV-004  Unauthenticated WebSocket Connection
  [MEDIUM]   OCL-ADV-007  Session History and Message Log Exposure
  [MEDIUM]   OCL-ADV-008  Model API Key Leakage via Config Endpoint
```

---

## Attacker (`openclaw-attack`)

> **Legal reminder:** Only run against systems you own or have explicit written permission to test. The attacker prints an authorization banner on every run.

The `--i-have-authorization` flag is **required** — the CLI will exit immediately without it.

### Modes

| Mode | Probes |
|------|--------|
| `safe` (default) | Unauthenticated API endpoint probes across all `/api/v1/*` paths |
| `deep` | Safe probes + message injection, WebSocket upgrade, SSRF via webhooks, prompt-injection payload report |

> **Note on prompt injection:** In deep mode, a prompt-injection payload report is generated (listing recommended payloads) but payloads are **not automatically sent** to the gateway's LLM backend. This prevents unintended model manipulation during automated scans. Review the report and send payloads manually as needed.

### CLI Options

| Option | Description |
|--------|-------------|
| `--i-have-authorization` | Required. Confirms authorized testing. |
| `--mode safe\|deep` | Attack depth (default: `safe`) |
| `--port INT` | Gateway port (default: `18789`) |
| `--tls` | Use HTTPS |
| `--header KEY:VALUE` | Extra HTTP header (repeatable) |
| `--timeout FLOAT` | Per-request timeout in seconds (default: `15.0`) |
| `--llm-judge` | Use LLM judge to build attack-path narrative for succeeded attacks |
| `--format console\|json` | Output format (default: `console`) |
| `--output FILE` | Write results to file |

---

## Python API

### Passive Scan

```python
import asyncio
from offsec_ai.core.openclaw_scanner import OpenClawScanner

async def main():
    scanner = OpenClawScanner(
        target="192.168.1.10",
        port=18789,
        timeout=15.0,
        use_tls=False,
        headers={"Authorization": "Bearer <token>"},  # optional
        judge=LLMJudge.from_env(),  # optional: enriches MEDIUM/LOW findings
    )
    result = await scanner.scan()

    if not result.is_openclaw:
        print(f"Not an OpenClaw gateway: {result.error}")
        return

    print(f"Version : {result.server_info.version}")
    print(f"Channels: {result.server_info.connected_channels}")
    print(f"Critical: {len(result.critical_vulns)}")
    print(f"High    : {len(result.high_vulns)}")

    for vuln in result.all_vulns:
        print(f"  [{vuln.severity.value.upper():8}] {vuln.vuln_id}: {vuln.title}")
        if vuln.evidence:
            print(f"             Evidence: {vuln.evidence}")

asyncio.run(main())
```

### Active Attack

```python
import asyncio
from offsec_ai.core.openclaw_scanner import OpenClawScanner
from offsec_ai.core.openclaw_attacker import OpenClawAttacker, AuthorizationRequired

async def main():
    # Step 1 — passive scan to guide the attack
    scanner = OpenClawScanner(target="192.168.1.10", port=18789)
    scan_result = await scanner.scan()

    if not scan_result.is_openclaw:
        print("Not an OpenClaw gateway.")
        return

    # Step 2 — active attack (authorized=True required)
    try:
        attacker = OpenClawAttacker(authorized=True, judge=LLMJudge.from_env())
    except AuthorizationRequired:
        print("Authorization not granted.")
        return

    report = await attacker.attack(
        target="192.168.1.10",
        port=18789,
        mode="deep",           # "safe" | "deep"
        scan_result=scan_result,
    )

    print(f"Attacks run   : {len(report.attack_results)}")
    print(f"Successful    : {len(report.successful_attacks)}")
    print(f"Critical hits : {len(report.critical_successes)}")

    for r in report.successful_attacks:
        sev = r.severity.value.upper()
        print(f"  [{sev:8}] {r.attack_id}: {r.evidence or 'no evidence captured'}")

    if report.prompt_injection_report:
        print(f"\nPrompt-injection payload report ({len(report.prompt_injection_report)} payloads)")
        print("  Review and send manually — not auto-executed.")

asyncio.run(main())
```

### Export Results

```python
import json

# Scan result to JSON file
with open("scan.json", "w") as f:
    json.dump(result.model_dump(mode="json"), f, indent=2)

# Attack report to JSON file
with open("attack.json", "w") as f:
    json.dump(report.model_dump(mode="json"), f, indent=2)
```

---

## LLM Judge Integration

Pass `--llm-judge` (CLI) or `judge=LLMJudge.from_env()` (Python API) to enable AI-assisted
triage. The judge evaluates each **MEDIUM** and **LOW** finding and annotates it with:

```python
class OpenClawVulnerability(BaseModel):
    # ... standard fields ...
    llm_confidence: float | None = None   # 0.0–1.0 confidence score
    llm_reasoning: str = ""               # judge's explanation
```

Findings with `llm_confidence > 0.7` and `vulnerable=True` are automatically upgraded:
`LOW` → `MEDIUM`. The attacker's `_enrich_with_llm()` appends an attack-path narrative to
the first succeeded result's `evidence` field.

```bash
# Configure provider — any one env var is sufficient
# Priority: Gemini > Anthropic > OpenAI
export GEMINI_API_KEY="AIza..."       # 1st priority
export ANTHROPIC_API_KEY="sk-ant-..." # 2nd priority
export OPENAI_API_KEY="sk-..."        # 3rd priority

# Or use a local OpenAI-compatible endpoint (Ollama, LM Studio, etc.)
export OFFSEC_LLM_BASE_URL="http://localhost:11434/v1"
export OFFSEC_LLM_MODEL="llama3"
```

---

## Remediation Guide

### OCL-ADV-001 — Unauthenticated REST API

Require authentication on all `/api/v1/*` routes:

```yaml
# openclaw config (config.yaml)
api:
  auth:
    enabled: true
    type: bearer          # or "basic", "oauth2"
    token_env: OPENCLAW_API_TOKEN
```

Then set `OPENCLAW_API_TOKEN` to a strong random secret and restrict access to the port at the network level (firewall / reverse proxy).

### OCL-ADV-002 — Open DM Policy

Restrict which channel users can trigger the AI assistant:

```yaml
dm_policy:
  mode: allowlist          # "allowlist" | "denylist" | "open"
  allowed_users:
    - "@admin"
    - "@your-username"
```

### OCL-ADV-003 — Sandbox Mode Disabled

Enable the sandbox to restrict what the LLM can execute:

```yaml
sandbox:
  mode: "non-main"         # "non-main" (recommended) | "all"
```

Never set `mode: disabled`, `mode: none`, or `mode: off` in production.

### OCL-ADV-004 — Unauthenticated WebSocket

Apply the same authentication requirement to WebSocket upgrade requests. Place the gateway behind a reverse proxy (nginx/Caddy) that enforces auth before proxying the upgrade:

```nginx
location /ws {
    auth_request /auth;
    proxy_pass http://localhost:18789;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### OCL-ADV-006 — SSRF via Webhooks

Add a URL allowlist and block RFC 1918 ranges in the OpenClaw webhook configuration:

```yaml
webhooks:
  url_allowlist:
    - "https://hooks.slack.com/**"
    - "https://discord.com/api/webhooks/**"
  block_private_ranges: true
```

### General Hardening Checklist

- [ ] API authentication enabled
- [ ] DM policy set to `allowlist` with named users
- [ ] Sandbox mode set to `non-main` or `all`
- [ ] Gateway not directly internet-exposed (sit behind reverse proxy)
- [ ] `/health`, `/status` restricted to internal network
- [ ] API keys not returned in `/api/v1/config` responses
- [ ] Session history endpoints require per-user auth
- [ ] Webhook URL allowlist configured with private range blocking
- [ ] TLS enforced end-to-end (reverse proxy → gateway)
