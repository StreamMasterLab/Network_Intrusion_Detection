from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from src.preprocessing import create_preprocessor


def create_models(X_train, random_state=42):

    models = {

        "Logistic Regression": Pipeline([
            ("preprocessor",
             create_preprocessor(X_train, scale=True)),

            ("classifier", LogisticRegression(
                max_iter=2000,
                random_state=random_state
            ))
        ]),

        "Decision Tree": Pipeline([
            ("preprocessor",
             create_preprocessor(X_train, scale=False)),

            ("classifier", DecisionTreeClassifier(
                criterion="gini",
                random_state=random_state
            ))
        ]),

        "Random Forest": Pipeline([
            ("preprocessor",
             create_preprocessor(X_train, scale=False)),

            ("classifier", RandomForestClassifier(
                n_estimators=100,
                random_state=random_state,
                n_jobs=-1
            ))
        ])
    }

    return models