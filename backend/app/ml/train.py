import os
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score
from backend.app.ml.feature_engineering import FEATURE_COLUMNS

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "datasets")

def generate_training_data(n_samples: int = 3000) -> pd.DataFrame:
    """
    Generates realistic synthetic cybersecurity event feature distribution for training.
    """
    np.random.seed(42)
    
    # 1. Normal Traffic (65%)
    n_normal = int(n_samples * 0.65)
    normal_data = {
        "failed_login_count": np.random.poisson(lam=0.2, size=n_normal),
        "unique_source_ips": np.random.choice([1, 2], size=n_normal, p=[0.9, 0.1]),
        "request_count": np.random.randint(1, 15, size=n_normal),
        "connection_count": np.random.randint(1, 10, size=n_normal),
        "bytes_transferred": np.random.exponential(scale=5000, size=n_normal),
        "destination_count": np.random.randint(1, 4, size=n_normal),
        "login_success_after_failures": np.zeros(n_normal),
        "event_frequency_per_min": np.random.uniform(1.0, 10.0, size=n_normal),
        "unusual_time_indicator": np.random.choice([0, 1], size=n_normal, p=[0.92, 0.08]),
        "privileged_command_flag": np.random.choice([0, 1], size=n_normal, p=[0.98, 0.02]),
        "high_risk_port_flag": np.zeros(n_normal),
        "internal_to_external_flag": np.random.choice([0, 1], size=n_normal, p=[0.95, 0.05]),
        "attack_type": ["Normal"] * n_normal
    }
    
    # 2. Brute Force (12%)
    n_brute = int(n_samples * 0.12)
    brute_data = {
        "failed_login_count": np.random.randint(5, 50, size=n_brute),
        "unique_source_ips": np.random.choice([1, 2, 3], size=n_brute, p=[0.6, 0.3, 0.1]),
        "request_count": np.random.randint(20, 100, size=n_brute),
        "connection_count": np.random.randint(10, 60, size=n_brute),
        "bytes_transferred": np.random.uniform(500, 4000, size=n_brute),
        "destination_count": np.random.choice([1, 2], size=n_brute, p=[0.8, 0.2]),
        "login_success_after_failures": np.random.choice([0, 1], size=n_brute, p=[0.4, 0.6]),
        "event_frequency_per_min": np.random.uniform(30.0, 120.0, size=n_brute),
        "unusual_time_indicator": np.random.choice([0, 1], size=n_brute, p=[0.4, 0.6]),
        "privileged_command_flag": np.zeros(n_brute),
        "high_risk_port_flag": np.random.choice([0, 1], size=n_brute, p=[0.7, 0.3]),
        "internal_to_external_flag": np.zeros(n_brute),
        "attack_type": ["Brute Force"] * n_brute
    }
    
    # 3. Privilege Escalation (8%)
    n_priv = int(n_samples * 0.08)
    priv_data = {
        "failed_login_count": np.random.poisson(lam=1.0, size=n_priv),
        "unique_source_ips": np.random.choice([1, 2], size=n_priv, p=[0.8, 0.2]),
        "request_count": np.random.randint(5, 25, size=n_priv),
        "connection_count": np.random.randint(3, 15, size=n_priv),
        "bytes_transferred": np.random.uniform(1000, 20000, size=n_priv),
        "destination_count": np.random.randint(1, 3, size=n_priv),
        "login_success_after_failures": np.random.choice([0, 1], size=n_priv, p=[0.5, 0.5]),
        "event_frequency_per_min": np.random.uniform(5.0, 30.0, size=n_priv),
        "unusual_time_indicator": np.random.choice([0, 1], size=n_priv, p=[0.3, 0.7]),
        "privileged_command_flag": np.ones(n_priv),
        "high_risk_port_flag": np.random.choice([0, 1], size=n_priv, p=[0.5, 0.5]),
        "internal_to_external_flag": np.random.choice([0, 1], size=n_priv, p=[0.6, 0.4]),
        "attack_type": ["Privilege Escalation"] * n_priv
    }
    
    # 4. Data Exfiltration (8%)
    n_exfil = int(n_samples * 0.08)
    exfil_data = {
        "failed_login_count": np.random.poisson(lam=0.5, size=n_exfil),
        "unique_source_ips": np.random.choice([1, 2], size=n_exfil, p=[0.85, 0.15]),
        "request_count": np.random.randint(15, 60, size=n_exfil),
        "connection_count": np.random.randint(10, 40, size=n_exfil),
        "bytes_transferred": np.random.uniform(5_000_000, 150_000_000, size=n_exfil),
        "destination_count": np.random.randint(1, 5, size=n_exfil),
        "login_success_after_failures": np.random.choice([0, 1], size=n_exfil, p=[0.7, 0.3]),
        "event_frequency_per_min": np.random.uniform(10.0, 50.0, size=n_exfil),
        "unusual_time_indicator": np.random.choice([0, 1], size=n_exfil, p=[0.2, 0.8]),
        "privileged_command_flag": np.random.choice([0, 1], size=n_exfil, p=[0.6, 0.4]),
        "high_risk_port_flag": np.random.choice([0, 1], size=n_exfil, p=[0.4, 0.6]),
        "internal_to_external_flag": np.ones(n_exfil),
        "attack_type": ["Data Exfiltration"] * n_exfil
    }
    
    # 5. Lateral Movement (7%)
    n_lat = n_samples - n_normal - n_brute - n_priv - n_exfil
    lat_data = {
        "failed_login_count": np.random.poisson(lam=1.5, size=n_lat),
        "unique_source_ips": np.random.randint(2, 6, size=n_lat),
        "request_count": np.random.randint(20, 70, size=n_lat),
        "connection_count": np.random.randint(15, 50, size=n_lat),
        "bytes_transferred": np.random.uniform(10000, 500000, size=n_lat),
        "destination_count": np.random.randint(4, 12, size=n_lat),
        "login_success_after_failures": np.random.choice([0, 1], size=n_lat, p=[0.4, 0.6]),
        "event_frequency_per_min": np.random.uniform(15.0, 60.0, size=n_lat),
        "unusual_time_indicator": np.random.choice([0, 1], size=n_lat, p=[0.3, 0.7]),
        "privileged_command_flag": np.random.choice([0, 1], size=n_lat, p=[0.5, 0.5]),
        "high_risk_port_flag": np.random.choice([0, 1], size=n_lat, p=[0.3, 0.7]),
        "internal_to_external_flag": np.random.choice([0, 1], size=n_lat, p=[0.8, 0.2]),
        "attack_type": ["Lateral Movement"] * n_lat
    }
    
    dfs = [pd.DataFrame(d) for d in [normal_data, brute_data, priv_data, exfil_data, lat_data]]
    dataset = pd.concat(dfs, ignore_index=True)
    return dataset.sample(frac=1.0, random_state=42).reset_index(drop=True)

