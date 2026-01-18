from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
import json
import os
import hashlib
import datetime
from uuid import uuid4

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = FastAPI(
    title="House of Consequences – Governance API",
    description="Legal-grade audit trail, validation, reporting and QES signing engine.",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(_file_))
SCHEMA_DIR = os.path.join(BASE_DIR, "../../schemas")
AUDIT_LOG_FILE = os.path.join(BASE_DIR, "../../audit.log.jsonl")
AUDIT_REPORT_DIR = os.path.join(BASE_DIR, "../../audit_reports")

os.makedirs(AUDIT_REPORT_DIR, exist_ok=True)


# ------------------------------
# Utility functions
# ------------------------------

def load_schema(schema_name: str) -> Dict[str, Any]:
    path = os.path.join(SCHEMA_DIR, schema_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema not found: {schema_name}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sha256_hash(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def get_last_audit_hash() -> str:
    if not os.path.exists(AUDIT_LOG_FILE):
        return "GENESIS"
    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines:
            return "GENESIS"
        last_entry = json.loads(lines[-1])
        return last_entry.get("entry_hash", "GENESIS")


def write_audit_log(entry: Dict[str, Any]) -> Dict[str, Any]:
    previous_hash = get_last_audit_hash()
    entry["previous_hash"] = previous_hash
    entry_string = json.dumps(entry, sort_keys=True)
    entry_hash = sha256_hash(entry_string)
    entry["entry_hash"] = entry_hash

    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return entry


def generate_pdf_report(report_id: str, title: str, sections: List[str]) -> str:
    filename = f"audit_report_{report_id}.pdf"
    path = os.path.join(AUDIT_REPORT_DIR, filename)

    doc = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(title, styles["Title"]))
    story.append(Spacer(1, 12))

    for section in sections:
        story.append(Paragraph(section, styles["BodyText"]))
        story.append(Spacer(1, 12))

    doc.build(story)
    return path


def qes_sign_pdf(pdf_path: str) -> str:
    """
    Placeholder for Qualified Electronic Signature (QES).
    This is designed to integrate with:
    - eIDAS-compliant trust service providers
    - PKI smart cards / HSMs
    - ETSI EN 319 142 / 319 102 standards

    For now, this function simulates a cryptographic seal.
    """
    signature_record = {
        "pdf_path": pdf_path,
        "signed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "signature_method": "QES-SIMULATED",
        "signer": "House of Consequences Authority",
        "legal_basis": "eIDAS Regulation (EU) No 910/2014",
        "signature_id": str(uuid4())
    }

    signature_file = pdf_path.replace(".pdf", ".signature.json")
    with open(signature_file, "w", encoding="utf-8") as f:
        json.dump(signature_record, f, indent=2, ensure_ascii=False)

    return signature_file


# ------------------------------
# API Models
# ------------------------------

class ValidationRequest(BaseModel):
    schema: str
    payload: Dict[str, Any]
    actor: str
    system: str


class AuditReportRequest(BaseModel):
    decision_id: str
    title: str
    sections: List[str]
    actor: str
    system: str


# ------------------------------
# Endpoints
# ------------------------------

@app.get("/")
def root():
    return {
        "service": "House of Consequences – Governance API",
        "status": "operational",
        "features": [
            "JSON Schema Validation",
            "Legal Audit Trail",
            "Audit Report Generation (PDF)",
            "QES Digital Signing",
            "OpenAPI Contract"
        ]
    }


@app.post("/validate")
def validate_payload(request: ValidationRequest):
    try:
        schema = load_schema(request.schema)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # Manual lightweight validation (placeholder for jsonschema library)
    if "required" in schema:
        for field in schema["required"]:
            if field not in request.payload:
                raise HTTPException(
                    status_code=422,
                    detail=f"Missing required field: {field}"
                )

    audit_entry = {
        "event_id": str(uuid4()),
        "event_type": "SCHEMA_VALIDATION",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "actor": request.actor,
        "system": request.system,
        "schema": request.schema,
        "payload_hash": sha256_hash(json.dumps(request.payload, sort_keys=True)),
        "result": "VALID",
        "legal_basis": "Administrative Procedure Act / Evidence Integrity Act",
        "retention_policy": "Permanent"
    }

    write_audit_log(audit_entry)

    return {
        "status": "valid",
        "audit_event_id": audit_entry["event_id"]
    }


@app.post("/audit/report")
def generate_audit_report(request: AuditReportRequest):
    report_id = str(uuid4())

    pdf_path = generate_pdf_report(
        report_id=report_id,
        title=request.title,
        sections=request.sections
    )

    signature_file = qes_sign_pdf(pdf_path)

    audit_entry = {
        "event_id": str(uuid4()),
        "event_type": "AUDIT_REPORT_GENERATED",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "actor": request.actor,
        "system": request.system,
        "decision_id": request.decision_id,
        "report_id": report_id,
        "pdf_path": pdf_path,
        "signature_file": signature_file,
        "legal_basis": "eIDAS Regulation / Administrative Evidence Standards",
        "retention_policy": "Permanent"
    }

    write_audit_log(audit_entry)

    return {
        "status": "report_generated_and_signed",
        "report_id": report_id,
        "pdf_path": pdf_path,
        "signature_file": signature_file,
        "audit_event_id": audit_entry["event_id"]
    }


@app.get("/audit/logs")
def get_audit_logs(limit: int = 100):
    if not os.path.exists(AUDIT_LOG_FILE):
        return []

    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logs = [json.loads(line) for line in lines[-limit:]]
    return logs


@app.get("/audit/verify-chain")
def verify_audit_chain():
    if not os.path.exists(AUDIT_LOG_FILE):
        return {"status": "empty_log", "valid": True}

    with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    previous_hash = "GENESIS"
    for line in lines:
        entry = json.loads(line)
        recorded_prev = entry.get("previous_hash")
        recorded_hash = entry.get("entry_hash")

        entry_copy = entry.copy()
        entry_copy.pop("entry_hash", None)

        recomputed_hash = sha256_hash(json.dumps(entry_copy, sort_keys=True))

        if recorded_prev != previous_hash or recorded_hash != recomputed_hash:
            return {
                "status": "broken_chain",
                "valid": False,
                "at_event_id": entry.get("event_id")
            }

        previous_hash = recorded_hash

    return {
        "status": "chain_valid",
        "valid": True,
        "entries": len(lines)
    }
