"""
offsec-ai — Offensive-security toolkit for authorized red-team engagements.

Capabilities:
- Port scanning with banner grabbing (async, configurable concurrency)
- L7/WAF/CDN detection with DNS tracing
- mTLS (Mutual TLS) authentication checking
- SSL/TLS certificate chain analysis and validation
- Hybrid identity / Azure AD / ADFS detection
- OWASP Top 10 2021/2025 web vulnerability scanning
- AI/LLM OWASP Top 10 2025 black-box endpoint probing
- MCP (Model Context Protocol) endpoint security scanning and CVE matching
- MCP endpoint active attack module (requires explicit authorization)
- Security header analysis and grading
- Multi-format reporting (PDF, JSON, CSV)
- Rich CLI interface with progress bars
"""

__version__ = "2.0.1"
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
from .core.ai_owasp_scanner import LLMOwaspScanner
from .core.mcp_scanner import MCPScanner
from .core.mcp_attacker import MCPAttacker, AuthorizationRequired
from .core.llm_judge import LLMJudge
from .models.scan_result import ScanResult, PortResult
from .models.l7_result import L7Result
from .models.mtls_result import MTLSResult, CertificateInfo
from .models.owasp_result import OwaspScanResult, OwaspFinding, OwaspCategoryResult, SeverityLevel
from .models.ai_owasp_result import LLMScanResult, LLMFinding, LLMCategoryResult, LLMSeverity
from .models.mcp_result import (
    MCPScanResult,
    MCPTool,
    MCPResource,
    MCPVulnerability,
    MCPAttackReport,
    MCPAttackResult,
    MCPTransport,
)

__all__ = [
    # Original scanners
    "PortChecker",
    "L7Detector",
    "L7Protection",
    "MTLSChecker",
    "CertificateAnalyzer",
    "HybridIdentityChecker",
    "HybridIdentityResult",
    "OwaspScanner",
    "SecurityHeaderChecker",
    # New AI/LLM scanners
    "LLMOwaspScanner",
    "LLMJudge",
    # New MCP modules
    "MCPScanner",
    "MCPAttacker",
    "AuthorizationRequired",
    # Original result models
    "ScanResult",
    "PortResult",
    "L7Result",
    "MTLSResult",
    "CertificateInfo",
    "OwaspScanResult",
    "OwaspFinding",
    "OwaspCategoryResult",
    "SeverityLevel",
    # New AI OWASP result models
    "LLMScanResult",
    "LLMFinding",
    "LLMCategoryResult",
    "LLMSeverity",
    # New MCP result models
    "MCPScanResult",
    "MCPTool",
    "MCPResource",
    "MCPVulnerability",
    "MCPAttackReport",
    "MCPAttackResult",
    "MCPTransport",
]
