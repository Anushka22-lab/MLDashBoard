import streamlit as st
st.markdown("""
<style>
body {
    background-color: #0F172A;
}
.block-container {
    padding: 2rem;
}
</style>
""", unsafe_allow_html=True)

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Crimson Analytics · Wine Quality Intelligence",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — LUXURY WINE THEME
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500&family=Outfit:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-deep:       #080E1A;
    --bg-base:       #0F172A;
    --bg-card:       #141F33;
    --bg-elevated:   #1A2744;
    --wine-deep:     #4A0E20;
    --wine-mid:      #7B1E3A;
    --wine-bright:   #C0294E;
    --wine-glow:     #E11D48;
    --gold:          #C9A96E;
    --gold-dim:      #8B6F47;
    --text-primary:  #F8FAFC;
    --text-secondary:#94A3B8;
    --text-muted:    #475569;
    --border-subtle: rgba(123,30,58,0.2);
    --border-card:   rgba(123,30,58,0.15);
    --glow-wine:     rgba(225,29,72,0.15);
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background: var(--bg-base);
    color: var(--text-primary);
}

/* ── Main Background ── */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(123,30,58,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(74,14,32,0.15) 0%, transparent 55%),
        var(--bg-base);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--wine-mid); border-radius: 2px; }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(74,14,32,0.3) 0%, transparent 30%),
        var(--bg-deep) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

[data-testid="stSidebar"] .stRadio label {
    font-size: 0.875rem !important;
    font-weight: 400 !important;
    color: var(--text-secondary) !important;
    padding: 7px 2px !important;
    transition: color 0.2s, letter-spacing 0.2s;
    letter-spacing: 0.01em;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: var(--wine-glow) !important;
    letter-spacing: 0.03em;
}

/* ══════════════════════════════════════
   HERO HEADER
══════════════════════════════════════ */
.hero {
    text-align: center;
    padding: 52px 24px 44px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 600px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--wine-bright), var(--gold), var(--wine-bright), transparent);
}
.hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 50%; transform: translateX(-50%);
    width: 300px; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(123,30,58,0.4), transparent);
}
.hero-eyebrow {
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    font-weight: 400;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--gold-dim);
    margin-bottom: 16px;
}
.hero-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.6rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    line-height: 1.05;
    margin-bottom: 6px;
}
.hero-title em {
    font-style: italic;
    color: var(--wine-glow);
    font-weight: 300;
}
.hero-tagline {
    font-family: 'Outfit', sans-serif;
    font-size: 0.92rem;
    font-weight: 300;
    color: var(--text-muted);
    letter-spacing: 0.04em;
    margin-top: 10px;
}
.hero-ornament {
    font-size: 2.2rem;
    margin-bottom: 16px;
    display: block;
    filter: drop-shadow(0 0 20px rgba(225,29,72,0.4));
}

/* ══════════════════════════════════════
   SECTION HEADERS
══════════════════════════════════════ */
.section-header {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 28px;
    padding-bottom: 18px;
    border-bottom: 1px solid var(--border-card);
    position: relative;
}
.section-header::before {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 48px; height: 2px;
    background: linear-gradient(90deg, var(--wine-bright), var(--gold));
}
.section-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--wine-bright);
    margin-bottom: 4px;
}
.section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.75rem;
    font-weight: 500;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    margin: 0;
    line-height: 1.2;
}
.section-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    font-weight: 300;
    margin-top: 3px;
    letter-spacing: 0.02em;
}

/* ══════════════════════════════════════
   CARDS
══════════════════════════════════════ */
.wine-card {
    background: linear-gradient(145deg, var(--bg-card) 0%, rgba(20,31,51,0.8) 100%);
    border: 1px solid var(--border-card);
    border-radius: 16px;
    padding: 24px 26px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
}
.wine-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(201,169,110,0.2), transparent);
}
.wine-card:hover {
    border-color: rgba(123,30,58,0.35);
    transform: translateY(-1px);
}
.wine-card.accent {
    border-color: rgba(225,29,72,0.25);
    background: linear-gradient(145deg, rgba(123,30,58,0.12) 0%, var(--bg-card) 100%);
}

/* ══════════════════════════════════════
   METRIC CARDS
══════════════════════════════════════ */
.metric-card {
    background: linear-gradient(145deg, var(--bg-card), var(--bg-elevated));
    border: 1px solid var(--border-card);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 12px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s;
}
.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--wine-mid), var(--wine-bright));
    opacity: 0;
    transition: opacity 0.25s;
}
.metric-card:hover::after { opacity: 1; }
.metric-card:hover { border-color: var(--border-subtle); }
.metric-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.64rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    line-height: 1;
}
.metric-sub {
    font-size: 0.73rem;
    color: var(--text-muted);
    margin-top: 6px;
    font-weight: 300;
}
.metric-card.wine .metric-value { color: var(--wine-glow); }
.metric-card.gold .metric-value { color: var(--gold); }

/* ══════════════════════════════════════
   STEP BREADCRUMB
══════════════════════════════════════ */
.breadcrumb {
    display: flex;
    gap: 5px;
    margin-bottom: 28px;
    flex-wrap: wrap;
    align-items: center;
}
.bc-item {
    font-family: 'Fira Code', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.05);
    color: var(--text-muted);
    background: rgba(255,255,255,0.02);
}
.bc-item.active {
    background: linear-gradient(135deg, var(--wine-mid), var(--wine-bright));
    color: var(--text-primary);
    border-color: transparent;
    font-weight: 500;
}
.bc-item.done {
    background: rgba(201,169,110,0.08);
    color: var(--gold-dim);
    border-color: rgba(201,169,110,0.15);
}
.bc-sep {
    color: var(--text-muted);
    font-size: 0.6rem;
    opacity: 0.4;
}

/* ══════════════════════════════════════
   STATUS BADGES
══════════════════════════════════════ */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.06em;
}
.badge.ok   { background: rgba(16,185,129,0.08); color: #34d399; border: 1px solid rgba(16,185,129,0.15); }
.badge.warn { background: rgba(245,158,11,0.08); color: #fbbf24; border: 1px solid rgba(245,158,11,0.15); }
.badge.info { background: rgba(59,130,246,0.08); color: #60a5fa; border: 1px solid rgba(59,130,246,0.15); }
.badge.wine { background: rgba(225,29,72,0.08);  color: var(--wine-glow); border: 1px solid rgba(225,29,72,0.15); }

/* ══════════════════════════════════════
   FEATURE IMPORTANCE BARS
══════════════════════════════════════ */
.fi-wrap { margin-bottom: 13px; }
.fi-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    font-size: 0.8rem;
    color: var(--text-secondary);
    font-family: 'Fira Code', monospace;
}
.fi-track {
    height: 5px;
    background: rgba(255,255,255,0.04);
    border-radius: 3px;
    overflow: hidden;
}
.fi-fill {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--wine-mid), var(--wine-glow), var(--gold));
}

