```
  ██████╗ ███████╗███████╗███████╗███████╗ ██████╗       █████╗ ██╗
 ██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝      ██╔══██╗██║
 ██║   ██║█████╗  █████╗  ███████╗█████╗  ██║     █████╗███████║██║
 ██║   ██║██╔══╝  ██╔══╝  ╚════██║██╔══╝  ██║     ╚════╝██╔══██║██║
 ╚██████╔╝██║     ██║     ███████║███████╗╚██████╗       ██║  ██║██║
  ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚══════╝ ╚═════╝       ╚═╝  ╚═╝╚═╝
  Offensive-Security Toolkit · AI/LLM · MCP · Red-Team
```

<p align="center">
  <a href="https://github.com/Htunn/offsec-ai/actions/workflows/test.yml"><img src="https://github.com/Htunn/offsec-ai/actions/workflows/test.yml/badge.svg?branch=develop" alt="Test and Build"/></a>
  <a href="https://github.com/Htunn/offsec-ai/actions/workflows/publish.yml"><img src="https://github.com/Htunn/offsec-ai/actions/workflows/publish.yml/badge.svg" alt="Publish to PyPI"/></a>
  <a href="https://github.com/Htunn/offsec-ai/actions/workflows/docker.yml"><img src="https://github.com/Htunn/offsec-ai/actions/workflows/docker.yml/badge.svg" alt="Docker Build"/></a>
  <a href="https://github.com/Htunn/offsec-ai/actions/workflows/codeql.yml"><img src="https://github.com/Htunn/offsec-ai/actions/workflows/codeql.yml/badge.svg" alt="CodeQL"/></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/offsec-ai/"><img src="https://img.shields.io/pypi/v/offsec-ai" alt="PyPI Version"/></a>
  <a href="https://pypistats.org/packages/offsec-ai"><img src="https://img.shields.io/pypi/dm/offsec-ai" alt="PyPI Downloads"/></a>
  <a href="https://pypi.org/project/offsec-ai/"><img src="https://img.shields.io/pypi/pyversions/offsec-ai" alt="Python Version"/></a>
  <a href="https://hub.docker.com/r/htunnthuthu/offsec-ai"><img src="https://img.shields.io/docker/pulls/htunnthuthu/offsec-ai" alt="Docker Pulls"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"/></a>
</p>

**Offensive-security toolkit for authorized red-team engagements.**

