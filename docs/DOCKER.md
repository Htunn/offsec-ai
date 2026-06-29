# offsec-ai — Docker Documentation

🐳 **Official Docker Hub Repository**: [htunnthuthu/offsec-ai](https://hub.docker.com/r/htunnthuthu/offsec-ai)

A comprehensive, lightweight Docker container for network security testing, port scanning, L7 protection detection, SSL/TLS certificate analysis, AI/LLM OWASP scanning, MCP security scanning, and mTLS authentication testing. Perfect for DevSecOps pipelines, security assessments, and network troubleshooting.

## 📦 Available Tags

| Tag | Description | Size | Architectures |
|-----|-------------|------|---------------|
| `latest` | Latest stable release | ~60MB | `linux/amd64`, `linux/arm64` |
| `v2.0.2` | v2.0.2 — Docker Hub fix, author metadata, docs cleanup | ~60MB | `linux/amd64`, `linux/arm64` |
| `v2.0.1` | v2.0.1 — logo fix, docs cleanup | ~60MB | `linux/amd64`, `linux/arm64` |
| `v2.0.0` | v2.0.0 — AI/LLM scanner, MCP scanner, Gemini judge | ~60MB | `linux/amd64`, `linux/arm64` |

**Recommendation**: Use `latest` for the most recent features, or pin to specific version tags for production deployments.

## 🚀 Quick Start

```bash
# Run a basic port scan
docker run --rm htunnthuthu/offsec-ai:latest scan example.com

# Check for L7 protection (WAF/CDN)
docker run --rm htunnthuthu/offsec-ai:latest l7-check example.com

# Analyze SSL/TLS certificate chain
docker run --rm htunnthuthu/offsec-ai:latest cert-check example.com

# Full security scan with all features
docker run --rm htunnthuthu/offsec-ai:latest full-scan example.com
```

## ️ Usage Examples

### Basic Port Scanning
```bash
# Scan common ports
docker run --rm htunnthuthu/offsec-ai:latest scan google.com

# Scan specific ports
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --ports 80,443,8080,9000

# Scan multiple targets
docker run --rm htunnthuthu/offsec-ai:latest scan google.com cloudflare.com --concurrent 10
```

### L7 Protection Detection
```bash
# Basic L7 protection check
docker run --rm htunnthuthu/offsec-ai:latest l7-check example.com

# L7 check with DNS tracing
docker run --rm htunnthuthu/offsec-ai:latest l7-check example.com --trace-dns

# Check multiple sites for protection
docker run --rm htunnthuthu/offsec-ai:latest l7-check site1.com site2.com
```

### Certificate Chain Analysis
```bash
# Basic certificate analysis
docker run --rm htunnthuthu/offsec-ai:latest cert-check github.com

# Complete certificate chain analysis
docker run --rm htunnthuthu/offsec-ai:latest cert-chain example.com

# Detailed certificate information with PEM format
docker run --rm htunnthuthu/offsec-ai:latest cert-info example.com --show-pem

# Certificate analysis with custom port
docker run --rm htunnthuthu/offsec-ai:latest cert-check example.com --port 8443

# Save certificate analysis results
docker run --rm -v $(pwd)/results:/app/output \
  htunnthuthu/offsec-ai:latest cert-chain example.com \
  --output /app/output/cert-analysis.json

# Verify hostname against certificate
docker run --rm htunnthuthu/offsec-ai:latest cert-check example.com --no-verify-hostname

# Enable revocation checking (OCSP/CRL)
docker run --rm htunnthuthu/offsec-ai:latest cert-chain example.com --check-revocation
```

### mTLS Authentication Testing
```bash
# Check mTLS support
docker run --rm htunnthuthu/offsec-ai:latest mtls-check example.com

# Test with client certificates (mount volume)
docker run --rm -v /path/to/certs:/certs \
  htunnthuthu/offsec-ai:latest mtls-check example.com \
  --client-cert /certs/client.crt --client-key /certs/client.key

# Generate test certificates
docker run --rm -v $(pwd)/certs:/output \
  htunnthuthu/offsec-ai:latest mtls-gen-cert test.example.com \
  --output-dir /output
```

### Comprehensive Security Scanning
```bash
# Full scan with all features
docker run --rm htunnthuthu/offsec-ai:latest full-scan example.com

# Save results to host system
docker run --rm -v $(pwd)/results:/app/output \
  htunnthuthu/offsec-ai:latest full-scan example.com \
  --output /app/output/security-report.json

# Verbose output with detailed logging
docker run --rm htunnthuthu/offsec-ai:latest full-scan example.com --verbose
```

## 🏗️ Integration Examples

### CI/CD Pipeline Integration

#### GitHub Actions
```yaml
- name: Security Port Scan
  run: |
    docker run --rm -v ${{ github.workspace }}/reports:/app/output \
      htunnthuthu/offsec-ai:latest full-scan ${{ env.TARGET_HOST }} \
      --output /app/output/security-scan.json

- name: Certificate Analysis
  run: |
    docker run --rm -v ${{ github.workspace }}/reports:/app/output \
      htunnthuthu/offsec-ai:latest cert-chain ${{ env.TARGET_HOST }} \
      --output /app/output/cert-analysis.json --check-revocation
```

#### GitLab CI
```yaml
security_scan:
  image: docker:latest
  script:
    - docker run --rm -v $PWD/reports:/app/output 
        htunnthuthu/offsec-ai:latest full-scan $TARGET_HOST 
        --output /app/output/security-scan.json
    - docker run --rm -v $PWD/reports:/app/output
        htunnthuthu/offsec-ai:latest cert-chain $TARGET_HOST
        --output /app/output/cert-analysis.json
  artifacts:
    reports:
      paths:
        - reports/security-scan.json
        - reports/cert-analysis.json
```

#### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm -v $WORKSPACE/reports:/app/output \
                      htunnthuthu/offsec-ai:latest full-scan $TARGET_HOST \
                      --output /app/output/security-scan.json
                '''
                sh '''
                    docker run --rm -v $WORKSPACE/reports:/app/output \
                      htunnthuthu/offsec-ai:latest cert-chain $TARGET_HOST \
                      --output /app/output/cert-analysis.json --verbose
                '''
                archiveArtifacts artifacts: 'reports/*.json'
            }
        }
    }
}
```

### Docker Compose Integration
```yaml
version: '3.8'
services:
  port-scanner:
    image: htunnthuthu/offsec-ai:latest
    command: full-scan example.com --output /app/output/results.json
    volumes:
      - ./scan-results:/app/output
    environment:
      - TARGET_HOST=example.com
      
  cert-analyzer:
    image: htunnthuthu/offsec-ai:latest
    command: cert-chain example.com --output /app/output/cert-analysis.json --check-revocation
    volumes:
      - ./cert-results:/app/output
    environment:
      - TARGET_HOST=example.com
```

### Kubernetes Job
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: security-port-scan
spec:
  template:
    spec:
      containers:
      - name: port-scanner
        image: htunnthuthu/offsec-ai:latest
        command: ["offsec-ai", "full-scan", "example.com"]
        volumeMounts:
        - name: results-volume
          mountPath: /app/output
      volumes:
      - name: results-volume
        persistentVolumeClaim:
          claimName: scan-results-pvc
      restartPolicy: Never
---
apiVersion: batch/v1
kind: Job
metadata:
  name: certificate-analysis
spec:
  template:
    spec:
      containers:
      - name: cert-analyzer
        image: htunnthuthu/offsec-ai:latest
        command: ["offsec-ai", "cert-chain", "example.com", "--output", "/app/output/cert-analysis.json"]
        volumeMounts:
        - name: cert-volume
          mountPath: /app/output
      volumes:
      - name: cert-volume
        persistentVolumeClaim:
          claimName: cert-results-pvc
      restartPolicy: Never
```

## � Certificate Analysis Features

### Certificate Chain Analysis
- ✅ Complete SSL/TLS certificate chain extraction
- ✅ Certificate validation and trust path verification  
- ✅ Missing intermediate certificate detection
- ✅ Certificate expiration and validity checking
- ✅ Hostname validation against certificate SAN/CN

### Certificate Information
- ✅ Certificate subject and issuer details
- ✅ Public key algorithm and key size analysis
- ✅ Digital signature algorithm identification
- ✅ Certificate extensions parsing (Key Usage, EKU, etc.)
- ✅ Subject Alternative Names (SAN) extraction

### Trust and Security Analysis
- ✅ Chain of trust validation
- ✅ Self-signed certificate detection
- ✅ CA certificate identification
- ✅ OCSP and CRL URL extraction for revocation checking
- ✅ Certificate fingerprint generation (SHA-1, SHA-256)

## 🤖 AI / LLM Security Usage

The image ships with `openai` and `anthropic` pre-installed (`[ai]` extra). Pass an API key at runtime to enable the **LLM Judge** for smarter semantic vulnerability detection.

### AI OWASP Top 10 Scan (rule-based, no key required)
```bash
docker run --rm htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions
```

### AI OWASP Top 10 Scan with LLM Judge

```bash
# OpenAI judge
docker run --rm \
  -e OPENAI_API_KEY=sk-... \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge

# Anthropic judge
docker run --rm \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge

# Google Gemini judge (no extra package needed)
docker run --rm \
  -e GEMINI_API_KEY=AIzaSy... \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge

# Custom OpenAI-compatible endpoint (Ollama, LM Studio, Azure OpenAI, etc.)
docker run --rm \
  -e OFFSEC_LLM_BASE_URL=http://host.docker.internal:11434/v1 \
  -e OFFSEC_LLM_MODEL=llama3 \
  htunnthuthu/offsec-ai:latest \
  ai-owasp-scan https://api.example.com/v1/chat/completions --llm-judge
```

### MCP Security Scan
```bash
# Scan an MCP endpoint
docker run --rm htunnthuthu/offsec-ai:latest \
  mcp-scan https://mcp.example.com/mcp

# Active MCP attack (requires authorization flag)
docker run --rm htunnthuthu/offsec-ai:latest \
  mcp-attack https://mcp.example.com/mcp --i-have-authorization --mode deep
```

---

## 🔧 Configuration & Environment

### LLM / AI Judge Environment Variables

| Variable | Provider | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | OpenAI | Enables OpenAI judge (e.g. `gpt-4o-mini`) |
| `ANTHROPIC_API_KEY` | Anthropic | Enables Anthropic judge (e.g. `claude-3-haiku`) |
| `GEMINI_API_KEY` | Google | Enables Gemini judge (e.g. `gemini-1.5-flash`) |
| `OFFSEC_LLM_BASE_URL` | Any OpenAI-compatible | Use a custom/local endpoint as the judge backend |
| `OFFSEC_LLM_MODEL` | All | Override the default model name |

Provider is **auto-detected** from whichever key is set; `OFFSEC_LLM_BASE_URL` takes precedence over `OPENAI_API_KEY`.

### General Environment Variables
```bash
# Set timeout for operations
docker run --rm -e TIMEOUT=30 htunnthuthu/offsec-ai:latest scan example.com

# Enable debug logging
docker run --rm -e DEBUG=1 htunnthuthu/offsec-ai:latest l7-check example.com

# Certificate analysis timeout
docker run --rm -e CERT_TIMEOUT=15 htunnthuthu/offsec-ai:latest cert-chain example.com
```

### Volume Mounts
```bash
# Mount configuration directory
docker run --rm -v /host/config:/app/config \
  htunnthuthu/offsec-ai:latest scan example.com

# Mount output directory for reports
docker run --rm -v /host/reports:/app/output \
  htunnthuthu/offsec-ai:latest full-scan example.com \
  --output /app/output/report.json

# Mount certificate directory for mTLS
docker run --rm -v /host/certs:/app/certs \
  htunnthuthu/offsec-ai:latest mtls-check example.com \
  --client-cert /app/certs/client.crt --client-key /app/certs/client.key
```

## 🔒 Security Features

### Non-Root User
- ✅ Container runs as non-root user `appuser` (UID: 1000)
- ✅ No privileged access required
- ✅ Minimal attack surface

### Minimal Dependencies
- ✅ Based on Debian slim for minimal footprint
- ✅ Only essential packages included
- ✅ Regular security updates via automated builds

### Security Scanning
- ✅ Images scanned with Trivy for vulnerabilities
- ✅ Security reports available in repository
- ✅ SARIF format reports for integration

## 🏷️ Image Specifications

### Base Image
- **OS**: Debian GNU/Linux 12 Bookworm slim (`python:3.12-slim-bookworm`)
- **Python**: 3.12+
- **Architecture**: Multi-arch (AMD64, ARM64)
- **User**: Non-root (`appuser:appuser`, UID/GID 1000)

### Installed Tools
- ✅ `offsec-ai` (latest version)
- ✅ Python runtime and required dependencies
- ✅ `openai` & `anthropic` packages — bundled via `[ai]` extra; LLM judge activates automatically when you pass an API key env var
- ✅ SSL/TLS libraries for certificate handling
- ✅ DNS resolution utilities
- ✅ `nmap` for port scanning
- ✅ Cryptography libraries for certificate analysis

### Performance
- **Image Size**: ~55MB compressed (with certificate analysis tools)
- **Startup Time**: <2 seconds
- **Memory Usage**: <100MB typical, <150MB with certificate analysis
- **CPU Usage**: Optimized for concurrent operations
- **Certificate Analysis**: <5 seconds for typical certificate chains

## 📊 Output Formats

### JSON Output
```bash
# Structured JSON for automation
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --format json

# Pretty printed JSON
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --format json --pretty

# Certificate analysis in JSON format
docker run --rm htunnthuthu/offsec-ai:latest cert-chain example.com --output cert-results.json
```

### Text Output
```bash
# Human readable text (default)
docker run --rm htunnthuthu/offsec-ai:latest scan example.com

# Verbose text output
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --verbose
```

### CSV Output
```bash
# CSV format for spreadsheet import
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --format csv
```

## 🐛 Troubleshooting

### Common Issues

#### Permission Denied
```bash
# Ensure proper volume permissions
docker run --rm -v $(pwd)/output:/app/output:Z \
  htunnthuthu/offsec-ai:latest scan example.com \
  --output /app/output/results.json
```

#### Network Connectivity
```bash
# Test network connectivity
docker run --rm htunnthuthu/offsec-ai:latest scan google.com

# Use host networking if needed
docker run --rm --network host \
  htunnthuthu/offsec-ai:latest scan localhost
```

#### Certificate Issues
```bash
# Debug certificate chain retrieval
docker run --rm htunnthuthu/offsec-ai:latest cert-check example.com --verbose

# Disable hostname verification for testing
docker run --rm htunnthuthu/offsec-ai:latest cert-check example.com --no-verify-hostname

# Test certificate with custom port
docker run --rm htunnthuthu/offsec-ai:latest cert-info example.com --port 8443

# Show certificate in PEM format for inspection
docker run --rm htunnthuthu/offsec-ai:latest cert-info example.com --show-pem
```

### Debug Mode
```bash
# Enable verbose logging
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --verbose

# Get version information
docker run --rm htunnthuthu/offsec-ai:latest --version

# Display help
docker run --rm htunnthuthu/offsec-ai:latest --help
```

## 📈 Performance Tuning

### Concurrent Operations
```bash
# Adjust concurrency for better performance
docker run --rm htunnthuthu/offsec-ai:latest scan example.com --concurrent 20

# Scan multiple targets efficiently
docker run --rm htunnthuthu/offsec-ai:latest scan \
  site1.com site2.com site3.com --concurrent 10
```

### Resource Limits
```bash
# Set memory limits
docker run --rm --memory=512m htunnthuthu/offsec-ai:latest scan example.com

# Set CPU limits
docker run --rm --cpus=2 htunnthuthu/offsec-ai:latest full-scan example.com
```

## �️ Building & Publishing Locally

The `Makefile` provides convenience targets for building and pushing to Docker Hub.

```bash
# Build the image locally
make docker-build

# Build without cache
make docker-build-no-cache

# Build multi-arch (linux/amd64 + linux/arm64) — requires docker buildx
make docker-build-multi

# Push to Docker Hub (builds first, then tags + pushes :version and :latest)
make docker-push                              # uses DOCKER_USERNAME=htunnthuthu by default
make docker-push DOCKER_USERNAME=youruser     # override username

# Full release in one command
make docker-release                           # equivalent to docker-build + docker-push

# Test the local image
make docker-test

# Scan image for vulnerabilities (requires trivy)
make docker-scan

# Clean up local Docker artifacts
make docker-clean
```

The `DOCKER_VERSION` is read automatically from `pyproject.toml`, so the published tags match the package version exactly.

---

## �🔗 Related Links

- **GitHub Repository**: [Htunn/offsec-ai](https://github.com/Htunn/offsec-ai)
- **PyPI Package**: [offsec-ai](https://pypi.org/project/offsec-ai/)
- **Documentation**: [Project Docs](https://github.com/Htunn/offsec-ai/tree/main/docs)
- **Issues & Support**: [GitHub Issues](https://github.com/Htunn/offsec-ai/issues)
- **Security Policy**: [SECURITY.md](https://github.com/Htunn/offsec-ai/blob/main/SECURITY.md)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Htunn/offsec-ai/blob/main/LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/Htunn/offsec-ai/blob/main/CONTRIBUTING.md) for details.

---

**Maintainer**: [htunnthuthu](https://github.com/Htunn) (htunnthuthu.linux@gmail.com)  
**Last Updated**: June 29, 2026  
**Docker Hub**: [htunnthuthu/offsec-ai](https://hub.docker.com/r/htunnthuthu/offsec-ai)