/* ══════════════════════════════════════
   PREDICTION BOX
══════════════════════════════════════ */
.prediction-result {
    background:
        radial-gradient(ellipse at top, rgba(123,30,58,0.25) 0%, transparent 60%),
        linear-gradient(145deg, var(--wine-deep), var(--bg-card));
    border: 1px solid rgba(225,29,72,0.3);
    border-radius: 20px;
    padding: 48px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.prediction-result::before {
    content: '🍷';
    position: absolute;
    font-size: 8rem;
    opacity: 0.04;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
}
.prediction-result::after {
    content: '';
    position: absolute;
    top: 0; left: 50%; transform: translateX(-50%);
    width: 240px; height: 1px;
    background: linear-gradient(90deg, transparent, var(--wine-glow), transparent);
}
.pred-eyebrow {
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--wine-bright);
    margin-bottom: 12px;
}
.pred-value {
    font-family: 'Cormorant Garamond', serif;
    font-size: 5rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1;
    text-shadow: 0 0 40px rgba(225,29,72,0.3);
}
.pred-model {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 12px;
    font-family: 'Fira Code', monospace;
    letter-spacing: 0.08em;
}

/* ══════════════════════════════════════
   BEST MODEL HIGHLIGHT
══════════════════════════════════════ */
.best-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: linear-gradient(135deg, rgba(201,169,110,0.15), rgba(201,169,110,0.05));
    color: var(--gold);
    border: 1px solid rgba(201,169,110,0.25);
    padding: 3px 12px;
    border-radius: 4px;
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-left: 10px;
}

/* ══════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
══════════════════════════════════════ */

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, var(--wine-mid) 0%, var(--wine-bright) 100%) !important;
    color: var(--text-primary) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    padding: 10px 24px !important;
    letter-spacing: 0.03em !important;
    font-family: 'Outfit', sans-serif !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* Selects */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border-card) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSelectbox label, .stMultiSelect label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* Number Input */
.stNumberInput input {
    background: var(--bg-card) !important;
    border-color: var(--border-card) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.88rem !important;
}
.stNumberInput label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* Slider */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--wine-glow) !important;
    border-color: var(--wine-glow) !important;
}
.stSlider label {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

/* Checkbox */
.stCheckbox label {
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 5px !important;
    gap: 3px !important;
    border: 1px solid var(--border-card) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 7px !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    padding: 7px 18px !important;
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: 0.02em !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--wine-mid), var(--wine-bright)) !important;
    color: var(--text-primary) !important;
}

/* Divider */
hr {
    border-color: var(--border-card) !important;
    margin: 28px 0 !important;
}

/* File uploader */
[data-testid="stFileUploader"] section {
    background: var(--bg-card) !important;
    border: 1px dashed rgba(123,30,58,0.3) !important;
    border-radius: 12px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* Alerts */
.stAlert { border-radius: 10px !important; font-size: 0.88rem !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-card) !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 2rem !important;
    color: var(--text-primary) !important;
}

/* Caption */
.stCaption { color: var(--text-muted) !important; font-size: 0.76rem !important; }

/* Sidebar nav label */
.nav-group-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 12px 4px 5px;
    opacity: 0.6;
}

/* Logo area */
.sidebar-logo {
    padding: 28px 16px 24px;
    border-bottom: 1px solid var(--border-card);
    margin-bottom: 6px;
}
.sidebar-logo-mark {
    font-size: 1.8rem;
    margin-bottom: 8px;
    display: block;
    filter: drop-shadow(0 0 12px rgba(225,29,72,0.5));
}
.sidebar-logo-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: var(--text-primary);
    letter-spacing: -0.01em;
    line-height: 1.1;
}
.sidebar-logo-sub {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--wine-bright);
    margin-top: 4px;
    opacity: 0.7;
}

/* Status panel */
.status-panel {
    margin: 8px 4px 20px;
    padding: 14px 16px;
    background: rgba(8,14,26,0.6);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.04);
}
.status-panel-title {
    font-family: 'Fira Code', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 10px;
    opacity: 0.6;
}

/* Drop zone */
.drop-zone {
    border: 1px dashed rgba(123,30,58,0.3);
    border-radius: 18px;
    padding: 72px 40px;
    text-align: center;
    background: rgba(20,31,51,0.4);
    margin-top: 16px;
    transition: border-color 0.3s;
}
.drop-zone:hover { border-color: rgba(225,29,72,0.3); }
.drop-zone-icon { font-size: 3rem; margin-bottom: 14px; display: block; opacity: 0.5; }

/* Info text */
.info-text {
    font-size: 0.85rem;
    color: var(--text-muted);
    line-height: 1.7;
    font-weight: 300;
}

/* Sidebar footer */
.sidebar-footer {
    padding: 16px;
    text-align: center;
    border-top: 1px solid var(--border-card);
    margin-top: 16px;
    font-family: 'Fira Code', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    opacity: 0.4;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
_defaults = {
    "df_raw": None, "df": None, "features": [],
    "target": None, "models": {}, "model_results": {},
    "trained_features": [], "selected_page": "🍷 Overview",
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ══════════════════════════════════════════════════════════════════════════════
# SHARED HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def N(n): return f"{n:,}"

def wine_chart_layout():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,31,51,0.5)",
        font=dict(color="#64748B", family="Outfit"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.04)", zerolinecolor="rgba(255,255,255,0.04)"),
        colorway=["#C0294E","#C9A96E","#7B1E3A","#E11D48","#8B6F47","#F43F5E","#FCD34D"],
    )

def section_header(icon, label, title, subtitle=None):
    sub_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-label">{icon} &nbsp; {label}</div>
        <div class="section-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def metric_card(label, value, sub="", variant="", col=None):
    html = f"""
    <div class="metric-card {variant}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {'<div class="metric-sub">' + sub + '</div>' if sub else ''}
    </div>"""
    (col or st).markdown(html, unsafe_allow_html=True)

