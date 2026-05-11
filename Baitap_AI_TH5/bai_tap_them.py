import pandas as pd

# 1. Đọc dữ liệu từ bảng bạn vừa tạo
df = pd.read_csv('du_lieu_cong_ty.csv')

# 2. Tính toán thêm các chỉ số thông minh
# Ví dụ: Tính tỷ lệ lợi nhuận trên doanh thu
df['Ty_le_loi_nhuan'] = (df['Loi nhuan'] / df['Doanh thu']) * 100

# 3. Lọc ra các công ty có hiệu suất "Xuất sắc" hoặc "Tốt"
hieu_suat_cao = df[df['Danh gia hieu suat'].isin(['Xuất sắc', 'Tốt'])]

print("--- Danh sách các công ty có hiệu suất cao ---")
print(hieu_suat_cao[['Cong ty', 'Doanh thu', 'Loi nhuan', 'Danh gia hieu suat']])

# 4. Thống kê cơ bản
print("\n--- Thống kê chung về lợi nhuận ---")
print(df['Loi nhuan'].describe())