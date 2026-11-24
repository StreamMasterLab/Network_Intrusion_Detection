import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


def clean_data(df):
    df = df.copy()

    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.drop(
        columns=["id", "attack_cat"],
        errors="ignore"
    )

    return df


def separate_features(df):
    X = df.drop(columns=["label"])
    y = df["label"]

    return X, y


def create_preprocessor(X, scale=True):

    numerical_features = X.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_features = X.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    numerical_steps = [
        ("imputer", SimpleImputer(strategy="median"))
    ]

    if scale:
        numerical_steps.append(
            ("scaler", StandardScaler())
        )

    numerical_pipeline = Pipeline(numerical_steps)

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(
            strategy="most_frequent"
        )),

        ("encoder", OneHotEncoder(
            handle_unknown="ignore",
            sparse_output=True
        ))
    ])

    preprocessor = ColumnTransformer([
        ("num", numerical_pipeline, numerical_features),
        ("cat", categorical_pipeline, categorical_features)
    ])

    return preprocessor