def fi_bar(label, value, max_val):
    pct = (value / max_val * 100) if max_val > 0 else 0
    st.markdown(f"""
    <div class="fi-wrap">
        <div class="fi-header"><span>{label}</span><span>{value:.4f}</span></div>
        <div class="fi-track"><div class="fi-fill" style="width:{pct:.1f}%"></div></div>
    </div>""", unsafe_allow_html=True)

def breadcrumb(current):
    steps  = ["Overview","Upload","Insights","EDA","Cleaning","Features","Training","Compare","Explain","Predict"]
    icons  = ["🍷","📁","🧠","📊","🧹","🎯","🤖","📈","🔍","🎯"]
    done_set = {
        "Upload":   st.session_state.df_raw is not None,
        "Insights": st.session_state.df_raw is not None,
        "EDA":      st.session_state.df_raw is not None,
        "Cleaning": st.session_state.df is not None,
        "Features": bool(st.session_state.features),
        "Training": bool(st.session_state.model_results),
        "Compare":  bool(st.session_state.model_results),
        "Explain":  bool(st.session_state.model_results),
        "Predict":  bool(st.session_state.model_results),
    }
    html = '<div class="breadcrumb">'
    for i, (s, ico) in enumerate(zip(steps, icons)):
        cls = "active" if s == current else ("done" if done_set.get(s) else "")
        tick = " ✓" if cls == "done" else ""
        html += f'<div class="bc-item {cls}">{ico} {s}{tick}</div>'
        if i < len(steps)-1:
            html += '<span class="bc-sep">›</span>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════

