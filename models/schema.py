from pydantic import BaseModel

class ClauseAnalysis(BaseModel):
    summary: str
    risk_level: str
    risk_reason: str
    renegotiation_suggestion: str
    one_sided: bool