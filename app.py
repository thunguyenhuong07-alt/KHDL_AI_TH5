import streamlit as st
import pandas as pd
from groq import Groq
import time

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI Survey Analyzer - Groq Edition", layout="wide")

with st.sidebar:
    st.title("⚙️ Cấu hình Groq Cloud")
    # Link hướng dẫn lấy Key: https://console.groq.com/keys
    api_key = st.text_input("Nhập Groq API Key:", type="password")
    model_option = st.selectbox(
        "Chọn Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
    )
    
    if api_key:
        try:
            client = Groq(api_key=api_key)
            st.success("✅ Kết nối Groq thành công!")
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")

st.title("🚀 Phân tích Insight Khảo sát (Tốc độ cao với Groq)")

# 2. Tải file dữ liệu
uploaded_file = st.file_uploader("Tải lên file Baitap_AI_TH4.xlsx", type=["xlsx"])

if uploaded_file and api_key:
    df = pd.read_excel(uploaded_file)
    
    # Tự động nhận diện cột
    cluster_col = "Cluster" if "Cluster" in df.columns else df.columns[0]
    content_col = "Content" if "Content" in df.columns else df.columns[1]

    if st.button("📊 Bắt đầu phân tích toàn bộ các Nhóm"):
        clusters = sorted([c for c in df[cluster_col].unique() if pd.notna(c)])
        
        progress_bar = st.progress(0)
        
        for index, cluster in enumerate(clusters):
            # Lọc dữ liệu thực tế
            valid_data = df[(df[cluster_col] == cluster) & (df[content_col].notna())][content_col].astype(str).tolist()
            
            if not valid_data:
                continue

            # Gom nội dung để phân tích
            text_block = "\n- ".join(valid_data[:20]) # Groq xử lý được nhiều dữ liệu hơn

            prompt = f"""
            Bạn là một chuyên gia phân tích dữ liệu. Hãy tóm tắt nội dung sau cho Nhóm {cluster}:
            1. Đặt tên chủ đề ngắn gọn cho nhóm này.
            2. Viết 2-3 câu tóm tắt insight chính.
            3. Trích dẫn 2 câu phản hồi ấn tượng nhất.
            
            Dữ liệu:
            {text_block}
            """

            with st.expander(f"📍 Kết quả Nhóm {cluster}", expanded=True):
                try:
                    # Gọi Groq API
                    chat_completion = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model=model_option,
                    )
                    st.markdown(chat_completion.choices[0].message.content)
                    
                    # Groq rất nhanh, chỉ cần nghỉ 1-2 giây là đủ (hoặc không cần)
                    time.sleep(1) 
                except Exception as e:
                    st.error(f"Lỗi tại nhóm {cluster}: {e}")
                    break
            
            progress_bar.progress((index + 1) / len(clusters))
        
        st.balloons()
        st.success("🎉 Hoàn thành! Tốc độ xử lý của Groq thật ấn tượng phải không?")

else:
    st.info("💡 Hãy nhập API Key từ Groq Cloud và tải file Excel lên để bắt đầu.")