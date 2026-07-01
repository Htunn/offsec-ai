# offsec-ai — Quick Start Guide

## Installation

```bash
# Core package
pip install offsec-ai

# With LLM judge support (OpenAI / Anthropic)
pip install "offsec-ai[ai]"

# With Google Gemini judge
pip install "offsec-ai[ai,gemini]"
```

## Configuration (optional)

Set environment variables for LLM-based features and runtime tuning:

```bash
# LLM provider keys (any one is sufficient for the judge)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."

# Custom OpenAI-compatible endpoint
export OFFSEC_LLM_BASE_URL="https://my-llm-proxy.internal/v1"
export OFFSEC_LLM_MODEL="gpt-4o"

# Operational tuning
export OFFSEC_DEFAULT_TIMEOUT=20.0   # per-request timeout (seconds)
export OFFSEC_LOG_FORMAT=json        # structured JSON logging
export OFFSEC_AUDIT_LOG_FILE=/var/log/offsec-ai/audit.log
```

Or create a `.env` file in your working directory — it is loaded automatically.

## Basic Usage

### Command Line

```bash
# ── Infrastructure ────────────────────────────────────────────────────
offsec-ai scan example.com
offsec-ai scan example.com --ports 80,443,8080
offsec-ai l7-check example.com
offsec-ai full-scan example.com --output results.json
offsec-ai cert-check example.com
offsec-ai mtls-check example.com

# ── Web OWASP Top 10 ──────────────────────────────────────────────────
offsec-ai owasp-scan example.com
offsec-ai owasp-scan example.com --mode deep --output owasp.json

# ── AI / LLM OWASP Top 10 (black-box) ────────────────────────────────
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions \
    --api-key "$MY_KEY" --llm-judge

# ── Active LLM attack suite (requires --i-have-authorization) ─────────
offsec-ai llm-attack https://api.example.com/v1/chat/completions \
    --i-have-authorization
offsec-ai llm-attack https://api.example.com/v1/chat/completions \
    --i-have-authorization --mode jailbreak
offsec-ai llm-attack https://api.example.com/v1/chat/completions \
    --i-have-authorization --mode deep    # all techniques; auto-executes payloads

# ── MCP endpoint security scanner ─────────────────────────────────────
offsec-ai mcp-scan https://mcp.example.com/mcp
offsec-ai mcp-scan https://mcp.example.com/mcp --no-tls-verify  # self-signed CA
offsec-ai mcp-scan https://mcp.example.com/mcp --output report.json

# MCP attacker (requires --i-have-authorization)
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization --mode deep

# ── OpenClaw gateway scanner ──────────────────────────────────────────
offsec-ai openclaw-scan 192.168.1.10
offsec-ai openclaw-scan gateway.example.com --port 18789 --tls \
    --format json --output report.json

# OpenClaw attacker (requires --i-have-authorization)
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep

# ── Kubernetes cluster security scanner ───────────────────────────────
offsec-ai k8s-scan 192.168.1.100
offsec-ai k8s-scan k8s.example.com --port 6443 --port 10250 --llm-judge
offsec-ai k8s-scan 192.168.1.100 --format json --output k8s-scan.json

# Kubernetes attacker (requires --i-have-authorization)
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization --mode deep
```

### Python API

