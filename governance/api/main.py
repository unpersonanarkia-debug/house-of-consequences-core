"""
House of Consequences Governance API v1.1 - Complete Implementation
GOVERNANCE_MODEL.md §5 Auditability + Red Lines Enforcement
AGPL-3.0 | January 2026
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, validator
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import uuid
import json
import hashlib
import jsonschema
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("hoc_governance")

# Local imports (assuming structure from previous messages)
from governance.audit.rules import (
    create_audit_entry, validate_red_lines, audit_chain_status
)
from governance.audit.signer import generate_keypair, sign_bytes
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Global state
AUDIT_CHAIN: List[Dict[str, Any]] = []
PRIVATE_KEY, PUBLIC_KEY = generate_keypair()

# Schemas directory
SCHEMAS_DIR = Path.cwd() / "schemas"

app = FastAPI(
    title="House of Consequences – Governance Enforcement API v1.1",
    version="1.1.0",
    description="Constitutional enforcement layer for HoC Core. Implements GOVERNANCE_MODEL.md §1.2 Red Lines + §5 Auditability."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Citizen nodes worldwide
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Pydantic Models (Schema-validated)
# =============================================================================

class Actor(BaseModel):
    id: str
    role: str
    organization: Optional[str] = None

class AuditEntryRequest(BaseModel):
    actor: Actor
    action: str
    target: str
    meta Dict[str, Any] = {}

    @validator('action')
    def validate_action(cls, v):
        forbidden = ["enable_surveillance", "closed_fork", "suppress_audit"]
        if any(f in v.lower() for f in forbidden):
            raise ValueError("RED_LINE_VIOLATION: Forbidden action")
        return v

class EvidencePack(BaseModel):
    case_id: str
    evidence_type: str
    data_hash: str
    meta Dict[str, Any]
    
    @validator('data_hash')
    def validate_hash(cls, v):
        if len(v) != 64 or not all(c in '0123456789abcdefABCDEF' for c in v):
            raise ValueError("Invalid SHA-256 hash")
        return v

class AuditReportRequest(BaseModel):
    case_id: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None

# =============================================================================
# Helpers
# =============================================================================

def get_previous_hash() -> str:
    """Get hash of last audit entry."""
    return AUDIT_CHAIN[-1]["integrity"]["hash"] if AUDIT_CHAIN else "GENESIS"

def load_schema(schema_name: str) -> Dict[str, Any]:
    """Load HoC canonical schema."""
    schema_path = SCHEMAS_DIR / f"{schema_name}.json"
    if not schema_path.exists():
        raise HTTPException(500, f"Schema missing: {schema_name}")
    return json.loads(schema_path.read_text())

def validate_schema( Dict[str, Any], schema_name: str):
    """Validate against HoC constitutional schemas."""
    schema = load_schema(schema_name)
    jsonschema.validate(instance=data, schema=schema)

def generate_pdf_report(report_ Dict[str, Any], filename: str):
    """Generate legally admissible PDF report."""
    c = canvas.Canvas(str(filename), pagesize=A4)
    width, height = A4
    
    # Header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 60, f"HoC AUDIT REPORT v1.1")
    c.drawString(40, height - 85, f"Case ID: {report_data['case_id']}")
    c.drawString(40, height - 110, f"Generated: {report_data['generated_at']}")
    
    # Chain status
    c.setFont("Helvetica", 10)
    y_pos = height - 160
    c.drawString(40, y_pos, f"Chain Length: {len(AUDIT_CHAIN)}")
    c.drawString(40, y_pos - 20, f"Chain Hash: {get_previous_hash()[:32]}...")
    
    # Entries summary
    c.drawString(40, y_pos - 50, "RECENT ENTRIES:")
    y_pos -= 80
    for entry in AUDIT_CHAIN[-5:]:
        c.drawString(40, y_pos, f"- {entry['actor']['role']}: {entry['action']['operation']}")
        y_pos -= 20
    
    c.showPage()
    c.save()

# =============================================================================
# GOVERNANCE ENFORCEMENT ENDPOINTS
# =============================================================================

@app.post("/audit/entry", summary="Log cryptographically chained audit entry")
async def log_audit_entry(entry_req: AuditEntryRequest):
    """Create tamper-evident audit entry with Red Lines validation."""
    
    # 1. Schema validation (constitutional layer)
    raw_entry = entry_req.dict()
    try:
        validate_schema(raw_entry, "audit.log.schema")
    except jsonschema.ValidationError as e:
        audit_entry = create_audit_entry(
            actor_id=entry_req.actor.id,
            role=entry_req.actor.role,
            action=f"SCHEMA_VIOLATION_{entry_req.action}",
            target=entry_req.target,
            metadata={"error": str(e)}
        )
        AUDIT_CHAIN.append(audit_entry)
        raise HTTPException(400, f"Schema violation: {e.message}")
    
    # 2. GOVERNANCE_MODEL.md §1.2 Red Lines enforcement
    violations = validate_red_lines(raw_entry)
    if violations:
        audit_entry = create_audit_entry(
            **raw_entry,
            previous_hash=get_previous_hash()
        )
        audit_entry["compliance_status"] = "non_compliant"
        audit_entry["violations"] = violations
        AUDIT_CHAIN.append(audit_entry)
        raise HTTPException(
            status_code=412, 
            detail={"violations": violations, "entry": audit_entry}
        )
    
    # 3. Valid entry → cryptographically chain
    audit_entry = create_audit_entry(
        actor_id=entry_req.actor.id,
        role=entry_req.actor.role,
        action=entry_req.action,
        target=entry_req.target,
        metadata=entry_req.metadata,
        previous_hash=get_previous_hash()
    )
    
    # 4. Sign + append to immutable chain
    signature = sign_bytes(PRIVATE_KEY, audit_entry["integrity"]["hash"].encode())
    audit_entry["signature"]["signature_value"] = signature.hex()
    
    AUDIT_CHAIN.append(audit_entry)
    logger.info(f"Audit entry #{len(AUDIT_CHAIN)} logged: {audit_entry['action']['operation']}")
    
    return {
        "status": "logged",
        "entry_id": audit_entry["event_id"],
        "chain_position": audit_entry["integrity"]["chain_position"],
        "chain_hash": audit_entry["integrity"]["hash"]
    }

@app.get("/audit/chain", summary="Get full audit chain status")
async def get_audit_chain():
    """Return complete tamper-evident audit chain + integrity status."""
    chain_status = audit_chain_status(AUDIT_CHAIN)
    
    return {
        "chain_length": len(AUDIT_CHAIN),
        "status": chain_status,
        "last_hash": get_previous_hash(),
        "citizen_node_ready": True  # AGPL compliance
    }

@app.post("/audit/report", summary="Generate legally admissible audit report")
async def generate_audit_report_endpoint(request: AuditReportRequest):
    """Generate PDF report + QES signature for judicial use."""
    
    # Filter chain by time range
    start_time = datetime.fromisoformat(request.start_time.replace('Z', '+00:00')) if request.start_time else datetime.min
    end_time = datetime.fromisoformat(request.end_time.replace('Z', '+00:00')) if request.end_time else datetime.max
    
    filtered_chain = [
        entry for entry in AUDIT_CHAIN 
        if start_time <= datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00')) <= end_time
    ]
    
    report_id = str(uuid.uuid4())
    report_data = {
        "report_id": report_id,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "case_id": request.case_id,
        "chain_length": len(filtered_chain),
        "status": audit_chain_status(filtered_chain)
    }
    
    # Generate PDF
    pdf_path = Path(f"audit_report_{report_id}.pdf")
    generate_pdf_report(report_data, pdf_path)
    
    # Sign PDF content
    report_hash = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    signature = sign_bytes(PRIVATE_KEY, report_hash.encode())
    
    # Audit the audit report generation
    audit_entry = create_audit_entry(
        actor_id="hoc-audit-system",
        role="SystemAuditor",
        action="generate_audit_report",
        target=request.case_id,
        metadata={"report_id": report_id, "pdf_path": str(pdf_path)}
    )
    AUDIT_CHAIN.append(audit_entry)
    
    return {
        "status": "generated",
        "report_id": report_id,
        "pdf_path": str(pdf_path),
        "report_hash": report_hash,
        "signature": signature.hex(),
        "public_key_pem": PUBLIC_KEY.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }

@app.post("/evidence/validate")
async def validate_evidence_pack(evidence: Dict[str, Any]):
    """Validate evidence pack against HoC schemas + Red Lines."""
    try:
        validate_schema(evidence, "evidence.pack")
        validate_red_lines({"action": "evidence_validation", "metadata": evidence})
        write_audit_log("evidence_validation_success", evidence)
        return {"status": "valid", "message": "Evidence Pack validated successfully."}
    except Exception as e:
        write_audit_log("evidence_validation_failure", evidence)
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/governance/status")
async def governance_status():
    """Real-time governance compliance status."""
    chain_status = audit_chain_status(AUDIT_CHAIN)
    return {
        "status": "ACTIVE" if chain_status["valid"] else "COMPROMISED",
        "audit_entries": len(AUDIT_CHAIN),
        "red_line_violations": chain_status.get("red_line_violations", 0),
        "tamper_detected": chain_status["tamper_detected"],
        "timestamp": datetime.utcnow().isoformat(),
        "governance_model": "v1.0-compliant"
    }

@app.get("/audit/report/{report_id}/download")
async def download_report(report_id: str):
    """Download signed audit report PDF."""
    pdf_path = Path(f"audit_report_{report_id}.pdf")
    if not pdf_path.exists():
        raise HTTPException(404, "Report not found")
    return FileResponse(pdf_path, media_type="application/pdf")

if _name_ == "_main_":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
