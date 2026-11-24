import streamlit as st
import pandas as pd
import json
import sys

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(BASE_DIR))

from src.predict import IntrusionPredictor


DATA_DIR = BASE_DIR / "data" / "processed"

RAW_DIR = BASE_DIR / "data" / "raw"

MODEL_DIR = BASE_DIR / "models"

RESULT_DIR = BASE_DIR / "reports" / "results"

FIGURE_DIR = BASE_DIR / "reports" / "figures"

PREDICTION_DIR = RESULT_DIR / "predictions"


@st.cache_data
def load_csv(path):

    return pd.read_csv(path)


@st.cache_data
def load_metadata():

    with open(
        RESULT_DIR / "final_model_metadata.json",
        "r"
    ) as file:

        return json.load(file)


@st.cache_resource
def load_predictor():

    return IntrusionPredictor()


def show_report(filename):

    path = RESULT_DIR / filename

    if path.exists():

        st.dataframe(
            load_csv(path),
            use_container_width=True
        )

    else:

        st.warning(f"Report not found: {filename}")


def show_figure(filename):

    path = FIGURE_DIR / filename

    if path.exists():

        st.image(
            str(path),
            use_container_width=True
        )

    else:

        st.warning(f"Figure not found: {filename}")


def apply_style():

    st.markdown(
        """
        <style>

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        div[data-testid="stMetric"] {
            background-color: #172235;
            border: 1px solid #334155;
            padding: 18px;
            border-radius: 12px;
        }

        div[data-testid="stMetricValue"] {
            color: #38BDF8;
        }

        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def page_header(title, description):

    st.title(title)

    st.caption(description)

    st.divider()