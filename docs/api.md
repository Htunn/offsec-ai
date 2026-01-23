# Simple Port Checker - Python API Documentation

This document provides comprehensive API documentation for using Simple Port Checker as a Python module.

## Installation

```bash
pip install simple-port-checker
```

## Quick Start

```python
import asyncio
from simple_port_checker import PortChecker, L7Detector, CertificateAnalyzer, MTLSChecker, HybridIdentityChecker, OwaspScanner

async def main():
    # Basic port scanning
    scanner = PortChecker()
    result = await scanner.scan_host("example.com")
    print(f"Open ports: {[p.port for p in result.open_ports]}")
    
    # L7 protection detection
    detector = L7Detector()
    l7_result = await detector.detect("example.com")
    if l7_result.is_protected:
        print(f"Protected by: {l7_result.primary_protection.service.value}")
    
    # SSL/TLS certificate analysis
    cert_analyzer = CertificateAnalyzer()
    cert_chain = await cert_analyzer.analyze_certificate_chain("example.com", 443)
    print(f"Certificate Subject: {cert_chain.server_cert.subject}")
    print(f"Issuer: {cert_chain.server_cert.issuer}")
    print(f"Valid: {cert_chain.server_cert.is_valid_now}")
    print(f"Chain Complete: {cert_chain.chain_complete}")
    
    # OWASP Top 10 vulnerability scanning
    owasp_scanner = OwaspScanner(mode="safe")
    owasp_result = await owasp_scanner.scan("example.com")
    print(f"Security Grade: {owasp_result.overall_grade}")
    print(f"Total Findings: {len(owasp_result.all_findings)}")
    
    # Hybrid identity detection
    hybrid_checker = HybridIdentityChecker()
    hybrid_result = await hybrid_checker.check("example.com")
    if hybrid_result.has_hybrid_identity:
        print(f"Hybrid Identity: Detected")
        if hybrid_result.adfs_endpoint:
            print(f"ADFS Endpoint: {hybrid_result.adfs_endpoint}")

asyncio.run(main())
```

## Core Classes

### PortChecker

The main class for port scanning operations.

#### Constructor

```python
from simple_port_checker import PortChecker
from simple_port_checker.core.port_scanner import ScanConfig

# Default configuration
scanner = PortChecker()

# Custom configuration
config = ScanConfig(
    timeout=5.0,
    concurrent_limit=100,
    delay_between_requests=0.1
)
scanner = PortChecker(config)
```

#### Methods

##### `scan_host(host, ports=None, timeout=None)`

Scan a single host for open ports.

**Parameters:**
- `host` (str): Target hostname or IP address
- `ports` (List[int], optional): List of ports to scan. Defaults to common ports
- `timeout` (float, optional): Connection timeout in seconds

**Returns:** `ScanResult` object

**Example:**
```python
# Scan common ports
result = await scanner.scan_host("example.com")

# Scan specific ports
result = await scanner.scan_host("example.com", [80, 443, 8080])

# Custom timeout
result = await scanner.scan_host("example.com", timeout=10.0)
```

##### `scan_multiple_hosts(hosts, ports=None, timeout=None)`

Scan multiple hosts concurrently.

**Parameters:**
- `hosts` (List[str]): List of hostnames or IP addresses
- `ports` (List[int], optional): List of ports to scan
- `timeout` (float, optional): Connection timeout in seconds

**Returns:** `List[ScanResult]`

**Example:**
```python
hosts = ["google.com", "github.com", "stackoverflow.com"]
results = await scanner.scan_multiple_hosts(hosts, [80, 443])

for result in results:
    print(f"{result.host}: {len(result.open_ports)} open ports")
```

##### `check_service_version(host, port, service_type=None)`

Get detailed service information for a specific port.

**Parameters:**
- `host` (str): Target hostname or IP address
- `port` (int): Port number to check
- `service_type` (str, optional): Expected service type

**Returns:** `Dict[str, Any]` with service information

**Example:**
```python
service_info = await scanner.check_service_version("example.com", 80, "http")
print(f"Server: {service_info['headers'].get('Server', 'Unknown')}")
```

### L7Detector

The main class for L7 protection detection (WAF, CDN, etc.).

#### Constructor

```python
from simple_port_checker import L7Detector

# Default configuration
detector = L7Detector()

# Custom configuration
detector = L7Detector(
    timeout=15.0,
    user_agent="Custom-Agent/1.0"
)
```

#### Methods

##### `detect(host, port=None, path="/", trace_dns=False)`

Detect L7 protection services on a host.

**Parameters:**
- `host` (str): Target hostname or IP address
- `port` (int, optional): Specific port to check
- `path` (str, optional): URL path to check. Defaults to "/"
- `trace_dns` (bool, optional): Include DNS tracing in detection

**Returns:** `L7Result` object

**Example:**
```python
# Basic detection
result = await detector.detect("cloudflare.com")

# With DNS tracing
result = await detector.detect("example.com", trace_dns=True)

# Specific port and path
result = await detector.detect("example.com", port=8080, path="/api")

if result.is_protected:
    protection = result.primary_protection
    print(f"Service: {protection.service.value}")
    print(f"Confidence: {protection.confidence:.1%}")
    print(f"Indicators: {protection.indicators}")
```

##### `trace_dns(host)`

Perform DNS trace analysis to identify protection services.

**Parameters:**
- `host` (str): Target hostname

**Returns:** `Dict[str, Any]` with DNS trace information

**Example:**
```python
dns_info = await detector.trace_dns("example.com")
print(f"CNAME chain: {dns_info['cname_chain']}")
print(f"Resolved IPs: {dns_info['resolved_ips']}")
```

##### `test_waf_bypass(host, port=None)`

Test for WAF presence using common bypass techniques.

**Parameters:**
- `host` (str): Target hostname
- `port` (int, optional): Port number

**Returns:** `Dict[str, Any]` with WAF test results

**Example:**
```python
waf_results = await detector.test_waf_bypass("example.com")
print(f"WAF detected: {waf_results['waf_detected']}")
print(f"Blocked requests: {len(waf_results['blocked_requests'])}")
```

### HybridIdentityChecker

Class for detecting hybrid identity setup, ADFS endpoints, and Azure AD integration. This checker uses the same method as Azure Portal to discover ADFS endpoints by querying the Azure AD realm API.

#### Constructor

```python
from simple_port_checker import HybridIdentityChecker

# Default configuration
checker = HybridIdentityChecker()

# Custom timeout
checker = HybridIdentityChecker(timeout=15.0)
```

**Parameters:**
- `timeout` (float): Request timeout in seconds (default: 10.0)

#### Methods

##### `check(fqdn)`

Check if a domain has hybrid identity setup and detect ADFS endpoints.

This checks for:
- ADFS endpoints via Azure AD login flow (most reliable method)
- Direct ADFS endpoints (/adfs/ls)
- Federation metadata
- Azure AD integration
- OpenID Connect configuration
- DNS records for Microsoft verification

**Parameters:**
- `fqdn` (str): Fully Qualified Domain Name to check

**Returns:** `HybridIdentityResult` object

