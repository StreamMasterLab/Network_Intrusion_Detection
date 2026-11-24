import pandas as pd
import numpy as np
import joblib
import json

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR / "models" /
    "best_model_pipeline.pkl"
)

METADATA_PATH = (
    BASE_DIR / "reports" / "results" /
    "final_model_metadata.json"
)


class IntrusionPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        with open(METADATA_PATH, "r") as file:

            self.metadata = json.load(file)

        self.feature_names = self.metadata[
            "feature_names"
        ]

        self.numerical_features = self.metadata[
            "numerical_features"
        ]

        self.categorical_features = self.metadata[
            "categorical_features"
        ]

    def validate_input(self, data):

        if isinstance(data, dict):
            data = pd.DataFrame([data])

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "Input must be a dictionary or DataFrame."
            )

        if data.empty:
            raise ValueError("Input data is empty.")

        if data.columns.duplicated().any():
            raise ValueError("Duplicate columns found.")

        data = data.copy()

        missing_features = [
            feature
            for feature in self.feature_names
            if feature not in data.columns
        ]

        if missing_features:

            raise ValueError(
                f"Missing features: {missing_features}"
            )

        data = data[self.feature_names]

        for feature in self.numerical_features:

            data[feature] = pd.to_numeric(
                data[feature],
                errors="raise"
            )

        for feature in self.categorical_features:

            data[feature] = data[feature].map(
                lambda value: str(value).strip()
                if pd.notna(value)
                else np.nan
            )

        data = data.replace(
            [np.inf, -np.inf],
            np.nan
        )

        if data.isna().all(axis=1).any():
            raise ValueError("Completely empty record found.")

        return data

    @staticmethod
    def get_risk_level(probability):

        if probability < 0.20:
            return "Very Low"

        elif probability < 0.40:
            return "Low"

        elif probability < 0.60:
            return "Moderate"

        elif probability < 0.80:
            return "High"

        else:
            return "Critical"

    def predict(self, data):

        data = self.validate_input(data)

        predictions = self.model.predict(data)

        probabilities = self.model.predict_proba(data)

        malicious_index = list(
            self.model.classes_
        ).index(1)

        malicious_probabilities = probabilities[
            :, malicious_index
        ]

        results = pd.DataFrame({

            "Predicted Label": predictions,

            "Prediction": [
                "Malicious" if label == 1
                else "Normal"
                for label in predictions
            ],

            "Malicious Probability":
                malicious_probabilities,

            "Normal Probability":
                1 - malicious_probabilities,

            "Risk Level": [
                self.get_risk_level(probability)
                for probability in malicious_probabilities
            ]
        })

        return results

    def predict_csv(self, file):

        data = pd.read_csv(file)

        return self.predict(data)

    def get_model_info(self):

        return self.metadata