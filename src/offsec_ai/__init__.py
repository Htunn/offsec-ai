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
- OpenClaw personal AI gateway security scanner and attacker
- Security header analysis and grading
- Multi-format reporting (PDF, JSON, CSV)
- Rich CLI interface with progress bars
"""

from importlib.metadata import PackageNotFoundError, version as _pkg_version

try:
    __version__ = _pkg_version("offsec-ai")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"

__author__ = "Johny htunn"
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
from .core.mcp_attacker import MCPAttacker
from .core.llm_judge import LLMJudge
from .exceptions import (
    AuthorizationRequired,
    ConfigError,
    NetworkError,
    OffsecError,
    ScanError,
    TargetUnreachableError,
)
from .config import OffsecConfig, get_config, reset_config
from .log_config import (
    configure_logging,
    new_correlation_id,
    get_correlation_id,
    audit_log,
)
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
    # Exceptions
    "OffsecError",
    "ScanError",
    "ConfigError",
    "NetworkError",
    "TargetUnreachableError",
    "AuthorizationRequired",
    # Configuration
    "OffsecConfig",
    "get_config",
    "reset_config",
    # Logging utilities
    "configure_logging",
    "new_correlation_id",
    "get_correlation_id",
    "audit_log",
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
