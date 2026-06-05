import io

import pandas as pd
import streamlit as st
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Phân tích dữ liệu gian lận bằng Isolation Forest")

@st.cache_data
def load_data():
    return pd.read_csv('AIML Dataset.csv')

# 1. Đọc dữ liệu từ file bạn đã giải nén
df = load_data()

# 2. Xem thông tin cơ bản (EDA)
st.subheader("Thông tin bộ dữ liệu")
info_buf = io.StringIO()
df.info(buf=info_buf)
st.text(info_buf.getvalue())

st.subheader("Thống kê mô tả")
st.write(df.describe())

st.subheader("Bảng mẫu dữ liệu")
st.write(df.head())

# 3. Sử dụng Isolation Forest để gán nhãn gian lận
# Giả sử tỷ lệ gian lận dự kiến là 2% (0.02)
model = IsolationForest(contamination=0.02, random_state=42)
# Chọn các cột số để phân tích
types = ['float64', 'int64']
features = df.select_dtypes(include=types).columns.tolist()

if len(features) < 2:
    st.error("Không tìm thấy đủ cột số để vẽ biểu đồ. Vui lòng kiểm tra lại dữ liệu.")
else:
    df['anomaly'] = model.fit_predict(df[features])
    anomalies = df[df['anomaly'] == -1]

    st.subheader("Kết quả phát hiện bất thường")
    st.write(f"Số lượng giao dịch nghi ngờ gian lận: {len(anomalies)}")
    st.write(anomalies.head(20))

    st.subheader("Trực quan hóa dữ liệu bất thường")
    fig, ax = plt.subplots(figsize=(10, 6))
    sample = df.sample(min(1000, len(df)), random_state=42)
    sns.scatterplot(data=sample, x=features[0], y=features[1], hue='anomaly', palette='coolwarm', ax=ax)
    ax.set_title("Phân tích điểm bất thường trong giao dịch")
    ax.legend(title='anomaly')
    st.pyplot(fig)
