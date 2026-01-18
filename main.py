from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Literal
from datetime import datetime

app = FastAPI(
    title="House of Consequences – Governance Decision Validator",
    description="Validates governance decisions against locked consequence protocol schema.",
    version="1.0.0"
)

# -----------------------------
# Data Models
# -----------------------------

class MeasurementIndicator(BaseModel):
    name: str = Field(..., min_length=3)
    metric: str = Field(..., min_length=3)
    acceptable_threshold: float
    allowed_duration_days: int = Field(..., ge=1)

class GovernanceRequirements(BaseModel):
    measurement_indicators: List[MeasurementIndicator]
    monitoring_plan: Dict[str, Any]
    reversal_protocol: Dict[str, Any]
    review_cycle_days: int = Field(..., ge=1, le=365)

class ConsequenceModel(BaseModel):
    predicted_impacts: List[str] = Field(..., min_items=1)
    uncertainty_level: float = Field(..., ge=0, le=1)
    reversibility_score: float = Field(..., ge=0, le=1)
    normalization_risk: float = Field(..., ge=0, le=1)

class Decision(BaseModel):
    decision_id: str = Field(..., regex=r"^[A-Z0-9._-]+$")
    domain: str = Field(..., min_length=3)
    authority: str = Field(..., min_length=3)
    timestamp: datetime
    intent: str = Field(..., min_length=10)
    action: str = Field(..., min_length=10)
    consequence_model: ConsequenceModel
    governance_requirements: GovernanceRequirements
    validation_state: Literal["PENDING", "VALID", "INVALID", "REVOKED"]

    @validator("consequence_model")
    def block_normalized_harm(cls, v):
        if v.normalization_risk > 0.7 and v.reversibility_score < 0.3:
            raise ValueError(
                "Decision blocked: high normalization risk combined with low reversibility."
            )
        return v

    @validator("governance_requirements")
    def enforce_monitoring_and_reversal(cls, v):
        if not v.monitoring_plan:
            raise ValueError("Monitoring plan must not be empty.")
        if not v.reversal_protocol:
            raise ValueError("Reversal protocol must not be empty.")
        if not v.measurement_indicators:
            raise ValueError("At least one measurement indicator is required.")
        return v

# -----------------------------
# API Endpoints
# -----------------------------

@app.post("/validate", summary="Validate governance decision", tags=["validation"])
def validate_decision(decision: Decision):
    if decision.validation_state != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only decisions in PENDING state may be validated."
        )

    return {
        "decision_id": decision.decision_id,
        "status": "VALID",
        "message": "Decision passed all consequence governance checks.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@app.get("/health", summary="Service health check", tags=["system"])
def health_check():
    return {"status": "ok", "service": "House of Consequences Validator"}
