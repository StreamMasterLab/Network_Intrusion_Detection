from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)


def evaluate_classifier(model, X, y):

    y_pred = model.predict(X)

    y_prob = model.predict_proba(X)[:, 1]

    tn, fp, fn, tp = confusion_matrix(
        y, y_pred, labels=[0, 1]
    ).ravel()

    return {
        "Accuracy": accuracy_score(y, y_pred),

        "Precision": precision_score(
            y, y_pred, zero_division=0
        ),

        "Recall": recall_score(
            y, y_pred, zero_division=0
        ),

        "F1 Score": f1_score(
            y, y_pred, zero_division=0
        ),

        "ROC AUC": roc_auc_score(y, y_prob),

        "True Negative": tn,

        "False Positive": fp,

        "False Negative": fn,

        "True Positive": tp,

        "False Negative Rate": fn / (fn + tp),

        "False Positive Rate": fp / (fp + tn)
    }