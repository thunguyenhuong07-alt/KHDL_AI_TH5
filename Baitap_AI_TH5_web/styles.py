CSS_STYLE = """
<style>
    .metric-card {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 8px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #58a6ff;
        margin-top: 8px;
    }
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 600;
    }
    .section-header {
        padding: 12px 0;
        border-bottom: 2px solid #30363d;
        margin-bottom: 16px;
    }
    .section-header h3 {
        margin: 0;
        color: #58a6ff;
        font-size: 1.3rem;
    }
    .result-box {
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        border: 2px solid;
        margin: 20px 0;
    }
    .result-normal {
        background: rgba(63, 185, 80, 0.1);
        border-color: #3fb950;
    }
    .result-anomaly {
        background: rgba(229, 149, 0, 0.1);
        border-color: #d29922;
    }
    .result-highrisk {
        background: rgba(248, 81, 73, 0.1);
        border-color: #f85149;
    }
</style>
"""

PLOTLY_LAYOUT = {
    'template': 'plotly_dark',
    'font': {'family': 'Arial, sans-serif', 'size': 12, 'color': '#8b949e'},
    'plot_bgcolor': '#0d1117',
    'paper_bgcolor': '#0d1117',
    'margin': {'l': 60, 'r': 40, 't': 50, 'b': 50},
    'hovermode': 'closest',
    'xaxis': {'gridcolor': 'rgba(48,54,61,0.4)', 'linecolor': 'rgba(48,54,61,0.4)', 'showgrid': True},
    'yaxis': {'gridcolor': 'rgba(48,54,61,0.4)', 'linecolor': 'rgba(48,54,61,0.4)', 'showgrid': True},
}

COLORS = {
    'Normal': '#3fb950',
    'Anomaly': '#d29922',
    'High Risk': '#f85149'
}

MODEL_COLORS = {
    'Random Forest': '#58a6ff',
    'Logistic Regression': '#79c0ff',
    'XGBoost': '#a371f7',
    'Gradient Boosting': '#a371f7'
}
