# offsec-ai — Kubernetes Cluster Security

`offsec-ai` ships a passive **scanner** and an authorization-gated **attacker** for assessing
Kubernetes cluster components against the
[OWASP Kubernetes Top 10 (2025)](https://owasp.org/www-project-kubernetes-top-ten/).

All probes are network-level via `httpx` — no `kubernetes` SDK, no kubeconfig, no cluster
credentials required for the passive scan.

---

## Quick Start

```bash
# Passive scan — probe all default K8s component ports
offsec-ai k8s-scan 192.168.1.100

# Target specific ports only
offsec-ai k8s-scan k8s.example.com --port 6443 --port 10250

# With bearer token (semi-auth scan)
offsec-ai k8s-scan k8s.example.com \
    --header "Authorization: Bearer <serviceaccount-token>"

# Enable LLM judge for triage and remediation advice
offsec-ai k8s-scan 192.168.1.100 --llm-judge

# Export JSON report
offsec-ai k8s-scan 192.168.1.100 --format json --output k8s-scan.json

# Authorized red-team attack (safe mode — passive reads, no destructive ops)
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization

# Attack with LLM judge for enriched attack-path narrative
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization --llm-judge

# Deep mode — adds kubelet /exec, Secret extraction, etcd dump, cloud IMDS SSRF
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization --mode deep

# Export attack report
offsec-ai k8s-attack 192.168.1.100 --i-have-authorization \
    --mode deep --format json --output k8s-attack.json
```

> **kubectl proxy tip:** If your kubeconfig points to a tunnel or remote port that is not
> locally reachable, use `kubectl proxy --port=8001` to expose the API server as plain HTTP
> on `http://127.0.0.1:8001`. Then scan with `--port 8001` — no TLS, no credentials needed:
>
> ```bash
> kubectl proxy --port=8001 &
> offsec-ai k8s-scan 127.0.0.1 --port 8001 --llm-judge
> offsec-ai k8s-attack 127.0.0.1 --port 8001 --i-have-authorization
> ```

---

## Scanner (`k8s-scan`)

The scanner performs five sequential phases with no active exploitation:

```
Phase 1 — Component Discovery
    Probe all well-known Kubernetes component ports:
      6443 / 443 / 8080  — kube-apiserver
      10250 / 10255       — kubelet (read-write / read-only)
      2379 / 2380         — etcd
      10259 / 10257       — kube-scheduler / controller-manager
      10249               — kube-proxy
      4194                — cAdvisor
      8001 / NodePorts    — Kubernetes Dashboard
    For each accessible port: identify component, TLS posture, and server headers.

Phase 2 — Version & CVE Matching (K07)
    GET /version on kube-apiserver to extract gitVersion, platform, goVersion.
    Match version against K8S_CVE_DB — real CVEs (CVE-2018-1002105 etc.)
    and K8S-ADV-### advisories.
    Flag insecure legacy HTTP port 8080 (--insecure-port).

Phase 3 — Authentication Posture (K09)
    Probe apiserver /api, /healthz, /metrics without credentials.
    Probe kubelet /pods, /healthz, /stats/summary without credentials.
    Probe etcd /health, /version without client certificate.
    Flag anonymous-auth=true where responses succeed without Authorization.

Phase 4 — Exposure & Workload Audit (K01/K03/K06)
    Attempt anonymous GET /api/v1/secrets (apiserver K03).
    Attempt anonymous GET /api/v1/configmaps.
    Read kubelet /pods — scan pod specs for:
      · privileged: true                    → K01 Critical
      · hostPath volumes                    → K01 High
      · hostNetwork / hostPID / hostIPC     → K01 High
    Flag cAdvisor /api/v1/subcontainers exposure.

Phase 5 — OWASP Map + LLM Triage
    Deduplicate findings; attach OWASP K8s Top 10 IDs (K01–K10).
    If LLMJudge is configured: call judge.evaluate() for each finding;
    store llm_confidence and llm_reasoning on K8sVulnerability.
    Enrich remediation text with LLM-generated guidance.
```

---

## Advisory & CVE Database

| ID | CVE | Severity | OWASP | Finding |
|----|-----|----------|-------|---------|
| K8S-ADV-001 | — | **Critical** | K06 | kube-apiserver exposed without authentication |
| K8S-ADV-002 | — | **Critical** | K06 | Kubelet read-write port (10250) exposed without auth |
| K8S-ADV-003 | — | **High** | K06 | Kubelet read-only port (10255) accessible |
| K8S-ADV-004 | — | **Critical** | K06 | etcd accessible without authentication |
| K8S-ADV-005 | — | Medium | K06 | Kubernetes Dashboard exposed without auth |
| K8S-ADV-006 | — | **High** | K07 | Scheduler / controller-manager metrics port exposed |
| CVE-2018-1002105 | CVE-2018-1002105 | **Critical** | K07 | API server privilege escalation via API aggregation (< 1.12.3) |
| CVE-2019-11253 | CVE-2019-11253 | **High** | K07 | API server DoS via malformed YAML/JSON (< 1.14.8 / < 1.15.5 / < 1.16.2) |
| CVE-2020-8558 | CVE-2020-8558 | **High** | K05 | NodePort services reachable via loopback interface |
| CVE-2021-25741 | CVE-2021-25741 | **High** | K01 | Symlink/hardlink path traversal in volume handling |
| CVE-2022-3294 | CVE-2022-3294 | **High** | K07 | Node address bypass for node restriction admission plugin |

---

## OWASP Kubernetes Top 10 (2025) Coverage

| ID | Category | Coverage | Notes |
|----|----------|----------|-------|
| **K01** | Insecure Workload Configurations | ⚠️ Partial | Kubelet `/pods` spec: privileged, hostPath, hostNetwork/PID/IPC |
| **K02** | Overly Permissive Authorization | ⚠️ Deep mode | `SelfSubjectAccessReview` + `SelfSubjectRulesReview` via apiserver |
| **K03** | Secrets Management Failures | ⚠️ Partial | Anon apiserver `/api/v1/secrets`; kubelet env vars; etcd key dump (deep) |
| **K04** | Lack of Cluster Policy Enforcement | 🔎 Informational | Admission webhook presence hints; limited without cluster access |
| **K05** | Missing Network Segmentation | 🔎 Informational | Exposed NodePort/internal services; CVE-2020-8558 |
| **K06** | Overly Exposed Components | ✅ Full | All component ports probed; anonymous access flagged |
| **K07** | Misconfigured / Vulnerable Components | ✅ Full | Version → CVE match; insecure port 8080 detection |
| **K08** | Cluster → Cloud Lateral Movement | ⚠️ Deep mode | Cloud IMDS SSRF probes for AWS/GCP/Azure metadata endpoints |
| **K09** | Broken Authentication Mechanisms | ✅ Full | Anonymous-auth detection on apiserver and kubelet |
| **K10** | Inadequate Logging and Monitoring | 🔎 Informational | Cannot fully assess via black-box network scan |

✅ Full coverage · ⚠️ Partial (requires deep attack mode or limited by anonymous access level) · 🔎 Informational

---

## Attacker (`k8s-attack`)

The attacker requires `--i-have-authorization` and prints a legal banner on every invocation.

### Safe Mode

Passive read-only probes — no destructive operations, no writes to the cluster:

| Probe | OWASP | Description |
|-------|-------|-------------|
| Anonymous apiserver resource list | K09 | Attempt `GET /api/v1/namespaces`, `/api/v1/pods`, `/api/v1/secrets` without auth |
| Kubelet `/pods` read | K06 | Read all pod specs via kubelet 10250/10255 |
| `SelfSubjectAccessReview` | K02 | POST to apiserver to query what anonymous user can do |
| etcd `/health` probe | K06 | Confirm etcd is accessible without client certificate |

### Deep Mode

Full attack suite — adds active exploitation probes:

| Probe | OWASP | Description |
|-------|-------|-------------|
| Kubelet `/exec` | K06 | Attempt command execution in a container via kubelet API |
| Anonymous Secret extraction | K03 | `GET /api/v1/namespaces/default/secrets` — read cluster Secrets |
| etcd key dump | K03 | Read keys from etcd v2/v3 API (cluster state + secrets) |
| AWS IMDS SSRF | K08 | Probe `http://169.254.169.254/latest/meta-data/` via kubelet/apiserver |
| GCP metadata SSRF | K08 | Probe `http://metadata.google.internal/computeMetadata/v1/` |
| Azure IMDS SSRF | K08 | Probe `http://169.254.169.254/metadata/instance` |

---

## Python API

### Passive Scan

```python
import asyncio
from offsec_ai.core.k8s_scanner import K8sScanner
from offsec_ai.core.llm_judge import LLMJudge

async def assess_k8s_cluster(host: str) -> None:
    # Optional LLM judge — auto-detects OPENAI/ANTHROPIC/GEMINI key from env
    judge = LLMJudge()

    scanner = K8sScanner(
        target=host,
        ports=[6443, 10250, 10255, 2379],  # or omit for all default ports
        timeout=15.0,
        judge=judge,
    )
    result = await scanner.scan()

    print(f"Kubernetes detected: {result.is_kubernetes}")
    print(f"Version            : {result.server_info.git_version}")
    print(f"Platform           : {result.server_info.platform}")
    print(f"OWASP coverage     : {result.owasp_coverage}")

    print(f"\nExposed components ({len(result.exposed_components)}):")
    for comp in result.exposed_components:
        auth = "anonymous" if comp.anonymous_access else "authenticated"
        tls = "TLS" if comp.tls else "plain"
        print(f"  {comp.component.value}:{comp.port}  [{auth}] [{tls}]")

    print(f"\nVulnerabilities ({len(result.vulnerabilities)}):")
    for v in result.vulnerabilities:
        print(f"  [{v.severity.value.upper():8}] {v.owasp_id} {v.vuln_id}: {v.title}")
        if v.evidence:
            print(f"    Evidence   : {v.evidence[:100]}")
        if v.llm_reasoning:
            print(f"    LLM triage : {v.llm_reasoning}")
        print(f"    Remediation: {v.remediation[:120]}")

    # JSON export
    import json
    with open("k8s-scan.json", "w") as f:
        json.dump(result.model_dump(mode="json"), f, indent=2, default=str)

asyncio.run(assess_k8s_cluster("192.168.1.100"))
```

### Scan + Attack

```python
import asyncio
from offsec_ai.core.k8s_scanner import K8sScanner
from offsec_ai.core.k8s_attacker import K8sAttacker
from offsec_ai.core.llm_judge import LLMJudge
from offsec_ai.exceptions import AuthorizationRequired

async def full_k8s_assessment(host: str) -> None:
    judge = LLMJudge()

    # Step 1: passive scan to guide attack selection
    scanner = K8sScanner(target=host, judge=judge)
    scan_result = await scanner.scan()

    print(f"Scan: {len(scan_result.vulnerabilities)} findings, "
          f"OWASP: {scan_result.owasp_coverage}")

    # Step 2: authorized red-team attack
    try:
        attacker = K8sAttacker(authorized=True, judge=judge)
        report = await attacker.attack(
            target=host,
            mode="deep",              # "safe" | "deep"
            scan_result=scan_result,  # guides attack selection
            timeout=20.0,
        )
        print(f"\nAttack: {len(report.attack_results)} probes run")
        print(f"        {len(report.successful_attacks)} succeeded")
        print(f"        {len(report.critical_successes)} critical")

        for r in report.successful_attacks:
            print(f"  [{r.severity.value}] {r.owasp_id} {r.attack_id}")
            print(f"    {r.description}")
            if r.evidence:
                print(f"    Evidence: {r.evidence[:120]}")
    except AuthorizationRequired as exc:
        print(f"Authorization required: {exc}")

asyncio.run(full_k8s_assessment("192.168.1.100"))
```

---

## Remediation Reference

### K06 — Overly Exposed Components

```bash
# Disable anonymous auth on kube-apiserver (kubeadm cluster)
# Edit /etc/kubernetes/manifests/kube-apiserver.yaml:
# --anonymous-auth=false
# --authorization-mode=Node,RBAC

# Disable anonymous auth on kubelet
# Edit /var/lib/kubelet/config.yaml:
# authentication:
#   anonymous:
#     enabled: false
# authorization:
#   mode: Webhook

# Disable kubelet read-only port
# kubelet --read-only-port=0

# Restrict etcd to control-plane-only network (firewall / security group):
# iptables -A INPUT -p tcp --dport 2379 -s <control-plane-cidr> -j ACCEPT
# iptables -A INPUT -p tcp --dport 2379 -j DROP
```

### K07 — Vulnerable Components

```bash
# Check your Kubernetes version
kubectl version --short

# Upgrade a kubeadm cluster
kubeadm upgrade plan
kubeadm upgrade apply v1.29.x

# Disable the insecure port (legacy, deprecated since 1.20, removed in 1.24)
# kube-apiserver --insecure-port=0
```

### K09 — Broken Authentication

```bash
# Confirm anonymous auth is disabled on the apiserver
kubectl get --raw /api/v1/secrets 2>&1 | grep -i forbidden
# Should return 403 Forbidden, not a list of secrets

# Check RBAC bindings that grant cluster-wide access to system:anonymous
kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.subjects[]?.name=="system:anonymous")'
```

### K01 — Insecure Workload Configurations

```yaml
# Use a PodSecurityAdmission policy (K8s >= 1.25)
# Add label to namespace:
kubectl label namespace production \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=latest

# Or use OPA/Gatekeeper / Kyverno to enforce policies.
# Example Kyverno policy to block privileged containers:
# https://kyverno.io/policies/pod-security/
```

### K03 — Secrets Management Failures

```bash
# Enable encryption at rest for Secrets
# /etc/kubernetes/encryption-config.yaml:
# apiVersion: apiserver.config.k8s.io/v1
# kind: EncryptionConfiguration
# resources:
#   - resources: [secrets]
#     providers:
#       - aescbc:
#           keys: [{name: key1, secret: <base64-key>}]

# Use external secrets management instead:
# - HashiCorp Vault + vault-agent-injector
# - AWS Secrets Manager / GCP Secret Manager via CSI driver
# - Azure Key Vault CSI provider
```

---

## LLM Judge Integration

When `--llm-judge` is passed (or `judge=LLMJudge()` in the Python API), the judge triages
each finding and adds annotations to the `K8sVulnerability` model:

```python
class K8sVulnerability(BaseModel):
    # ... standard fields ...
    llm_confidence: float | None = None   # 0.0–1.0 confidence score
    llm_reasoning: str = ""               # judge's explanation
```

The judge also enriches `remediation` with context-aware fix guidance. It falls back to
rule-based detection automatically when no API key is configured.

```bash
# Configure provider — any one env var is sufficient
# Priority: Gemini > Anthropic > OpenAI
export GEMINI_API_KEY="AIza..."       # 1st priority
export ANTHROPIC_API_KEY="sk-ant-..." # 2nd priority
export OPENAI_API_KEY="sk-..."        # 3rd priority

# Or via custom OpenAI-compatible endpoint (Ollama, LM Studio, etc.)
export OFFSEC_LLM_BASE_URL="http://localhost:11434/v1"
export OFFSEC_LLM_MODEL="llama3"
```

---

## Sample Console Output

```
╭──────────────────────────────────────────────────────────────╮
│           Kubernetes Cluster Security Scan                    │
│  Target  : 192.168.1.100                                      │
│  K8s     : ✅ YES  (v1.27.3)                                   │
│  Exposed : api_server:6443  kubelet:10250  etcd:2379          │
│  Vulns   : 3 critical  2 high  1 medium  — 6 total           │
│  OWASP   : K06, K07, K09                                      │
│  Duration: 4.2s                                               │
╰──────────────────────────────────────────────────────────────╯

Exposed Components
┌─────────────────────────┬───────┬───────────────┬─────┐
│ Component               │ Port  │ Auth          │ TLS │
├─────────────────────────┼───────┼───────────────┼─────┤
│ api_server              │ 6443  │ anonymous ⚠️  │ ✅  │
│ kubelet                 │ 10250 │ anonymous ⚠️  │ ✅  │
│ etcd                    │ 2379  │ anonymous ⚠️  │ ❌  │
└─────────────────────────┴───────┴───────────────┴─────┘

Vulnerabilities
┌────────────────────┬──────────┬───────┬─────────────────────────────────────────┐
│ ID                 │ OWASP    │ Sev   │ Title                                   │
├────────────────────┼──────────┼───────┼─────────────────────────────────────────┤
│ K8S-ADV-001        │ K06      │ CRIT  │ API Server Exposed Without Auth         │
│ K8S-ADV-002        │ K06      │ CRIT  │ Kubelet 10250 Exposed Without Auth      │
│ K8S-ADV-004        │ K06      │ CRIT  │ etcd Accessible Without Authentication  │
│ CVE-2018-1002105   │ K07      │ HIGH  │ API Server Privilege Escalation         │
│ K8S-ADV-003        │ K06      │ HIGH  │ Kubelet Read-Only Port (10255) Open     │
│ K8S-ADV-006        │ K07      │ MED   │ Scheduler Metrics Port Exposed          │
└────────────────────┴──────────┴───────┴─────────────────────────────────────────┘
```

---

## Scope and Limitations

| Limitation | Detail |
|------------|--------|
| No cluster credentials | Deep K01/K02/K03 auditing requires authenticated API access; scanner only sees what anonymous users can reach |
| No kubeconfig / SDK | Workload policy (OPA/Kyverno), NetworkPolicy presence, audit log config are not assessable via black-box probing |
| TLS verification disabled | `verify=False` is intentional — self-signed certs are common in K8s clusters; use on authorized targets only |
| CVE DB | Covers major pre-2025 CVEs; new CVEs require database updates |

For a full credentialed audit, combine with tools like `kube-bench`, `kubescape`, or `trivy operator`.

---

## Ethics and Legal Notice

> The `k8s-attack` command and all deep-mode probes require `--i-have-authorization`.
> **Only use against clusters you own or have explicit written authorization to test.**
> Unauthorized use constitutes a violation of the Computer Fraud and Abuse Act (CFAA),
> the Computer Misuse Act (CMA), and equivalent laws in your jurisdiction.

`K8sAttacker(authorized=False)` raises `AuthorizationRequired` at instantiation — the gate
cannot be bypassed. Every authorized attack invocation is written to the audit log.
