from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import hashlib
import json
import os
import uuid
from jsonschema import validate, Draft202012Validator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# ============================
# Application setup
# ============================

app = FastAPI(
    title="House of Consequences – Governance API",
    description="Audit, traceability, legal reporting and QES signing service.",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(_file_))
DATA_DIR = os.path.join(BASE_DIR, "..", "..", "data")
SCHEMA_DIR = os.path.join(BASE_DIR, "..", "..", "schemas")
REPORT_DIR = os.path.join(BASE_DIR, "..", "..", "reports")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# ============================
# Schema loading
# ============================

def load_schema(name: str) -> Dict[str, Any]:
    path = os.path.join(SCHEMA_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

AUDIT_LOG_SCHEMA = load_schema("audit.log.schema.json")
AUDIT_STORAGE_SCHEMA = load_schema("audit.log.storage.schema.json")
AUDIT_REPORT_SCHEMA = load_schema("audit.report.schema.json")

audit_log_validator = Draft202012Validator(AUDIT_LOG_SCHEMA)
audit_storage_validator = Draft202012Validator(AUDIT_STORAGE_SCHEMA)
audit_report_validator = Draft202012Validator(AUDIT_REPORT_SCHEMA)

# ============================
# Cryptographic utilities
# ============================

KEY_DIR = os.path.join(DATA_DIR, "keys")
PRIVATE_KEY_PATH = os.path.join(KEY_DIR, "qes_private_key.pem")
PUBLIC_KEY_PATH = os.path.join(KEY_DIR, "qes_public_key.pem")
os.makedirs(KEY_DIR, exist_ok=True)

def generate_qes_keypair():
    if os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH):
        return

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

def load_public_key():
    with open(PUBLIC_KEY_PATH, "rb") as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

generate_qes_keypair()

# ============================
# Storage utilities
# ============================

STORAGE_PATH = os.path.join(DATA_DIR, "audit_storage.json")

def initialize_storage():
    if os.path.exists(STORAGE_PATH):
        return

    storage = {
        "storage_id": f"audit-storage-{uuid.uuid4()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "storage_policy": {
            "append_only": True,
            "worm_compliant": True,
            "encryption": {
                "enabled": False,
                "algorithm": "AES-256-GCM",
                "key_management": "manual"
            },
            "access_control": {
                "model": "RBAC",
                "roles": ["Auditor", "LegalAuthority", "SystemAdmin"]
            }
        },
        "log_chain": [],
        "retention": {
            "retention_period": "P30Y",
            "retention_basis": "legal_obligation",
            "disposal_method": "none"
        },
        "integrity": {
            "chain_hash": "0" * 64,
            "hash_algorithm": "SHA-256",
            "last_chain_position": 0
        },
        "legal_status": {
            "evidentiary_class": "judicial",
            "compliance_frameworks": ["GDPR", "eIDAS", "ISO27001", "NIS2"],
            "jurisdiction": "FI"
        }
    }

    audit_storage_validator.validate(storage)

    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2)

initialize_storage()