**Example:**
```python
# Basic hybrid identity check
result = await checker.check("example.com")

if result.has_hybrid_identity:
    print("✅ Hybrid Identity Detected")
    
    if result.has_adfs:
        print(f"ADFS Endpoint: {result.adfs_endpoint}")
        print(f"Status Code: {result.adfs_status_code}")
    
    if result.federation_metadata_found:
        print("Federation Metadata: Found")
    
    if result.azure_ad_detected:
        print("Azure AD Integration: Detected")
    
    if result.openid_config_found:
        print("OpenID Configuration: Found")
else:
    print("⚠️  No Hybrid Identity Found")

# Check DNS records
if result.dns_records:
    if 'microsoft_verification' in result.dns_records:
        print("Microsoft Verification: Found")
    if 'adfs_subdomains' in result.dns_records:
        print(f"ADFS Subdomains: {result.dns_records['adfs_subdomains']}")

# Error handling
if result.error:
    print(f"Error: {result.error}")
```

##### `batch_check(fqdns, max_concurrent=10)`

Check multiple domains for hybrid identity setup concurrently.

**Parameters:**
- `fqdns` (List[str]): List of domain names to check
- `max_concurrent` (int, optional): Maximum concurrent checks. Defaults to 10

**Returns:** `List[HybridIdentityResult]`

**Example:**
```python
domains = ["company1.com", "company2.com", "company3.com"]
results = await checker.batch_check(domains, max_concurrent=5)

for result in results:
    status = "✅" if result.has_hybrid_identity else "❌"
    adfs = f" - {result.adfs_endpoint}" if result.adfs_endpoint else ""
    print(f"{status} {result.fqdn}{adfs}")

# Summary statistics
hybrid_count = sum(1 for r in results if r.has_hybrid_identity)
adfs_count = sum(1 for r in results if r.has_adfs)
print(f"\nHybrid Identity: {hybrid_count}/{len(results)}")
print(f"ADFS Endpoints: {adfs_count}/{len(results)}")
```

### MTLSChecker

Class for checking mTLS (Mutual TLS) authentication support and requirements.

#### Constructor

```python
from simple_port_checker import MTLSChecker

# Default configuration
checker = MTLSChecker()

# Custom configuration
checker = MTLSChecker(timeout=10, verify_ssl=True)
```

**Parameters:**
- `timeout` (int): Connection timeout in seconds (default: 10)
- `verify_ssl` (bool): Whether to verify SSL certificates (default: True)

#### Methods

##### `check_mtls(target, port=443, client_cert_path=None, client_key_path=None, ca_bundle_path=None)`

Check if target supports mTLS authentication.

**Parameters:**
- `target` (str): Target hostname or IP address
- `port` (int): Target port (default: 443)
- `client_cert_path` (str, optional): Path to client certificate file (PEM format)
- `client_key_path` (str, optional): Path to client private key file (PEM format)
- `ca_bundle_path` (str, optional): Path to CA bundle file

**Returns:** `MTLSResult` object

**Example:**
```python
# Basic mTLS check
result = await checker.check_mtls("example.com")
print(f"Supports mTLS: {result.supports_mtls}")
print(f"Requires client cert: {result.requires_client_cert}")

# With client certificates
result = await checker.check_mtls(
    "example.com", 
    client_cert_path="client.crt",
    client_key_path="client.key"
)
print(f"Handshake successful: {result.handshake_successful}")
print(f"TLS version: {result.tls_version}")
```

##### `batch_check_mtls(targets, client_cert_path=None, client_key_path=None, ca_bundle_path=None, max_concurrent=10)`

Perform mTLS checks on multiple targets concurrently.

**Parameters:**
- `targets` (List[Tuple[str, int]]): List of (hostname, port) tuples
- `client_cert_path` (str, optional): Path to client certificate file
- `client_key_path` (str, optional): Path to client private key file
- `ca_bundle_path` (str, optional): Path to CA bundle file
- `max_concurrent` (int): Maximum concurrent connections (default: 10)

**Returns:** `List[MTLSResult]`

**Example:**
```python
targets = [
    ("example.com", 443),
    ("test.example.com", 8443),
]

results = await checker.batch_check_mtls(targets)
for result in results:
    print(f"{result.target}:{result.port} - mTLS: {result.supports_mtls}")
```

### CertificateAnalyzer

