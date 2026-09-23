"""Sanitized public-identity scanning primitives."""

from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable


TEXT_EXTENSIONS = {
    ".c", ".cc", ".cpp", ".css", ".csv", ".entitlements", ".go", ".h",
    ".html", ".htm", ".java", ".js", ".json", ".jsx", ".kt", ".m",
    ".md", ".mm", ".plist", ".py", ".rb", ".rs", ".sh", ".strings",
    ".swift", ".toml", ".ts", ".tsx", ".txt", ".xcconfig", ".xml",
    ".yaml", ".yml",
}
METADATA_NAMES = {
    "appfile", "appstore.json", "cargo.toml", "dockerfile", "fastfile",
    "gemfile", "package.json", "package.swift", "podfile", "project.pbxproj",
}
SKIP_DIRECTORIES = {
    ".git", ".cache", "cache", "caches", "deriveddata", "build", "dist",
    "node_modules", "vendor", "pods", ".build",
}
HARD_BLOCKER_CODES = {
    "PRIVATE_ADDRESS_PATTERN", "UNAUTHORIZED_REGISTERED_SYMBOL",
    "APPLICATION_DESCRIBED_AS_REGISTERED", "OWNER_CONFLICT", "SELLER_CONFLICT",
}
OVERRIDABLE_CODES = {
    "PUBLIC_STREET_ADDRESS_UNAPPROVED", "NONCANONICAL_PUBLIC_EMAIL",
    "NONCANONICAL_PUBLIC_PHONE", "TRADEMARK_STATE_CLAIM",
    "LIFECYCLE_CONTRADICTION", "PRICING_CONTRADICTION", "PLATFORM_CONTRADICTION",
    "FEATURES_CONTRADICTION", "PRIVACY_CONTRADICTION", "FUNCTION_CONTRADICTION",
}
STREET_RE = re.compile(
    r"\b\d{1,6}\s+[A-Za-z0-9][A-Za-z0-9 .'-]{1,48}\s(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Way)\b",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?<!\w)(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\w)")
OWNER_RE = re.compile(r"[\"']?(?:owner|legal_owner|owner_name)[\"']?\s*[:=]\s*[\"']?([^\"'\n,}]+)", re.IGNORECASE)
SELLER_RE = re.compile(r"[\"']?(?:seller|seller_name|developer_name)[\"']?\s*[:=]\s*[\"']?([^\"'\n,}]+)", re.IGNORECASE)


