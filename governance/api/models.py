from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class DataSource(BaseModel):
    provider: str
    dataset: str
    year: int


class Metadata(BaseModel):
    case_id: str
    domain: str
    version: str
    created_at: datetime
    authors: List[str]
    data_sources: List[DataSource]


class Timeframe(BaseModel):
    start_year: int
    end_year: int


class Scope(BaseModel):
    population: str
    timeframe: Timeframe
    exclusions: List[str]


class Method(BaseModel):
    method_type: str
    description: str
    controls: Optional[List[str]] = None
    limitations: Optional[str] = None


class Finding(BaseModel):
    metric: str
    baseline: float
    exposed: float
    unit: str
    confidence_interval: Optional[str] = None


class EconomicImpact(BaseModel):
    per_case_cost: float
    annual_total_cost: float
    currency: str


class Attribution(BaseModel):
    risk_difference: float
    hazard_ratio: float
    attributable_fraction: float
    economic_impact: EconomicImpact


class PDCA_Support(BaseModel):
    plan_signal: str
    do_signal: str
    check_signal: str
    act_leverage_points: List[str]


class GovernanceAssessment(BaseModel):
    normalized_error_indicator: bool
    structural_risk_score: float
    notes: Optional[str] = None


class EvidencePack(BaseModel):
    metadata: Metadata
    scope: Scope
    methods: List[Method]
    findings: List[Finding]
    attribution: Attribution
    pdca_support: PDCA_Support
    governance_assessment: GovernanceAssessment
