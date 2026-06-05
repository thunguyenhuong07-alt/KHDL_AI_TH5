import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    from sklearn.ensemble import GradientBoostingClassifier as XGBClassifier
    HAS_XGBOOST = False
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
import warnings
warnings.filterwarnings('ignore')

FEATURE_COLS = ['Amount', 'TransactionType_code', 'Location_code', 'Merchant_code']

VN_NAMES = {
    'Amount': 'Số tiền',
    'TransactionType_code': 'Loại giao dịch',
    'Location_code': 'Mã địa điểm',
    'Merchant_code': 'Mã cửa hàng'
}

STATUS_MAP = {'Normal': 0, 'Anomaly': 1, 'High Risk': 2}
STATUS_LABELS = ['Normal', 'Anomaly', 'High Risk']


def _create_labels(row):
    if row['TransactionType'] == 'Transfer' or row['Amount'] > 90000:
        return 'High Risk'
    if row['TransactionType'] == 'Withdrawal' or row['Amount'] > 50000:
        return 'Anomaly'
    return 'Normal'


def load_data():
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / 'Financial Statement Anomaly Dataset.csv' / 'financial_anomaly_data.csv'
    df = pd.read_csv(data_path)
    # Loại bỏ các hàng chứa giá trị thiếu trong các cột dùng cho huấn luyện
    df = df.dropna(subset=['Amount', 'TransactionType', 'Location', 'Merchant']).reset_index(drop=True)
    df['TransactionType_code'] = df['TransactionType'].astype('category').cat.codes
    df['Location_code'] = df['Location'].astype('category').cat.codes
    df['Merchant_code'] = df['Merchant'].astype('category').cat.codes
    df['Financial_Status'] = df.apply(_create_labels, axis=1)
    return df


def prepare_data(df, test_size=0.2, random_state=42):
    X = df[FEATURE_COLS]
    y = df['Financial_Status'].map(STATUS_MAP)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)


def get_models():
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, class_weight='balanced'),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
    }
    if HAS_XGBOOST:
        models['XGBoost'] = XGBClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42, eval_metric='mlogloss', use_label_encoder=False)
    else:
        models['Gradient Boosting'] = XGBClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42)
    return models


def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = get_models()
    results = {}
    trained = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_pred': y_pred,
            'y_proba': y_proba,
            'report': classification_report(y_test, y_pred, target_names=STATUS_LABELS, output_dict=True)
        }
        trained[name] = model
    return results, trained


def get_feature_importance(model, name):
    if name in ('Random Forest', 'XGBoost', 'Gradient Boosting'):
        return model.feature_importances_
    if name == 'Logistic Regression':
        return np.mean(np.abs(model.coef_), axis=0)
    return None


def compute_roc_curves(results, y_test):
    y_bin = label_binarize(y_test, classes=[0, 1, 2])
    roc_data = {}
    for name, res in results.items():
        fpr, tpr, roc_auc_val = {}, {}, {}
        for i in range(3):
            fpr[i], tpr[i], _ = roc_curve(y_bin[:, i], res['y_proba'][:, i])
            roc_auc_val[i] = auc(fpr[i], tpr[i])
        roc_data[name] = {'fpr': fpr, 'tpr': tpr, 'auc': roc_auc_val}
    return roc_data