```python
import asyncio
from offsec_ai import (
    PortChecker, L7Detector, CertificateAnalyzer, MTLSChecker,
    LLMOwaspScanner, MCPScanner, MCPAttacker, LLMJudge,
)
from offsec_ai.core.openclaw_scanner import OpenClawScanner
from offsec_ai.core.openclaw_attacker import OpenClawAttacker
from offsec_ai.core.llm_conversation_attacker import LLMConversationAttacker
from offsec_ai.core.guardrail_bench import GuardrailBench

async def main():
    # Infrastructure: port scanning
    scanner = PortChecker()
    result = await scanner.scan_host("example.com", [80, 443, 22])
    print(f"Open ports: {[p.port for p in result.open_ports]}")

    # L7 / WAF detection
    detector = L7Detector()
    l7 = await detector.detect("example.com")
    if l7.is_protected:
        print(f"WAF/CDN: {l7.primary_protection.service.value}")

    # AI / LLM OWASP Top 10 scanner
    llm_scanner = LLMOwaspScanner(
        endpoint="https://api.example.com/v1/chat/completions",
        api_key="sk-...",
    )
    report = await llm_scanner.scan()
    print(f"LLM findings: {len(report.findings)}")

    # MCP security scan (passive); pass verify_tls=False for self-signed certs
    mcp = MCPScanner("https://mcp.example.com/mcp", verify_tls=True)
    mcp_result = await mcp.scan()
    print(f"MCP tools exposed: {len(mcp_result.tools)}")
    print(f"Auth required: {mcp_result.auth_posture.requires_auth}")

    # OpenClaw gateway scan (passive)
    ocl_scanner = OpenClawScanner(target="192.168.1.10", port=18789)
    ocl_result = await ocl_scanner.scan()
    if ocl_result.is_openclaw:
        print(f"OpenClaw {ocl_result.server_info.version} — "
              f"{len(ocl_result.critical_vulns)} critical, "
              f"{len(ocl_result.high_vulns)} high")

    # OpenClaw active attack (authorized=True required)
    ocl_attacker = OpenClawAttacker(authorized=True)
    attack_report = await ocl_attacker.attack(target="192.168.1.10", mode="deep")
    print(f"Successful attacks: {len(attack_report.successful_attacks)}")

    # Multi-turn LLM conversation attack (authorized=True required)
    conv_attacker = LLMConversationAttacker(authorized=True)
    conv_result = await conv_attacker.attack(
        endpoint="https://api.example.com/v1/chat/completions",
        api_key="sk-...",
        mode="crescendo",
    )
    print(f"Jailbreak succeeded: {conv_result.jailbreak_detected}")
    for turn in conv_result.turns:
        print(f"  Turn {turn.turn_number}: escalation={turn.escalation_detected}")

    # Guardrail benchmarking
    bench = GuardrailBench(
        endpoint="https://api.example.com/v1/chat/completions",
        api_key="sk-...",
    )
    bench_result = await bench.run()
    print(f"Guardrail coverage grade: {bench_result.grade}")
    for cat, blocked in bench_result.category_block_rates.items():
        print(f"  {cat}: {blocked:.0%} blocked")

asyncio.run(main())
```

## Enterprise Features

### Structured Logging

```python
from offsec_ai.log_config import configure_logging, new_correlation_id, audit_log

# Enable JSON logging (machine-parseable, suitable for SIEM ingestion)
configure_logging(level="INFO", fmt="json")

# Each scan/attack gets a unique correlation ID — all log lines carry it
cid = new_correlation_id()
result = await scanner.scan(...)

# Explicit audit log entry (always JSON; optionally rotated to file)
audit_log("scan_completed", target="192.168.1.10", findings=3, correlation_id=cid)
```

### Config Validation

```python
from offsec_ai.config import get_config

cfg = get_config()
print(cfg.default_timeout)          # 15.0 (or OFFSEC_DEFAULT_TIMEOUT)
print(cfg.openai_api_key)           # SecretStr — never logs as plain text
print(cfg.log_format)               # "text" | "json"
```

### Exception Handling

```python
from offsec_ai.exceptions import (
    OffsecError, ScanError, NetworkError,
    TargetUnreachableError, AuthorizationRequired,
)

try:
    result = await scanner.scan("target.example.com")
except TargetUnreachableError as exc:
    logger.warning("host down: %s", exc)
except ScanError as exc:
    logger.error("scan failed: %s", exc)
except OffsecError as exc:
    logger.error("offsec-ai error: %s", exc)
```

## Output Formats

```bash
# JSON
offsec-ai scan example.com --output scan_results.json

# CSV (where supported)
offsec-ai owasp-scan example.com --format csv --output findings.csv
```

```python
import json
# All result models are pydantic v2 — JSON-serialisable
data = result.model_dump(mode="json")
with open("results.json", "w") as f:
    json.dump(data, f, indent=2)
```

## Security Considerations

- Only scan systems you own or have **explicit written permission** to test
- Active attack commands (`llm-attack`, `mcp-attack`, `openclaw-attack`) require `--i-have-authorization`
- API keys are stored as `SecretStr` — they will not appear in logs or tracebacks
- Audit log (`OFFSEC_AUDIT_LOG_FILE`) records every authorized attack invocation with target, mode, operator, and timestamp


## Basic Usage

### Command Line

```bash
# Infrastructure scanning
offsec-ai scan example.com
offsec-ai scan example.com --ports 80,443,8080
offsec-ai l7-check example.com
offsec-ai full-scan example.com --output results.json
offsec-ai cert-check example.com
offsec-ai mtls-check example.com

# AI / LLM OWASP Top 10 black-box scanner
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions \
    --api-key "$MY_KEY" --llm-judge

# MCP endpoint security scanner (passive)
offsec-ai mcp-scan https://mcp.example.com/mcp
offsec-ai mcp-scan https://mcp.example.com/mcp --output report.json

# MCP attacker (requires --i-have-authorization flag)
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization

# OpenClaw gateway scanner (passive)
offsec-ai openclaw-scan 192.168.1.10
offsec-ai openclaw-scan gateway.example.com --port 18789 --tls --format json --output report.json

# OpenClaw attacker (requires --i-have-authorization flag)
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep
```

