import os
import joblib
import numpy as np
from typing import Dict, Any, List, Tuple
from backend.app.ml.feature_engineering import extract_features_from_event

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

class MLPredictionService:
    def __init__(self):
        self.rf_model = None
        self.iso_forest = None
        self.scaler = None
        self.is_loaded = False
        self._load_models()

    def _load_models(self):
        try:
            rf_path = os.path.join(MODELS_DIR, "rf_classifier.joblib")
            if_path = os.path.join(MODELS_DIR, "iso_forest.joblib")
            scaler_path = os.path.join(MODELS_DIR, "feature_scaler.joblib")
            
            if os.path.exists(rf_path) and os.path.exists(if_path) and os.path.exists(scaler_path):
                self.rf_model = joblib.load(rf_path)
                self.iso_forest = joblib.load(if_path)
                self.scaler = joblib.load(scaler_path)
                self.is_loaded = True
            else:
                self.is_loaded = False
        except Exception as e:
            print(f"[-] Error loading ML models: {e}")
            self.is_loaded = False

    def predict_event(self, event: Dict[str, Any], history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Runs event features through Random Forest and Isolation Forest.
        Returns:
            - attack_type: "Normal" | "Brute Force" | "Privilege Escalation" | "Data Exfiltration" | "Lateral Movement"
            - confidence: float (0.0 to 1.0)
            - is_anomaly: bool
            - anomaly_score: float (0.0 to 1.0)
            - is_suspicious: bool
        """
        if not self.is_loaded:
            self._load_models()

        if not self.is_loaded:
            # Fallback heuristic if models unavailable
            return {
                "prediction": "Normal",
                "attack_type": "Normal",
                "confidence": 0.5,
                "is_anomaly": False,
                "anomaly_score": 0.1,
                "is_suspicious": False,
                "service_status": "MODELS_UNAVAILABLE"
            }

        # Extract features
        features = extract_features_from_event(event, history)
        features_scaled = self.scaler.transform(features)

        # 1. Random Forest prediction & probability
        rf_pred = self.rf_model.predict(features_scaled)[0]
        rf_proba = self.rf_model.predict_proba(features_scaled)[0]
        max_idx = np.argmax(rf_proba)
        confidence = float(rf_proba[max_idx])

        # 2. Isolation Forest anomaly scoring
        # score_samples returns negative anomaly score (lower means more anomalous)
        raw_score = self.iso_forest.score_samples(features_scaled)[0]
        # Normalize into 0.0 (very normal) to 1.0 (highly anomalous)
        # Typically raw_score is between -0.8 and 0.0
        normalized_anomaly_score = float(np.clip(1.0 - (raw_score + 0.7) / 0.7, 0.05, 0.99))
        
        is_anomaly = bool(self.iso_forest.predict(features_scaled)[0] == -1 or normalized_anomaly_score > 0.65)
        is_suspicious = bool(rf_pred != "Normal" or is_anomaly or confidence < 0.6)

        return {
            "prediction": "Suspicious" if is_suspicious else "Normal",
            "attack_type": rf_pred,
            "confidence": round(confidence, 4),
            "is_anomaly": is_anomaly,
            "anomaly_score": round(normalized_anomaly_score, 4),
            "is_suspicious": is_suspicious,
            "service_status": "ACTIVE"
        }

ml_service = MLPredictionService()
