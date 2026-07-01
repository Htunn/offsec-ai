"""OpenClaw gateway security scan result models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OpenClawVulnSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class OpenClawAuthPosture(BaseModel):
    """Authentication posture of the OpenClaw gateway."""
    unauthenticated_api_access: bool = False
    unauthenticated_ws_access: bool = False
    auth_type: str = "unknown"   # none / token / basic / oauth
    auth_header_present: bool = False


class OpenClawDMPolicy(BaseModel):
    """DM policy configuration discovered from the gateway."""
    policy: str = "unknown"       # pairing / open / unknown
    has_wildcard_allowlist: bool = False
    channels_with_open_dm: list[str] = Field(default_factory=list)
    channels_with_pairing: list[str] = Field(default_factory=list)


class OpenClawSandboxInfo(BaseModel):
    """Sandbox configuration discovered from the gateway."""
    sandbox_mode: str = "unknown"  # disabled / non-main / all / unknown
    sandbox_backend: str = "unknown"  # docker / ssh / openShell / none
    is_sandboxed: bool = False


class OpenClawServerInfo(BaseModel):
    """Fingerprint of the discovered OpenClaw gateway."""
    version: str = ""
    gateway_id: str = ""
    connected_channels: list[str] = Field(default_factory=list)
    active_sessions: int = 0
    node_count: int = 0
    raw: dict[str, Any] = Field(default_factory=dict)


class OpenClawVulnerability(BaseModel):
    """A single vulnerability finding."""
    vuln_id: str
    cve_id: str | None = None
    severity: OpenClawVulnSeverity
    title: str
    description: str
    evidence: str = ""
    remediation: str = ""
    references: list[str] = Field(default_factory=list)
    discovered_at: datetime = Field(default_factory=datetime.utcnow)
    llm_confidence: float | None = None
    llm_reasoning: str = ""


class OpenClawAccessibleEndpoint(BaseModel):
    """An endpoint found accessible during scanning."""
    path: str
    method: str = "GET"
    status_code: int = 0
    response_size: int = 0
    requires_auth: bool = True
    sensitive_data_found: list[str] = Field(default_factory=list)


class OpenClawScanResult(BaseModel):
    """Full result of an OpenClaw gateway security scan."""
    target: str
    port: int = 18789
    scan_duration: float = 0.0
    scanned_at: datetime = Field(default_factory=datetime.utcnow)
    error: str = ""

    # Discovery
    is_openclaw: bool = False
    server_info: OpenClawServerInfo = Field(default_factory=OpenClawServerInfo)
    auth_posture: OpenClawAuthPosture = Field(default_factory=OpenClawAuthPosture)
    dm_policy: OpenClawDMPolicy = Field(default_factory=OpenClawDMPolicy)
    sandbox_info: OpenClawSandboxInfo = Field(default_factory=OpenClawSandboxInfo)

    # Findings
    accessible_endpoints: list[OpenClawAccessibleEndpoint] = Field(default_factory=list)
    vulnerabilities: list[OpenClawVulnerability] = Field(default_factory=list)
    cve_matches: list[str] = Field(default_factory=list)

    @property
    def all_vulns(self) -> list[OpenClawVulnerability]:
        return self.vulnerabilities

    @property
    def critical_vulns(self) -> list[OpenClawVulnerability]:
        return [v for v in self.vulnerabilities if v.severity == OpenClawVulnSeverity.CRITICAL]

    @property
    def high_vulns(self) -> list[OpenClawVulnerability]:
        return [v for v in self.vulnerabilities if v.severity == OpenClawVulnSeverity.HIGH]


# ---------------------------------------------------------------------------
# Attack report models
# ---------------------------------------------------------------------------

class OpenClawAttackResult(BaseModel):
    """Result of a single attack attempt."""
    attack_id: str
    description: str
    severity: OpenClawVulnSeverity
    succeeded: bool = False
    payload_sent: str = ""
    response_snippet: str = ""
    evidence: str = ""
    error: str = ""


class OpenClawAttackReport(BaseModel):
    """Full report from an OpenClaw red-team attack session."""
    target: str
    port: int = 18789
    authorized: bool = True
    attack_duration: float = 0.0
    attacked_at: datetime = Field(default_factory=datetime.utcnow)
    mode: str = "safe"

    scan_result: OpenClawScanResult | None = None
    attack_results: list[OpenClawAttackResult] = Field(default_factory=list)

    @property
    def successful_attacks(self) -> list[OpenClawAttackResult]:
        return [r for r in self.attack_results if r.succeeded]

    @property
    def critical_successes(self) -> list[OpenClawAttackResult]:
        return [
            r for r in self.attack_results
            if r.succeeded and r.severity == OpenClawVulnSeverity.CRITICAL
        ]