def _token(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _safe_path(value: Any) -> str:
    text = str(value or "structured-observation")
    path = Path(text)
    if path.is_absolute() or ".." in path.parts:
        return path.name or "structured-observation"
    return path.as_posix()


def _finding(code: str, severity: str, path: str, line: int, identity: str, value: str) -> dict[str, Any]:
    return {
        "code": code,
        "severity": severity,
        "classification": "BLOCKER" if severity == "BLOCKER" else "WARNING",
        "path": path,
        "line": line,
        "identity": identity,
        "redacted_identifier": _token(value),
    }


def _locally_negated(prefix: str) -> bool:
    clause = re.split(r"(?:[;,]|\b(?:and|but)\b)", prefix, flags=re.IGNORECASE)[-1]
    predicates = list(re.finditer(r"\b(?:is|was|are|were)\b", clause, re.IGNORECASE))
    if predicates:
        clause = clause[predicates[-1].start():]
    if re.search(r"\bnot\s+(?:only|merely|just|simply|solely|exclusively)\b", clause, re.IGNORECASE):
        return False
    return bool(re.search(r"\b(?:no\s+longer|no|not|never)\b", clause, re.IGNORECASE))


def _identity_data(registry: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    identities = {str(item.get("name", "")).casefold(): item for item in registry.get("identities", []) if item.get("name")}
    marks = {str(item.get("mark", "")).casefold(): item for item in registry.get("trademarks", []) if item.get("mark")}
    return identities, marks


def _identity_for_line(line: str, identities: dict[str, dict[str, Any]], marks: dict[str, dict[str, Any]]) -> str:
    folded = line.casefold()
    matches = [item for name, item in {**identities, **marks}.items() if name and name in folded]
    return str(matches[0].get("entity_id", "UNKNOWN")) if matches else "UNKNOWN"


def _iter_files(roots: Iterable[Path]) -> Iterable[tuple[Path, str]]:
    for root in roots:
        root = root.resolve()
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not path.is_file() or any(part.casefold() in SKIP_DIRECTORIES for part in path.parts):
                continue
            relative = path.name if root.is_file() else path.relative_to(root).as_posix()
            yield path, relative


def _text_findings(
    path: str,
    text: str,
    registry: dict[str, Any],
    private_patterns: list[str],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    identities, marks = _identity_data(registry)
    governed_names = dict(identities)
    governed_names.update(marks)
    canonical_emails = {str(item.get("email", "")).casefold() for item in registry.get("contacts", [])}
    legal_owner = registry.get("legal_entity", {}).get("legal_name")
    mark_owners = {item.get("entity_id"): item.get("owner_name") for item in registry.get("trademarks", [])}
    for number, line in enumerate(text.splitlines(), 1):
        identity = _identity_for_line(line, identities, marks)
        folded = line.casefold()
        approved_sellers = {legal_owner} - {None}
        for name, governed in governed_names.items():
            expected_state = governed.get("state") or governed.get("trademark_state")
            if name and re.search(rf"\b{re.escape(name)}\s*\u00ae", folded, re.IGNORECASE) and expected_state != "REGISTERED":
                findings.append(_finding("UNAUTHORIZED_REGISTERED_SYMBOL", "BLOCKER", path, number, str(governed["entity_id"]), name))
            registration_matches = list(re.finditer(
                rf"\b{re.escape(name)}\b(?P<context>.{{0,50}}?)(?P<claim>\bis\s+registered\b|\bregistered\s+trademark\b|\btrademark\s+registration\b)",
                line,
                re.IGNORECASE,
            ))
            registration_matches.extend(re.finditer(
                rf"(?P<claim>\bregistered\s+trademark\b|\btrademark\s+registration\b)(?P<context>.{{0,50}}?)\b{re.escape(name)}\b",
                line,
                re.IGNORECASE,
            ))
            if expected_state != "REGISTERED" and any(not _locally_negated(
                match.group("context") if match.start("context") < match.start("claim") else line[max(0, match.start("claim") - 40):match.start("claim")]
            ) for match in registration_matches):
                findings.append(_finding("APPLICATION_DESCRIBED_AS_REGISTERED", "BLOCKER", path, number, str(governed["entity_id"]), name))
            state_matches = list(re.finditer(
                rf"\b{re.escape(name)}\b(?P<context>.{{0,50}}?)\b(?P<state>INTERNAL|PROVISIONAL|CLEARANCE_REQUIRED|CLEARED|FILED|REGISTERED|LEGAL_REVIEW_REQUIRED|ABANDONED|RETIRED)\b",
                line,
                re.IGNORECASE,
            ))
            state_matches.extend(re.finditer(
                rf"\b(?P<state>INTERNAL|PROVISIONAL|CLEARANCE_REQUIRED|CLEARED|FILED|REGISTERED|LEGAL_REVIEW_REQUIRED|ABANDONED|RETIRED)\b(?P<context>.{{0,50}}?)\b{re.escape(name)}\b",
                line,
                re.IGNORECASE,
            ))
            for state_match in state_matches:
                observed_state = state_match.group("state").upper()
                prefix = state_match.group("context") if state_match.start("context") < state_match.start("state") else line[max(0, state_match.start("state") - 40):state_match.start("state")]
                if not _locally_negated(prefix) and observed_state != expected_state:
                    findings.append(_finding("TRADEMARK_STATE_CLAIM", "BLOCKER", path, number, str(governed["entity_id"]), observed_state))
        for pattern in private_patterns:
            if pattern and pattern.casefold() in folded:
                findings.append(_finding("PRIVATE_ADDRESS_PATTERN", "BLOCKER", path, number, identity, pattern))
        for match in STREET_RE.finditer(line):
            findings.append(_finding("PUBLIC_STREET_ADDRESS_UNAPPROVED", "BLOCKER", path, number, identity, match.group(0)))
        for match in EMAIL_RE.finditer(line):
            if match.group(0).casefold() not in canonical_emails:
                findings.append(_finding("NONCANONICAL_PUBLIC_EMAIL", "WARNING", path, number, identity, match.group(0)))
        for match in PHONE_RE.finditer(line):
            findings.append(_finding("NONCANONICAL_PUBLIC_PHONE", "WARNING", path, number, identity, match.group(0)))
        owner = OWNER_RE.search(line)
        if owner:
            approved_owners = {legal_owner, mark_owners.get(identity)} - {None}
            if owner.group(1).strip() not in approved_owners:
                findings.append(_finding("OWNER_CONFLICT", "BLOCKER", path, number, identity, owner.group(1).strip()))
        seller = SELLER_RE.search(line)
        if seller and seller.group(1).strip() not in approved_sellers:
            findings.append(_finding("SELLER_CONFLICT", "BLOCKER", path, number, identity, seller.group(1).strip()))
    return findings


def _observation_findings(observations: dict[str, Any], registry: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    approved_global = {registry.get("legal_entity", {}).get("legal_name")}
    approved_global.discard(None)
    identity_by_id = {item.get("entity_id"): item for item in registry.get("identities", [])}
    mark_by_name = {str(item.get("mark", "")).casefold(): item for item in registry.get("trademarks", [])}
    contacts = {str(item.get("email", "")).casefold() for item in registry.get("contacts", [])}
    for surface in observations.get("surfaces", []):
        path = _safe_path(surface.get("path", "structured-observation"))
        line = int(surface.get("line", 1))
        requested_identity = str(surface.get("identity", "UNKNOWN"))
        identity_id = requested_identity if requested_identity in identity_by_id else "UNKNOWN"
        identity = identity_by_id.get(identity_id, {})
        mark = mark_by_name.get(str(identity.get("name", "")).casefold(), {})
        approved_owners = set(surface.get("approved_owner_names", [])) or approved_global
        approved_sellers = set(surface.get("approved_seller_names", [])) or approved_global
        if surface.get("registered_symbol") and mark.get("state") != "REGISTERED":
            findings.append(_finding("UNAUTHORIZED_REGISTERED_SYMBOL", "BLOCKER", path, line, identity_id, identity_id))
        if surface.get("application_described_as_registration") and mark.get("state") != "REGISTERED":
            findings.append(_finding("APPLICATION_DESCRIBED_AS_REGISTERED", "BLOCKER", path, line, identity_id, identity_id))
        if surface.get("private_address_exposed") or surface.get("stale_address_exposed"):
            findings.append(_finding("PRIVATE_ADDRESS_PATTERN", "BLOCKER", path, line, identity_id, identity_id))
        if surface.get("owner") and surface.get("owner") not in approved_owners:
            findings.append(_finding("OWNER_CONFLICT", "BLOCKER", path, line, identity_id, str(surface["owner"])))
        if surface.get("seller") and surface.get("seller") not in approved_sellers:
            findings.append(_finding("SELLER_CONFLICT", "BLOCKER", path, line, identity_id, str(surface["seller"])))
        if surface.get("contact_email") and str(surface["contact_email"]).casefold() not in contacts:
            findings.append(_finding("NONCANONICAL_PUBLIC_EMAIL", "WARNING", path, line, identity_id, str(surface["contact_email"])))
        if surface.get("contact_phone"):
            findings.append(_finding("NONCANONICAL_PUBLIC_PHONE", "WARNING", path, line, identity_id, str(surface["contact_phone"])))
        claimed_state = surface.get("trademark_state")
        expected_state = identity.get("trademark_state") or mark.get("state")
        if claimed_state and claimed_state != expected_state:
            findings.append(_finding("TRADEMARK_STATE_CLAIM", "BLOCKER", path, line, identity_id, str(claimed_state)))
    fields = {"lifecycle", "pricing", "platform", "features", "privacy", "function"}
    for comparison in observations.get("comparisons", []):
        field = str(comparison.get("field", "")).casefold()
        if field in fields and comparison.get("expected") != comparison.get("observed"):
            code = f"{field.upper()}_CONTRADICTION"
            requested_identity = str(comparison.get("identity", "UNKNOWN"))
            identity_id = requested_identity if requested_identity in identity_by_id else "UNKNOWN"
            findings.append(_finding(code, "BLOCKER", _safe_path(comparison.get("path", "structured-observation")), int(comparison.get("line", 1)), identity_id, json.dumps(comparison.get("observed"), sort_keys=True)))
    return findings


def _scope_matches(scope: Any, finding: dict[str, Any], mode: str) -> bool:
    if scope == "*":
        return True
    if isinstance(scope, str):
        return scope == finding["path"] or scope == mode
    if isinstance(scope, list):
        return finding["path"] in scope or mode in scope
    return False


def apply_overrides(findings: list[dict[str, Any]], overrides: list[dict[str, Any]], mode: str, today: date | None = None) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    today = today or date.today()
    remaining = list(findings)
    audit: list[dict[str, str]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for override in overrides:
        override_id = str(override.get("id", ""))
        code = str(override.get("code", ""))
        status = "APPLIED"
        if not override_id or override_id in seen:
            status = "REJECTED_INVALID_ID"
        elif code in HARD_BLOCKER_CODES:
            status = "REJECTED_HARD_BLOCKER"
        elif code not in OVERRIDABLE_CODES:
            status = "REJECTED_UNKNOWN_CODE"
        elif not all(str(override.get(field, "")).strip() for field in ("authorization_reference", "rationale", "expires_on")) or "scope" not in override:
            status = "REJECTED_INCOMPLETE"
        else:
            try:
                if date.fromisoformat(str(override["expires_on"])) < today:
                    status = "REJECTED_EXPIRED"
            except ValueError:
                status = "REJECTED_INVALID_EXPIRY"
        seen.add(override_id)
        matched = [item for item in remaining if item["code"] == code and _scope_matches(override.get("scope"), item, mode)]
        if status == "APPLIED" and not matched:
            status = "REJECTED_NO_MATCH"
        if status == "APPLIED":
            remaining = [item for item in remaining if item not in matched]
        else:
            errors.append(f"override {override_id or '<missing>'}: {status}")
        audit.append({"id": override_id or "MISSING", "code": code or "MISSING", "status": status})
    return remaining, audit, errors


def scan(
    roots: list[Path],
    registry: dict[str, Any],
    private_patterns: list[str] | None = None,
    observations: dict[str, Any] | None = None,
    overrides: list[dict[str, Any]] | None = None,
    mode: str = "audit",
    today: date | None = None,
    subject_identity: str | None = None,
) -> dict[str, Any]:
    today = today or date.today()
    findings: list[dict[str, Any]] = []
    scanned_files = 0
    scanned_paths: list[str] = []
    scope_entries: list[tuple[str, str]] = []
    for root in roots:
        if not root.exists():
            findings.append(_finding("SCAN_INPUT_MISSING", "BLOCKER", root.name or "scan-input", 0, subject_identity or "UNKNOWN", str(root)))
    for source, relative in _iter_files(roots):
        try:
            content = source.read_bytes()
        except OSError:
            findings.append(_finding("SCAN_INPUT_UNREADABLE", "BLOCKER", relative, 0, subject_identity or "UNKNOWN", relative))
            continue
        scope_entries.append((relative, hashlib.sha256(content).hexdigest()))
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            if source.suffix.casefold() in TEXT_EXTENSIONS or source.name.casefold() in METADATA_NAMES:
                findings.append(_finding("SCAN_INPUT_UNREADABLE", "BLOCKER", relative, 0, subject_identity or "UNKNOWN", relative))
            continue
        scanned_files += 1
        scanned_paths.append(relative)
        findings.extend(_text_findings(relative, text, registry, private_patterns or []))
    if mode == "release" and scanned_files == 0:
        findings.append(_finding("SCAN_SCOPE_EMPTY", "BLOCKER", "scan-input", 0, subject_identity or "UNKNOWN", "empty-scan-scope"))
    if observations:
        findings.extend(_observation_findings(observations, registry))
    findings.sort(key=lambda item: (item["path"], item["line"], item["code"], item["redacted_identifier"]))
    effective, override_audit, override_errors = apply_overrides(findings, overrides or [], mode, today=today)
    blocker_count = sum(item["classification"] == "BLOCKER" for item in effective)
    warning_count = sum(item["classification"] == "WARNING" for item in effective)
    status = "BLOCKED" if blocker_count or override_errors else "WARN" if warning_count else "PASS"
    evaluation_inputs = {
        "mode": mode,
        "subject_identity": subject_identity,
        "roots": sorted(_safe_path(root.name) for root in roots),
        "scope": sorted(scope_entries),
        "registry": registry,
        "observations": observations,
        "private_pattern_hashes": sorted(_token(pattern) for pattern in (private_patterns or []) if pattern),
        "overrides": overrides or [],
    }
    evaluation_payload = json.dumps(evaluation_inputs, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return {
        "schema_version": 1,
        "captured_at": today.isoformat(),
        "subject_identity": subject_identity,
        "mode": mode,
        "status": status,
        "scanned_files": scanned_files,
        "scoped_files": len(scope_entries),
        "scanned_paths": sorted(scanned_paths),
        "evaluation_digest": "sha256:" + hashlib.sha256(evaluation_payload.encode("utf-8")).hexdigest(),
        "finding_count": len(effective),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "findings": effective,
        "override_audit": override_audit,
        "override_errors": override_errors,
    }