def page_overview():
    # Hero
    st.markdown("""
    <div class="hero">
        <span class="hero-ornament">🍷</span>
        <div class="hero-eyebrow">Wine Quality Intelligence Studio</div>
        <div class="hero-title">Crimson <em>Analytics</em></div>
        <div class="hero-tagline">A precision ML pipeline for the art and science of wine — guided, not automated.</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Pipeline overview cards
    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        st.markdown("""
        <div class="wine-card">
            <div style="font-size:1.6rem;margin-bottom:12px">📁</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;font-weight:600;color:#F8FAFC;margin-bottom:6px">Data Ingestion</div>
            <div class="info-text">Upload your Red Wine Quality CSV. Preview, profile, and understand your dataset before touching a single parameter.</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="wine-card">
            <div style="font-size:1.6rem;margin-bottom:12px">🧠</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;font-weight:600;color:#F8FAFC;margin-bottom:6px">Intelligence Layer</div>
            <div class="info-text">Automated insights surface correlations, missing patterns, and skewness — guiding your cleaning decisions with evidence.</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="wine-card">
            <div style="font-size:1.6rem;margin-bottom:12px">🤖</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.15rem;font-weight:600;color:#F8FAFC;margin-bottom:6px">Model Orchestration</div>
            <div class="info-text">Train Logistic Regression, Random Forest, and SVM. Compare, explain, and predict — all under your control.</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Pipeline steps
    st.markdown("""
    <div style="margin-bottom:18px">
        <div class="section-label">🍷 &nbsp; The Pipeline</div>
        <div class="section-title" style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;margin-top:4px">Your Journey</div>
    </div>""", unsafe_allow_html=True)

    steps = [
        ("01", "Upload Data",        "Import your CSV and inspect shape, types, and null counts at a glance."),
        ("02", "Insights",           "Surface missing value patterns, high correlations, and skewness alerts."),
        ("03", "Exploratory Analysis","Heatmaps, histograms, and box plots to visualise your data landscape."),
        ("04", "Data Cleaning",      "Impute missing values, remove outliers, and encode categoricals."),
        ("05", "Feature Selection",  "Manually choose which predictors enter your model."),
        ("06", "Model Training",     "Select algorithms, set train/test split, and launch training."),
        ("07", "Model Comparison",   "Bar chart of accuracies — you decide which model wins."),
        ("08", "Explainability",     "Random Forest feature importances reveal what drives quality."),
        ("09", "Prediction",         "Input custom values and receive a quality class prediction."),
    ]
    col_a, col_b = st.columns(2, gap="large")
    for i, (num, title, desc) in enumerate(steps):
        col = col_a if i % 2 == 0 else col_b
        col.markdown(f"""
        <div class="wine-card" style="padding:16px 20px;margin-bottom:10px;display:flex;gap:16px;align-items:flex-start">
            <div style="font-family:'Fira Code',monospace;font-size:0.72rem;color:var(--wine-bright);min-width:28px;padding-top:2px;letter-spacing:0.1em">{num}</div>
            <div>
                <div style="font-family:'Outfit',sans-serif;font-size:0.92rem;font-weight:600;color:#F8FAFC;margin-bottom:3px">{title}</div>
                <div class="info-text" style="font-size:0.8rem">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # Current status
    has_data = st.session_state.df is not None
    has_feat = bool(st.session_state.features)
    has_mdl  = bool(st.session_state.model_results)

    st.markdown("""
    <div style="margin-bottom:14px">
        <div class="section-label">🍷 &nbsp; Status</div>
        <div class="section-title" style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;margin-top:4px">Session State</div>
    </div>""", unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3, gap="large")
    with sc1:
        variant = "ok" if has_data else "info"
        icon    = "✓" if has_data else "○"
        sc1.markdown(f'<div class="wine-card" style="text-align:center;padding:22px"><div style="font-size:1.5rem;margin-bottom:8px">{"✅" if has_data else "📂"}</div><div class="metric-label">Dataset</div><span class="badge {variant}">{icon} {"Loaded" if has_data else "Awaiting"}</span></div>', unsafe_allow_html=True)
    with sc2:
        variant = "ok" if has_feat else "info"
        icon    = "✓" if has_feat else "○"
        sc2.markdown(f'<div class="wine-card" style="text-align:center;padding:22px"><div style="font-size:1.5rem;margin-bottom:8px">{"✅" if has_feat else "🎯"}</div><div class="metric-label">Features</div><span class="badge {variant}">{icon} {"Selected" if has_feat else "Pending"}</span></div>', unsafe_allow_html=True)
    with sc3:
        variant = "ok" if has_mdl else "info"
        icon    = "✓" if has_mdl else "○"
        sc3.markdown(f'<div class="wine-card" style="text-align:center;padding:22px"><div style="font-size:1.5rem;margin-bottom:8px">{"✅" if has_mdl else "🤖"}</div><div class="metric-label">Models</div><span class="badge {variant}">{icon} {"Trained" if has_mdl else "Pending"}</span></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: UPLOAD
# ══════════════════════════════════════════════════════════════════════════════

def page_upload():
    section_header("📁", "Step 01", "Upload Dataset", "Import your CSV and inspect its anatomy")
    breadcrumb("Upload")

    st.markdown("""
    <div class="wine-card">
        <p class="info-text">Upload a <strong style="color:#F8FAFC">CSV file</strong> to begin.
        Crimson Analytics will parse your dataset, run a shape analysis, and give you a
        column-level diagnostic — all before you touch a single hyperparameter.</p>
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Decanting your dataset…"):
            df = pd.read_csv(uploaded)
            st.session_state.df_raw = df.copy()
            st.session_state.df     = df.copy()

        st.success(f"✓  **{uploaded.name}** — {N(df.shape[0])} rows × {df.shape[1]} columns")
        st.divider()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows",        N(df.shape[0]),                            "observations")
        c2.metric("Columns",     str(df.shape[1]),                          "total fields")
        c3.metric("Numeric",     str(df.select_dtypes(include=np.number).shape[1]), "numeric cols")
        c4.metric("Categorical", str(df.select_dtypes(exclude=np.number).shape[1]),"object / bool")

        st.divider()

        tab1, tab2 = st.tabs(["  Data Preview  ", "  Column Diagnostics  "])
        with tab1:
            st.dataframe(df.head(20), use_container_width=True, height=330)
        with tab2:
            dtype_df = pd.DataFrame({
                "Column":  df.columns,
                "Type":    df.dtypes.astype(str).values,
                "Non-Null":df.count().values,
                "Null %":  (df.isnull().mean()*100).round(2).values,
                "Unique":  df.nunique().values,
                "Sample":  [str(df[c].dropna().iloc[0]) if df[c].count() > 0 else "—" for c in df.columns],
            })
            st.dataframe(dtype_df, use_container_width=True, height=390)

    else:
        st.markdown("""
        <div class="drop-zone">
            <span class="drop-zone-icon">🍷</span>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#475569;margin-bottom:6px">
                Drop your wine dataset here
            </div>
            <div class="info-text">Supports classification & regression · CSV format</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════

def page_insights():
    section_header("🧠", "Step 02", "Insights & Guidance", "Automated quality audit — act on what you find")
    breadcrumb("Insights")

    df = st.session_state.df_raw
    if df is None:
        st.warning("⚠️  Upload a dataset first to unlock insights.")
        return

    # ── Missing Values
    st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#F8FAFC;margin-bottom:14px;font-weight:500">
        🕳  Missing Value Analysis</div>""", unsafe_allow_html=True)

    miss     = df.isnull().sum()
    miss_pct = (miss / len(df) * 100).round(2)
    miss_df  = pd.DataFrame({"Column": miss.index, "Count": miss.values, "Percentage %": miss_pct.values})
    miss_df  = miss_df[miss_df["Count"] > 0]

    if miss_df.empty:
        st.success("✓  No missing values detected. Your dataset is pristine.")
    else:
        st.warning(f"**{len(miss_df)} columns** contain missing values.")
        st.dataframe(miss_df.sort_values("Percentage %", ascending=False), use_container_width=True, height=220)
        st.markdown("""
        <div class="wine-card accent">
            <div style="font-family:'Fira Code',monospace;font-size:0.65rem;letter-spacing:0.14em;color:var(--wine-bright);margin-bottom:10px">SUGGESTED ACTIONS</div>
            <ul class="info-text" style="margin:0;padding-left:18px;line-height:2.4">
                <li><strong style="color:#F8FAFC">&lt; 5% missing</strong> — Median or mean imputation is safe and low-risk.</li>
                <li><strong style="color:#F8FAFC">5–30% missing</strong> — Consider model-based imputation, or create a binary indicator feature.</li>
                <li><strong style="color:#F8FAFC">&gt; 30% missing</strong> — Evaluate dropping the column; imputation may introduce significant noise.</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Correlation
    st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#F8FAFC;margin-bottom:14px;font-weight:500">
        🔗  Correlation Audit</div>""", unsafe_allow_html=True)

    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] >= 2:
        corr   = num_df.corr().abs()
        upper  = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        hi     = [(c, r, upper.loc[r,c]) for c in upper.columns for r in upper.index
                  if pd.notna(upper.loc[r,c]) and upper.loc[r,c] > 0.85]

        if hi:
            st.warning(f"**{len(hi)} highly correlated pairs** (|r| > 0.85) detected — consider pruning.")
            hc_df = pd.DataFrame(hi, columns=["Feature A","Feature B","|r|"])
            hc_df["|r|"] = hc_df["|r|"].round(4)
            st.dataframe(hc_df.sort_values("|r|", ascending=False), use_container_width=True, height=220)
            st.markdown("""
            <div class="wine-card accent">
                <div style="font-family:'Fira Code',monospace;font-size:0.65rem;letter-spacing:0.14em;color:var(--wine-bright);margin-bottom:10px">SUGGESTED ACTIONS</div>
                <ul class="info-text" style="margin:0;padding-left:18px;line-height:2.4">
                    <li>Drop one feature from each correlated pair to reduce multicollinearity.</li>
                    <li>Apply PCA to compress correlated dimensions into orthogonal components.</li>
                </ul>
            </div>""", unsafe_allow_html=True)
        else:
            st.success("✓  No highly correlated pairs found (threshold |r| > 0.85).")

    st.divider()

    # ── Descriptive Stats
    st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#F8FAFC;margin-bottom:14px;font-weight:500">
        📐  Descriptive Statistics</div>""", unsafe_allow_html=True)
    st.dataframe(num_df.describe().T.round(4), use_container_width=True, height=360)

    st.divider()

    # ── Skewness
    st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:#F8FAFC;margin-bottom:14px;font-weight:500">
        📉  Skewness Alerts</div>""", unsafe_allow_html=True)
    skew      = num_df.skew().abs().sort_values(ascending=False)
    hi_skew   = skew[skew > 1.5]
    if not hi_skew.empty:
        st.warning(f"**{len(hi_skew)} features** are highly skewed (|skewness| > 1.5).")
        sk_df = pd.DataFrame({"Feature": hi_skew.index, "Abs Skewness": hi_skew.values.round(3)})
        st.dataframe(sk_df, use_container_width=True, height=200)
        st.markdown("""
        <div class="wine-card">
            <div class="info-text">
                Tree-based models tolerate skewness well.
                For linear models, consider <em>log-transform</em> or <em>Box-Cox</em> before training.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.success("✓  No severely skewed features detected.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EDA
# ══════════════════════════════════════════════════════════════════════════════

def page_eda():
    section_header("📊", "Step 03", "Exploratory Data Analysis", "Visual cartography of your dataset")
    breadcrumb("EDA")

    df = st.session_state.df
    if df is None:
        st.warning("Upload a dataset first.")
        return

    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    layout   = wine_chart_layout()

    tab1, tab2, tab3 = st.tabs(["  Correlation Heatmap  ", "  Distributions  ", "  Box Plots  "])

    with tab1:
        if len(num_cols) < 2:
            st.info("Need at least 2 numeric columns.")
        else:
            corr_m = df[num_cols].corr()
            fig = go.Figure(go.Heatmap(
                z=corr_m.values, x=corr_m.columns, y=corr_m.index,
                colorscale=[[0,"#0F172A"],[0.35,"#4A0E20"],[0.65,"#7B1E3A"],[0.85,"#C0294E"],[1,"#C9A96E"]],
                text=corr_m.round(2).values, texttemplate="%{text}", textfont=dict(size=10),
                hoverongaps=False, showscale=True,
                colorbar=dict(
                    tickfont=dict(color="#64748B", family="Fira Code", size=10),
                    outlinecolor="rgba(0,0,0,0)",
                    bgcolor="rgba(0,0,0,0)",
                )
            ))
            fig.update_layout(**layout, height=540,
                title=dict(text="Feature Correlation Matrix", font=dict(family="Cormorant Garamond", size=16, color="#F8FAFC"), x=0.02),
                margin=dict(t=52,b=20,l=20,r=20))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if not num_cols:
            st.info("No numeric columns.")
        else:
            col_pick = st.multiselect("Select features", num_cols, default=num_cols[:min(6,len(num_cols))])
            if col_pick:
                ncols  = 2
                nrows  = (len(col_pick)+1)//2
                fig    = make_subplots(rows=nrows, cols=ncols, subplot_titles=col_pick,
                                       vertical_spacing=0.12, horizontal_spacing=0.08)
                for i, col in enumerate(col_pick):
                    r, c = divmod(i, 2)
                    fig.add_trace(
                        go.Histogram(x=df[col], nbinsx=34, name=col,
                            marker=dict(color="#C0294E", opacity=0.75,
                                        line=dict(color="#080E1A", width=0.4))),
                        row=r+1, col=c+1)
                fig.update_layout(**layout, height=max(360, nrows*230), showlegend=False,
                    margin=dict(t=44,b=20,l=20,r=20))
                fig.update_xaxes(gridcolor="rgba(255,255,255,0.04)")
                fig.update_yaxes(gridcolor="rgba(255,255,255,0.04)")
                st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if not num_cols:
            st.info("No numeric columns.")
        else:
            bp_cols = st.multiselect("Select features for box plots", num_cols,
                                     default=num_cols[:min(6,len(num_cols))], key="bp")
            if bp_cols:
                fig = go.Figure()
                palette = ["#C0294E","#C9A96E","#7B1E3A","#E11D48","#8B6F47","#F43F5E","#FCD34D"]
                for j, col in enumerate(bp_cols):
                    clr = palette[j % len(palette)]
                    fig.add_trace(go.Box(
                        y=df[col], name=col, boxmean=True,
                        marker_color=clr, line_color=clr,
                       fillcolor=f'rgba({int(clr[1:3],16)}, {int(clr[3:5],16)}, {int(clr[5:7],16)}, 0.06)',
                    ))
                fig.update_layout(**layout, height=450, showlegend=False,
                    title=dict(text="Spread & Outlier Profile", font=dict(family="Cormorant Garamond",size=16,color="#F8FAFC"), x=0.02),
                    margin=dict(t=52,b=20,l=20,r=20))
                st.plotly_chart(fig, use_container_width=True)

    if cat_cols:
        st.divider()
        st.markdown("""<div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:#F8FAFC;margin-bottom:12px;font-weight:500">
            🏷  Categorical Feature Frequencies</div>""", unsafe_allow_html=True)
        cat_pick = st.selectbox("Column", cat_cols)
        vc = df[cat_pick].value_counts().reset_index()
        vc.columns = [cat_pick, "count"]
        fig = px.bar(vc.head(20), x=cat_pick, y="count",
                     color="count", color_continuous_scale=["#0F172A","#4A0E20","#C0294E","#C9A96E"])
        fig.update_layout(**layout, height=380, showlegend=False,
                          coloraxis_showscale=False, margin=dict(t=30,b=30,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DATA CLEANING
# ══════════════════════════════════════════════════════════════════════════════

def page_cleaning():
    section_header("🧹", "Step 04", "Data Cleaning & Engineering", "Impute, clip, and encode — on your terms")
    breadcrumb("Cleaning")

    df = st.session_state.df
    if df is None:
        st.warning("Upload a dataset first.")
        return

    r1c1, r1c2, r1c3 = st.columns(3)
    r1c1.metric("Current Rows",    N(df.shape[0]),  "observations")
    r1c2.metric("Current Columns", str(df.shape[1]),"fields")
    r1c3.metric("Missing Cells",   str(df.isnull().sum().sum()), "total nulls")

    st.divider()

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:14px">Missing Value Strategy</div>""",
            unsafe_allow_html=True)
        miss_strat = st.selectbox("Strategy", [
            "Drop rows with any missing values",
            "Fill numeric columns with Mean",
            "Fill numeric columns with Median"],
            label_visibility="collapsed")
        if st.button("Apply Imputation", use_container_width=True, key="miss_btn"):
            with st.spinner("Treating missing values…"):
                dfw   = st.session_state.df.copy()
                before = dfw.shape[0]
                if "Drop" in miss_strat:
                    dfw = dfw.dropna()
                else:
                    nc = dfw.select_dtypes(include=np.number).columns
                    fn = dfw[nc].mean() if "Mean" in miss_strat else dfw[nc].median()
                    dfw[nc] = dfw[nc].fillna(fn)
                st.session_state.df = dfw
            after = dfw.shape[0]
            st.success(f"✓  {N(before)} → {N(after)} rows  ({before-after} affected)")

    with col_b:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:14px">IQR Outlier Removal</div>""",
            unsafe_allow_html=True)
        num_cols  = df.select_dtypes(include=np.number).columns.tolist()
        iqr_cols  = st.multiselect("Columns", num_cols, label_visibility="collapsed")
        iqr_k     = st.slider("Fence multiplier k  (Q1/Q3 ± k × IQR)", 1.0, 3.0, 1.5, 0.1)
        if st.button("Apply Outlier Removal", use_container_width=True, key="iqr_btn"):
            if iqr_cols:
                with st.spinner("Removing outliers…"):
                    dfw    = st.session_state.df.copy()
                    before = dfw.shape[0]
                    for c in iqr_cols:
                        Q1, Q3 = dfw[c].quantile(.25), dfw[c].quantile(.75)
                        IQR    = Q3 - Q1
                        dfw    = dfw[(dfw[c] >= Q1-iqr_k*IQR) & (dfw[c] <= Q3+iqr_k*IQR)]
                    st.session_state.df = dfw
                after = dfw.shape[0]
                st.success(f"✓  {N(before)} → {N(after)} rows  ({before-after} outliers removed)")
            else:
                st.warning("Select at least one column for IQR removal.")

    st.divider()

    col_c, col_d = st.columns(2, gap="large")

    with col_c:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:14px">One-Hot Encoding</div>""",
            unsafe_allow_html=True)
        cat_cols = st.session_state.df.select_dtypes(exclude=np.number).columns.tolist()
        if cat_cols:
            enc_cols = st.multiselect("Columns to encode", cat_cols, label_visibility="collapsed")
            if st.button("Apply Encoding", use_container_width=True, key="enc_btn") and enc_cols:
                with st.spinner("Encoding…"):
                    dfw = pd.get_dummies(st.session_state.df, columns=enc_cols, drop_first=True)
                    st.session_state.df = dfw
                st.success(f"✓  Encoded {len(enc_cols)} column(s) → shape now {dfw.shape[0]} × {dfw.shape[1]}")
        else:
            st.info("No categorical columns present.")

    with col_d:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:14px">Reset Dataset</div>""",
            unsafe_allow_html=True)
        st.markdown('<div class="info-text">Revert to the original upload, discarding all cleaning steps.</div>',
                    unsafe_allow_html=True)
        if st.button("↺  Reset to Original", use_container_width=True, key="reset_btn"):
            st.session_state.df = st.session_state.df_raw.copy()
            st.success("✓  Dataset restored to original state.")

    st.divider()

    st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
        text-transform:uppercase;color:#475569;margin-bottom:12px">Current State Preview</div>""",
        unsafe_allow_html=True)
    st.dataframe(st.session_state.df.head(10), use_container_width=True, height=270)
    st.caption(f"Shape: {st.session_state.df.shape[0]:,} rows × {st.session_state.df.shape[1]} columns")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: FEATURE SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def page_features():
    section_header("🎯", "Step 05", "Feature Selection", "Choose your predictors with intention")
    breadcrumb("Features")

    df = st.session_state.df
    if df is None:
        st.warning("Upload a dataset first.")
        return

    st.markdown("""
    <div class="wine-card">
        <p class="info-text">Select the <strong style="color:#F8FAFC">input features</strong> your model will learn from.
        The target column is configured separately on the Training page.
        Consult the Insights and EDA pages to guide your choices.</p>
    </div>""", unsafe_allow_html=True)

    all_cols     = df.columns.tolist()
    default_feat = [c for c in all_cols if c != all_cols[-1]]
    selected     = st.multiselect(
        "Input features", all_cols,
        default=st.session_state.features or default_feat,
        label_visibility="collapsed")
    st.session_state.features = selected

    if selected:
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Selected",  str(len(selected)),            "feature(s) chosen")
        c2.metric("Available", str(len(all_cols)),            "total columns")
        c3.metric("Excluded",  str(len(all_cols)-len(selected)), "columns dropped")

        num_f = df[selected].select_dtypes(include=np.number).columns.tolist()
        cat_f = df[selected].select_dtypes(exclude=np.number).columns.tolist()

        st.markdown(f"""
        <div class="wine-card" style="margin-top:16px">
            <div style="font-family:'Fira Code',monospace;font-size:0.65rem;letter-spacing:0.14em;color:#475569;margin-bottom:10px">FEATURE COMPOSITION</div>
            <div style="display:flex;gap:10px;flex-wrap:wrap">
                <span class="badge ok">✦ {len(num_f)} Numeric</span>
                <span class="badge warn">✦ {len(cat_f)} Categorical</span>
            </div>
        </div>""", unsafe_allow_html=True)

        if cat_f:
            st.warning(f"**{len(cat_f)} categorical feature(s)** selected: `{'`, `'.join(cat_f)}`. "
                       "Encode them in the Data Cleaning step before training.")

        st.divider()
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:12px">Feature Preview</div>""",
            unsafe_allow_html=True)
        st.dataframe(df[selected].head(8), use_container_width=True, height=250)
    else:
        st.info("Select at least one feature to proceed.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MODEL TRAINING
# ══════════════════════════════════════════════════════════════════════════════

def page_training():
    from sklearn.linear_model     import LogisticRegression
    from sklearn.ensemble         import RandomForestClassifier
    from sklearn.svm              import SVC
    from sklearn.model_selection  import train_test_split
    from sklearn.metrics          import accuracy_score
    from sklearn.preprocessing    import LabelEncoder

    section_header("🤖", "Step 06", "Model Training", "Configure your run — nothing trains until you say so")
    breadcrumb("Training")

    df       = st.session_state.df
    features = st.session_state.features
    if df is None:
        st.warning("Upload a dataset first.")
        return
    if not features:
        st.warning("Select features on the Feature Selection page first.")
        return

    st.markdown("""
    <div class="wine-card">
        <p class="info-text">Set your target, tune your split, pick your algorithms, then click
        <strong style="color:#F8FAFC">Launch Training</strong>.
        Crimson Analytics trains only what you explicitly request — no assumptions, no surprises.</p>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        target = st.selectbox("Target Column",
                              [c for c in df.columns if c not in features],
                              key="target_select")
        st.session_state.target = target
    with col2:
        test_sz = st.slider("Test Set Proportion", 0.1, 0.5, 0.2, 0.05)

    st.divider()

    st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
        text-transform:uppercase;color:#475569;margin-bottom:16px">Select Algorithms</div>""",
        unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3, gap="large")
    with m1:
        st.markdown('<div class="wine-card" style="padding:18px 20px">', unsafe_allow_html=True)
        use_lr  = st.checkbox("Logistic Regression",      value=True,  key="lr")
        st.markdown('<div class="info-text" style="font-size:0.76rem;margin-top:4px">Linear classifier · fast · interpretable</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="wine-card" style="padding:18px 20px">', unsafe_allow_html=True)
        use_rf  = st.checkbox("Random Forest",             value=True,  key="rf")
        st.markdown('<div class="info-text" style="font-size:0.76rem;margin-top:4px">Ensemble · robust · feature importance</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="wine-card" style="padding:18px 20px">', unsafe_allow_html=True)
        use_svm = st.checkbox("Support Vector Machine",    value=True,  key="svm")
        st.markdown('<div class="info-text" style="font-size:0.76rem;margin-top:4px">Kernel-based · high-dimensional · powerful</div></div>', unsafe_allow_html=True)

    st.divider()
    go_btn = st.button("🍷  Launch Training", use_container_width=True)

    if go_btn:
        if not any([use_lr, use_rf, use_svm]):
            st.error("Select at least one algorithm.")
            return

        with st.spinner("Training models — patience is a virtue…"):
            X = df[features].select_dtypes(include=np.number).fillna(
                df[features].select_dtypes(include=np.number).median())
            y = df[target]
            if y.dtype == "object":
                le = LabelEncoder()
                y  = le.fit_transform(y)

            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=test_sz, random_state=42)

            results, store = {}, {}
            if use_lr:
                m = LogisticRegression(max_iter=1000, random_state=42)
                m.fit(X_tr, y_tr)
                results["Logistic Regression"] = {"accuracy": accuracy_score(y_te, m.predict(X_te)), "model": m}
                store["Logistic Regression"] = m
            if use_rf:
                m = RandomForestClassifier(n_estimators=100, random_state=42)
                m.fit(X_tr, y_tr)
                results["Random Forest"] = {"accuracy": accuracy_score(y_te, m.predict(X_te)), "model": m}
                store["Random Forest"] = m
            if use_svm:
                m = SVC(random_state=42, probability=True)
                m.fit(X_tr, y_tr)
                results["SVM"] = {"accuracy": accuracy_score(y_te, m.predict(X_te)), "model": m}
                store["SVM"] = m

            st.session_state.model_results   = results
            st.session_state.models          = store
            st.session_state.trained_features = X.columns.tolist()

        st.success("✓  All selected models trained successfully.")
        st.divider()

        cols = st.columns(len(results))
        for i, (name, res) in enumerate(results.items()):
            cols[i].metric(name, f"{res['accuracy']*100:.2f}%", "test accuracy")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MODEL COMPARISON
