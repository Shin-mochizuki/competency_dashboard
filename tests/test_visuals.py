import pandas as pd
from app.visuals import radar_for_person, dept_profile_heatmap, correlation_heatmap

def _df():
    cols = ["PersonID","Name","Department"] + [f"C{i:02d}" for i in range(1,26)]
    row = ["P0001","Alice","Sales"] + [i for i in range(25)]
    row2 = ["P0002","Bob","Engineering"] + [100-i for i in range(25)]
    return pd.DataFrame([row, row2], columns=cols), [f"C{i:02d}" for i in range(1,26)]

def test_radar_person():
    df, comps = _df()
    fig = radar_for_person(df, comps, "P0001")
    assert fig is not None

def test_heatmaps():
    df, comps = _df()
    assert dept_profile_heatmap(df, comps) is not None
    assert correlation_heatmap(df, comps) is not None
