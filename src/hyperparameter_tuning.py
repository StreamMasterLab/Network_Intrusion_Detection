import pandas as pd

from sklearn.model_selection import (
    GridSearchCV,
    StratifiedGroupKFold
)


def tune_model(
    model,
    param_grid,
    X_train,
    y_train,
    n_splits=5,
    random_state=42
):

    groups = pd.util.hash_pandas_object(
        X_train,
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

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring=scoring,
        refit="f1",
        cv=cv,
        n_jobs=1,
        verbose=2,
        return_train_score=True,
        error_score="raise"
    )

    grid_search.fit(
        X_train,
        y_train,
        groups=groups
    )

    return grid_search