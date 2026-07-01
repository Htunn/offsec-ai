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

> **Legal Notice**: Active attack features (`mcp-attack`, `openclaw-attack`, `k8s-attack`, deep mode) require the `--i-have-authorization` flag. Only use against systems you own or have explicit written permission to test.

---

## Features

### New in v2.3.0 — Kubernetes Cluster Security

| Feature | Description |
|---------|-------------|
| ☸️ **Kubernetes Scanner** | Five-phase black-box scan of exposed K8s components: kube-apiserver (6443/8080), kubelet (10250/10255), etcd (2379), scheduler, controller-manager, cAdvisor, dashboard |
| 📋 **OWASP K8s Top 10 (2025)** | Findings mapped to K01–K10; 10+ advisories (`K8S-ADV-###`) + real CVEs (CVE-2018-1002105, CVE-2019-11253, CVE-2020-8558, CVE-2021-25741, CVE-2022-3294) |
| 🤖 **Optional LLM Judge** | `LLMJudge` triages ambiguous findings and generates remediation advice; supports OpenAI, Anthropic, and Google Gemini; rule-based fallback when no API key is set |
| ⚔️ **Kubernetes Attacker** | Authorized red-team probes: anonymous API reads, kubelet `/exec` command execution, Secret extraction, SelfSubjectAccessReview privilege audit, etcd key dump, cloud metadata SSRF (K08) |

### New in v2.1.0 — OpenClaw Gateway Security

