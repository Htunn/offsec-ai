# offsec-ai — Quick Start Guide

## Installation

```bash
pip install offsec-ai
```

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
