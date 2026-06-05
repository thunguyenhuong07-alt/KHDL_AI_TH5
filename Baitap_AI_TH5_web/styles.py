CSS_STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid rgba(48,54,61,0.8);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 { color: #58a6ff !important; }
.metric-card {
    background: linear-gradient(135deg, rgba(30,40,60,0.8), rgba(20,30,50,0.9));
    border: 1px solid rgba(88,166,255,0.2);
    border-radius: 16px; padding: 24px; text-align: center;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
.metric-card:hover {
    border-color: rgba(88,166,255,0.5);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(88,166,255,0.15);
}
.metric-value { font-size: 2.2rem; font-weight: 800; color: #58a6ff; margin: 8px 0; }
.metric-label { font-size: 0.85rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.metric-delta { font-size: 0.9rem; margin-top: 4px; }
.section-header {
    background: linear-gradient(90deg, rgba(88,166,255,0.1), transparent);
    border-left: 4px solid #58a6ff;
    padding: 12px 20px; margin: 20px 0 16px;
    border-radius: 0 8px 8px 0;
}
.section-header h3 { color: #e6edf3 !important; margin: 0; font-weight: 600; }
.result-box {
    border-radius: 16px; padding: 24px; text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
}
.result-normal {
    background: linear-gradient(135deg, rgba(35,134,54,0.2), rgba(35,134,54,0.05));
    border: 1px solid rgba(35,134,54,0.4);
}
.result-anomaly {
    background: linear-gradient(135deg, rgba(210,153,34,0.2), rgba(210,153,34,0.05));
    border: 1px solid rgba(210,153,34,0.4);
}
.result-highrisk {
    background: linear-gradient(135deg, rgba(248,81,73,0.2), rgba(248,81,73,0.05));
    border: 1px solid rgba(248,81,73,0.4);
}
.compare-table {
    background: rgba(22,27,34,0.8); border-radius: 12px;
    border: 1px solid rgba(48,54,61,0.8); overflow: hidden;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    background: rgba(22,27,34,0.6); border-radius: 8px 8px 0 0;
    border: 1px solid rgba(48,54,61,0.5); color: #8b949e;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: rgba(88,166,255,0.15) !important;
    border-color: #58a6ff !important; color: #58a6ff !important;
}
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,40,60,0.7), rgba(20,30,50,0.8));
    border: 1px solid rgba(88,166,255,0.15);
    border-radius: 12px; padding: 16px;
}
h1, h2, h3 { color: #e6edf3 !important; }
.stButton > button {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 10px 24px !important;
    font-weight: 600 !important; transition: all 0.3s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 4px 20px rgba(46,160,67,0.4) !important;
    transform: translateY(-1px) !important;
}
</style>
"""

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e6edf3', family='Inter'),
    margin=dict(l=40,r=40,t=50,b=40),
    legend=dict(bgcolor='rgba(22,27,34,0.8)', bordercolor='rgba(48,54,61,0.5)', borderwidth=1),
    xaxis=dict(gridcolor='rgba(48,54,61,0.4)', zerolinecolor='rgba(48,54,61,0.6)'),
    yaxis=dict(gridcolor='rgba(48,54,61,0.4)', zerolinecolor='rgba(48,54,61,0.6)')
)

COLORS = {'Normal':'#238636','Anomaly':'#d29922','High Risk':'#f85149'}
MODEL_COLORS = {'Random Forest':'#58a6ff','Logistic Regression':'#bc8cff','XGBoost':'#f78166'}