The CertificateAnalyzer class provides comprehensive SSL/TLS certificate chain analysis and validation capabilities with enhanced trusted root CA database (Amazon Trust Services, Let's Encrypt, GlobalSign, Google Trust Services, etc.).

#### Constructor

```python
from simple_port_checker import CertificateAnalyzer

# Default configuration
analyzer = CertificateAnalyzer()

# Custom timeout
analyzer = CertificateAnalyzer(timeout=15.0)
```

**Parameters:**
- `timeout` (float): Connection timeout in seconds (default: 10.0)

#### Methods

##### `analyze_certificate_chain(host, port=443)`

Analyze the complete SSL/TLS certificate chain for a target host.

**Parameters:**
- `host` (str): Target hostname
- `port` (int): Target port (default: 443)

**Returns:** `CertificateChain` object

**Example:**
```python
# Basic certificate chain analysis
cert_chain = await analyzer.analyze_certificate_chain("github.com")

# Custom port
cert_chain = await analyzer.analyze_certificate_chain("example.com", 8443)

# Check results
print(f"Chain valid: {cert_chain.chain_valid}")
print(f"Chain complete: {cert_chain.chain_complete}")
print(f"Server cert subject: {cert_chain.server_cert.subject}")
print(f"Intermediate certs: {len(cert_chain.intermediate_certs)}")

if cert_chain.missing_intermediates:
    print("Missing intermediates:")
    for missing in cert_chain.missing_intermediates:
        print(f"  - {missing}")
```

##### `validate_hostname(cert, hostname)`

Validate if a certificate is valid for the given hostname (including wildcard support).

**Parameters:**
- `cert` (x509.Certificate): Certificate object to validate
- `hostname` (str): Hostname to validate against

**Returns:** `bool`

**Example:**
```python
# Get certificate chain first
cert_chain = await analyzer.analyze_certificate_chain("github.com")
server_cert = cert_chain.server_cert.raw_cert

# Validate hostname
is_valid = analyzer.validate_hostname(server_cert, "github.com")
print(f"Hostname valid: {is_valid}")

# Test with different hostname
is_valid_www = analyzer.validate_hostname(server_cert, "www.github.com")
print(f"www.github.com valid: {is_valid_www}")
```

##### `check_certificate_revocation(ocsp_url)`

Check certificate revocation status using OCSP (placeholder implementation).

**Parameters:**
- `ocsp_url` (str): OCSP URL to check

**Returns:** `Dict[str, Any]` with revocation status information

**Example:**
```python
# Get OCSP URLs from certificate chain
cert_chain = await analyzer.analyze_certificate_chain("example.com")
ocsp_urls = cert_chain.ocsp_urls

if ocsp_urls:
    revocation_status = analyzer.check_certificate_revocation(ocsp_urls[0])
    print(f"Revocation status: {revocation_status['status']}")
```

## Data Models

### ScanResult

Contains the results of a port scan operation.

**Attributes:**
- `host` (str): Target hostname
- `ip_address` (str): Resolved IP address
- `ports` (List[PortResult]): List of port scan results
- `scan_time` (float): Time taken for the scan
- `error` (str, optional): Error message if scan failed

**Properties:**
- `open_ports`: List of open port results
- `closed_ports`: List of closed port results

**Example:**
```python
result = await scanner.scan_host("example.com")
print(f"Host: {result.host}")
print(f"IP: {result.ip_address}")
print(f"Scan time: {result.scan_time:.2f}s")

for port in result.open_ports:
    print(f"Port {port.port}: {port.service}")
```

### PortResult

Contains information about a single port.

**Attributes:**
- `port` (int): Port number
- `is_open` (bool): Whether the port is open
- `service` (str): Service name (e.g., "http", "ssh")
- `banner` (str): Service banner if available
- `error` (str, optional): Error message if applicable

### L7Result

Contains the results of L7 protection detection.

**Attributes:**
- `host` (str): Target hostname
- `url` (str): Full URL that was checked
- `detections` (List[L7Detection]): List of detected protection services
- `response_headers` (Dict[str, str]): HTTP response headers
- `response_time` (float): Response time in seconds
- `status_code` (int, optional): HTTP status code
- `error` (str, optional): Error message if detection failed
- `dns_trace` (Dict[str, Any], optional): DNS trace information

**Properties:**
- `is_protected`: Whether any L7 protection was detected
- `primary_protection`: The protection service with highest confidence

**Example:**
```python
result = await detector.detect("cloudflare.com")
print(f"Protected: {result.is_protected}")

if result.primary_protection:
    protection = result.primary_protection
    print(f"Service: {protection.service.value}")
    print(f"Confidence: {protection.confidence:.1%}")

# Example with Microsoft HTTPAPI/2.0 (ADFS server)
result = await detector.detect("loginfs.ntu.edu.sg")
if result.primary_protection and result.primary_protection.service == L7Protection.MICROSOFT_HTTPAPI:
    print(f"Detected: {result.primary_protection.get_display_name()}")  # MS WAP or F5 Proxy
    print(f"Confidence: {result.primary_protection.confidence:.1%}")    # 100.0%
```

### L7Detection

Information about a detected L7 protection service.

**Attributes:**
- `service` (L7Protection): The protection service type
- `confidence` (float): Confidence level (0.0 to 1.0)
- `indicators` (List[str]): Evidence that led to this detection
- `details` (Dict[str, Any]): Additional detection details

### L7Protection

Enumeration of supported L7 protection services.

**Values:**
- `CLOUDFLARE`: Cloudflare WAF and DDoS Protection
- `AWS_WAF`: Amazon Web Application Firewall
- `AZURE_WAF`: Microsoft Azure Web Application Firewall
- `AZURE_FRONT_DOOR`: Azure Front Door
- `MICROSOFT_HTTPAPI`: Microsoft HTTPAPI/2.0 (Windows Web Application Proxy or F5-protected ADFS Server)
- `F5_BIG_IP`: F5 Application Security Manager (Enhanced detection for banking/enterprise F5 deployments)
- `AKAMAI`: Akamai Web Application Protector
- `IMPERVA`: Imperva SecureSphere WAF
- `SUCURI`: Sucuri Website Firewall
- `FASTLY`: Fastly Edge Security
- `KEYCDN`: KeyCDN Security
- `MAXCDN`: MaxCDN Security
- `INCAPSULA`: Incapsula (now part of Imperva)
- `BARRACUDA`: Barracuda WAF
- `FORTINET`: FortiWeb WAF
- `CITRIX`: Citrix NetScaler
- `RADWARE`: Radware DefensePro
- `UNKNOWN`: Unknown protection service

### HybridIdentityResult

Contains the results of hybrid identity detection checks.

**Attributes:**
- `fqdn` (str): Fully Qualified Domain Name checked
- `has_hybrid_identity` (bool): Whether hybrid identity setup was detected
- `has_adfs` (bool): Whether ADFS endpoint was found
- `adfs_endpoint` (str, optional): Full ADFS endpoint URL if found
- `adfs_status_code` (int, optional): HTTP status code from ADFS endpoint
- `federation_metadata_found` (bool): Whether federation metadata was found
- `azure_ad_detected` (bool): Whether Azure AD integration was detected
- `openid_config_found` (bool): Whether OpenID Connect configuration was found
- `dns_records` (Dict[str, List[str]]): DNS records found for the domain
- `error` (str, optional): Error message if check failed
- `response_time` (float): Total response time in seconds

**Example:**
```python
result = await checker.check("example.com")

print(f"Domain: {result.fqdn}")
print(f"Hybrid Identity: {result.has_hybrid_identity}")
print(f"ADFS: {result.has_adfs}")
print(f"Response Time: {result.response_time:.2f}s")

if result.adfs_endpoint:
    print(f"ADFS Endpoint: {result.adfs_endpoint}")
    print(f"Status Code: {result.adfs_status_code}")

# Convert to dictionary for JSON serialization
result_dict = result.to_dict()
```

### MTLSResult

Contains the results of mTLS authentication checks.

**Attributes:**
- `target` (str): Target hostname or IP address
- `port` (int): Target port number
- `supports_mtls` (bool): Whether the target supports mTLS
- `requires_client_cert` (bool): Whether client certificate is required
- `server_cert_info` (CertificateInfo, optional): Server certificate information
- `client_cert_requested` (bool): Whether server requests client certificate
- `handshake_successful` (bool): Whether mTLS handshake was successful
- `error_message` (str, optional): Error message if check failed
- `cipher_suite` (str, optional): Cipher suite used in successful connection
- `tls_version` (str, optional): TLS version used
- `verification_mode` (str, optional): Certificate verification mode
- `ca_bundle_path` (str, optional): Path to CA bundle used

### CertificateInfo

Contains detailed information about a single SSL/TLS certificate.

**Attributes:**
- `subject` (str): Certificate subject (Distinguished Name)
- `issuer` (str): Certificate issuer (Distinguished Name)
- `serial_number` (str): Certificate serial number
- `fingerprint_sha1` (str): SHA-1 fingerprint of the certificate
- `fingerprint_sha256` (str): SHA-256 fingerprint of the certificate
- `not_before` (datetime): Certificate validity start date
- `not_after` (datetime): Certificate validity end date
- `is_ca` (bool): Whether this is a Certificate Authority certificate
- `is_self_signed` (bool): Whether the certificate is self-signed
- `is_expired` (bool): Whether the certificate is expired
- `is_valid_now` (bool): Whether the certificate is currently valid
- `key_size` (int): Public key size in bits
- `signature_algorithm` (str): Signature algorithm used
- `public_key_algorithm` (str): Public key algorithm
- `san_domains` (List[str]): Subject Alternative Names (domains)
- `extensions` (Dict[str, Any]): Certificate extensions
- `pem_data` (str): Certificate in PEM format
- `raw_cert` (x509.Certificate): Raw cryptography certificate object

**Example:**
```python
cert_chain = await analyzer.analyze_certificate_chain("github.com")
server_cert = cert_chain.server_cert

print(f"Subject: {server_cert.subject}")
print(f"Issuer: {server_cert.issuer}")
print(f"Valid from: {server_cert.not_before}")
print(f"Valid until: {server_cert.not_after}")
print(f"Key size: {server_cert.key_size} bits")
print(f"SAN domains: {server_cert.san_domains}")
print(f"Is CA: {server_cert.is_ca}")
print(f"Self-signed: {server_cert.is_self_signed}")
```

### CertificateChain

Contains the complete SSL/TLS certificate chain analysis results.

**Attributes:**
- `server_cert` (CertificateInfo): Server (end-entity) certificate
- `intermediate_certs` (List[CertificateInfo]): Intermediate CA certificates
- `root_cert` (CertificateInfo, optional): Root CA certificate (if available)
- `chain_valid` (bool): Whether the certificate chain is valid
- `chain_complete` (bool): Whether the certificate chain is complete
- `missing_intermediates` (List[str]): List of missing intermediate certificates
- `trust_issues` (List[str]): List of trust validation issues
- `ocsp_urls` (List[str]): OCSP URLs extracted from certificates
- `crl_urls` (List[str]): CRL URLs extracted from certificates

**Example:**
```python
cert_chain = await analyzer.analyze_certificate_chain("example.com")

# Chain validation
print(f"Chain valid: {cert_chain.chain_valid}")
print(f"Chain complete: {cert_chain.chain_complete}")

# Certificate hierarchy
print(f"Server cert: {cert_chain.server_cert.subject}")
print(f"Intermediate certs: {len(cert_chain.intermediate_certs)}")
for i, cert in enumerate(cert_chain.intermediate_certs):
    print(f"  Intermediate {i+1}: {cert.subject}")

if cert_chain.root_cert:
    print(f"Root cert: {cert_chain.root_cert.subject}")

# Issues and warnings
if cert_chain.missing_intermediates:
    print("Missing intermediates:")
    for missing in cert_chain.missing_intermediates:
        print(f"  - {missing}")

if cert_chain.trust_issues:
    print("Trust issues:")
    for issue in cert_chain.trust_issues:
        print(f"  - {issue}")

# Revocation information
print(f"OCSP URLs: {cert_chain.ocsp_urls}")
print(f"CRL URLs: {cert_chain.crl_urls}")
```
- `timestamp` (str): Timestamp of the check

**Example:**
```python
result = await checker.check_mtls("example.com")
print(f"mTLS supported: {result.supports_mtls}")
print(f"Client cert required: {result.requires_client_cert}")

if result.server_cert_info:
    cert = result.server_cert_info
    print(f"Server cert subject: {cert.subject}")
    print(f"Valid until: {cert.not_valid_after}")
```

### CertificateInfo

Information about an X.509 certificate.

**Attributes:**
- `subject` (str): Certificate subject DN
- `issuer` (str): Certificate issuer DN
- `version` (int): Certificate version
- `serial_number` (str): Certificate serial number
- `not_valid_before` (str): Certificate validity start date
- `not_valid_after` (str): Certificate validity end date
- `signature_algorithm` (str): Signature algorithm used
- `key_algorithm` (str): Public key algorithm
- `key_size` (int, optional): Public key size in bits
- `san_dns_names` (List[str]): Subject Alternative Name DNS entries
- `san_ip_addresses` (List[str]): Subject Alternative Name IP entries
- `is_ca` (bool): Whether this is a CA certificate
- `is_self_signed` (bool): Whether this is a self-signed certificate
- `fingerprint_sha256` (str): SHA-256 fingerprint of the certificate

**Example:**
```python
if result.server_cert_info:
    cert = result.server_cert_info
    print(f"Subject: {cert.subject}")
    print(f"Algorithm: {cert.key_algorithm} ({cert.key_size} bits)")
    print(f"SAN DNS: {', '.join(cert.san_dns_names)}")
    print(f"Fingerprint: {cert.fingerprint_sha256}")
```

### BatchMTLSResult

Contains the results of batch mTLS checks.

**Attributes:**
- `results` (List[MTLSResult]): Individual mTLS check results
- `total_targets` (int): Total number of targets checked
- `successful_checks` (int): Number of successful checks
- `failed_checks` (int): Number of failed checks
- `mtls_supported_count` (int): Number of targets supporting mTLS
- `mtls_required_count` (int): Number of targets requiring client certificates
- `timestamp` (str): Batch operation timestamp

**Example:**
```python
batch_result = BatchMTLSResult.from_results(results)
print(f"Total: {batch_result.total_targets}")
print(f"mTLS supported: {batch_result.mtls_supported_count}")
print(f"Success rate: {batch_result.successful_checks / batch_result.total_targets:.1%}")
```

## Configuration

### ScanConfig

Configuration class for port scanning operations.

**Parameters:**
- `timeout` (float): Connection timeout in seconds. Default: 3.0
- `concurrent_limit` (int): Maximum concurrent connections. Default: 100
- `delay_between_requests` (float): Delay between requests in seconds. Default: 0.0

**Example:**
```python
from simple_port_checker.core.port_scanner import ScanConfig

config = ScanConfig(
    timeout=5.0,
    concurrent_limit=50,
    delay_between_requests=0.1
)

scanner = PortChecker(config)
```

## Error Handling

The library raises standard Python exceptions and includes error information in result objects.

```python
try:
    result = await scanner.scan_host("invalid-hostname.local")
    if result.error:
        print(f"Scan error: {result.error}")
        
    l7_result = await detector.detect("example.com")
    if l7_result.error:
        print(f"Detection error: {l7_result.error}")
        
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Use Cases

### Security Assessment

```python
async def security_assessment(target):
    scanner = PortChecker()
    detector = L7Detector()
    
    # 1. Port scan
    scan_result = await scanner.scan_host(target)
    print(f"Open ports: {[p.port for p in scan_result.open_ports]}")
    
    # 2. L7 protection check
    l7_result = await detector.detect(target, trace_dns=True)
    if l7_result.is_protected:
        print(f"Protected by: {l7_result.primary_protection.service.value}")
    
    # 3. Service fingerprinting
    for port in scan_result.open_ports[:5]:  # Check first 5 open ports
        service_info = await scanner.check_service_version(
            target, port.port, port.service
        )
        print(f"Port {port.port}: {service_info['service']} {service_info['version']}")
```

### Batch Processing

```python
async def scan_multiple_targets(targets):
    scanner = PortChecker()
    detector = L7Detector()
    
    # Concurrent port scanning
    scan_results = await scanner.scan_multiple_hosts(targets, [80, 443])
    
    # Concurrent L7 detection
    l7_tasks = [detector.detect(target) for target in targets]
    l7_results = await asyncio.gather(*l7_tasks, return_exceptions=True)
    
    # Process results
    for i, target in enumerate(targets):
        scan_result = scan_results[i]
        l7_result = l7_results[i] if not isinstance(l7_results[i], Exception) else None
        
        print(f"\n{target}:")
        print(f"  Open ports: {len(scan_result.open_ports)}")
        if l7_result and l7_result.is_protected:
            print(f"  Protection: {l7_result.primary_protection.service.value}")
```

### Custom Analysis

```python
async def custom_waf_analysis(target):
    detector = L7Detector()
    
    # Standard detection
    result = await detector.detect(target)
    
    # DNS analysis
    dns_info = await detector.trace_dns(target)
    
    # WAF bypass testing (use responsibly!)
    waf_test = await detector.test_waf_bypass(target)
    
    # Combine results
    analysis = {
        'target': target,
        'protection_detected': result.is_protected,
        'protection_services': [d.service.value for d in result.detections],
        'dns_chain': dns_info.get('cname_chain', []),
        'waf_behavior': waf_test['waf_detected']
    }
    
    return analysis
```

### mTLS Authentication Testing

```python
async def mtls_security_assessment(targets):
    checker = MTLSChecker(timeout=10)
    
    # Batch check for mTLS support
    target_ports = [(target, 443) for target in targets]
    results = await checker.batch_check_mtls(target_ports)
    
    for result in results:
        print(f"\n{result.target}:{result.port}")
        print(f"  Supports mTLS: {result.supports_mtls}")
        print(f"  Requires client cert: {result.requires_client_cert}")
        
        if result.server_cert_info:
            cert = result.server_cert_info
            print(f"  Certificate issuer: {cert.issuer}")
            print(f"  Key algorithm: {cert.key_algorithm} ({cert.key_size} bits)")
            
        if result.error_message:
            print(f"  Error: {result.error_message}")

# Generate test certificates
from simple_port_checker.core.mtls_checker import generate_self_signed_cert

async def test_with_client_certs(target):
    # Generate certificates for testing
    cert_path = "test_client.crt"
    key_path = "test_client.key"
    
    if generate_self_signed_cert("test-client", cert_path, key_path):
        checker = MTLSChecker()
        
        # Test with client certificates
        result = await checker.check_mtls(
            target,
            client_cert_path=cert_path,
            client_key_path=key_path
        )
        
        print(f"mTLS handshake successful: {result.handshake_successful}")
        print(f"TLS version: {result.tls_version}")
        print(f"Cipher suite: {result.cipher_suite}")
        
        # Clean up
        Path(cert_path).unlink(missing_ok=True)
        Path(key_path).unlink(missing_ok=True)
```

## Performance Considerations

- Use `ScanConfig` to tune performance for your network conditions
- The library uses async/await for concurrent operations
- DNS resolution is cached automatically
- Consider rate limiting for large-scale scans
- Use `trace_dns=True` only when needed as it adds overhead

## Usage Examples

### Complete Certificate Chain Analysis

```python
import asyncio
from simple_port_checker import CertificateAnalyzer

async def analyze_website_certificates():
    analyzer = CertificateAnalyzer(timeout=15.0)
    
    # Analyze multiple websites
    websites = ["github.com", "google.com", "stackoverflow.com"]
    
    for site in websites:
        print(f"\n=== Analyzing {site} ===")
        try:
            cert_chain = await analyzer.analyze_certificate_chain(site)
            
            # Basic certificate info
            server_cert = cert_chain.server_cert
            print(f"Subject: {server_cert.subject}")
            print(f"Issuer: {server_cert.issuer}")
            print(f"Valid: {server_cert.not_before} to {server_cert.not_after}")
            print(f"Key Algorithm: {server_cert.public_key_algorithm} ({server_cert.key_size} bits)")
            print(f"Signature Algorithm: {server_cert.signature_algorithm}")
            
            # Certificate status
            print(f"Currently Valid: {server_cert.is_valid_now}")
            print(f"Expired: {server_cert.is_expired}")
            print(f"Self-Signed: {server_cert.is_self_signed}")
            print(f"Is CA: {server_cert.is_ca}")
            
            # SAN domains
            if server_cert.san_domains:
                print(f"SAN Domains: {', '.join(server_cert.san_domains[:5])}")
                if len(server_cert.san_domains) > 5:
                    print(f"  ... and {len(server_cert.san_domains) - 5} more")
            
            # Chain analysis
            print(f"\nChain Analysis:")
            print(f"  Chain Valid: {cert_chain.chain_valid}")
            print(f"  Chain Complete: {cert_chain.chain_complete}")
            print(f"  Intermediate Certs: {len(cert_chain.intermediate_certs)}")
            print(f"  Has Root Cert: {'Yes' if cert_chain.root_cert else 'No'}")
            
            # Show certificate hierarchy
            print(f"\nCertificate Hierarchy:")
            print(f"  Server: {server_cert.subject}")
            for i, intermediate in enumerate(cert_chain.intermediate_certs):
                print(f"  Intermediate {i+1}: {intermediate.subject}")
            if cert_chain.root_cert:
                print(f"  Root: {cert_chain.root_cert.subject}")
            
            # Trust issues
            if cert_chain.trust_issues:
                print(f"\nTrust Issues:")
                for issue in cert_chain.trust_issues:
                    print(f"  - {issue}")
            
            # Missing intermediates
            if cert_chain.missing_intermediates:
                print(f"\nMissing Intermediates:")
                for missing in cert_chain.missing_intermediates:
                    print(f"  - {missing}")
            
            # Revocation information
            if cert_chain.ocsp_urls:
                print(f"\nOCSP URLs: {', '.join(cert_chain.ocsp_urls[:3])}")
            if cert_chain.crl_urls:
                print(f"CRL URLs: {', '.join(cert_chain.crl_urls[:3])}")
                
        except Exception as e:
            print(f"Error analyzing {site}: {e}")

asyncio.run(analyze_website_certificates())
```

### Certificate Validation and Hostname Checking

```python
import asyncio
from simple_port_checker import CertificateAnalyzer

async def validate_certificate_hostname():
    analyzer = CertificateAnalyzer()
    
    # Test hostname validation
    cert_chain = await analyzer.analyze_certificate_chain("github.com")
    server_cert_raw = cert_chain.server_cert.raw_cert
    
    # Test various hostnames
    test_hostnames = [
        "github.com",          # Should be valid
        "www.github.com",      # Should be valid (SAN)
        "api.github.com",      # May be valid (SAN)
        "invalid.github.com",  # Should be invalid
        "example.com"          # Should be invalid
    ]
    
    print("Hostname Validation Results:")
    for hostname in test_hostnames:
        is_valid = analyzer.validate_hostname(server_cert_raw, hostname)
        status = "✅ VALID" if is_valid else "❌ INVALID"
        print(f"  {hostname}: {status}")
    
    # Show certificate SAN domains for reference
    print(f"\nCertificate covers these domains:")
    for domain in cert_chain.server_cert.san_domains[:10]:
        print(f"  - {domain}")

asyncio.run(validate_certificate_hostname())
```

### Combined Security Analysis

```python
import asyncio
from simple_port_checker import PortChecker, L7Detector, CertificateAnalyzer, MTLSChecker

async def comprehensive_security_analysis(target):
    """Perform comprehensive security analysis including ports, L7 protection, and certificates."""
    
    print(f"🔍 Comprehensive Security Analysis for {target}")
    print("=" * 60)
    
    # 1. Port Scanning
    print("\n📡 Port Scanning...")
    scanner = PortChecker()
    scan_result = await scanner.scan_host(target, [80, 443, 8080, 8443])
    
    open_ports = [p.port for p in scan_result.ports if p.is_open]
    print(f"Open ports: {open_ports}")
    
    # 2. L7 Protection Detection
    print("\n🛡️ L7 Protection Detection...")
    l7_detector = L7Detector()
    l7_result = await l7_detector.detect(target)
    
    if l7_result.primary_protection:
        service = l7_result.primary_protection.service.value
        confidence = l7_result.primary_protection.confidence
        print(f"Protected by: {service} (confidence: {confidence:.1%})")
        print(f"Detection indicators: {', '.join(l7_result.primary_protection.indicators[:3])}")
    else:
        print("No L7 protection detected")
    
    # 3. SSL/TLS Certificate Analysis
    if 443 in open_ports:
        print("\n🔒 SSL/TLS Certificate Analysis...")
        cert_analyzer = CertificateAnalyzer()
        try:
            cert_chain = await cert_analyzer.analyze_certificate_chain(target, 443)
            server_cert = cert_chain.server_cert
            
            print(f"Certificate Subject: {server_cert.subject}")
            print(f"Issuer: {server_cert.issuer}")
            print(f"Valid until: {server_cert.not_after}")
            print(f"Chain valid: {cert_chain.chain_valid}")
            print(f"Chain complete: {cert_chain.chain_complete}")
            
            # Security indicators
            print(f"Key strength: {server_cert.key_size} bits ({server_cert.public_key_algorithm})")
            print(f"Signature algorithm: {server_cert.signature_algorithm}")
            
            # Hostname validation
            hostname_valid = cert_analyzer.validate_hostname(server_cert.raw_cert, target)
            print(f"Hostname valid: {'✅ Yes' if hostname_valid else '❌ No'}")
            
            # Warnings
            if cert_chain.missing_intermediates:
                print("⚠️ Missing intermediate certificates detected")
            if not cert_chain.chain_complete:
                print("⚠️ Certificate chain incomplete")
            if cert_chain.trust_issues:
                print(f"⚠️ Trust issues: {', '.join(cert_chain.trust_issues)}")
                
        except Exception as e:
            print(f"Certificate analysis failed: {e}")
    
    # 4. mTLS Support Check
    if 443 in open_ports:
        print("\n🔐 mTLS Support Check...")
        mtls_checker = MTLSChecker()
        try:
            mtls_result = await mtls_checker.check_mtls(target, 443)
            print(f"Supports mTLS: {'✅ Yes' if mtls_result.supports_mtls else '❌ No'}")
            print(f"Requires client cert: {'✅ Yes' if mtls_result.requires_client_cert else '❌ No'}")
            if mtls_result.tls_version:
                print(f"TLS version: {mtls_result.tls_version}")
        except Exception as e:
            print(f"mTLS check failed: {e}")
    
    print(f"\n✅ Analysis complete for {target}")

# Run comprehensive analysis
asyncio.run(comprehensive_security_analysis("github.com"))
```

### Hybrid Identity Detection

```python
import asyncio
from simple_port_checker import HybridIdentityChecker

async def check_hybrid_identity():
    """Check for hybrid identity and ADFS configuration."""
    checker = HybridIdentityChecker(timeout=15.0)
    
    # Single domain check
    result = await checker.check("example.com")
    
    print(f"Domain: {result.fqdn}")
    print(f"Hybrid Identity: {'✅ Detected' if result.has_hybrid_identity else '❌ Not Found'}")
    
    if result.has_adfs:
        print(f"\nADFS Configuration:")
        print(f"  Endpoint: {result.adfs_endpoint}")
        print(f"  Status: {result.adfs_status_code}")
    
    if result.federation_metadata_found:
        print("  Federation Metadata: ✅ Found")
    
    if result.azure_ad_detected:
        print("  Azure AD Integration: ✅ Detected")
    
    if result.openid_config_found:
        print("  OpenID Configuration: ✅ Found")
    
    # DNS analysis
    if result.dns_records:
        print(f"\nDNS Records:")
        if 'microsoft_verification' in result.dns_records:
            print("  Microsoft Verification: ✅ Found")
        if 'microsoft_mail' in result.dns_records:
            print("  Microsoft Mail (MX): ✅ Found")
        if 'adfs_subdomains' in result.dns_records:
            print(f"  ADFS Subdomains: {', '.join(result.dns_records['adfs_subdomains'])}")
    
    print(f"\nResponse Time: {result.response_time:.2f}s")

async def batch_hybrid_identity_check():
    """Check multiple domains for hybrid identity."""
    checker = HybridIdentityChecker()
    
    domains = [
        "company1.com",
        "company2.com",
        "company3.com",
    ]
    
    print("Checking hybrid identity for multiple domains...\n")
    results = await checker.batch_check(domains, max_concurrent=5)
    
    # Summary
    hybrid_count = sum(1 for r in results if r.has_hybrid_identity)
    adfs_count = sum(1 for r in results if r.has_adfs)
    
    print(f"\nSummary:")
    print(f"  Total Domains: {len(results)}")
    print(f"  Hybrid Identity Found: {hybrid_count}")
    print(f"  ADFS Endpoints Found: {adfs_count}")
    
    # Detailed results
    print(f"\nDetailed Results:")
    for result in results:
        status = "✅" if result.has_hybrid_identity else "❌"
        adfs = f" (ADFS: {result.adfs_endpoint})" if result.adfs_endpoint else ""
        print(f"  {status} {result.fqdn}{adfs}")

async def hybrid_identity_with_error_handling():
    """Production-ready hybrid identity checking with error handling."""
    checker = HybridIdentityChecker(timeout=10.0)
    
    domains = ["example.com", "test.com", "invalid-domain-xyz.com"]
    
    for domain in domains:
        try:
            result = await checker.check(domain)
            
            if result.error:
                print(f"❌ {domain}: {result.error}")
                continue
            
            if result.has_hybrid_identity:
                print(f"✅ {domain}: Hybrid Identity Detected")
                if result.adfs_endpoint:
                    print(f"   ADFS: {result.adfs_endpoint}")
            else:
                print(f"ℹ️  {domain}: Cloud-only (no hybrid identity)")
                
        except Exception as e:
            print(f"❌ {domain}: Exception - {e}")

# Run examples
asyncio.run(check_hybrid_identity())
```

---

## OWASP Top 10 Vulnerability Scanner

### OwaspScanner

The `OwaspScanner` class performs comprehensive security vulnerability scanning based on OWASP Top 10 2021 categories.

#### Constructor

```python
OwaspScanner(
    mode: str = "safe",
    enabled_categories: Optional[List[str]] = None,
    timeout: float = 10.0
)
```

**Parameters:**
- `mode` (str): Scan mode - either "safe" (passive scanning) or "deep" (active probing). Default: "safe"
  - **Safe mode**: Only scans A02, A05, A06, A07 (passive header analysis)
  - **Deep mode**: Scans all testable categories (excludes only A09)
- `enabled_categories` (List[str], optional): Specific OWASP categories to scan (e.g., ["A02", "A05"]). Overrides mode settings.
- `timeout` (float): Timeout for HTTP requests in seconds. Default: 10.0

**Example:**
```python
from simple_port_checker import OwaspScanner

# Safe mode scanner (default)
scanner = OwaspScanner(mode="safe", timeout=15.0)

# Deep mode scanner
deep_scanner = OwaspScanner(mode="deep")

# Custom categories only
custom_scanner = OwaspScanner(enabled_categories=["A02", "A05", "A06"])
```

#### Methods

##### scan()

Scan a single target for OWASP Top 10 vulnerabilities.

```python
async def scan(
    self,
    target: str,
    port: int = 443,
    tech_stack: str = "generic"
) -> OwaspScanResult
```

**Parameters:**
- `target` (str): Hostname or IP address to scan
- `port` (int): Port number to scan. Default: 443
- `tech_stack` (str): Technology stack for tailored remediation ("apache", "nginx", "iis", "cloudflare", "generic"). Default: "generic"

**Returns:** `OwaspScanResult` object containing scan results

**Example:**
```python
import asyncio
from simple_port_checker import OwaspScanner

async def main():
    scanner = OwaspScanner(mode="safe")
    result = await scanner.scan("example.com", port=443, tech_stack="nginx")
    
    print(f"Target: {result.target}:{result.port}")
    print(f"Overall Grade: {result.overall_grade}")
    print(f"Total Score: {result.total_score}")
    print(f"Total Findings: {len(result.all_findings)}")
    
    # Display findings by severity
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        findings = [f for f in result.all_findings if f.severity.value == severity]
        if findings:
            print(f"\n{severity} ({len(findings)} findings):")
            for finding in findings:
                print(f"  - [{finding.category}] {finding.title}")

asyncio.run(main())
```

##### batch_scan()

Scan multiple targets in parallel.

```python
async def batch_scan(
    self,
    targets: List[Tuple[str, int]],
    tech_stack: str = "generic",
    max_concurrent: int = 5
) -> BatchOwaspResult
```

**Parameters:**
- `targets` (List[Tuple[str, int]]): List of (hostname, port) tuples
- `tech_stack` (str): Technology stack for all targets. Default: "generic"
- `max_concurrent` (int): Maximum concurrent scans. Default: 5

**Returns:** `BatchOwaspResult` object containing all scan results

**Example:**
```python
import asyncio
from simple_port_checker import OwaspScanner

async def main():
    scanner = OwaspScanner(mode="deep")
    targets = [
        ("example.com", 443),
        ("api.example.com", 443),
        ("admin.example.com", 443)
    ]
    
    batch_result = await scanner.batch_scan(targets, max_concurrent=3)
    
    print(f"Scanned {batch_result.total_scanned} targets")
    print(f"Failed: {batch_result.failed_count}")
    
    for target_result in batch_result.results:
        print(f"\n{target_result.target}: Grade {target_result.overall_grade}")

asyncio.run(main())
```

---

### SecurityHeaderChecker

The `SecurityHeaderChecker` class analyzes HTTP security headers and detects common misconfigurations.

#### Constructor

```python
SecurityHeaderChecker(timeout: float = 10.0)
```

**Parameters:**
- `timeout` (float): Timeout for HTTP requests. Default: 10.0

#### Methods

##### check_headers()

Analyze security headers for a single target.

```python
async def check_headers(
    self,
    target: str,
    port: int = 443,
    use_https: bool = True
) -> HeaderAnalysisResult
```

**Parameters:**
- `target` (str): Hostname or IP address
- `port` (int): Port number. Default: 443
- `use_https` (bool): Use HTTPS protocol. Default: True

**Returns:** `HeaderAnalysisResult` with security header grades and findings

**Example:**
```python
import asyncio
from simple_port_checker.core import SecurityHeaderChecker

async def main():
    checker = SecurityHeaderChecker(timeout=15.0)
    result = await checker.check_headers("example.com", port=443)
    
    print(f"Security Headers Analysis for {result.url}")
    print(f"HSTS Grade: {result.hsts_grade}")
    print(f"CSP Grade: {result.csp_grade}")
    print(f"CORS Issues: {result.cors_issues}")
    
    if result.server_header:
        print(f"Server: {result.server_header}")
    if result.powered_by:
        print(f"X-Powered-By: {result.powered_by}")

asyncio.run(main())
```

---

### OWASP Result Models

#### OwaspScanResult

Main result object from an OWASP scan.

**Properties:**
- `target` (str): Scanned hostname
- `port` (int): Scanned port
- `scan_mode` (ScanMode): "safe" or "deep"
- `timestamp` (datetime): Scan completion time
- `duration` (float): Scan duration in seconds
- `categories` (Dict[str, OwaspCategoryResult]): Results per category
- `overall_grade` (str): Overall security grade (A-F)
- `total_score` (int): Total vulnerability score
- `tech_stack` (str): Technology stack used for remediation

**Computed Properties:**
- `all_findings` (List[OwaspFinding]): All findings across categories
- `critical_findings` (List[OwaspFinding]): CRITICAL severity findings
- `high_findings` (List[OwaspFinding]): HIGH severity findings
- `medium_findings` (List[OwaspFinding]): MEDIUM severity findings
- `low_findings` (List[OwaspFinding]): LOW severity findings

**Methods:**
- `calculate_overall_grade() -> str`: Calculate overall security grade (auto-F if critical cryptographic failures)
- `get_findings_by_severity(severity: SeverityLevel) -> List[OwaspFinding]`: Filter findings by severity

**Example:**
```python
result = await scanner.scan("example.com")

# Access category results
a02_result = result.categories.get("A02")
if a02_result:
    print(f"A02 Grade: {a02_result.grade}")
    print(f"A02 Findings: {len(a02_result.findings)}")

# Get critical issues
critical = result.critical_findings
if critical:
    print(f"\n⚠️  {len(critical)} CRITICAL issues found:")
    for finding in critical:
        print(f"  - {finding.title}")
        print(f"    {finding.description}")
```

#### OwaspFinding

Individual vulnerability finding.

**Properties:**
- `category` (str): OWASP category (e.g., "A02")
- `title` (str): Finding title
- `description` (str): Detailed description
- `severity` (SeverityLevel): CRITICAL, HIGH, MEDIUM, or LOW
- `evidence` (str): Technical evidence or details
- `cwe_ids` (List[str], optional): Related CWE identifiers

**Example:**
```python
for finding in result.all_findings:
    print(f"[{finding.severity.value}] {finding.category}: {finding.title}")
    print(f"  Evidence: {finding.evidence}")
    if finding.cwe_ids:
        print(f"  CWE: {', '.join(finding.cwe_ids)}")
```

#### SeverityLevel

Enum for finding severity levels.

**Values:**
- `CRITICAL`: 15 points (auto-F grade for A02 cryptographic failures)
- `HIGH`: 10 points
- `MEDIUM`: 5 points
- `LOW`: 1 point

#### OwaspCategoryResult

Result for a single OWASP category.

**Properties:**
- `category_id` (str): Category identifier (A01-A10)
- `category_name` (str): Category name
- `findings` (List[OwaspFinding]): Findings for this category
- `scanned` (bool): Whether category was scanned
- `grade` (str): Category grade (A-F)
- `score` (int): Category vulnerability score

---

### Export Functions

#### PDF Export

Generate a comprehensive PDF report.

```python
from simple_port_checker.utils import OwaspPdfExporter

exporter = OwaspPdfExporter()
exporter.export(result, "security_report.pdf", tech_stack="nginx")
```

**OwaspPdfExporter Methods:**

```python
def export(
    self,
    result: OwaspScanResult,
    output_path: str,
    tech_stack: str = "generic",
    include_remediation: bool = True
) -> None
```

**Parameters:**
- `result`: OwaspScanResult object
- `output_path`: Path for output PDF file
- `tech_stack`: Technology stack for remediation examples
- `include_remediation`: Include remediation guidance. Default: True

**PDF Report Contents:**
- Cover page with overall grade and scan metadata
- Executive summary with findings breakdown
- Category-by-category analysis
- Detailed findings with evidence
- Remediation guidance with code examples
- CWE references

#### CSV Export

Export findings to CSV format.

```python
from simple_port_checker.utils import export_to_csv

export_to_csv(result, "findings.csv")
```

**Function Signature:**
```python
def export_to_csv(result: OwaspScanResult, output_path: str) -> None
```

**CSV Columns:**
- Category
- Severity
- Title
- Description
- Evidence
- CWE IDs

#### JSON Export

Export complete results to JSON.

```python
from simple_port_checker.utils import export_to_json

export_to_json(result, "results.json", tech_stack="apache", include_remediation=True)
```

**Function Signature:**
```python
def export_to_json(
    result: OwaspScanResult,
    output_path: str,
    tech_stack: str = "generic",
    include_remediation: bool = False,
    indent: int = 2
) -> None
```

**Parameters:**
- `result`: OwaspScanResult object
- `output_path`: Path for output JSON file
- `tech_stack`: Technology stack for remediation filtering
- `include_remediation`: Include remediation data. Default: False
- `indent`: JSON indentation spaces. Default: 2

---

### Remediation Access

Access remediation guidance programmatically.

```python
from simple_port_checker.utils import get_remediation

# Get remediation for specific category and tech stack
remediation = get_remediation("A02", tech_stack="nginx")

if remediation:
    print(f"Description: {remediation.description}")
    print(f"\nRemediation Steps:")
    for i, step in enumerate(remediation.steps, 1):
        print(f"{i}. {step}")
    
    # Get tech-specific code example
    if "nginx" in remediation.code_examples:
        print(f"\nNginx Configuration:")
        print(remediation.code_examples["nginx"])
    
    print(f"\nReferences:")
    for ref in remediation.references:
        print(f"  - {ref}")
    
    print(f"\nCWE IDs: {', '.join(remediation.cwe_ids)}")
```

**Available Tech Stacks:**
- `apache`: Apache HTTP Server
- `nginx`: Nginx
- `iis`: Microsoft IIS
- `cloudflare`: Cloudflare CDN
- `generic`: Framework-agnostic guidance

**OWASP Categories:**
- A01: Broken Access Control
- A02: Cryptographic Failures (testable)
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration (testable)
- A06: Vulnerable and Outdated Components (testable)
- A07: Identification and Authentication Failures (testable)
- A08: Software and Data Integrity Failures
- A09: Security Logging and Monitoring Failures (not externally testable)
- A10: Server-Side Request Forgery (SSRF)

---

### Complete OWASP Scanner Example

```python
import asyncio
from simple_port_checker import OwaspScanner
from simple_port_checker.utils import OwaspPdfExporter, export_to_csv, export_to_json

async def comprehensive_scan():
    # Configure scanner
    scanner = OwaspScanner(
        mode="deep",
        timeout=15.0
    )
    
    # Scan target
    print("Scanning example.com...")
    result = await scanner.scan(
        "example.com",
        port=443,
        tech_stack="nginx"
    )
    
    # Display results
    print(f"\n{'='*60}")
    print(f"Security Assessment: {result.target}:{result.port}")
    print(f"{'='*60}")
    print(f"Overall Grade: {result.overall_grade}")
    print(f"Total Score: {result.total_score}")
    print(f"Scan Mode: {result.scan_mode.value}")
    print(f"Duration: {result.duration:.2f}s")
    
    # Show findings by severity
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        findings = result.get_findings_by_severity(severity)
        if findings:
            print(f"\n{severity} ({len(findings)}):")
            for finding in findings:
                print(f"  [{finding.category}] {finding.title}")
    
    # Export results
    print(f"\nExporting results...")
    
    # PDF report with remediation
    pdf_exporter = OwaspPdfExporter()
    pdf_exporter.export(
        result,
        "security_report.pdf",
        tech_stack="nginx",
        include_remediation=True
    )
    print("  ✓ PDF: security_report.pdf")
    
    # CSV for spreadsheet analysis
    export_to_csv(result, "findings.csv")
    print("  ✓ CSV: findings.csv")
    
    # JSON with remediation for automation
    export_to_json(
        result,
        "results.json",
        tech_stack="nginx",
        include_remediation=True
    )
    print("  ✓ JSON: results.json")
    
    # Category-specific analysis
    print(f"\nCategory Analysis:")
    for cat_id in ["A02", "A05", "A06", "A07"]:
        cat_result = result.categories.get(cat_id)
        if cat_result and cat_result.scanned:
            print(f"  {cat_id}: Grade {cat_result.grade} ({cat_result.score} points, {len(cat_result.findings)} findings)")

asyncio.run(comprehensive_scan())
```

---

## Best Practices

1. **Always use async/await context**:
   ```python
   async def main():
       scanner = PortChecker()
       result = await scanner.scan_host("example.com")
   
   asyncio.run(main())
   ```

2. **Handle errors gracefully**:
   ```python
   result = await scanner.scan_host("example.com")
   if result.error:
       print(f"Scan failed: {result.error}")
       return
   ```

3. **Use appropriate timeouts**:
   ```python
   config = ScanConfig(timeout=10.0)  # Longer timeout for slow networks
   scanner = PortChecker(config)
   ```

4. **Respect rate limits**:
   ```python
   config = ScanConfig(
       concurrent_limit=20,  # Reduce for rate-limited targets
       delay_between_requests=0.5
   )
   ```

5. **Use specific port lists when possible**:
   ```python
   # Instead of scanning all common ports
   web_ports = [80, 443, 8080, 8443]
   result = await scanner.scan_host("example.com", web_ports)
   ```

6. **Certificate analysis best practices**:
   ```python
   # Use appropriate timeouts for certificate analysis
   analyzer = CertificateAnalyzer(timeout=15.0)
   
   # Always check for errors
   try:
       cert_chain = await analyzer.analyze_certificate_chain("example.com")
       if not cert_chain.chain_valid:
           print("Certificate chain validation failed")
   except Exception as e:
       print(f"Certificate analysis error: {e}")
   ```

7. **Validate certificate hostname matches**:
   ```python
   cert_chain = await analyzer.analyze_certificate_chain("example.com")
   hostname_valid = analyzer.validate_hostname(cert_chain.server_cert.raw_cert, "example.com")
   if not hostname_valid:
       print("Certificate hostname validation failed")
   ```

8. **Check for certificate chain completeness**:
   ```python
   if not cert_chain.chain_complete:
       print("Warning: Certificate chain incomplete - may cause browser compatibility issues")
       if cert_chain.missing_intermediates:
           print(f"Missing: {', '.join(cert_chain.missing_intermediates)}")
   ```

9. **OWASP scanning best practices**:
   ```python
   # Start with safe mode (passive scanning)
   scanner = OwaspScanner(mode="safe")
   result = await scanner.scan("example.com")
   
   # Only use deep mode when you have permission
   # Deep mode performs active probing which may trigger alerts
   deep_scanner = OwaspScanner(mode="deep")
   
   # Use appropriate tech stack for targeted remediation
   result = await scanner.scan("example.com", tech_stack="nginx")
   ```

10. **Batch OWASP scanning with concurrency control**:
    ```python
    # Limit concurrent scans to avoid overwhelming targets
    batch_result = await scanner.batch_scan(
        targets=[("example.com", 443), ("api.example.com", 443)],
        max_concurrent=3  # Adjust based on target capacity
    )
    ```

11. **Filter OWASP findings by severity**:
    ```python
    result = await scanner.scan("example.com")
    
    # Focus on critical and high severity issues first
    critical = result.critical_findings
    high = result.high_findings
    
    print(f"Immediate action required: {len(critical)} critical, {len(high)} high")
    ```

12. **Export OWASP results for reporting**:
    ```python
    from simple_port_checker.utils import OwaspPdfExporter, export_to_csv
    
    # PDF for stakeholder reports
    pdf_exporter = OwaspPdfExporter()
    pdf_exporter.export(result, "report.pdf", include_remediation=True)
    
    # CSV for tracking and spreadsheet analysis
    export_to_csv(result, "findings.csv")
    ```

## Legal and Ethical Considerations

- Only scan systems you own or have explicit permission to test
- Respect robots.txt and security policies
- Use rate limiting to avoid overwhelming target systems
- Be aware that scanning may trigger security alerts
- Consider using the library in compliance with your organization's security policies
- **OWASP scanning**: Deep mode performs active probing - ensure you have authorization before use
- **Vulnerability disclosure**: Responsibly disclose discovered vulnerabilities following industry best practices
