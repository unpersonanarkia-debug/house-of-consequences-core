from fastapi import FastAPI, HTTPException
from typing import Dict, Any
from pathlib import Path

from governance.api.models import EvidencePack
from governance.api.audit import write_audit_log
from governance.api.pdf_report import generate_audit_report
from governance.api.signer import QESSigner
from governance.api.utils import validate_evidence_pack

app = FastAPI(
    title="House of Consequences – Governance API",
    version="1.0.0",
    description="Evidence Pack validation, audit logging, legal reporting & QES signing engine"
)


@app.post("/evidence/validate")
def validate_evidence(pack: Dict[str, Any]):
    try:
        validate_evidence_pack(pack)
        write_audit_log("evidence_validation_success", pack)
        return {"status": "valid", "message": "Evidence Pack validated successfully."}
    except Exception as e:
        write_audit_log("evidence_validation_failure", pack)
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/evidence/submit")
def submit_evidence(pack: EvidencePack):
    pack_dict = pack.dict()
    write_audit_log("evidence_submitted", pack_dict)
    return {"status": "submitted", "case_id": pack.metadata.case_id}


@app.post("/audit/report")
def generate_report(audit_event: Dict[str, Any]):
    output_path = Path("audit_report.pdf")
    pdf_path = generate_audit_report(audit_event, str(output_path))
    write_audit_log("audit_report_generated", audit_event)
    return {"status": "generated", "pdf": pdf_path}


@app.post("/audit/sign")
def sign_report():
    signer = QESSigner()
    signed_pdf = signer.sign_pdf("audit_report.pdf")
    write_audit_log("audit_report_signed", {"file": signed_pdf})
    return {"status": "signed", "file": signed_pdf}
