import pandas as pd
from app.data_loader import validate_dataframe

def test_validate_ok():
    cols = ["PersonID","Name","Department"] + [f"C{i:02d}" for i in range(1,26)]
    df = pd.DataFrame([["P0001","Alice","Sales", *([50.0]*25)]], columns=cols)
    out, schema = validate_dataframe(df)
    assert list(sorted(schema.competencies)) == [f"C{i:02d}" for i in range(1,26)]
    assert len(out) == 1

def test_validate_range_error():
    cols = ["PersonID","Name","Department"] + [f"C{i:02d}" for i in range(1,26)]
    bad = [150.0] + [50.0]*24  # first competency out of range
    df = pd.DataFrame([["P0001","Alice","Sales", *bad]], columns=cols)
    try:
        validate_dataframe(df)
    except ValueError as e:
        assert "out of range" in str(e)
    else:
        assert False, "Expected ValueError"