### Python API

```python
import asyncio
from offsec_ai import (
    PortChecker, L7Detector, CertificateAnalyzer, MTLSChecker,
    LLMOwaspScanner, MCPScanner, MCPAttacker, LLMJudge,
)
from offsec_ai.core.openclaw_scanner import OpenClawScanner
from offsec_ai.core.openclaw_attacker import OpenClawAttacker

async def main():
    # Infrastructure: port scanning
    scanner = PortChecker()
    result = await scanner.scan_host("example.com", [80, 443, 22])
    print(f"Open ports: {[p.port for p in result.open_ports]}")

    # L7 / WAF detection
    detector = L7Detector()
    l7 = await detector.detect("example.com")
    if l7.is_protected:
        print(f"WAF/CDN: {l7.primary_protection.service.value}")

    # AI / LLM OWASP Top 10 scanner
    llm_scanner = LLMOwaspScanner(
        endpoint="https://api.example.com/v1/chat/completions",
        api_key="sk-...",
    )
    report = await llm_scanner.scan()
    print(f"LLM findings: {len(report.findings)}")

    # MCP security scan (passive)
    mcp = MCPScanner("https://mcp.example.com/mcp")
    mcp_result = await mcp.scan()
    print(f"MCP tools exposed: {len(mcp_result.tools)}")
    print(f"Auth required: {mcp_result.auth_posture.requires_auth}")

    # OpenClaw gateway scan (passive)
    ocl_scanner = OpenClawScanner(target="192.168.1.10", port=18789)
    ocl_result = await ocl_scanner.scan()
    if ocl_result.is_openclaw:
        print(f"OpenClaw {ocl_result.server_info.version} — "
              f"{len(ocl_result.critical_vulns)} critical, "
              f"{len(ocl_result.high_vulns)} high")

    # OpenClaw active attack (authorized=True required)
    attacker = OpenClawAttacker(authorized=True)
    attack_report = await attacker.attack(target="192.168.1.10", mode="deep")
    print(f"Successful attacks: {len(attack_report.successful_attacks)}")

asyncio.run(main())
```

## Configuration

Create `~/.offsec-ai.yaml`:

```yaml
default_ports: [80, 443, 8080, 8443, 22, 21, 25, 53]
timeout: 5
concurrent_limit: 50
user_agent: "offsec-ai/2.0.0"
```

## Advanced Features

### Batch Scanning

```python
hosts = ["example.com", "google.com", "github.com"]
results = await scanner.scan_multiple_hosts(hosts, [80, 443])

for result in results:
    print(f"{result.host}: {len(result.open_ports)} open ports")
```

### Service Detection

```python
service_info = await scanner.check_service_version("example.com", 80)
print(f"Server: {service_info['version']}")
```

### WAF Testing

```python
waf_results = await detector.test_waf_bypass("example.com")
print(f"WAF detected: {waf_results['waf_detected']}")
```

## Output Formats

### JSON Output

```bash
offsec-ai scan example.com --output scan_results.json
```

### Programmatic Access

```python
# Save to file
result.save_to_file("results.json")

# Convert to dict
data = result.to_dict()

# Get JSON string
json_str = result.to_json(indent=2)
```

## Security Considerations

- Only scan systems you own or have explicit permission to test
- Be mindful of rate limiting and network policies
- Some scans may trigger security alerts
- Use responsibly for legitimate security testing only

## Troubleshooting

### Common Issues

1. **DNS Resolution Errors**
   ```bash
   # Check if hostname resolves
   nslookup example.com
   ```

2. **Connection Timeouts**
   ```bash
   # Increase timeout
   offsec-ai scan example.com --timeout 10
   ```

3. **Rate Limiting**
   ```bash
   # Reduce concurrency
   offsec-ai scan example.com --concurrent 10
   ```

### Debug Mode

```bash
offsec-ai scan example.com --verbose
```

## Examples

See the `examples/` directory for complete usage examples:
- `usage_examples.py` — Core infrastructure scanning examples
- `comprehensive_examples.py` — All features with detailed output
- `mtls_examples.py` — mTLS testing and certificate generation
- `owasp_scan_examples.py` — OWASP Top 10 scanning with PDF/CSV export
