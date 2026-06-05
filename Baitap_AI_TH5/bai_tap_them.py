import pandas as pd
from pathlib import Path

# 1. Đọc dữ liệu từ bảng bạn vừa tạo
base_dir = Path(__file__).resolve().parent
csv_path = base_dir / 'du_lieu_cong_ty.csv'
df = pd.read_csv(csv_path)

# 2. Tính toán thêm các chỉ số thông minh
# Ví dụ: Tính tỷ lệ lợi nhuận trên doanh thu
df['Ty_le_loi_nhuan'] = (df['Loi nhuan'] / df['Doanh thu']) * 100

# 3. Lọc ra các công ty có hiệu suất "Xuat sac" hoặc "Tot"
# (Dữ liệu thực tế trong file dùng giá trị không dấu)
high_performance_labels = ['Xuat sac', 'Tot']
hieu_suat_cao = df[df['Danh gia hieu suat'].isin(high_performance_labels)]

print("--- Danh sách các công ty có hiệu suất cao ---")
if hieu_suat_cao.empty:
    print("Không có công ty nào có đánh giá hiệu suất cao trong dữ liệu.")
else:
    print(hieu_suat_cao[['Cong ty', 'Doanh thu', 'Loi nhuan', 'Danh gia hieu suat']])

# 4. Thống kê cơ bản
print("\n--- Thống kê chung về lợi nhuận ---")
print(df['Loi nhuan'].describe())