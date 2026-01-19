"""
House of Consequences Core - Governance Enforcement Rules
GOVERNANCE_MODEL.md §1.2 Red Lines + §5 Auditability implementation
AGPL-3.0 | January 2026
"""

from typing import Dict, List, Any
from datetime import datetime
import hashlib
import uuid
import json
import jsonschema
from pathlib import Path

# Load schemas for validation
SCHEMAS_DIR = Path(_file_).parent.parent.parent / "schemas"
AUDIT_ENTRY_SCHEMA = json.loads((SCHEMAS_DIR / "audit.log.schema.json").read_text())
AUDIT_STORAGE_SCHEMA = json.loads((SCHEMAS_DIR / "audit.log.storage.schema.json").read_text())

# =============================================================================
# GOVERNANCE_MODEL.md §1.2 RED LINES (Non-Negotiable)
# =============================================================================

RED_LINES = {
    1: "No features enabling surveillance, repression, or population profiling",
    2: "No exclusive access agreements with states or corporations", 
    3: "No closed or proprietary forks of the core protocol",
    4: "No suppression, distortion, or hiding of core analytical outputs",
    5: "No opaque or non-auditable AI/ML models",
    6: "No centralized control over data, logic, or governance",
    7: "No integration that enables discrimination, coercion, or manipulation"
}

FORBIDDEN_ACTIONS = [
    # §1.2.1 Surveillance
    "enable_surveillance", "population_profiling", "track_users", "behavior_analysis",
    # §1.2.2 Exclusive access  
    "exclusive_license", "state_monopoly", "corporate_lockin",
    # §1.2.3 Closed forks
    "proprietary_fork", "closed_source", "license_restrict",
    # §1.2.4 Output suppression
    "suppress_audit", "hide_evidence", "distort_analysis",
    # §1.2.5 Opaque models
    "black_box_model", "proprietary_ai", "undocumented_ml",
    # §1.2.6 Centralization
    "centralize_control", "single_point_failure", "kill_switch",
    # §1.2.7 Discrimination/Coercion
    "discriminate", "coerce_civic_process", "manipulate_vote"
]

SURVEILLANCE_PATTERNS = [
    "user_tracking", "personal_data_retention", "profiling", "behavior_score"
]

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def hash_entry(entry: Dict[str, Any], previous_hash: str) -> str:
    """Cryptographic hash of audit entry (SHA-256, canonical JSON)."""
    # Remove hash field itself for self-referential integrity
    entry_copy = entry.copy()
    entry_copy.pop("hash", None)
    
    canonical = json.dumps(
        entry_copy, 
        sort_keys=True, 
        separators=(",", ":"), 
        ensure_ascii=False
    ).encode("utf-8")
    
    return hashlib.sha256(canonical + previous_hash.encode()).hexdigest()

def validate_schema( Dict[str, Any], schema_name: str) -> bool:
    """Validate against HoC canonical schemas."""
    schemas = {
        "audit_entry": AUDIT_ENTRY_SCHEMA,
        "audit_storage": AUDIT_STORAGE_SCHEMA
    }
    
    try:
        jsonschema.validate(instance=data, schema=schemas[schema_name])
        return True
    except jsonschema.ValidationError:
        return False

def validate_red_lines(entry: Dict[str, Any]) -> List[str]:
    """GOVERNANCE_MODEL.md §1.2 Red Lines enforcement - BLOCKS VIOLATIONS."""
    violations = []
    
    # 1. Forbidden actions (hard block)
    action = entry.get("action", "")
    if action in FORBIDDEN_ACTIONS:
        idx = FORBIDDEN_ACTIONS.index(action) // 7 + 1  # Map to Red Line #
        violations.append(f"RED_LINE_VIOLATION_{idx}: {RED_LINES[idx]}")
    
    # 2. Surveillance patterns in metadata
    metadata = str(entry.get("metadata", {}))
    for pattern in SURVEILLANCE_PATTERNS:
        if pattern in metadata.lower():
            violations.append("RED_LINE_VIOLATION_1: surveillance pattern detected")
    
    # 3. Schema compliance (constitutional layer)
    if not validate_schema(entry, "audit_entry"):
        violations.append("CONSTITUTIONAL_VIOLATION: schema non-compliance")
    
    # 4. Centralization attempts
    if entry.get("actor", {}).get("role") in ["SuperAdmin", "GodMode", "Root"]:
        violations.append("RED_LINE_VIOLATION_6: centralized control attempt")
    
    return violations

