import pandas as pd

from sklearn.model_selection import (
    StratifiedGroupKFold,
    cross_validate
)

def perform_cross_validation(
    model,
    X,
    y,
    n_splits=5,
    random_state=42
):

    groups = pd.util.hash_pandas_object(
        X,
        index=False
    ).to_numpy()

    cv = StratifiedGroupKFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=random_state
    )

    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }

    scores = cross_validate(
        estimator=model,
        X=X,
        y=y,
        groups=groups,
        cv=cv,
        scoring=scoring,
        n_jobs=1,
        return_train_score=True,
        error_score="raise"
    )

    return scores