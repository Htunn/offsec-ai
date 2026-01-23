"""
Simple Port Checker - A comprehensive tool for checking firewall ports and L7 protection.

This package provides functionality for:
- Scanning well-known firewall ports
- Detecting L7 protection services (WAF, CDN, etc.)
- Checking mTLS (Mutual TLS) authentication support
- SSL/TLS certificate chain analysis and validation
- Certificate authority identification and trust validation
- Hybrid identity and ADFS endpoint detection
- OWASP Top 10 2021 vulnerability scanning
- Security header analysis and grading
- Multi-format reporting (PDF, JSON, CSV)
- Async port scanning with configurable concurrency
- Rich CLI interface with progress bars
"""

__version__ = "1.1.0"
__author__ = "htunn"
__email__ = "htunnthuthu.linux@gmail.com"
__license__ = "MIT"

from .core.port_scanner import PortChecker
from .core.l7_detector import L7Detector, L7Protection
from .core.mtls_checker import MTLSChecker
from .core.cert_analyzer import CertificateAnalyzer
from .core.hybrid_identity_checker import HybridIdentityChecker, HybridIdentityResult
from .core.owasp_scanner import OwaspScanner
from .core.security_headers import SecurityHeaderChecker
from .models.scan_result import ScanResult, PortResult
from .models.l7_result import L7Result
from .models.mtls_result import MTLSResult, CertificateInfo
from .models.owasp_result import OwaspScanResult, OwaspFinding, OwaspCategoryResult, SeverityLevel

__all__ = [
    "PortChecker",
    "L7Detector",
    "L7Protection",
    "MTLSChecker",
    "CertificateAnalyzer",
    "HybridIdentityChecker",
    "HybridIdentityResult",
    "OwaspScanner",
    "SecurityHeaderChecker",
    "ScanResult",
    "PortResult",
    "L7Result",
    "MTLSResult",
    "CertificateInfo",
    "OwaspScanResult",
    "OwaspFinding",
    "OwaspCategoryResult",
    "SeverityLevel",
]