def create_audit_entry(
    actor_id: str, 
    role: str, 
    action: str, 
    target: str, 
    meta Dict[str, Any] = None,
    previous_hash: str = "GENESIS"
) -> Dict[str, Any]:
    """Create cryptographically valid audit entry."""
    if metadata is None:
        metadata = {}
    
    entry = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "actor": {
            "actor_id": actor_id,
            "actor_type": "human" if "@" in actor_id else "system",
            "authentication_method": "session",
            "role": role,
            "organization": metadata.get("organization", "HoC Core")
        },
        "action": {
            "type": "create" if "create" in action.lower() else "update",
            "operation": action,
            "status": "pending"
        },
        "object": {
            "object_type": "audit_entry",
            "object_id": target,
            "object_hash": hashlib.sha256(target.encode()).hexdigest()
        },
        "context": {
            "decision_id": metadata.get("decision_id", "N/A"),
            "lifecycle_stage": "learning",
            "jurisdiction": "FI"
        },
        "integrity": {
            "previous_hash": previous_hash,
            "hash_algorithm": "SHA-256",
            "chain_position": 0  # Updated by storage layer
        },
        "legal_status": {
            "evidentiary_class": "administrative",
            "retention_policy": "P30Y",
            "admissibility": "prima_facie"
        },
        "signature": {
            "signature_type": "none",
            "signed_at": None,
            "signer_id": None
        },
        "metadata": metadata
    }
    
    # Self-referential hash
    entry["integrity"]["hash"] = hash_entry(entry, previous_hash)
    entry["integrity"]["chain_position"] = 1  # First entry
    
    return entry

def enforce_governance_decision(decision: Dict[str, Any]) -> Dict[str, Any]:
    """Validate governance decision against GOVERNANCE_MODEL.md."""
    enforcement_schema = json.loads(
        (SCHEMAS_DIR / "governance.enforcement.schema.json").read_text()
    )
    
    try:
        jsonschema.validate(instance=decision, schema=enforcement_schema)
        
        if decision["compliance_status"] == "non_compliant":
            for violation in decision["violations"]:
                if "RED_LINE" in violation:
                    return {
                        "blocked": True,
                        "reason": f"Governance blocked: {violation}",
                        "red_line": True
                    }
        
        return {"allowed": True, "decision": decision}
        
    except jsonschema.ValidationError as e:
        return {
            "blocked": True, 
            "reason": f"Constitutional schema violation: {e.message}"
        }

# =============================================================================
# API INTEGRATION HELPERS
# =============================================================================
def audit_chain_status(chain: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Validate entire audit chain integrity."""
    if not chain:
        return {"valid": True, "length": 0}
    
    violations = 0
    for i, entry in enumerate(chain):
        entry_violations = validate_red_lines(entry)
        if entry_violations:
            violations += 1
        
        # Verify hash chain
        expected_hash = hash_entry(entry, 
            chain[i-1]["integrity"]["hash"] if i > 0 else "GENESIS")
        if expected_hash != entry["integrity"]["hash"]:
            violations += 1
    
    return {
        "valid": violations == 0,
        "length": len(chain),
        "red_line_violations": violations,
        "tamper_detected": violations > 0
    }

if _name_ == "_main_":
    # Test Red Lines enforcement
    test_entry = create_audit_entry(
        "test-user", "admin", "enable_surveillance", "users", 
        {"test": "data"}
    )
    print("Red Line test:", validate_red_lines(test_entry))


Red lines testi: curl -X POST "http://127.0.0.1:8000/audit/entry" \
  -H "Content-Type: application/json" \
  -d '{"actor":{"id":"test","role":"admin"},"action":"enable_surveillance","target":"users","metadata":{}}'