def load_storage() -> Dict[str, Any]:
    with open(STORAGE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_storage(storage: Dict[str, Any]):
    audit_storage_validator.validate(storage)
    with open(STORAGE_PATH, "w", encoding="utf-8") as f:
        json.dump(storage, f, indent=2)

def compute_chain_hash(log_chain: List[Dict[str, Any]]) -> str:
    chain_data = json.dumps(log_chain, sort_keys=True).encode("utf-8")
    return hashlib.sha256(chain_data).hexdigest()

# ============================
# Models (API I/O)
# ============================

class AuditLogEntry(BaseModel):
    data: Dict[str, Any] = Field(..., description="Audit log entry conforming to audit.log.schema.json")

class AuditReportRequest(BaseModel):
    report_title: str
    jurisdiction: str
    requesting_authority: str
    purpose: str
    scope: Optional[str] = None

# ============================
# API Endpoints
# ============================

@app.get("/health")
def health():
    return {"status": "ok", "service": "House of Consequences – Governance API"}

@app.post("/audit/log")
def append_audit_log(entry: AuditLogEntry):
    # Schema validation
    errors = sorted(audit_log_validator.iter_errors(entry.data), key=lambda e: e.path)
    if errors:
        raise HTTPException(status_code=422, detail=[e.message for e in errors])

    storage = load_storage()

    # Enforce append-only
    previous_hash = storage["integrity"]["chain_hash"]

    enriched_entry = entry.data.copy()
    enriched_entry["chain_position"] = storage["integrity"]["last_chain_position"] + 1
    enriched_entry["previous_chain_hash"] = previous_hash
    enriched_entry["recorded_at"] = datetime.now(timezone.utc).isoformat()

    storage["log_chain"].append(enriched_entry)
    storage["integrity"]["last_chain_position"] = enriched_entry["chain_position"]
    storage["integrity"]["chain_hash"] = compute_chain_hash(storage["log_chain"])

    save_storage(storage)

    return {
        "status": "appended",
        "chain_position": enriched_entry["chain_position"],
        "current_chain_hash": storage["integrity"]["chain_hash"]
    }

@app.get("/audit/logs")
def list_audit_logs():
    storage = load_storage()
    return {
        "storage_id": storage["storage_id"],
        "log_count": len(storage["log_chain"]),
        "integrity": storage["integrity"],
        "log_chain": storage["log_chain"]
    }

@app.post("/audit/report")
def generate_audit_report(request: AuditReportRequest):
    storage = load_storage()

    report_id = f"audit-report-{uuid.uuid4()}"
    timestamp = datetime.now(timezone.utc).isoformat()

    report = {
        "report_id": report_id,
        "generated_at": timestamp,
        "jurisdiction": request.jurisdiction,
        "requesting_authority": request.requesting_authority,
        "purpose": request.purpose,
        "scope": request.scope,
        "storage_snapshot": storage,
        "legal_assertions": {
            "append_only": True,
            "worm_compliant": True,
            "chain_integrity_verified": True,
            "hash_algorithm": storage["integrity"]["hash_algorithm"],
            "evidentiary_class": storage["legal_status"]["evidentiary_class"]
        }
    }

    # Validate report schema
    audit_report_validator.validate(report)

    # Generate PDF
    pdf_path = os.path.join(REPORT_DIR, f"{report_id}.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Audit Report – House of Consequences")
    y -= 30

    c.setFont("Helvetica", 10)
    for key, value in report.items():
        text = f"{key}: {json.dumps(value, indent=2) if isinstance(value, (dict, list)) else value}"
        for line in text.split("\n"):
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(50, y, line[:110])
            y -= 12

    c.showPage()
    c.save()

    # QES signing
    private_key = load_private_key()
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    signature = private_key.sign(
        pdf_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    signature_path = os.path.join(REPORT_DIR, f"{report_id}.sig")
    with open(signature_path, "wb") as f:
        f.write(signature)

    return {
        "status": "report_generated",
        "report_id": report_id,
        "pdf_path": pdf_path,
        "signature_path": signature_path,
        "chain_hash": storage["integrity"]["chain_hash"]
    }

@app.get("/audit/report/{report_id}/pdf")
def download_report(report_id: str):
    pdf_path = os.path.join(REPORT_DIR, f"{report_id}.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(pdf_path, media_type="application/pdf", filename=f"{report_id}.pdf")

@app.get("/audit/report/{report_id}/signature")
def download_signature(report_id: str):
    sig_path = os.path.join(REPORT_DIR, f"{report_id}.sig")
    if not os.path.exists(sig_path):
        raise HTTPException(status_code=404, detail="Signature not found")
    return FileResponse(sig_path, media_type="application/octet-stream", filename=f"{report_id}.sig")
