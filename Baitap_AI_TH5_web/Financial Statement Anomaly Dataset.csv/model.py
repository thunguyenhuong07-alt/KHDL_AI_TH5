import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
# pyrefly: ignore [missing-import]
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
import warnings
warnings.filterwarnings('ignore')

FEATURE_COLS = ['Total_Assets','Total_Liabilities','Revenue','Operating_Expenses',
    'Net_Income','Cash_Flow_Operating','Cash_Flow_Investing','Cash_Flow_Financing',
    'Current_Ratio','Debt_to_Equity','Gross_Margin','Return_on_Assets','Return_on_Equity']

VN_NAMES = {
    'Total_Assets':'Tổng tài sản','Total_Liabilities':'Tổng nợ phải trả',
    'Revenue':'Doanh thu','Operating_Expenses':'Chi phí hoạt động',
    'Net_Income':'Lợi nhuận ròng','Cash_Flow_Operating':'Dòng tiền hoạt động',
    'Cash_Flow_Investing':'Dòng tiền đầu tư','Cash_Flow_Financing':'Dòng tiền tài chính',
    'Current_Ratio':'Tỷ số thanh toán hiện hành','Debt_to_Equity':'Tỷ lệ nợ/vốn',
    'Gross_Margin':'Biên lợi nhuận gộp','Return_on_Assets':'ROA',
    'Return_on_Equity':'ROE'
}

STATUS_MAP = {'Normal':0, 'Anomaly':1, 'High Risk':2}
STATUS_LABELS = ['Normal','Anomaly','High Risk']

def load_data(path='Financial Statement Anomaly Dataset.csv'):
    df = pd.read_csv(path)
    return df

def prepare_data(df, test_size=0.2, random_state=42):
    X = df[FEATURE_COLS]
    y = df['Financial_Status'].map(STATUS_MAP)
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)

def get_models():
    return {
        'Random Forest': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, class_weight='balanced'),
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial', class_weight='balanced'),
        'XGBoost': XGBClassifier(n_estimators=200, max_depth=8, learning_rate=0.1, random_state=42, eval_metric='mlogloss', use_label_encoder=False)
    }

def train_and_evaluate(X_train, X_test, y_train, y_test):
    models = get_models()
    results = {}
    trained = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1': f1_score(y_test, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_pred': y_pred, 'y_proba': y_proba,
            'report': classification_report(y_test, y_pred, target_names=STATUS_LABELS, output_dict=True)
        }
        results[name] = metrics
        trained[name] = model
    return results, trained

def get_feature_importance(model, name):
    if name == 'Random Forest':
        return model.feature_importances_
    elif name == 'XGBoost':
        return model.feature_importances_
    elif name == 'Logistic Regression':
        return np.mean(np.abs(model.coef_), axis=0)
    return None

def compute_roc_curves(results, y_test):
    y_bin = label_binarize(y_test, classes=[0,1,2])
    roc_data = {}
    for name, res in results.items():
        fpr, tpr, roc_auc_val = {}, {}, {}
        for i in range(3):
            fpr[i], tpr[i], _ = roc_curve(y_bin[:,i], res['y_proba'][:,i])
            roc_auc_val[i] = auc(fpr[i], tpr[i])
        roc_data[name] = {'fpr':fpr,'tpr':tpr,'auc':roc_auc_val}
    return roc_data