# ══════════════════════════════════════════════════════════════════════════════

def page_comparison():
    section_header("📈", "Step 07", "Model Comparison", "Evaluate performance — the best choice is yours")
    breadcrumb("Compare")

    results = st.session_state.model_results
    if not results:
        st.warning("Train at least one model first.")
        return

    layout     = wine_chart_layout()
    names      = list(results.keys())
    accs       = [results[n]["accuracy"]*100 for n in names]
    best_name  = names[int(np.argmax(accs))]

    # Summary table
    st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
        text-transform:uppercase;color:#475569;margin-bottom:12px">Performance Summary</div>""",
        unsafe_allow_html=True)
    res_df = pd.DataFrame({
        "Model":         names,
        "Test Accuracy": [f"{a:.4f}%" for a in accs],
        "Status":        ["⭐ Highest accuracy" if n == best_name else "—" for n in names],
    })
    st.dataframe(res_df, use_container_width=True, hide_index=True, height=175)

    # Highlight card
    st.markdown(f"""
    <div class="wine-card accent" style="margin-top:20px">
        <div style="font-family:'Fira Code',monospace;font-size:0.65rem;letter-spacing:0.16em;color:var(--wine-bright);margin-bottom:10px">HIGHEST ACCURACY MODEL</div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
            <span style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-weight:600;color:#F8FAFC;letter-spacing:-0.01em">{best_name}</span>
            <span class="best-badge">✦ Best on test set</span>
        </div>
        <div style="font-family:'Fira Code',monospace;font-size:1.1rem;color:var(--wine-glow);margin-top:8px">{max(accs):.4f}%</div>
        <div class="info-text" style="margin-top:10px">This is the highest-performing model on your test split. Evaluate domain fit, inference speed, and interpretability before committing.</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # Bar chart
    bar_colors = [
        "rgba(201,169,110,0.85)" if n == best_name else "rgba(123,30,58,0.7)"
        for n in names
    ]
    fig = go.Figure(go.Bar(
        x=names, y=accs,
        marker=dict(color=bar_colors, line=dict(color="#080E1A", width=1)),
        text=[f"{a:.2f}%" for a in accs],
        textposition="outside",
        textfont=dict(color="#F8FAFC", size=13, family="Fira Code"),
    ))
    

    fig = go.Figure(go.Bar(
        x=names, y=accs,
        marker=dict(color=bar_colors, line=dict(color="#080E1A", width=1)),
        text=[f"{a:.2f}%" for a in accs],
        textposition="outside",
        textfont=dict(color="#F8FAFC", size=13, family="Fira Code"),
    ))

    # ✅ FIX: properly indented
    fig.update_layout(
        **layout,
        height=430,
        title=dict(
            text="Accuracy Comparison",
            font=dict(family="Cormorant Garamond", size=18, color="#F8FAFC"),
            x=0.02
        ),
        showlegend=False,
        margin=dict(t=56, b=30, l=20, r=20),
        bargap=0.45,
    )

    fig.update_yaxes(range=[0, max(accs)*1.18], ticksuffix="%")

    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: EXPLAINABILITY
# ══════════════════════════════════════════════════════════════════════════════

def page_explainability():
    section_header("🔍", "Step 08", "Model Explainability", "What drives wine quality? Random Forest reveals all.")
    breadcrumb("Explain")

    results = st.session_state.model_results
    models  = st.session_state.models
    if not results:
        st.warning("Train at least one model first.")
        return
    if "Random Forest" not in models:
        st.info("Feature importance requires a trained **Random Forest** model. Return to Training and enable it.")
        return

    rf           = models["Random Forest"]
    feat_names   = st.session_state.get("trained_features", st.session_state.features)
    importances  = rf.feature_importances_

    fi_df = pd.DataFrame({"Feature": feat_names, "Importance": importances})
    fi_df = fi_df.sort_values("Importance", ascending=False).reset_index(drop=True)
    fi_df["Rank"] = range(1, len(fi_df)+1)

    layout = wine_chart_layout()
    top_n  = min(20, len(fi_df))

    # Horizontal bar chart
    gradient_colors = [
        f"rgba({int(192-(192-201)*i/(top_n-1))},{int(41+(169-41)*i/(top_n-1))},{int(78+(110-78)*i/(top_n-1))},0.85)"
        for i in range(top_n)
    ]

    fig = go.Figure(go.Bar(
        x=fi_df["Importance"][:top_n][::-1],
        y=fi_df["Feature"][:top_n][::-1],
        orientation="h",
        marker=dict(
            color=list(reversed(gradient_colors)),
            line=dict(color="#080E1A", width=0.4)
        ),
        text=[f"{v:.4f}" for v in fi_df["Importance"][:top_n][::-1]],
        textposition="outside",
        textfont=dict(color="#F8FAFC", size=10, family="Fira Code"),
    ))
    fig.update_layout(
    **layout,
    height=max(420, top_n*28+110),   # ✅ dynamic height (better UI)
    title=dict(
        text="Feature Importance",
        font=dict(
            family="Cormorant Garamond",
            size=18,
            color="#F8FAFC"
        ),
        x=0.02
    ),
    margin=dict(t=56, b=30, l=20, r=110),   # ✅ proper margin
)gg

    fig.update_xaxes(title="Importance Score")   # ✅ separate
    st.divider()

    col_bars, col_table = st.columns([1, 1], gap="large")
    with col_bars:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:16px">Importance Profile</div>""",
            unsafe_allow_html=True)
        max_imp = fi_df["Importance"].max()
        for _, row in fi_df.head(12).iterrows():
            fi_bar(row["Feature"], row["Importance"], max_imp)

    with col_table:
        st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
            text-transform:uppercase;color:#475569;margin-bottom:12px">Full Ranking</div>""",
            unsafe_allow_html=True)
        display_df = fi_df[["Rank","Feature","Importance"]].copy()
        display_df["Importance"] = display_df["Importance"].round(6)
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=390)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: PREDICTION
# ══════════════════════════════════════════════════════════════════════════════

