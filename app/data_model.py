from typing import Dict, List
from pydantic import BaseModel, Field, validator

class CompetencyRecord(BaseModel):
    PersonID: str
    Name: str
    Department: str
    # 25 competencies scored 0..100
    scores: Dict[str, float] = Field(..., description="Competency -> score 0..100")

    @validator("scores")
    def _check_scores(cls, v: Dict[str, float]):
        if len(v) != 25:
            raise ValueError("Expected exactly 25 competencies")
        for k, val in v.items():
            if not (0.0 <= float(val) <= 100.0):
                raise ValueError(f"Score out of range for {k}: {val}")
        return v

class CompetencySchema(BaseModel):
    competencies: List[str]
