import streamlit as st
import pandas as pd
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
    load_metadata,
    apply_style,
    page_header
)


st.set_page_config(
    page_title="Dataset Overview",
    page_icon="📁",
    layout="wide"
)

apply_style()

page_header(
    "📁 Dataset Overview",
    "Explore the UNSW-NB15 network security dataset"
)


train_df = load_csv(
    RAW_DIR / "UNSW_NB15_training-set.csv"
)

test_df = load_csv(
    RAW_DIR / "UNSW_NB15_testing-set.csv"
)

metadata = load_metadata()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{len(train_df) + len(test_df):,}"
)

col2.metric(
    "Training Records",
    f"{len(train_df):,}"
)

col3.metric(
    "Testing Records",
    f"{len(test_df):,}"
)

col4.metric(
    "Input Features",
    metadata["total_features"]
)


st.subheader("About the Dataset")

st.write(
    """
    UNSW-NB15 is a network intrusion detection dataset
    containing normal network traffic and different
    categories of malicious network activity.
    """
)

st.markdown(
    "[Official UNSW-NB15 Dataset]"
    "(https://research.unsw.edu.au/projects/unsw-nb15-dataset)"
)


st.divider()

st.subheader("Dataset Preview")

dataset_choice = st.selectbox(
    "Select Dataset",
    ["Training Dataset", "Testing Dataset"]
)

df = (
    train_df
    if dataset_choice == "Training Dataset"
    else test_df
)

rows = st.slider(
    "Number of records",
    min_value=5,
    max_value=100,
    value=10
)

st.dataframe(
    df.head(rows),
    use_container_width=True
)


st.subheader("Class Distribution")

distribution = df["label"].value_counts()

class_df = pd.DataFrame({

    "Class": [
        "Normal",
        "Malicious"
    ],

    "Records": [
        distribution.get(0, 0),
        distribution.get(1, 0)
    ]
})

fig = px.pie(
    class_df,
    names="Class",
    values="Records",
    hole=0.55,
    color="Class",
    color_discrete_map={
        "Normal": "#22C55E",
        "Malicious": "#EF4444"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Feature Information")

feature_df = pd.DataFrame({

    "Feature": metadata["feature_names"],

    "Type": [
        "Categorical"
        if feature in metadata["categorical_features"]
        else "Numerical"
        for feature in metadata["feature_names"]
    ]
})

st.dataframe(
    feature_df,
    use_container_width=True
)


st.subheader("Dataset Quality")

col1, col2 = st.columns(2)

col1.metric(
    "Missing Values",
    int(df.isna().sum().sum())
)

col2.metric(
    "Duplicate Feature Records",
    int(
        df.drop(
            columns=["id", "label", "attack_cat"],
            errors="ignore"
        ).duplicated().sum()
    )
)


st.subheader("Statistical Summary")

st.dataframe(
    df.describe().T,
    use_container_width=True
)