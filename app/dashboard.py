import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from app.data_loader import load_csv
from app.visuals import radar_for_person, dept_profile_heatmap, correlation_heatmap

st.set_page_config(page_title="Competency Dashboard", layout="wide")

st.title("人材コンピテンシー可視化ダッシュボード")

uploaded = st.file_uploader("CSVファイルをアップロード (columns: PersonID, Name, Department, C01..C25)", type=["csv"])
if uploaded is not None:
    df = pd.read_csv(uploaded)
else:
    st.info("サンプルデータを使用しています（`sample_data/competencies.csv`）")
    df = pd.read_csv("sample_data/competencies.csv")

try:
    df_valid, schema = load_csv(df.to_csv(index=False))
except Exception:
    # load_csv expects a path; allow fallback
    from io import StringIO
    sio = StringIO(df.to_csv(index=False))
    df_valid = pd.read_csv(sio)
    from app.data_loader import validate_dataframe
    df_valid, schema = validate_dataframe(df_valid)

left, right = st.columns([1, 2])

with left:
    st.subheader("フィルタ")
    dept = st.selectbox("Department", ["(All)"] + sorted(df_valid["Department"].unique().tolist()))
    if dept != "(All)":
        view = df_valid[df_valid["Department"] == dept]
    else:
        view = df_valid

    person = st.selectbox("Person", view["PersonID"] + " — " + view["Name"])
    person_id = person.split(" — ")[0]

    st.subheader("レーダーチャート")
    radar = radar_for_person(view, schema.competencies, person_id)
    st.plotly_chart(radar, use_container_width=True)

with right:
    st.subheader("部門×コンピテンシー（平均）")
    heat = dept_profile_heatmap(view, schema.competencies, agg="mean")
    st.plotly_chart(heat, use_container_width=True)

    st.subheader("コンピテンシー相関")
    corr = correlation_heatmap(view, schema.competencies)
    st.plotly_chart(corr, use_container_width=True)

st.caption("Tips: 0〜100のスコア、列名は C01..C25 を想定。")