| Feature | Description |
|---------|-------------|
| 🦞 **OpenClaw Scanner** | Six-phase passive assessment of [OpenClaw](https://github.com/openclaw/openclaw) AI-gateway deployments: fingerprint (including HTML-based detection for OpenClaw 2026.x), endpoint enumeration, auth posture, config review, CVE/misconfiguration matching, optional LLM triage |
| 🔟 **10 Advisory Checks** | OCL-ADV-001 through OCL-ADV-010 — from unauthenticated REST/WebSocket access to insecure sandbox modes, DM policy exposure, and API-key leakage via config endpoint |
| ⚔️ **OpenClaw Attacker** | Authorized active exploitation: prompt injection, SSRF via webhook, session history dump, WebSocket message injection; optional `--llm-judge` for attack-path narrative |

### New in v2.0.0 — AI / LLM Security

| Feature | Description |
|---------|-------------|
| 🤖 **AI OWASP Top 10 Scanner** | Black-box probing of live LLM/chat API endpoints for all 10 OWASP LLM categories |
| 🔬 **Rule-based + LLM Judge** | Pattern-based detection + optional LLM judge (OpenAI / Anthropic / Gemini) via `[ai]` extra |
| 🔌 **MCP Security Scanner** | Enumerate tools/resources/prompts, detect CVEs, check auth posture (HTTP, SSE, stdio) |
| ⚔️ **MCP Attacker** | Authorized active testing: auth bypass, path traversal, tool injection, command injection; optional `--llm-judge` for attack-path narrative |
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

# With optional LLM judge (OpenAI / Anthropic / Gemini)
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

# OpenClaw gateway security
offsec-ai openclaw-scan 192.168.1.10
offsec-ai openclaw-scan gateway.example.com --port 18789 --tls
offsec-ai openclaw-scan 192.168.1.10 --llm-judge
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep --llm-judge

# Kubernetes cluster security
offsec-ai k8s-scan 192.168.1.100
offsec-ai k8s-scan k8s.example.com --port 6443 --port 10250 --llm-judge
# kubectl proxy makes the API server reachable on plain HTTP locally:
offsec-ai k8s-scan 127.0.0.1 --port 8001 --llm-judge
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization --mode deep
offsec-ai k8s-attack 127.0.0.1 --port 8001 --i-have-authorization --llm-judge

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

# Enable LLM judge (requires OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY env var)
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
export GEMINI_API_KEY="AIza..."       # Google Gemini  (1st priority)
export ANTHROPIC_API_KEY="sk-ant-..." # or Anthropic   (2nd priority)
export OPENAI_API_KEY="sk-..."        # or OpenAI      (3rd priority)
```

If multiple keys are set, Gemini is used first, then Anthropic, then OpenAI.
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

# With LLM judge for enriched triage
offsec-ai mcp-scan https://mcp.example.com/mcp --llm-judge
offsec-ai mcp-attack https://mcp.example.com/mcp --i-have-authorization --llm-judge
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
        judge=LLMJudge.from_env(),  # optional: enriches MEDIUM/LOW findings
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

## OpenClaw Gateway Security

[OpenClaw](https://github.com/openclaw/openclaw) is a self-hosted AI-assistant gateway that bridges messaging platforms (Telegram, Discord, Slack, etc.) to LLM backends. Because OpenClaw instances are often internet-exposed, misconfigurations lead to unauthenticated LLM access, conversation history disclosure, SSRF, and prompt injection surfaces.

### Scanner (`openclaw-scan`)

Five-phase **passive** assessment — no exploitation:

| Phase | What it does |
|-------|--------------|
| 1 — Fingerprint | Probe `/health`, `/status`, `/api/v1/status`; match headers/body against OpenClaw signatures; extract version and gateway ID |
| 2 — Endpoint Enumeration | Probe all known API paths (`/api/v1/*`, `/ws/*`, `/webhooks`); flag endpoints leaking API keys or tokens in response bodies |
| 3 — Authentication Posture | Detect unauthenticated REST API access; probe for unauthenticated WebSocket upgrade on `/ws` and `/api/v1/ws` |
| 4 — Configuration Assessment | Parse `/api/v1/config` for DM policy and sandbox mode settings |
| 5 — CVE / Misconfiguration | Cross-reference findings against advisory database; produce severity-ranked vulnerability list |

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

### CLI Usage

```bash
# Passive scan — fingerprint and report misconfigurations
offsec-ai openclaw-scan 192.168.1.10

# Custom port / TLS
offsec-ai openclaw-scan gateway.example.com --port 18789 --tls

# With bearer token (authenticated scan)
offsec-ai openclaw-scan gateway.example.com \
    --header "Authorization: Bearer <token>"

# Export JSON report
offsec-ai openclaw-scan 192.168.1.10 --format json --output report.json

# Active attack (requires explicit authorization flag)
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization

# Deep mode — message injection + WebSocket + SSRF probes
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization --mode deep

# Export attack report
offsec-ai openclaw-attack 192.168.1.10 --i-have-authorization \
    --mode deep --format json --output attack.json
```

### Python API

```python
import asyncio
from offsec_ai.core.openclaw_scanner import OpenClawScanner
from offsec_ai.core.openclaw_attacker import OpenClawAttacker
from offsec_ai.exceptions import AuthorizationRequired

async def main():
    # Passive scan
    scanner = OpenClawScanner(
        target="192.168.1.10",
        port=18789,
        use_tls=False,
    )
    result = await scanner.scan()

    print(f"OpenClaw detected : {result.openclaw_detected}")
    print(f"Version           : {result.version}")
    print(f"Unauthenticated   : {result.unauthenticated_access}")
    print(f"Vulnerabilities   : {len(result.vulnerabilities)}")
    for v in result.vulnerabilities:
        print(f"  [{v.severity}] {v.advisory_id}: {v.title}")

    # Authorized active attack
    try:
        attacker = OpenClawAttacker(authorized=True)
        report = await attacker.attack(
            target="192.168.1.10",
            port=18789,
            mode="safe",   # "safe" | "deep"
        )
        print(f"Attacks triggered : {len(report.triggered_results)}")
        for r in report.triggered_results:
            print(f"  [{r.severity}] {r.title}")
    except AuthorizationRequired as exc:
        print(exc)

asyncio.run(main())
```

See [docs/openclaw.md](docs/openclaw.md) for the full guide including remediation advice.

---

## Kubernetes Cluster Security

Black-box scanning and authorized red-team testing of exposed Kubernetes cluster components, aligned with the [OWASP Kubernetes Top 10 (2025)](https://owasp.org/www-project-kubernetes-top-ten/). No `kubernetes` SDK or kubeconfig required — all probes are over the network via `httpx`.

### Component Surface

| Component | Default Ports | Key Probes |
|-----------|--------------|------------|
| kube-apiserver | 6443, 443, 8080 | `/version`, `/healthz`, `/api`, anon `/api/v1/secrets`/`/pods`, `SelfSubjectAccessReview` |
| kubelet | 10250 (rw), 10255 (ro) | `/pods`, `/runningpods`, `/stats/summary`, `/spec`; `/exec` `/run` (attack) |
| etcd | 2379, 2380 | `/version`, `/health`, v2/v3 keys |
| scheduler / controller-mgr | 10259 / 10257 | `/healthz`, `/metrics` |
| kube-proxy / cAdvisor | 10249 / 4194 | `/healthz`, metrics |
| Dashboard | 8001, 30000–32767 | UI accessibility, auth posture |

### OWASP K8s Top 10 Coverage

| ID | Category | Black-box coverage |
|----|----------|-----------------|
| K01 | Insecure Workload Configurations | ⚠️ via kubelet `/pods` spec (privileged, hostPath, hostNetwork) |
| K02 | Overly Permissive Authorization | ⚠️ via anonymous `SelfSubjectAccessReview` (deep mode) |
| K03 | Secrets Management Failures | ⚠️ via anon apiserver `/api/v1/secrets` + kubelet env exposure |
| K04 | Lack of Cluster Policy Enforcement | 🔎 informational (admission webhook hints) |
| K05 | Missing Network Segmentation | 🔎 informational (exposed NodePort / internal services) |
| K06 | Overly Exposed Components | ✅ PRIMARY — all component ports probed for accessibility |
| K07 | Misconfigured / Vulnerable Components | ✅ `/version` → CVE match; insecure port 8080 detection |
| K08 | Cluster → Cloud Lateral Movement | ⚠️ cloud IMDS SSRF probes (deep mode) |
| K09 | Broken Authentication Mechanisms | ✅ anonymous-auth detection on apiserver + kubelet |
| K10 | Inadequate Logging and Monitoring | 🔎 informational only |

✅ Full coverage · ⚠️ Partial (deep mode or limited by anon access) · 🔎 Informational

### Advisory Database

| ID | CVE | Severity | Finding |
|----|-----|----------|---------|
| K8S-ADV-001 | — | **Critical** | kube-apiserver exposed without authentication |
| K8S-ADV-002 | — | **Critical** | Kubelet read-write port (10250) exposed without auth |
| K8S-ADV-003 | — | **High** | Kubelet read-only port (10255) accessible |
| K8S-ADV-004 | — | **Critical** | etcd accessible without authentication |
| K8S-ADV-005 | — | Medium | Kubernetes Dashboard exposed without auth |
| K8S-ADV-006 | — | **High** | Scheduler / controller-manager metrics port exposed |
| CVE-2018-1002105 | CVE-2018-1002105 | **Critical** | API server privilege escalation via API aggregation |
| CVE-2019-11253 | CVE-2019-11253 | **High** | API server DoS via malformed YAML/JSON |
| CVE-2020-8558 | CVE-2020-8558 | **High** | NodePort services reachable via loopback interface |
| CVE-2021-25741 | CVE-2021-25741 | **High** | Symlink + hardlink in volume path traversal |
| CVE-2022-3294 | CVE-2022-3294 | **High** | Node address bypass for node restriction admission plugin |

### CLI Usage

```bash
# Passive scan — probe all default K8s component ports
offsec-ai k8s-scan 192.168.1.100

# Target specific ports
offsec-ai k8s-scan k8s.example.com --port 6443 --port 10250

# With authentication header (semi-auth scan)
offsec-ai k8s-scan k8s.example.com \
    --header "Authorization: Bearer <token>"

# Enable LLM judge for finding triage and remediation advice
offsec-ai k8s-scan 192.168.1.100 --llm-judge

# Export JSON report
offsec-ai k8s-scan 192.168.1.100 --format json --output k8s-scan.json

# Authorized active attack (safe mode — anon reads + RBAC review)
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization

# Deep mode — kubelet /exec, secret extraction, etcd dump, cloud IMDS SSRF
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization --mode deep

# Export attack report
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization \
    --mode deep --format json --output k8s-attack.json
```

### Python API

```python
import asyncio
from offsec_ai.core.k8s_scanner import K8sScanner
from offsec_ai.core.k8s_attacker import K8sAttacker
from offsec_ai.core.llm_judge import LLMJudge
from offsec_ai.exceptions import AuthorizationRequired

async def main():
    # Optional LLM judge — auto-detects OPENAI/ANTHROPIC/GEMINI key from env
    judge = LLMJudge()   # rule-based fallback when no key is set

    # Passive scan
    scanner = K8sScanner(
        target="192.168.1.100",
        ports=[6443, 10250, 2379],
        judge=judge,
    )
    result = await scanner.scan()

    print(f"Kubernetes detected : {result.is_kubernetes}")
    print(f"Version             : {result.server_info.git_version}")
    print(f"Exposed components  : {[c.component.value for c in result.exposed_components]}")
    print(f"OWASP coverage      : {result.owasp_coverage}")
    print(f"Vulnerabilities     : {len(result.vulnerabilities)}")
    for v in result.vulnerabilities:
        print(f"  [{v.severity.value}] {v.owasp_id} {v.vuln_id}: {v.title}")
        if v.llm_reasoning:
            print(f"    LLM: {v.llm_reasoning}")

    # Authorized active attack
    try:
        attacker = K8sAttacker(authorized=True, judge=judge)
        report = await attacker.attack(
            target="192.168.1.100",
            mode="safe",           # "safe" | "deep"
            scan_result=result,   # guides attack selection
        )
        print(f"Attacks run       : {len(report.attack_results)}")
        print(f"Succeeded         : {len(report.successful_attacks)}")
        for r in report.successful_attacks:
            print(f"  [{r.severity.value}] {r.owasp_id} {r.attack_id}: {r.description}")
    except AuthorizationRequired as exc:
        print(exc)

asyncio.run(main())
```

See [docs/k8s.md](docs/k8s.md) for the full guide including OWASP K8s Top 10 mapping, CVE database, attack sequences, and remediation advice.

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
  openclaw-scan       Five-phase passive security scan of an OpenClaw AI gateway
  openclaw-attack     Authorized active attack against an OpenClaw gateway
  k8s-scan            Black-box Kubernetes cluster security scan (OWASP K8s Top 10)
  k8s-attack          Authorized active red-team attack against Kubernetes components
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