def train_and_save_models():
    print("[*] Generating training dataset for CyberGuard AI ML Engine...")
    df = generate_training_data(n_samples=4000)
    
    os.makedirs(DATASETS_DIR, exist_ok=True)
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    csv_path = os.path.join(DATASETS_DIR, "security_events_training.csv")
    df.to_csv(csv_path, index=False)
    print(f"[+] Saved training dataset to {csv_path}")
    
    X = np.array(df[FEATURE_COLUMNS].values, dtype=np.float64)
    y = np.array(df["attack_type"].values, dtype=str)
    
    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)
    
    # 1. Train Random Forest Classifier
    print("[*] Training Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=120, max_depth=12, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    print(f"[+] Random Forest Accuracy: {acc * 100:.2f}% | F1 Score: {f1:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # 2. Train Isolation Forest for Anomaly Detection
    print("[*] Training Isolation Forest for Anomaly Detection...")
    # Train anomaly detector primarily on baseline normal data
    X_normal_scaled = scaler.transform(df[df["attack_type"] == "Normal"][FEATURE_COLUMNS].values)
    iso_forest = IsolationForest(n_estimators=100, contamination=0.08, random_state=42, n_jobs=-1)
    iso_forest.fit(X_normal_scaled)
    
    # Save artifacts
    joblib.dump(rf_model, os.path.join(MODELS_DIR, "rf_classifier.joblib"))
    joblib.dump(iso_forest, os.path.join(MODELS_DIR, "iso_forest.joblib"))
    joblib.dump(scaler, os.path.join(MODELS_DIR, "feature_scaler.joblib"))
    
    print("[+] All ML models successfully trained and serialized to backend/app/ml/models/")

if __name__ == "__main__":
    train_and_save_models()