`offsec-ai` is a Python library and CLI that combines classic network reconnaissance with modern AI/LLM security testing. It probes live AI/LLM endpoints for the [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/), scans and actively attacks [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers for known CVEs, and performs full-stack infrastructure security assessments.

> **Legal Notice**: Active attack features (`mcp-attack`, deep mode) require the `--i-have-authorization` flag. Only use against systems you own or have explicit written permission to test.

---

## Features

### New in v2.0.0 — AI / LLM Security

| Feature | Description |
|---------|-------------|
| 🤖 **AI OWASP Top 10 Scanner** | Black-box probing of live LLM/chat API endpoints for all 10 OWASP LLM categories |
| 🔬 **Rule-based + LLM Judge** | Pattern-based detection + optional LLM judge (OpenAI/Anthropic) via `[ai]` extra |
| 🔌 **MCP Security Scanner** | Enumerate tools/resources/prompts, detect CVEs, check auth posture (HTTP, SSE, stdio) |
| ⚔️ **MCP Attacker** | Authorized active testing: auth bypass, path traversal, tool injection, command injection |
| 🛡️ **Authorization Gating** | `MCPAttacker(authorized=False)` raises `AuthorizationRequired`; `--i-have-authorization` flag required at CLI |

### Infrastructure Security

| Feature | Description |
|---------|-------------|
| 🔍 **Port Scanning** | Async concurrent scanning of well-known and custom ports |
| 🌐 **L7 Protection Detection** | Identify WAF/CDN services (Cloudflare, AWS WAF, Azure, F5, Akamai, etc.) |
| 🔐 **mTLS Checker** | Test mutual TLS support, client certificate requirements, handshake validation |
| 🔒 **Certificate Analysis** | Full chain analysis, trust path, issuer identification, expiry, missing intermediates |
| 🏛️ **Hybrid Identity Detection** | Azure AD / ADFS federation endpoint discovery (same method as Azure Portal) |
| 🕵️ **OWASP Top 10 Web Scanner** | Web OWASP Top 10 2021 & 2025 with safe/deep modes, PDF/JSON/CSV reports |
| 🛡️ **Security Headers** | Grade HTTP headers (HSTS, CSP, X-Frame-Options, Referrer-Policy, etc.) |
| 📄 **Multi-format Reporting** | Export to PDF, JSON, CSV with tech-specific remediation (Nginx, Apache, IIS, Cloudflare) |

---

## Installation

```bash
# Core toolkit
pip install offsec-ai

# With optional LLM judge (OpenAI / Anthropic)
pip install "offsec-ai[ai]"
```

### From Source

```bash
git clone https://github.com/htunn/offsec-ai.git
cd offsec-ai
pip install -e ".[dev]"
```

### Docker

```bash
docker run --rm htunnthuthu/offsec-ai:latest --help
```

---

## Quick Start

```
  ██████╗ ███████╗███████╗███████╗███████╗ ██████╗       █████╗ ██╗
 ██╔═══██╗██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝      ██╔══██╗██║
 ██║   ██║█████╗  █████╗  ███████╗█████╗  ██║     █████╗███████║██║
 ██║   ██║██╔══╝  ██╔══╝  ╚════██║██╔══╝  ██║     ╚════╝██╔══██║██║
 ╚██████╔╝██║     ██║     ███████║███████╗╚██████╗       ██║  ██║██║
  ╚═════╝ ╚═╝     ╚═╝     ╚══════╝╚══════╝ ╚═════╝       ╚═╝  ╚═╝╚═╝
  Offensive-Security Toolkit · AI/LLM · MCP · Red-Team
```

### CLI

```bash
# AI / LLM security
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions
offsec-ai mcp-scan https://mcp.example.com/mcp
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization

# Infrastructure
offsec-ai scan example.com
offsec-ai l7-check example.com
offsec-ai cert-check example.com
offsec-ai owasp-scan example.com
offsec-ai hybrid-identity example.com
offsec-ai mtls-check example.com
```

### Python API

```python
import asyncio
from offsec_ai import LLMOwaspScanner, MCPScanner, MCPAttacker, AuthorizationRequired

async def main():
    # AI OWASP scan
    scanner = LLMOwaspScanner("https://api.example.com/v1/chat/completions")
    result = await scanner.scan()
    print(f"Grade: {result.overall_grade}  Score: {result.total_score}")
    for cat_id, cat in result.categories.items():
        if cat.findings:
            print(f"  {cat_id}: {len(cat.findings)} finding(s) — grade {cat.grade}")

    # MCP scan
    mcp = MCPScanner("https://mcp.example.com/mcp")
    mcp_result = await mcp.scan()
    print(f"MCP vulnerabilities: {len(mcp_result.vulnerabilities)}")

    # MCP attack (requires explicit authorization)
    try:
        attacker = MCPAttacker(authorized=True)   # must be True
        report = await attacker.attack(
            target="https://mcp.example.com/mcp",
            transport="http",
            mode="safe",
        )
        print(f"Attacks run: {report.attacks_run}, triggered: {len(report.triggered_results)}")
    except AuthorizationRequired:
        print("Provide authorized=True to unlock attack mode")

asyncio.run(main())
```

---

## AI OWASP Top 10 Scanner

Probes a live LLM/chat endpoint for the [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/). Designed for black-box testing — no model access required.

### Categories Covered

| ID | Category | Safe Mode | Deep Mode |
|----|----------|-----------|-----------|
| LLM01 | Prompt Injection | ✅ | ✅ |
| LLM02 | Sensitive Information Disclosure | ✅ | ✅ |
| LLM03 | Supply Chain | 🚫 | 🚫 |
| LLM04 | Data & Model Poisoning | 🚫 | 🚫 |
| LLM05 | Improper Output Handling (XSS/SQLi) | ✅ | ✅ |
| LLM06 | Excessive Agency | ✅ | ✅ |
| LLM07 | System Prompt Leakage | ✅ | ✅ |
| LLM08 | Vector & Embedding Weaknesses | 🚫 | 🚫 |
| LLM09 | Misinformation | ✅ | ✅ |
| LLM10 | Unbounded Consumption | ✅ | ✅ |

🚫 = Not externally testable via black-box probing

### CLI Usage

```bash
# Basic scan (safe mode, OpenAI-compatible endpoint)
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions

# Deep mode with all probes
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions --mode deep

# Specific categories only
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions \
  --categories LLM01,LLM02,LLM07

# Generic/custom API format (non-OpenAI)
offsec-ai ai-owasp-scan https://chat.example.com/api/chat --api-format generic

# With authentication header
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions \
  --header "Authorization: Bearer sk-..."

# JSON output
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions --output results.json

# Enable LLM judge (requires OPENAI_API_KEY or ANTHROPIC_API_KEY env var)
offsec-ai ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge
```

### Python API

```python
import asyncio
from offsec_ai import LLMOwaspScanner, LLMScanMode, LLMJudge

async def main():
    # Optional: enable LLM judge for smarter detection
    judge = LLMJudge.from_env()  # reads OPENAI_API_KEY / ANTHROPIC_API_KEY

    scanner = LLMOwaspScanner(
        endpoint="https://api.example.com/v1/chat/completions",
        mode=LLMScanMode.DEEP,
        categories=["LLM01", "LLM02", "LLM07"],
        api_format="openai",
        headers={"Authorization": "Bearer sk-..."},
        judge=judge,                # None = rule-based only
    )

    result = await scanner.scan()
    print(f"Grade: {result.overall_grade}  ({result.total_score} pts)")

    for cat_id, cat in result.categories.items():
        if cat.findings:
            print(f"\n{cat_id}: {cat.category_name}")
            for finding in cat.findings:
                print(f"  [{finding.severity.value}] {finding.title}")
                print(f"  Evidence: {finding.evidence[:80]}...")

asyncio.run(main())
```

### Severity & Grading

| Severity | Points |
|----------|--------|
| CRITICAL | 15 |
| HIGH | 10 |
| MEDIUM | 5 |
| LOW | 1 |

Grade: A (0–10), B (11–25), C (26–50), D (51–100), F (>100 or any CRITICAL finding).

### LLM Judge (Optional)

Install the `[ai]` extra and set an API key to enable smarter semantic detection:

```bash
pip install "offsec-ai[ai]"
export OPENAI_API_KEY="sk-..."   # or ANTHROPIC_API_KEY
```

Without the extra, detection falls back to rule-based pattern matching.

---

## MCP Security Scanner

Scans [Model Context Protocol](https://modelcontextprotocol.io) servers for security vulnerabilities. Supports HTTP/SSE transports (remote URL) and stdio transport (local subprocess).

### CVEs / Checks Performed

| Check | Description |
|-------|-------------|
| Unauthenticated Exposure | Server accessible without credentials |
| Tool Poisoning | Malicious instructions hidden in tool descriptions |
| Path Traversal in Resources | `../` patterns in resource URIs |
| Command Injection | Shell metacharacters in tool params |
| Secrets in Descriptions | API keys, passwords leaked in tool/resource descriptions |
| Excessive Agency | Unrestricted file system or network tools |
| Prompt Injection via Tool Response | LLM instruction injection through tool output |
| Rug-pull / Tool Shadowing | Tool behavior changed post-trust-establishment |

### CLI Usage

```bash
# Scan HTTP/SSE MCP endpoint
offsec-ai mcp-scan https://mcp.example.com/mcp

# Scan local stdio server
offsec-ai mcp-scan --transport stdio --cmd "npx @example/mcp-server"

# With authentication
offsec-ai mcp-scan https://mcp.example.com/mcp \
  --header "Authorization: Bearer token"

# JSON output
offsec-ai mcp-scan https://mcp.example.com/mcp --output mcp-scan.json

# Verbose output
offsec-ai mcp-scan https://mcp.example.com/mcp --verbose
```

### Python API

```python
import asyncio
from offsec_ai import MCPScanner, MCPTransport

async def main():
    # HTTP transport
    scanner = MCPScanner(
        target="https://mcp.example.com/mcp",
        transport=MCPTransport.HTTP,
        headers={"Authorization": "Bearer token"},
    )
    result = await scanner.scan()

    print(f"Server: {result.server_info.name} v{result.server_info.version}")
    print(f"Tools: {len(result.tools)}, Resources: {len(result.resources)}")
    print(f"Vulnerabilities: {len(result.vulnerabilities)}")

    for vuln in result.vulnerabilities:
        print(f"  [{vuln.severity.value}] {vuln.title}: {vuln.description}")

    # Stdio transport
    scanner = MCPScanner(
        target="stdio://local",
        transport=MCPTransport.STDIO,
        cmd=["npx", "@example/mcp-server"],
    )
    result = await scanner.scan()

asyncio.run(main())
```

---

## MCP Attacker

Performs active security testing against MCP servers. **Requires explicit authorization.**

### Attack Suite

| Attack | Safe Mode | Deep Mode | Description |
|--------|-----------|-----------|-------------|
| Auth Bypass | ✅ | ✅ | Null token, empty bearer, X-Forwarded-For injection |
| Path Traversal | ❌ | ✅ | `/etc/passwd`, `.env`, `shadow` file read attempts |
| Tool Injection | ❌ | ✅ | Malicious payload in tool call arguments |
| Command Injection | ❌ | ✅ | Shell metacharacter injection in tool params |

### CLI Usage

```bash
# Safe mode (auth bypass only) — must provide --i-have-authorization
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization

# Deep mode (all attacks)
offsec-ai mcp-attack https://mcp.example.com/mcp \
  --i-have-authorization --mode deep

# JSON output
offsec-ai mcp-attack https://mcp.example.com/mcp \
  --i-have-authorization --output attack-report.json
```

### Python API

```python
import asyncio
from offsec_ai import MCPAttacker, MCPScanner, AuthorizationRequired

async def main():
    # Authorization is enforced at instantiation
    try:
        bad = MCPAttacker()               # raises AuthorizationRequired
    except AuthorizationRequired:
        pass

    attacker = MCPAttacker(authorized=True)

    # Optional: use scan result to guide attacks
    scanner = MCPScanner("https://mcp.example.com/mcp")
    scan_result = await scanner.scan()

    report = await attacker.attack(
        target="https://mcp.example.com/mcp",
        transport="http",
        mode="deep",
        scan_result=scan_result,
    )

    print(f"Attacks run: {report.attacks_run}")
    print(f"Triggered: {len(report.triggered_results)}")
    for r in report.triggered_results:
        print(f"  [{r.severity.value}] {r.title}")

asyncio.run(main())
```

---

## Infrastructure Scanning

### Port Scanner

```bash
offsec-ai scan example.com
offsec-ai scan example.com --ports 80,443,8080,8443
offsec-ai scan example.com google.com --output results.json
```

```python
from offsec_ai import PortChecker
import asyncio

async def main():
    checker = PortChecker()
    result = await checker.scan_host("example.com", ports=[80, 443, 8080])
    open_ports = [p for p in result.ports if p.is_open]
    print(f"Open: {[p.port for p in open_ports]}")

asyncio.run(main())
```

### L7 Protection Detection

```bash
offsec-ai l7-check example.com
offsec-ai l7-check example.com --trace-dns
offsec-ai full-scan example.com
```

### SSL/TLS Certificate Analysis

```bash
offsec-ai cert-check example.com
offsec-ai cert-chain github.com
offsec-ai cert-info google.com
```

```python
from offsec_ai import CertificateAnalyzer
import asyncio

async def main():
    analyzer = CertificateAnalyzer()
    chain = await analyzer.analyze_certificate_chain("example.com", 443)
    print(f"Subject: {chain.server_cert.subject}")
    print(f"Issuer: {chain.server_cert.issuer}")
    print(f"Chain complete: {chain.chain_complete}")
    print(f"Days until expiry: {chain.server_cert.days_until_expiry}")

asyncio.run(main())
```

### mTLS Checker

```bash
offsec-ai mtls-check example.com
offsec-ai mtls-check example.com --client-cert client.crt --client-key client.key
offsec-ai mtls-gen-cert test-client.example.com
offsec-ai mtls-validate-cert client.crt client.key
```

### OWASP Top 10 Web Scanner (2021 & 2025)

```bash
offsec-ai owasp-scan example.com
offsec-ai owasp-scan example.com --deep
offsec-ai owasp-scan example.com -c A02,A05,A07 -t nginx --verbose
offsec-ai owasp-scan example.com -f pdf -o report.pdf
```

### Hybrid Identity Detection

```bash
offsec-ai hybrid-identity example.com
offsec-ai hybrid-identity example.com --verbose --output results.json
```

---

## All CLI Commands

```
offsec-ai --help

Commands:
  ai-owasp-scan       Probe a live LLM/AI endpoint for AI OWASP Top 10
  mcp-scan            Scan an MCP endpoint for security vulnerabilities
  mcp-attack          Perform authorized active testing against an MCP server
  scan                Scan target hosts for open ports
  l7-check            Check for L7 protection services (WAF, CDN, etc.)
  full-scan           Port scan + L7 protection detection
  cert-check          Analyze SSL/TLS certificate chain
  cert-chain          Analyze complete certificate chain and trust path
  cert-info           Show detailed certificate information
  dns-trace           Trace DNS records and analyze L7 protection
  owasp-scan          OWASP Top 10 2021/2025 vulnerability scanner
  hybrid-identity     Check for Azure AD/ADFS hybrid identity setup
  mtls-check          Check for mTLS authentication support
  mtls-gen-cert       Generate a self-signed certificate for mTLS testing
  mtls-validate-cert  Validate client certificate and private key files
  service-detect      Detect service version and information
```

---

## Docker

```bash
docker run --rm htunnthuthu/offsec-ai:latest ai-owasp-scan https://api.example.com/v1/chat/completions
docker run --rm htunnthuthu/offsec-ai:latest mcp-scan https://mcp.example.com/mcp
docker run --rm htunnthuthu/offsec-ai:latest scan example.com
docker run --rm htunnthuthu/offsec-ai:latest owasp-scan example.com

# Save output to host
docker run --rm -v $(pwd):/app/output htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions \
  --output /app/output/llm-report.json

# LLM Judge — openai, anthropic, or gemini key auto-detected; no extra install needed
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge

# Custom OpenAI-compatible backend (Ollama, LM Studio, Azure OpenAI…)
docker run --rm \
  -e OFFSEC_LLM_BASE_URL=http://host.docker.internal:11434/v1 \
  -e OFFSEC_LLM_MODEL=llama3 \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge
```

See [docs/DOCKER.md](docs/DOCKER.md) for the full Docker reference including CI/CD integration, Kubernetes jobs, Makefile publish targets, and troubleshooting.

---

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Enable OpenAI-based LLM judge |
| `ANTHROPIC_API_KEY` | Enable Anthropic-based LLM judge |
| `OFFSEC_LLM_BASE_URL` | Custom OpenAI-compatible base URL for LLM judge |

### Optional Extras

```bash
pip install "offsec-ai[ai]"   # Adds openai + anthropic for LLM judge
```

---

## Security & Ethics

This tool is designed for **authorized security assessments only**.

- Active attack features display an authorization banner and require `--i-have-authorization`
- `MCPAttacker(authorized=False)` raises `AuthorizationRequired` at instantiation — cannot be bypassed
- Default scan modes are passive (safe mode) and will not modify target systems
- Do not use against systems you do not own or lack explicit written permission to test

Please review [SECURITY.md](SECURITY.md) and [CONTRIBUTING.md](CONTRIBUTING.md) before contributing.

---

## Requirements

- Python 3.12+
- See [requirements.txt](requirements.txt) for full dependency list

---

## License

MIT — see [LICENSE](LICENSE)
