import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from models import (load_data, prepare_data, train_and_evaluate,
    get_feature_importance, compute_roc_curves, FEATURE_COLS, VN_NAMES, STATUS_LABELS, STATUS_MAP)
from styles import CSS_STYLE, PLOTLY_LAYOUT, COLORS, MODEL_COLORS

st.set_page_config(page_title="Phát hiện Gian lận BCTC", page_icon="🛡️", layout="wide")
st.markdown(CSS_STYLE, unsafe_allow_html=True)

def metric_card(label, value, icon="📊", delta=None, delta_color="green"):
    d = ""
    if delta:
        c = "#238636" if delta_color == "green" else "#f85149"
        d = f'<div class="metric-delta" style="color:{c}">{delta}</div>'
    st.markdown(f'''<div class="metric-card">
        <div style="font-size:1.5rem">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>{d}
    </div>''', unsafe_allow_html=True)

def section_header(title):
    st.markdown(f'<div class="section-header"><h3>{title}</h3></div>', unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def run_training(test_size):
    df = get_data()
    X_train, X_test, y_train, y_test = prepare_data(df, test_size=test_size)
    results, trained = train_and_evaluate(X_train, X_test, y_train, y_test)
    roc_data = compute_roc_curves(results, y_test)
    return results, trained, roc_data, X_test, y_test

# =================== SIDEBAR ===================
with st.sidebar:
    st.markdown("## 🛡️ KIỂM TOÁN AI")
    st.markdown("##### Phát hiện Gian lận Báo cáo Tài chính")
    st.markdown("---")
    page = st.radio("📌 Điều hướng", ["🏠 Tổng quan", "📊 Phân tích dữ liệu",
        "🤖 Huấn luyện & So sánh", "🔍 Dự đoán"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("##### ⚙️ Cấu hình")
    test_size = st.slider("Tỷ lệ test", 0.1, 0.4, 0.2, 0.05)
    st.markdown("---")
    st.markdown("""<div style='text-align:center;color:#8b949e;font-size:0.75rem'>
    <p>🎓 Bài tập lớn</p><p>Môi trường: Anaconda Python 3.9</p>
    <p>© 2026 Kiểm Toán AI</p></div>""", unsafe_allow_html=True)

df = get_data()

# =================== TRANG 1: TỔNG QUAN ===================
if page == "🏠 Tổng quan":
    st.markdown("# 🛡️ Hệ thống Phát hiện Gian lận Báo cáo Tài chính")
    st.markdown("> *Phân tích các khoản mục trên BCTC để đánh giá rủi ro và độ tin cậy bằng AI*")
    st.markdown("")

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Tổng mẫu", f"{len(df):,}", "📁")
    with c2: metric_card("Bình thường", f"{(df['Financial_Status']=='Normal').sum():,}", "✅", 
             f"{(df['Financial_Status']=='Normal').mean()*100:.1f}%")
    with c3: metric_card("Bất thường", f"{(df['Financial_Status']=='Anomaly').sum():,}", "⚠️",
             f"{(df['Financial_Status']=='Anomaly').mean()*100:.1f}%", "red")
    with c4: metric_card("Rủi ro cao", f"{(df['Financial_Status']=='High Risk').sum():,}", "🚨",
             f"{(df['Financial_Status']=='High Risk').mean()*100:.1f}%", "red")

    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        section_header("📊 Phân bố trạng thái tài chính")
        vc = df['Financial_Status'].value_counts()
        fig = go.Figure(go.Pie(labels=vc.index, values=vc.values,
            hole=0.55, marker=dict(colors=[COLORS[l] for l in vc.index]),
            textinfo='label+percent', textfont=dict(size=13)))
        fig.update_layout(**PLOTLY_LAYOUT, height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        section_header("📈 Thống kê các chỉ số tài chính")
        stats = df[FEATURE_COLS].describe().T[['mean','std','min','max']]
        stats.index = [VN_NAMES.get(c,c) for c in stats.index]
        stats.columns = ['Trung bình','Độ lệch chuẩn','Nhỏ nhất','Lớn nhất']
        st.dataframe(stats.style.format("{:.4f}").background_gradient(cmap='Blues'),
            height=400, use_container_width=True)

    section_header("🔥 Ma trận tương quan giữa các chỉ số")
    corr = df[FEATURE_COLS].corr()
    fig = go.Figure(go.Heatmap(z=corr.values, x=[VN_NAMES.get(c,c) for c in corr.columns],
        y=[VN_NAMES.get(c,c) for c in corr.index], colorscale='RdBu_r', zmid=0,
        text=np.round(corr.values,2), texttemplate='%{text}', textfont=dict(size=9)))
    fig.update_layout(**PLOTLY_LAYOUT, height=550)
    st.plotly_chart(fig, use_container_width=True)

# =================== TRANG 2: PHÂN TÍCH DỮ LIỆU ===================
elif page == "📊 Phân tích dữ liệu":
    st.markdown("# 📊 Phân tích Khám phá Dữ liệu (EDA)")
    st.markdown("> *So sánh phân bố các chỉ số tài chính giữa các nhóm trạng thái*")

    section_header("📦 Biểu đồ Box Plot - So sánh theo nhóm")
    sel_features = st.multiselect("Chọn chỉ số", FEATURE_COLS,
        default=FEATURE_COLS[:4], format_func=lambda x: VN_NAMES.get(x,x))

    if sel_features:
        cols = st.columns(2)
        for i, feat in enumerate(sel_features):
            with cols[i % 2]:
                fig = px.box(df, x='Financial_Status', y=feat, color='Financial_Status',
                    color_discrete_map=COLORS, title=VN_NAMES.get(feat,feat))
                fig.update_layout(**PLOTLY_LAYOUT, height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

    section_header("📊 Phân bố chỉ số theo trạng thái")
    feat_hist = st.selectbox("Chọn chỉ số để xem phân bố",FEATURE_COLS,
        format_func=lambda x:VN_NAMES.get(x,x))
    fig = px.histogram(df, x=feat_hist, color='Financial_Status', barmode='overlay',
        color_discrete_map=COLORS, nbins=40, opacity=0.7, title=f"Phân bố {VN_NAMES.get(feat_hist,feat_hist)}")
    fig.update_layout(**PLOTLY_LAYOUT, height=400)
    st.plotly_chart(fig, use_container_width=True)

    section_header("🔵 Scatter Plot tương tác")
    sc1, sc2 = st.columns(2)
    with sc1:
        sx = st.selectbox("Trục X", FEATURE_COLS, index=0, format_func=lambda x:VN_NAMES.get(x,x))
    with sc2:
        sy = st.selectbox("Trục Y", FEATURE_COLS, index=min(4, len(FEATURE_COLS)-1), format_func=lambda x:VN_NAMES.get(x,x))
    fig = px.scatter(df, x=sx, y=sy, color='Financial_Status', color_discrete_map=COLORS,
        opacity=0.6, title=f"{VN_NAMES.get(sx,sx)} vs {VN_NAMES.get(sy,sy)}")
    fig.update_layout(**PLOTLY_LAYOUT, height=500)
    st.plotly_chart(fig, use_container_width=True)

# =================== TRANG 3: HUẤN LUYỆN & SO SÁNH ===================
elif page == "🤖 Huấn luyện & So sánh":
    st.markdown("# 🤖 Huấn luyện & So sánh Mô hình")
    st.markdown("> *So sánh 3 mô hình AI phát hiện gian lận: Random Forest, Logistic Regression, XGBoost*")

    if st.button("🚀 Huấn luyện mô hình", use_container_width=True):
        st.session_state['trained'] = True

    if st.session_state.get('trained'):
        with st.spinner("⏳ Đang huấn luyện 3 mô hình..."):
            results, trained_models, roc_data, X_test, y_test = run_training(test_size)
            st.session_state['models'] = trained_models
            st.session_state['results'] = results

        st.success("✅ Huấn luyện hoàn tất!")
        st.markdown("")

        # Bảng so sánh
        section_header("📋 Bảng so sánh hiệu suất 3 mô hình")
        comp_data = []
        for name, res in results.items():
            comp_data.append({
                'Mô hình': name,
                'Accuracy': f"{res['accuracy']*100:.2f}%",
                'Precision': f"{res['precision']*100:.2f}%",
                'Recall': f"{res['recall']*100:.2f}%",
                'F1-Score': f"{res['f1']*100:.2f}%"
            })
        st.dataframe(pd.DataFrame(comp_data).set_index('Mô hình'),use_container_width=True)

        # Bar chart so sánh
        section_header("📊 Biểu đồ so sánh Metrics")
        metrics_names = ['Accuracy','Precision','Recall','F1-Score']
        fig = go.Figure()
        for name, res in results.items():
            vals = [res['accuracy'], res['precision'], res['recall'], res['f1']]
            fig.add_trace(go.Bar(name=name, x=metrics_names, y=vals,
                marker_color=MODEL_COLORS[name], text=[f"{v*100:.1f}%" for v in vals], textposition='outside'))
        layout_no_y = {k:v for k,v in PLOTLY_LAYOUT.items() if k != 'yaxis'}
        fig.update_layout(**layout_no_y, barmode='group', height=450, title="So sánh hiệu suất 3 mô hình",
            yaxis=dict(range=[0,1.15], gridcolor='rgba(48,54,61,0.4)'))
        st.plotly_chart(fig, use_container_width=True)

        # Confusion Matrix + ROC
        section_header("🎯 Confusion Matrix & ROC Curve")
        tab1, tab2 = st.tabs(["📊 Confusion Matrix", "📈 ROC Curve"])

        with tab1:
            cols = st.columns(3)
            for idx, (name, res) in enumerate(results.items()):
                with cols[idx]:
                    cm = res['confusion_matrix']
                    fig = go.Figure(go.Heatmap(z=cm, x=STATUS_LABELS, y=STATUS_LABELS,
                        colorscale='Blues', text=cm, texttemplate='%{text}', textfont=dict(size=14)))
                    fig.update_layout(**PLOTLY_LAYOUT, height=350, title=name,
                        xaxis_title="Dự đoán", yaxis_title="Thực tế")
                    st.plotly_chart(fig, use_container_width=True)

        with tab2:
            fig = go.Figure()
            for name, rd in roc_data.items():
                for i, label in enumerate(STATUS_LABELS):
                    fig.add_trace(go.Scatter(x=rd['fpr'][i], y=rd['tpr'][i], mode='lines',
                        name=f"{name} - {label} (AUC={rd['auc'][i]:.3f})",
                        line=dict(color=MODEL_COLORS[name], dash=['solid','dash','dot'][i])))
            fig.add_trace(go.Scatter(x=[0,1],y=[0,1],mode='lines',
                line=dict(color='gray',dash='dash'),name='Random',showlegend=False))
            fig.update_layout(**PLOTLY_LAYOUT, height=500, title="ROC Curve - So sánh 3 mô hình",
                xaxis_title="False Positive Rate", yaxis_title="True Positive Rate")
            st.plotly_chart(fig, use_container_width=True)

        # Feature Importance
        section_header("🏆 Mức độ quan trọng của các chỉ số")
        cols = st.columns(3)
        for idx, (name, model) in enumerate(trained_models.items()):
            with cols[idx]:
                imp = get_feature_importance(model, name)
                if imp is not None:
                    imp_df = pd.DataFrame({'Feature':[VN_NAMES.get(f,f) for f in FEATURE_COLS],
                        'Importance':imp}).sort_values('Importance',ascending=True)
                    fig = go.Figure(go.Bar(x=imp_df['Importance'], y=imp_df['Feature'],
                        orientation='h', marker_color=MODEL_COLORS[name]))
                    fig.update_layout(**PLOTLY_LAYOUT, height=400, title=name)
                    st.plotly_chart(fig, use_container_width=True)

# =================== TRANG 4: DỰ ĐOÁN ===================
elif page == "🔍 Dự đoán":
    st.markdown("# 🔍 Dự đoán Rủi ro Báo cáo Tài chính")
    st.markdown("> *Nhập các chỉ số tài chính để đánh giá mức độ rủi ro*")

    if not st.session_state.get('models'):
        st.warning("⚠️ Vui lòng huấn luyện mô hình trước tại trang **🤖 Huấn luyện & So sánh**")
    else:
        trained_models = st.session_state['models']
        section_header("📝 Nhập thông tin báo cáo tài chính")

        cols = st.columns(3)
        inputs = {}
        for i, feat in enumerate(FEATURE_COLS):
            with cols[i % 3]:
                inputs[feat] = st.number_input(VN_NAMES.get(feat,feat),
                    value=0.0, step=0.01, format="%.4f", key=feat)

        st.markdown("")
        sel_model = st.selectbox("🤖 Chọn mô hình dự đoán", list(trained_models.keys()))

        if st.button("🔍 Phân tích & Dự đoán", use_container_width=True):
            model = trained_models[sel_model]
            X_input = pd.DataFrame([inputs])
            pred = model.predict(X_input)[0]
            proba = model.predict_proba(X_input)[0]
            label = STATUS_LABELS[pred]

            st.markdown("")
            section_header("📋 Kết quả phân tích")

            css_class = {'Normal':'result-normal','Anomaly':'result-anomaly','High Risk':'result-highrisk'}[label]
            icon = {'Normal':'✅','Anomaly':'⚠️','High Risk':'🚨'}[label]
            vn_label = {'Normal':'Bình thường','Anomaly':'Bất thường - Nghi ngờ gian lận','High Risk':'Rủi ro cao - Cần kiểm tra ngay'}[label]
            color = COLORS[label]

            st.markdown(f'''<div class="result-box {css_class}">
                <div style="font-size:3rem">{icon}</div>
                <h2 style="color:{color} !important;margin:10px 0">{vn_label}</h2>
                <p style="color:#8b949e">Mô hình: {sel_model} | Độ tin cậy: {proba[pred]*100:.1f}%</p>
            </div>''', unsafe_allow_html=True)

            st.markdown("")
            pc1, pc2, pc3 = st.columns(3)
            with pc1: metric_card("Bình thường", f"{proba[0]*100:.1f}%", "✅")
            with pc2: metric_card("Bất thường", f"{proba[1]*100:.1f}%", "⚠️")
            with pc3: metric_card("Rủi ro cao", f"{proba[2]*100:.1f}%", "🚨")

            # Radar chart
            section_header("📡 Biểu đồ Radar - Chỉ số đầu vào")
            vals = list(inputs.values())
            fig = go.Figure(go.Scatterpolar(r=vals + [vals[0]],
                theta=[VN_NAMES.get(f,f) for f in FEATURE_COLS] + [VN_NAMES.get(FEATURE_COLS[0],FEATURE_COLS[0])],
                fill='toself', fillcolor=f'rgba(88,166,255,0.15)',
                line=dict(color='#58a6ff',width=2)))
            fig.update_layout(**PLOTLY_LAYOUT, height=450, polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(gridcolor='rgba(48,54,61,0.4)',linecolor='rgba(48,54,61,0.4)'),
                angularaxis=dict(gridcolor='rgba(48,54,61,0.4)',linecolor='rgba(48,54,61,0.4)')))
            st.plotly_chart(fig, use_container_width=True)