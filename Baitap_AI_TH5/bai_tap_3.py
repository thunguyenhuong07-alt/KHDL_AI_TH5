# --- BÀI 1: TÍNH GIAI THỪA ---
def tinh_giai_thua(n):
    ket_qua = 1
    for i in range(1, n + 1): # Chạy từ 1 đến n
        ket_qua = ket_qua * i
    return ket_qua

so_can_tinh = 5
print("Kết quả giai thừa của 5 là:", tinh_giai_thua(so_can_tinh))
# --- BÀI 2: TÍNH TRUNG BÌNH ---
day_so = [10, 20, 30, 40, 50] # Một danh sách các số

def tinh_trung_binh(danh_sach):
    tong = sum(danh_sach)        # Cộng tất cả các số lại
    so_luong = len(danh_sach)    # Đếm xem có bao nhiêu số
    return tong / so_luong

print("Giá trị trung bình của dãy số là:", tinh_trung_binh(day_so))
# --- BÀI 3: TÍNH LỢI NHUẬN ---
tien_goc = 100000000  # 100 triệu
lai_suat = 0.005      # 0.5% mỗi tháng

def tinh_lai_kep(goc, lai):
    # Công thức: Tiền cuối cùng = Gốc * (1 + Lãi)^12 tháng
    tien_cuoi = goc * (1 + lai)**12
    loi_nhuan = tien_cuoi - goc
    return tien_cuoi, loi_nhuan

tong_tien, loi_nhuan_rong = tinh_lai_kep(tien_goc, lai_suat)
print(f"Tổng tiền nhận được: {tong_tien:,.0f} VNĐ")
print(f"Tiền lãi thu về: {loi_nhuan_rong:,.0f} VNĐ")