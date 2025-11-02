from __future__ import annotations
from typing import List, Tuple
import pandas as pd
from pydantic import ValidationError
from .data_model import CompetencyRecord, CompetencySchema

def infer_competencies(df: pd.DataFrame) -> List[str]:
    base_cols = {"PersonID", "Name", "Department"}
    candidates = [c for c in df.columns if c not in base_cols]
    # Ensure deterministic order
    return sorted(candidates)

def validate_dataframe(df: pd.DataFrame) -> Tuple[pd.DataFrame, CompetencySchema]:
    comps = infer_competencies(df)
    if len(comps) != 25:
        raise ValueError(f"Expected 25 competencies, found {len(comps)}: {comps}")

    # Validate ranges and structure via pydantic
    for _, row in df.iterrows():
        scores = {c: float(row[c]) for c in comps}
        try:
            CompetencyRecord(
                PersonID=str(row["PersonID"]),
                Name=str(row["Name"]),
                Department=str(row["Department"]),
                scores=scores,
            )
        except ValidationError as e:
            raise ValueError(f"Validation error: {e}") from e

    return df.copy(), CompetencySchema(competencies=comps)

def load_csv(path: str) -> Tuple[pd.DataFrame, CompetencySchema]:
    df = pd.read_csv(path)
    return validate_dataframe(df)
