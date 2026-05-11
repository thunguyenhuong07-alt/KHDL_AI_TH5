import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Đọc dữ liệu từ file bạn đã giải nén
df = pd.read_csv('AIML Dataset.csv')

# 2. Xem thông tin cơ bản (EDA)
print("Thông tin bộ dữ liệu:")
print(df.info())
print("\nThống kê mô tả:")
print(df.describe())

# 3. Sử dụng Isolation Forest để gán nhãn gian lận
# Giả sử tỷ lệ gian lận dự kiến là 2% (0.02)
model = IsolationForest(contamination=0.02, random_state=42)
# Chọn các cột số để phân tích (ví dụ: amount, oldbalance, newbalance)
# Lưu ý: Thay đổi tên cột cho đúng với file .csv của bạn
features = df.select_dtypes(include=['float64', 'int64']).columns
df['anomaly'] = model.fit_predict(df[features])

# Nhãn -1 là bất thường (nghi ngờ gian lận)
anomalies = df[df['anomaly'] == -1]
print(f"\nSố lượng giao dịch nghi ngờ gian lận: {len(anomalies)}")

# 4. Trực quan hóa (Vẽ biểu đồ)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df.sample(1000), x=features[0], y=features[1], hue='anomaly', palette='coolwarm')
plt.title("Phân tích điểm bất thường trong giao dịch")
plt.show()