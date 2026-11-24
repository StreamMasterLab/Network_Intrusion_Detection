import streamlit as st
import plotly.express as px
import sys

from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from utils import (
    RAW_DIR,
    load_csv,
    show_figure,
    show_report,
    apply_style,
    page_header
)


st.set_page_config(
    page_title="Data Analysis",
    page_icon="📊",
    layout="wide"
)

apply_style()

page_header(
    "📊 Exploratory Data Analysis",
    "Analyze network traffic and attack patterns"
)


df = load_csv(
    RAW_DIR / "UNSW_NB15_training-set.csv"
)


tab1, tab2, tab3, tab4 = st.tabs([

    "Attack Distribution",

    "Protocol Analysis",

    "Numerical Analysis",

    "Correlation Analysis"
])


with tab1:

    st.subheader("Attack Category Distribution")

    attacks = (
        df["attack_cat"]
        .value_counts()
        .rename_axis("Attack Category")
        .reset_index(name="Records")
    )

    fig = px.bar(
        attacks,
        x="Records",
        y="Attack Category",
        orientation="h",
        color="Records",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        attacks,
        use_container_width=True
    )


with tab2:

    st.subheader("Categorical Feature Analysis")

    feature = st.selectbox(
        "Select Feature",
        ["proto", "service", "state"]
    )

    counts = (
        df[feature]
        .value_counts()
        .head(15)
        .rename_axis(feature)
        .reset_index(name="Records")
    )

    fig = px.bar(
        counts,
        x=feature,
        y="Records",
        color="Records",
        color_continuous_scale="Teal"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with tab3:

    st.subheader("Numerical Feature Distribution")

    feature = st.selectbox(
        "Select Numerical Feature",

        [
            "dur",
            "spkts",
            "dpkts",
            "sbytes",
            "dbytes",
            "rate",
            "sload",
            "dload"
        ]
    )

    sample = df.sample(
        min(10000, len(df)),
        random_state=42
    ).copy()

    sample["Traffic Type"] = sample["label"].map({
        0: "Normal",
        1: "Malicious"
    })

    fig = px.histogram(
        sample,
        x=feature,
        color="Traffic Type",
        nbins=50,
        barmode="overlay",
        color_discrete_map={
            "Normal": "#22C55E",
            "Malicious": "#EF4444"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Histogram uses up to 10,000 sampled records."
    )

    fig = px.box(
        sample,
        x="Traffic Type",
        y=feature,
        color="Traffic Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with tab4:

    st.subheader("Feature Correlation")

    show_report("feature_correlation.csv")

    numeric_df = df.drop(
        columns=["id"],
        errors="ignore"
    ).select_dtypes(include="number")

    correlation = numeric_df.corr()

    fig = px.imshow(
        correlation,
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto"
    )

    fig.update_layout(height=850)

    st.plotly_chart(
        fig,
        use_container_width=True
    )