def page_prediction():
    section_header("🎯", "Step 09", "Prediction", "Input a wine profile and receive its quality class")
    breadcrumb("Predict")

    models = st.session_state.models
    if not models:
        st.warning("Train at least one model first.")
        return

    df        = st.session_state.df
    feat_names = st.session_state.get("trained_features", st.session_state.features)
    num_feats  = df[feat_names].select_dtypes(include=np.number).columns.tolist()

    if not num_feats:
        st.error("No numeric features available for input.")
        return

    st.markdown("""
    <div class="wine-card">
        <p class="info-text">Enter values for each feature, select your model, and click
        <strong style="color:#F8FAFC">Run Prediction</strong> to reveal the quality classification.</p>
    </div>""", unsafe_allow_html=True)

    model_choice = st.selectbox("Model", list(models.keys()))

    st.divider()
    st.markdown("""<div style="font-family:'Fira Code',monospace;font-size:0.68rem;letter-spacing:0.14em;
        text-transform:uppercase;color:#475569;margin-bottom:16px">Wine Profile Input</div>""",
        unsafe_allow_html=True)

    input_vals   = {}
    col_per_row  = 3
    feat_rows    = [num_feats[i:i+col_per_row] for i in range(0, len(num_feats), col_per_row)]
    for row in feat_rows:
        cols = st.columns(len(row))
        for widget_col, feat in zip(cols, row):
            default = float(df[feat].median()) if pd.notna(df[feat].median()) else 0.0
            input_vals[feat] = widget_col.number_input(feat, value=default, format="%.4f", key=f"pred_{feat}")

    st.divider()
    predict_btn = st.button("🍷  Run Prediction", use_container_width=True)

    if predict_btn:
        with st.spinner("Analysing wine profile…"):
            import time; time.sleep(0.4)   # brief dramatic pause
            model   = models[model_choice]
            X_in    = pd.DataFrame([input_vals])
            pred    = model.predict(X_in)[0]
            proba   = model.predict_proba(X_in)[0] if hasattr(model, "predict_proba") else None

        proba_html = ""
        if proba is not None:
            parts = "  ·  ".join(
                [f'Class {i}: <strong style="color:var(--wine-glow)">{p*100:.1f}%</strong>'
                 for i, p in enumerate(proba)])
            proba_html = f'<div style="margin-top:14px;font-family:Fira Code,monospace;font-size:0.78rem;color:var(--text-muted)">{parts}</div>'

        st.markdown(f"""
        <div class="prediction-result">
            <div class="pred-eyebrow">Quality Classification  ·  {model_choice}</div>
            <div class="pred-value">{pred}</div>
            {proba_html}
            <div class="pred-model">Wine quality class on a 3–9 scale</div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

PAGES = {
    "🍷 Overview":         page_overview,
    "📁 Upload Data":      page_upload,
    "🧠 Insights":         page_insights,
    "📊 EDA":              page_eda,
    "🧹 Data Cleaning":    page_cleaning,
    "🎯 Feature Selection":page_features,
    "🤖 Model Training":   page_training,
    "📈 Model Comparison": page_comparison,
    "🔍 Explainability":   page_explainability,
    "🎯 Prediction":       page_prediction,
}

with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="sidebar-logo-mark">🍷</span>
        <div class="sidebar-logo-name">Crimson Analytics</div>
        <div class="sidebar-logo-sub">Wine Quality Intelligence</div>
    </div>""", unsafe_allow_html=True)

    has_data = st.session_state.df is not None
    has_feat = bool(st.session_state.features)
    has_mdl  = bool(st.session_state.model_results)

    st.markdown(f"""
    <div class="status-panel">
        <div class="status-panel-title">Pipeline Status</div>
        <div style="display:flex;flex-direction:column;gap:7px">
            <span class="badge {'ok' if has_data else 'info'}">{'✓' if has_data else '○'} &nbsp;Dataset loaded</span>
            <span class="badge {'ok' if has_feat else 'info'}">{'✓' if has_feat else '○'} &nbsp;Features selected</span>
            <span class="badge {'ok' if has_mdl  else 'info'}">{'✓' if has_mdl  else '○'} &nbsp;Models trained</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-group-label">Navigate</div>', unsafe_allow_html=True)

    selected_page = st.radio(
        "nav",
        list(PAGES.keys()),
        label_visibility="collapsed",
        index=list(PAGES.keys()).index(st.session_state.selected_page)
              if st.session_state.selected_page in PAGES else 0,
    )
    st.session_state.selected_page = selected_page

    st.markdown("""
    <div class="sidebar-footer">
        You guide every step · No auto-decisions
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════════

PAGES[selected_page]()