import streamlit as st

from utils import (
    load_metadata,
    apply_style,
    page_header,
    show_figure
)


st.set_page_config(
    page_title="Network Intrusion Detection",
    page_icon="🛡️",
    layout="wide"
)

apply_style()

metadata = load_metadata()


page_header(
    "🛡️ Network Intrusion Detection System",
    "Machine Learning Based Network Security Analysis"
)


st.sidebar.success(
    "Select a page to explore the system."
)


st.subheader("System Overview")

st.write(
    """
    This system uses machine learning to classify
    network traffic as normal or malicious using
    the UNSW-NB15 cybersecurity dataset.
    """
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Test Accuracy",
    f"{metadata['accuracy'] * 100:.2f}%"
)

col2.metric(
    "Attack Recall",
    f"{metadata['recall'] * 100:.2f}%"
)

col3.metric(
    "F1 Score",
    f"{metadata['f1_score'] * 100:.2f}%"
)

col4.metric(
    "ROC AUC",
    f"{metadata['roc_auc'] * 100:.2f}%"
)


st.divider()

st.subheader("Selected Machine Learning Model")


col1, col2, col3 = st.columns(3)

col1.metric(
    "Best Model",
    metadata["model_name"]
)

col2.metric(
    "Model Type",
    metadata["model_type"]
)

col3.metric(
    "Input Features",
    metadata["total_features"]
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "Training Records",
    f"{metadata['training_records']:,}"
)

col2.metric(
    "Testing Records",
    f"{metadata['testing_records']:,}"
)

col3.metric(
    "Missed Attacks",
    f"{metadata['false_negatives']:,}"
)


st.divider()

st.subheader("Model Performance")


col1, col2 = st.columns(2)

with col1:

    show_figure("final_model_ranking.png")

with col2:

    show_figure("final_confusion_matrix.png")


st.divider()

st.subheader("System Capabilities")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        - Network traffic classification
        - Machine learning model comparison
        - Automatic data preprocessing
        - Malicious traffic probability
        """
    )

with col2:

    st.markdown(
        """
        - Single record prediction
        - Batch CSV prediction
        - Probability-based risk indication
        - Downloadable prediction reports
        """
    )


st.info(
    "This is an ML-based intrusion detection prototype. "
    "It does not capture or block live network traffic."
)

st.caption(
    "Network Intrusion Detection System | MCA Project"
)