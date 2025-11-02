from __future__ import annotations
from typing import List, Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def radar_for_person(df: pd.DataFrame, competencies: List[str], person_id: str):
    row = df.loc[df["PersonID"] == person_id]
    if row.empty:
        raise ValueError(f"PersonID {person_id} not found")
    values = [float(row.iloc[0][c]) for c in competencies]
    fig = go.Figure(
        data=go.Scatterpolar(r=values, theta=competencies, fill="toself")
    )
    fig.update_layout(title=f"Radar — {row.iloc[0]['Name']} ({person_id})", polar=dict(radialaxis=dict(range=[0, 100])))
    return fig

def dept_profile_heatmap(df: pd.DataFrame, competencies: List[str], agg: str = "mean"):
    if agg not in {"mean", "median"}:
        raise ValueError("agg must be 'mean' or 'median'")
    grouped = getattr(df.groupby("Department")[competencies], agg)().reset_index()
    long_df = grouped.melt(id_vars="Department", var_name="Competency", value_name="Score")
    fig = px.density_heatmap(
        long_df, x="Competency", y="Department", z="Score", histfunc="avg", nbinsx=len(competencies)
    )
    fig.update_layout(title=f"Department × Competency heatmap ({agg})")
    return fig

def correlation_heatmap(df: pd.DataFrame, competencies: List[str]):
    corr = df[competencies].corr()
    corr_long = corr.reset_index().melt(id_vars="index", var_name="Competency", value_name="Correlation")
    corr_long.rename(columns={"index": "CompetencyA"}, inplace=True)
    fig = px.density_heatmap(
        corr_long, x="Competency", y="CompetencyA", z="Correlation", histfunc="avg", nbinsx=len(competencies)
    )
    fig.update_layout(title="Competency Correlation Heatmap")
    return fig
