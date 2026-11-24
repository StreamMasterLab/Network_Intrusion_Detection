import streamlit as st
import plotly.express as px
import sys

from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

from utils import (
    RESULT_DIR,
    load_csv,
    load_metadata,
    show_report,
    show_figure,
    apply_style,
    page_header
)


st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

apply_style()

page_header(
    "📈 Model Performance",
    "Compare machine learning models and evaluation results"
)


tab1, tab2, tab3, tab4 = st.tabs([

    "Baseline Models",

    "Cross-Validation",

    "Hyperparameter Tuning",

    "Final Model"
])


with tab1:

    st.subheader("Baseline Model Comparison")

    df = load_csv(
        RESULT_DIR / "model_performance.csv"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    metric = st.selectbox(
        "Select Evaluation Metric",

        [
            "Accuracy",
            "Precision",
            "Recall",
            "F1 Score",
            "ROC AUC"
        ]
    )

    fig = px.bar(
        df,
        x="Model",
        y=metric,
        color="Model",
        text_auto=".4f"
    )

    fig.update_yaxes(range=[0, 1.05])

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    show_figure("error_comparison.png")


with tab2:

    st.subheader("5-Fold Cross-Validation")

    show_report(
        "cross_validation_results.csv"
    )

    show_figure(
        "cross_validation_comparison.png"
    )

    show_figure(
        "fold_performance.png"
    )

    show_figure(
        "overfitting_comparison.png"
    )


with tab3:

    st.subheader("Hyperparameter Optimization")

    show_report(
        "hyperparameter_tuning_summary.csv"
    )

    show_report(
        "baseline_vs_tuned_comparison.csv"
    )

    col1, col2 = st.columns(2)

    with col1:

        show_figure(
            "baseline_vs_tuned_f1.png"
        )

    with col2:

        show_figure(
            "baseline_vs_tuned_recall.png"
        )

    show_figure(
        "baseline_vs_tuned_fn.png"
    )


with tab4:

    metadata = load_metadata()

    st.subheader(
        f"Selected Model: {metadata['model_name']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Accuracy",
        f"{metadata['accuracy']:.2%}"
    )

    col2.metric(
        "Precision",
        f"{metadata['precision']:.2%}"
    )

    col3.metric(
        "Recall",
        f"{metadata['recall']:.2%}"
    )

    col4.metric(
        "F1 Score",
        f"{metadata['f1_score']:.2%}"
    )

    col1, col2 = st.columns(2)

    with col1:

        show_figure(
            "final_confusion_matrix.png"
        )

    with col2:

        show_figure(
            "final_roc_curve.png"
        )

    st.subheader("Final Classification Report")

    show_report(
        "final_classification_report.csv"
    )

    st.subheader("Final Model Ranking")

    show_report(
        "final_model_ranking.csv"
    )

    st.subheader("Validation vs Test Performance")

    show_figure(
        "validation_vs_test.png"
    )

    st.subheader("Dataset Overlap")

    st.metric(
        "Overlapping Test Records",
        metadata["overlapping_test_records"]
    )

    show_report(
        "non_overlap_test_performance.csv"
    )