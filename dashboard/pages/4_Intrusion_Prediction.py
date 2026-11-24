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
    DATA_DIR,
    PREDICTION_DIR,
    load_csv,
    load_predictor,
    apply_style,
    page_header
)


st.set_page_config(
    page_title="Intrusion Prediction",
    page_icon="🛡️",
    layout="wide"
)

apply_style()

page_header(
    "🛡️ Intrusion Prediction",
    "Classify network traffic as normal or malicious"
)


predictor = load_predictor()

metadata = predictor.get_model_info()


st.sidebar.subheader("Detection Engine")

st.sidebar.write(
    "Model:", metadata["model_name"]
)

st.sidebar.write(
    "Features:", metadata["total_features"]
)

st.sidebar.success("Model loaded successfully")


def display_prediction(result):

    row = result.iloc[0]

    if row["Predicted Label"] == 1:

        st.error(
            "🚨 Malicious Network Traffic Detected"
        )

    else:

        st.success(
            "🛡️ Network Traffic Classified as Normal"
        )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Malicious Probability",
        f"{row['Malicious Probability']:.2%}"
    )

    col2.metric(
        "Normal Probability",
        f"{row['Normal Probability']:.2%}"
    )

    col3.metric(
        "Risk Indication",
        row["Risk Level"]
    )

    probability = float(
        row["Malicious Probability"]
    )

    st.progress(
        probability,
        text="Estimated malicious probability"
    )

    st.caption(
        "Risk indication is based on model probability, "
        "not verified attack severity."
    )


tab1, tab2 = st.tabs([

    "Manual Prediction",

    "CSV Batch Prediction"
])


with tab1:

    st.subheader("Single Network Record Prediction")

    sample_choice = st.selectbox(

        "Choose an Input Template",

        [
            "Normal Sample",
            "Malicious Sample",
            "Custom Input"
        ]
    )

    if sample_choice == "Normal Sample":

        sample = load_csv(
            PREDICTION_DIR / "normal_sample.csv"
        ).iloc[0]

    elif sample_choice == "Malicious Sample":

        sample = load_csv(
            PREDICTION_DIR / "malicious_sample.csv"
        ).iloc[0]

    else:

        sample = load_csv(
            PREDICTION_DIR / "custom_sample.csv"
        ).iloc[0]

    st.caption(
        "Edit the network feature values below. "
        "Custom Input starts with an editable example."
    )

    user_input = {}

    with st.form(
        key=f"prediction_form_{sample_choice}"
    ):

        columns = st.columns(3)

        for index, feature in enumerate(
            predictor.feature_names
        ):

            with columns[index % 3]:

                if feature in predictor.categorical_features:

                    user_input[feature] = st.text_input(

                        feature,

                        value=str(sample[feature]),

                        key=f"{sample_choice}_{feature}"
                    )

                else:

                    user_input[feature] = st.number_input(

                        feature,

                        value=float(sample[feature]),

                        format="%.8f",

                        key=f"{sample_choice}_{feature}"
                    )

        submitted = st.form_submit_button(

            "Analyze Network Traffic",

            type="primary",

            use_container_width=True
        )

    if submitted:

        try:

            with st.spinner(
                "Analyzing network traffic..."
            ):

                result = predictor.predict(
                    user_input
                )

            display_prediction(result)

            st.dataframe(
                result,
                use_container_width=True
            )

            st.download_button(

                "Download Prediction Result",

                result.to_csv(index=False),

                file_name="single_prediction.csv",

                mime="text/csv"
            )

        except Exception as error:

            st.error(
                f"Prediction failed: {error}"
            )


with tab2:

    st.subheader("Batch Network Traffic Prediction")

    st.write(
        "Upload a CSV file containing the required "
        "network traffic features."
    )

    template = pd.DataFrame(
        columns=predictor.feature_names
    )

    st.download_button(

        "Download Input Template",

        template.to_csv(index=False),

        file_name="network_input_template.csv",

        mime="text/csv"
    )

    sample_file = (
        PREDICTION_DIR / "batch_sample.csv"
    )

    if sample_file.exists():

        st.download_button(

            "Download Sample Dataset",

            sample_file.read_bytes(),

            file_name="batch_sample.csv",

            mime="text/csv"
        )

    uploaded_file = st.file_uploader(

        "Upload Network Traffic CSV",

        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            input_df = pd.read_csv(
                uploaded_file
            )

            st.subheader("Uploaded Dataset")

            st.dataframe(
                input_df.head(10),
                use_container_width=True
            )

            st.write(
                "Total Records:", len(input_df)
            )

            if st.button(

                "Analyze Uploaded Dataset",

                type="primary",

                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing network records..."
                ):

                    results = predictor.predict(
                        input_df
                    )

                total = len(results)

                normal = int(
                    (results["Predicted Label"] == 0).sum()
                )

                malicious = int(
                    (results["Predicted Label"] == 1).sum()
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric(
                    "Total Records", total
                )

                col2.metric(
                    "Normal Traffic", normal
                )

                col3.metric(
                    "Malicious Traffic", malicious
                )

                col4.metric(
                    "Malicious Traffic %",
                    f"{malicious / total:.2%}"
                )

                distribution = pd.DataFrame({

                    "Traffic Type": [
                        "Normal",
                        "Malicious"
                    ],

                    "Records": [
                        normal,
                        malicious
                    ]
                })

                fig = px.pie(

                    distribution,

                    names="Traffic Type",

                    values="Records",

                    hole=0.55,

                    color="Traffic Type",

                    color_discrete_map={

                        "Normal": "#22C55E",

                        "Malicious": "#EF4444"
                    }
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                st.subheader("Prediction Results")

                final_output = pd.concat([

                    input_df.reset_index(drop=True),

                    results.reset_index(drop=True)

                ], axis=1)

                st.dataframe(
                    final_output,
                    use_container_width=True
                )

                st.download_button(

                    "Download Complete Prediction Report",

                    final_output.to_csv(index=False),

                    file_name="intrusion_predictions.csv",

                    mime="text/csv"
                )

        except Exception as error:

            st.error(
                f"Unable to process CSV: {error}"
            )