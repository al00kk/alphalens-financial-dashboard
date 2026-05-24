import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════

import streamlit as st

st.set_page_config(
    page_title="AlphaLens · Financial Research Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════
#  GLOBAL STYLES
# ══════════════════════════════════════════════

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..60,400;12..60,600;12..60,700;12..60,800&family=JetBrains+Mono:wght@300;400;500;600&display=swap');

/* VARIABLES */
:root {
    --bg:      #07080c;
    --surface: #0d0f16;
    --card:    #111420;
    --border:  #1c1f2e;
    --border2: #262a3d;
    --accent:  #e8ff47;
    --blue:    #4d9eff;
    --red:     #ff5252;
    --green:   #00e676;
    --orange:  #ff9800;
    --text:    #d8dce8;
    --muted:   #4a5068;
    --muted2:  #6b7490;
}

/* APP BACKGROUND */
.stApp { background-color: var(--bg) !important; }
[data-testid="stAppViewContainer"] { background-color: var(--bg) !important; }
section[data-testid="stMain"] { background-color: var(--bg) !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* SIDEBAR — dark themed, NOT hidden */
[data-testid="stSidebar"] {
    background-color: #0d0f16 !important;
}
[data-testid="stSidebar"] > div:first-child {
    background-color: #0d0f16 !important;
    border-right: 1px solid #1c1f2e !important;
    padding-top: 1.5rem !important;
}
[data-testid="stSidebar"] input {
    background-color: #111420 !important;
    border: 1px solid #262a3d !important;
    color: #d8dce8 !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
}
[data-testid="stSidebar"] input:focus {
    border-color: #e8ff47 !important;
    box-shadow: 0 0 0 2px rgba(232,255,71,0.15) !important;
}
[data-testid="stSidebar"] textarea {
    background-color: #111420 !important;
    border: 1px solid #262a3d !important;
    color: #d8dce8 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background-color: #111420 !important;
    border-color: #262a3d !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #d8dce8 !important;
}
[data-testid="stSidebar"] hr { border-color: #1c1f2e !important; }

/* MAIN FONT */
[data-testid="stMain"] * { font-family: 'JetBrains Mono', monospace; }

/* BANNER */
.banner {
    background: linear-gradient(135deg, #0d0f16 0%, #111420 60%, #0a0d18 100%);
    border: 1px solid #262a3d;
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.banner::before {
    content: '';
    position: absolute; top: -80px; right: -80px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(232,255,71,0.07) 0%, transparent 65%);
    pointer-events: none;
}
.banner-title {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 2.8rem !important;
    font-weight: 800 !important;
    color: #fff !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
}
.banner-price {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    color: #fff !important;
    margin: 0 !important;
    line-height: 1 !important;
}
.badge {
    display: inline-block;
    background: rgba(232,255,71,0.1);
    border: 1px solid rgba(232,255,71,0.25);
    color: #e8ff47;
    font-size: 0.63rem;
    padding: 3px 12px;
    border-radius: 20px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-right: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* METRIC CARDS */
[data-testid="metric-container"] {
    background: #111420 !important;
    border: 1px solid #1c1f2e !important;
    border-radius: 14px !important;
    padding: 1.2rem 1.4rem !important;
    transition: border-color 0.2s, transform 0.2s;
}
[data-testid="metric-container"]:hover {
    border-color: #262a3d !important;
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] > div {
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #6b7490 !important;
    font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricValue"] > div {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #fff !important;
}

/* TABS */
[data-baseweb="tab-list"] {
    background: #111420 !important;
    border: 1px solid #1c1f2e !important;
    border-radius: 12px !important;
    padding: 5px !important;
    gap: 3px !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: #6b7490 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 9px !important;
    padding: 8px 20px !important;
    border: none !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: #e8ff47 !important;
    color: #000 !important;
    font-weight: 700 !important;
}

/* SECTION LABELS */
.sec-title {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    color: #fff !important;
    margin: 0 0 0.25rem 0 !important;
}
.sec-sub {
    font-size: 0.68rem !important;
    color: #6b7490 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 1rem !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.divider {
    border: none !important;
    border-top: 1px solid #1c1f2e !important;
    margin: 2rem 0 !important;
}

/* NEWS CARDS */
.news-card {
    background: #111420;
    border: 1px solid #1c1f2e;
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.news-card:hover { border-color: #262a3d; }
.news-headline {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    margin-bottom: 0.35rem !important;
    line-height: 1.4 !important;
}
.news-meta {
    font-size: 0.65rem;
    color: #6b7490;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-family: 'JetBrains Mono', monospace;
}
.news-bull { color: #00e676 !important; }
.news-bear { color: #ff5252 !important; }
.news-neut { color: #6b7490 !important; }

/* DATA TABLE */
[data-testid="stDataFrame"] {
    border: 1px solid #1c1f2e !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* DOWNLOAD BUTTON */
[data-testid="stDownloadButton"] button {
    background: transparent !important;
    border: 1px solid #262a3d !important;
    color: #6b7490 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
    padding: 0.5rem 1.2rem !important;
}
[data-testid="stDownloadButton"] button:hover {
    border-color: #e8ff47 !important;
    color: #e8ff47 !important;
}

/* ALERTS */
[data-testid="stAlert"] {
    background: #111420 !important;
    border: 1px solid #262a3d !important;
    border-radius: 10px !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #07080c; }
::-webkit-scrollbar-thumb { background: #1c1f2e; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #e8ff47; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  PLOTLY BASE THEME
# ══════════════════════════════════════════════

# Helper: returns a fresh layout dict every call — prevents duplicate-key errors
# when callers need to override xaxis/yaxis/title/etc.
def BL(**overrides):
    base = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace", color="#4a5068", size=11),
        xaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                   linecolor="#1c1f2e", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                   linecolor="#1c1f2e", tickfont=dict(size=10)),
        legend=dict(
            bgcolor="rgba(13,15,22,0.85)",
            bordercolor="#1c1f2e", borderwidth=1,
            font=dict(family="JetBrains Mono", size=10),
        ),
        margin=dict(l=10, r=10, t=50, b=10),
        hoverlabel=dict(
            bgcolor="#111420", bordercolor="#262a3d",
            font=dict(family="JetBrains Mono", size=11),
        ),
    )
    base.update(overrides)
    return base

# Keep BASE_LAYOUT as alias for the rare places that don't need overrides
BASE_LAYOUT = BL()

ACCENT      = "#e8ff47"
BLUE        = "#4d9eff"
RED         = "#ff5252"
GREEN       = "#00e676"
ORANGE      = "#ff9800"
PURPLE      = "#b388ff"

# ══════════════════════════════════════════════
#  DATA HELPERS
# ══════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def load_stock(symbol, start, end):
    df = yf.download(symbol, start=start, end=end, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

@st.cache_data(ttl=600, show_spinner=False)
def load_info(symbol):
    try:
        return yf.Ticker(symbol).info
    except:
        return {}

@st.cache_data(ttl=600, show_spinner=False)
def load_news(symbol):
    try:
        t = yf.Ticker(symbol)
        return t.news or []
    except:
        return []

def enrich(df):
    """Add all technical indicators to dataframe."""
    df = df.copy()
    c = df["Close"].squeeze()

    # Returns
    df["Daily_Ret"]  = c.pct_change() * 100
    df["Cum_Return"] = (1 + c.pct_change()).cumprod()

    # Moving averages
    for w in [10, 20, 50, 200]:
        df[f"MA_{w}"] = c.rolling(w).mean()

    # Bollinger Bands (20, 2σ)
    df["BB_Mid"]   = c.rolling(20).mean()
    df["BB_Std"]   = c.rolling(20).std()
    df["BB_Upper"] = df["BB_Mid"] + 2 * df["BB_Std"]
    df["BB_Lower"] = df["BB_Mid"] - 2 * df["BB_Std"]
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Mid"]

    # RSI (14)
    delta = c.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df["RSI"] = 100 - 100 / (1 + gain / loss.replace(0, np.nan))

    # MACD
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    df["MACD"]        = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"]   = df["MACD"] - df["MACD_Signal"]

    # ATR (14)
    h, l, pc = df["High"].squeeze(), df["Low"].squeeze(), c.shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    df["ATR"] = tr.rolling(14).mean()

    # OBV
    direction = np.where(c.diff() >= 0, 1, -1)
    df["OBV"] = (df["Volume"].squeeze() * direction).cumsum()

    return df

def risk_metrics(df, rf=0.04):
    """Compute key risk/return statistics."""
    ret = df["Daily_Ret"].dropna() / 100
    ann = 252
    mu  = float(ret.mean()) * ann
    vol = float(ret.std()) * np.sqrt(ann)
    sharpe = (mu - rf) / vol if vol else 0
    sortino_denom = float(ret[ret < 0].std()) * np.sqrt(ann)
    sortino = (mu - rf) / sortino_denom if sortino_denom else 0

    cum = (1 + ret).cumprod()
    roll_max = cum.cummax()
    dd = (cum - roll_max) / roll_max
    max_dd = float(dd.min())
    calmar = mu / abs(max_dd) if max_dd else 0

    var_95 = float(np.percentile(ret, 5))
    cvar_95 = float(ret[ret <= var_95].mean())

    skew  = float(ret.skew())
    kurt  = float(ret.kurt())
    pos_days = int((ret > 0).sum())
    neg_days = int((ret < 0).sum())
    win_rate = pos_days / (pos_days + neg_days) if (pos_days + neg_days) else 0

    return {
        "Annual Return":  mu,
        "Annual Vol":     vol,
        "Sharpe Ratio":   sharpe,
        "Sortino Ratio":  sortino,
        "Calmar Ratio":   calmar,
        "Max Drawdown":   max_dd,
        "VaR 95%":        var_95,
        "CVaR 95%":       cvar_95,
        "Skewness":       skew,
        "Kurtosis":       kurt,
        "Win Rate":       win_rate,
        "Pos Days":       pos_days,
        "Neg Days":       neg_days,
    }

def scalar(v):
    if isinstance(v, (pd.Series, pd.DataFrame)):
        return float(v.iloc[-1])
    return float(v) if v is not None else 0.0

# ══════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <p style="font-family:'Bricolage Grotesque',sans-serif;font-size:1.05rem;
       font-weight:800;color:#fff;margin-bottom:0.1rem;">⚡ AlphaLens</p>
    <p style="font-size:0.62rem;color:#4a5068;text-transform:uppercase;
       letter-spacing:0.1em;margin-bottom:1.4rem;">Research Platform v2.0</p>
    """, unsafe_allow_html=True)

    st.markdown("**Primary Ticker**")
    ticker = st.text_input("", "AAPL", key="t1",
                           placeholder="e.g. AAPL, TSLA, MSFT").upper().strip()

    st.markdown("**Benchmark**")
    benchmark = st.text_input("", "SPY", key="bench",
                              placeholder="SPY, QQQ, DIA…").upper().strip()

    st.markdown("**Compare Tickers** *(comma-separated)*")
    comp_raw = st.text_input("", "", key="comp",
                             placeholder="MSFT, GOOGL…")
    comp_list = [x.strip().upper() for x in comp_raw.split(",") if x.strip()]

    st.markdown("---")
    st.markdown("**Date Range**")
    presets = st.selectbox("Quick Select", ["Custom", "1M", "3M", "6M", "1Y", "2Y", "5Y"], index=4)

    today = datetime.today()
    preset_map = {
        "1M": today - timedelta(days=30),
        "3M": today - timedelta(days=90),
        "6M": today - timedelta(days=180),
        "1Y": today - timedelta(days=365),
        "2Y": today - timedelta(days=730),
        "5Y": today - timedelta(days=1825),
    }
    default_start = preset_map.get(presets, today - timedelta(days=365))

    col_a, col_b = st.columns(2)
    with col_a:
        start_date = st.date_input("From", default_start, label_visibility="collapsed")
    with col_b:
        end_date = st.date_input("To", today, label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**Portfolio Holdings**")
    portfolio_input = st.text_area(
        "", placeholder="AAPL:10\nMSFT:5\nTSLA:3\n(Ticker:Shares)",
        height=110, key="port", label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Chart Overlays**")
    show_ma20  = st.checkbox("MA 20",  value=True)
    show_ma50  = st.checkbox("MA 50",  value=True)
    show_ma200 = st.checkbox("MA 200", value=False)
    show_bb    = st.checkbox("Bollinger Bands", value=False)
    show_vol   = st.checkbox("Volume Bars", value=True)

    st.markdown("---")
    st.markdown(
        '<p style="font-size:0.6rem;color:#2a2f42;text-align:center;">'
        'Data via Yahoo Finance · For educational use</p>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════
#  LOAD PRIMARY DATA
# ══════════════════════════════════════════════

if not ticker:
    st.warning("Enter a ticker in the sidebar.")
    st.stop()

with st.spinner(f"Loading {ticker}…"):
    raw = load_stock(ticker, start_date, end_date)

if raw is None or raw.empty:
    st.error(f"No data for **{ticker}**. Check the symbol or date range.")
    st.stop()

stock = enrich(raw)
info  = load_info(ticker)
news  = load_news(ticker)

# Latest values
last_close  = scalar(stock["Close"].iloc[-1])
prev_close  = scalar(stock["Close"].iloc[-2]) if len(stock) > 1 else last_close
day_chg     = last_close - prev_close
day_chg_pct = (day_chg / prev_close * 100) if prev_close else 0
rm          = risk_metrics(stock)

# Benchmark
bench_data = load_stock(benchmark, start_date, end_date)
if not bench_data.empty:
    bench_data = enrich(bench_data)

# ══════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════

company_name = info.get("shortName", ticker)
sector       = info.get("sector", "—")
industry     = info.get("industry", "—")
exchange     = info.get("exchange", "—")

up = day_chg >= 0
chg_color = "#00e676" if up else "#ff5252"
arrow = "▲" if up else "▼"

st.markdown(f"""
<div class="banner">
  <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:1.5rem;">
    <div>
      <p class="banner-title">{ticker}
        <span style="font-size:1.6rem;font-weight:400;color:#6b7490;"> · {company_name}</span>
      </p>
      <div style="margin-top:0.5rem;">
        <span class="badge">{exchange}</span>
        <span class="badge">{sector}</span>
        <span class="badge">{industry}</span>
      </div>
    </div>
    <div style="text-align:right;">
      <p class="banner-price">${last_close:,.2f}</p>
      <p style="font-size:1.1rem;color:{chg_color};margin:0.3rem 0 0 0;font-weight:600;font-family:'Bricolage Grotesque',sans-serif;">
        {arrow} {abs(day_chg):.2f} &nbsp;({abs(day_chg_pct):.2f}%)
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  KPI ROW
# ══════════════════════════════════════════════

k1, k2, k3, k4, k5, k6 = st.columns(6)
with k1: st.metric("52W High",   f"${scalar(stock['Close'].max()):,.2f}")
with k2: st.metric("52W Low",    f"${scalar(stock['Close'].min()):,.2f}")
with k3: st.metric("Sharpe",     f"{rm['Sharpe Ratio']:.2f}")
with k4: st.metric("Max DD",     f"{rm['Max Drawdown']*100:.1f}%")
with k5: st.metric("Ann. Vol",   f"{rm['Annual Vol']*100:.1f}%")
with k6: st.metric("Win Rate",   f"{rm['Win Rate']*100:.0f}%")

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  MAIN TABS
# ══════════════════════════════════════════════

tabs = st.tabs([
    "📈  Price & Technicals",
    "⚠️  Risk Analytics",
    "🔍  Stock Screener",
    "📰  News & Sentiment",
    "💼  Portfolio",
])

# ─────────────────────────────────────────────
# TAB 1 — PRICE & TECHNICALS
# ─────────────────────────────────────────────
with tabs[0]:
    rows = 2 if show_vol else 1
    row_h = [0.7, 0.3] if show_vol else [1.0]

    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        row_heights=row_h,
        vertical_spacing=0.04,
    )

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=stock.index,
        open=stock["Open"].squeeze(),
        high=stock["High"].squeeze(),
        low=stock["Low"].squeeze(),
        close=stock["Close"].squeeze(),
        name="OHLC",
        increasing=dict(line=dict(color=GREEN, width=1), fillcolor=GREEN),
        decreasing=dict(line=dict(color=RED,   width=1), fillcolor=RED),
    ), row=1, col=1)

    # MA overlays
    ma_cfg = [(20, BLUE, "dot"), (50, ORANGE, "dash"), (200, PURPLE, "dashdot")]
    flags  = [show_ma20, show_ma50, show_ma200]
    for (w, col, dash), flag in zip(ma_cfg, flags):
        if flag and f"MA_{w}" in stock.columns:
            fig.add_trace(go.Scatter(
                x=stock.index, y=stock[f"MA_{w}"].squeeze(),
                name=f"MA {w}", mode="lines",
                line=dict(color=col, width=1.4, dash=dash),
            ), row=1, col=1)

    # Bollinger Bands
    if show_bb:
        fig.add_trace(go.Scatter(
            x=stock.index, y=stock["BB_Upper"].squeeze(),
            name="BB Upper", mode="lines",
            line=dict(color=ACCENT, width=1, dash="dot"),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=stock.index, y=stock["BB_Lower"].squeeze(),
            fill="tonexty", fillcolor="rgba(232,255,71,0.04)",
            name="BB Lower", mode="lines",
            line=dict(color=ACCENT, width=1, dash="dot"),
        ), row=1, col=1)

    # Volume
    if show_vol:
        vol_colors = [GREEN if r >= 0 else RED
                      for r in stock["Daily_Ret"].fillna(0)]
        fig.add_trace(go.Bar(
            x=stock.index, y=stock["Volume"].squeeze(),
            name="Volume", marker_color=vol_colors, opacity=0.6,
        ), row=2, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1,
                         title_font=dict(size=10))

    fig.update_layout(**BL(
        height=620,
        xaxis_rangeslider_visible=False,
        title=dict(text=f"{ticker} · Price & Technicals",
                   font=dict(family="Bricolage Grotesque", size=16, color="#fff")),
        yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                   linecolor="#1c1f2e", tickfont=dict(size=10), title="Price (USD)"),
    ))
    st.plotly_chart(fig,width="stretch")

    # ── MACD + RSI Row ──
    col_macd, col_rsi = st.columns(2)

    with col_macd:
        st.markdown('<p class="sec-title">MACD</p><p class="sec-sub">12 · 26 · 9 EMA</p>', unsafe_allow_html=True)
        fm = go.Figure()
        fm.add_trace(go.Scatter(
            x=stock.index, y=stock["MACD"].squeeze(),
            name="MACD", line=dict(color=BLUE, width=1.8),
        ))
        fm.add_trace(go.Scatter(
            x=stock.index, y=stock["MACD_Signal"].squeeze(),
            name="Signal", line=dict(color=ORANGE, width=1.4, dash="dot"),
        ))
        hist_colors = [GREEN if v >= 0 else RED for v in stock["MACD_Hist"].fillna(0)]
        fm.add_trace(go.Bar(
            x=stock.index, y=stock["MACD_Hist"].squeeze(),
            name="Histogram", marker_color=hist_colors, opacity=0.7,
        ))
        fm.update_layout(**BASE_LAYOUT, height=280, showlegend=True,
                         title=dict(text="MACD", font=dict(size=13, color="#fff",
                                                            family="Bricolage Grotesque")))
        st.plotly_chart(fm,width="stretch")

    with col_rsi:
        st.markdown('<p class="sec-title">RSI</p><p class="sec-sub">14-Period Relative Strength</p>', unsafe_allow_html=True)
        fr = go.Figure()
        rsi_vals = stock["RSI"].squeeze()
        fr.add_trace(go.Scatter(
            x=stock.index, y=rsi_vals,
            name="RSI", line=dict(color=ACCENT, width=1.8),
            fill="tozeroy", fillcolor="rgba(232,255,71,0.04)",
        ))
        for lvl, col in [(70, RED), (50, "#4a5068"), (30, GREEN)]:
            fr.add_hline(y=lvl, line_dash="dot", line_color=col, line_width=1)
        fr.update_layout(**BL(
            height=280,
            yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                       linecolor="#1c1f2e", tickfont=dict(size=10), range=[0, 100]),
            title=dict(text="RSI (14)", font=dict(size=13, color="#fff",
                                                   family="Bricolage Grotesque"))))
        st.plotly_chart(fr,width="stretch")

    # ── ATR ──
    st.markdown('<p class="sec-title">Average True Range (ATR 14)</p>'
                '<p class="sec-sub">Volatility measure — higher = wider swings</p>', unsafe_allow_html=True)
    fatr = go.Figure()
    fatr.add_trace(go.Scatter(
        x=stock.index, y=stock["ATR"].squeeze(),
        name="ATR", line=dict(color=PURPLE, width=1.6),
        fill="tozeroy", fillcolor="rgba(179,136,255,0.05)",
    ))
    fatr.update_layout(**BASE_LAYOUT, height=220,
                       title=dict(text="ATR (14)", font=dict(size=13, color="#fff",
                                                              family="Bricolage Grotesque")))
    st.plotly_chart(fatr,width="stretch")

# ─────────────────────────────────────────────
# TAB 2 — RISK ANALYTICS
# ─────────────────────────────────────────────
with tabs[1]:
    st.markdown('<p class="sec-title">Risk & Return Profile</p>'
                '<p class="sec-sub">Annualised metrics · 252 trading days</p>', unsafe_allow_html=True)

    # Metric grid
    r1c1, r1c2, r1c3, r1c4 = st.columns(4)
    with r1c1: st.metric("Ann. Return",  f"{rm['Annual Return']*100:.2f}%")
    with r1c2: st.metric("Ann. Volatility", f"{rm['Annual Vol']*100:.2f}%")
    with r1c3: st.metric("Sharpe Ratio",  f"{rm['Sharpe Ratio']:.3f}")
    with r1c4: st.metric("Sortino Ratio", f"{rm['Sortino Ratio']:.3f}")

    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    with r2c1: st.metric("Max Drawdown", f"{rm['Max Drawdown']*100:.2f}%")
    with r2c2: st.metric("Calmar Ratio", f"{rm['Calmar Ratio']:.3f}")
    with r2c3: st.metric("VaR (95%)",    f"{rm['VaR 95%']*100:.2f}%")
    with r2c4: st.metric("CVaR (95%)",   f"{rm['CVaR 95%']*100:.2f}%")

    r3c1, r3c2, r3c3, r3c4 = st.columns(4)
    with r3c1: st.metric("Skewness",  f"{rm['Skewness']:.3f}")
    with r3c2: st.metric("Kurtosis",  f"{rm['Kurtosis']:.3f}")
    with r3c3: st.metric("Win Days",  str(rm['Pos Days']))
    with r3c4: st.metric("Loss Days", str(rm['Neg Days']))

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    left, right = st.columns([3, 2])

    with left:
        # Drawdown chart
        ret_s = stock["Daily_Ret"].dropna() / 100
        cum   = (1 + ret_s).cumprod()
        roll_max = cum.cummax()
        dd   = (cum - roll_max) / roll_max * 100

        fdd = go.Figure()
        fdd.add_trace(go.Scatter(
            x=dd.index, y=dd.values,
            name="Drawdown", fill="tozeroy",
            fillcolor="rgba(255,82,82,0.12)",
            line=dict(color=RED, width=1.5),
        ))
        fdd.update_layout(**BL(
            height=280,
            title=dict(text="Drawdown (%)",
                       font=dict(family="Bricolage Grotesque", size=14, color="#fff")),
            yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                       linecolor="#1c1f2e", tickfont=dict(size=10), title="%"),
        ))
        st.plotly_chart(fdd,width="stretch")

        # Return distribution
        daily_ret_vals = stock["Daily_Ret"].dropna()
        fhist = go.Figure()
        fhist.add_trace(go.Histogram(
            x=daily_ret_vals.values, name="Daily Return",
            nbinsx=60, marker_color=BLUE, opacity=0.75,
        ))
        # VaR line
        var_val = float(np.percentile(daily_ret_vals, 5))
        fhist.add_vline(x=var_val, line_dash="dot", line_color=RED, line_width=1.5,
                        annotation_text=f"VaR 95% {var_val:.2f}%",
                        annotation_font=dict(size=10, color=RED))
        fhist.update_layout(**BASE_LAYOUT, height=260,
                            title=dict(text="Return Distribution",
                                       font=dict(family="Bricolage Grotesque", size=14, color="#fff")),
                            showlegend=False)
        st.plotly_chart(fhist,width="stretch")

    with right:
        # Rolling Sharpe (60-day)
        roll_ret = ret_s.rolling(60).mean() * 252
        roll_vol = ret_s.rolling(60).std() * np.sqrt(252)
        roll_sharpe = (roll_ret - 0.04) / roll_vol

        frs = go.Figure()
        frs.add_trace(go.Scatter(
            x=roll_sharpe.index, y=roll_sharpe.values,
            name="Rolling Sharpe", fill="tozeroy",
            fillcolor="rgba(232,255,71,0.05)",
            line=dict(color=ACCENT, width=1.5),
        ))
        frs.add_hline(y=0, line_dash="dot", line_color="#4a5068", line_width=1)
        frs.update_layout(**BASE_LAYOUT, height=260,
                          title=dict(text="Rolling Sharpe (60d)",
                                     font=dict(family="Bricolage Grotesque", size=14, color="#fff")))
        st.plotly_chart(frs,width="stretch")

        # Beta vs benchmark
        if not bench_data.empty:
            joined = pd.concat([
                stock["Daily_Ret"].rename("stock"),
                bench_data["Daily_Ret"].rename("bench"),
            ], axis=1).dropna()

            if len(joined) > 10:
                cov   = np.cov(joined["stock"], joined["bench"])
                beta  = cov[0, 1] / cov[1, 1]
                corr  = joined["stock"].corr(joined["bench"])

                # Scatter
                fsc = go.Figure()
                fsc.add_trace(go.Scatter(
                    x=joined["bench"], y=joined["stock"],
                    mode="markers", name="Returns",
                    marker=dict(color=BLUE, size=3, opacity=0.5),
                ))
                x_range = np.linspace(joined["bench"].min(), joined["bench"].max(), 100)
                fsc.add_trace(go.Scatter(
                    x=x_range,
                    y=beta * x_range + float(joined["stock"].mean() - beta * joined["bench"].mean()),
                    mode="lines", name=f"β={beta:.2f}",
                    line=dict(color=ACCENT, width=1.5, dash="dot"),
                ))
                fsc.update_layout(**BL(
                    height=280,
                    title=dict(text=f"Beta vs {benchmark} · β={beta:.2f} · ρ={corr:.2f}",
                               font=dict(family="Bricolage Grotesque", size=13, color="#fff")),
                    xaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                               linecolor="#1c1f2e", tickfont=dict(size=10), title=benchmark),
                    yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                               linecolor="#1c1f2e", tickfont=dict(size=10), title=ticker),
                ))
                st.plotly_chart(fsc,width="stretch")

# ─────────────────────────────────────────────
# TAB 3 — STOCK SCREENER / COMPARISON
# ─────────────────────────────────────────────
with tabs[2]:
    st.markdown('<p class="sec-title">Multi-Stock Comparison</p>'
                '<p class="sec-sub">Add tickers in the sidebar to compare</p>', unsafe_allow_html=True)

    all_tickers = [ticker] + [b for b in ([benchmark] + comp_list) if b]
    all_tickers = list(dict.fromkeys(all_tickers))  # deduplicate

    rows_data = []
    price_data = {}

    with st.spinner("Loading comparison data…"):
        for sym in all_tickers:
            d = load_stock(sym, start_date, end_date)
            if d is None or d.empty:
                continue
            d = enrich(d)
            price_data[sym] = d
            rm_s = risk_metrics(d)
            inf_s = load_info(sym)
            rows_data.append({
                "Ticker":      sym,
                "Name":        inf_s.get("shortName", sym)[:22],
                "Sector":      inf_s.get("sector", "—")[:18],
                "Price":       f"${scalar(d['Close'].iloc[-1]):,.2f}",
                "Ann. Ret %":  f"{rm_s['Annual Return']*100:.1f}%",
                "Volatility":  f"{rm_s['Annual Vol']*100:.1f}%",
                "Sharpe":      f"{rm_s['Sharpe Ratio']:.2f}",
                "Max DD %":    f"{rm_s['Max Drawdown']*100:.1f}%",
                "Win Rate":    f"{rm_s['Win Rate']*100:.0f}%",
                "VaR 95%":     f"{rm_s['VaR 95%']*100:.2f}%",
            })

    if rows_data:
        st.dataframe(pd.DataFrame(rows_data).set_index("Ticker"),
                    width="stretch", height=250)

        # Normalised cumulative returns
        st.markdown('<p class="sec-title" style="margin-top:1.4rem;">Normalised Performance</p>'
                    '<p class="sec-sub">Base = 1.0 at start date</p>', unsafe_allow_html=True)

        fcum = go.Figure()
        palette = [ACCENT, BLUE, GREEN, ORANGE, PURPLE, RED, "#e91e63", "#00bcd4"]
        for i, (sym, d) in enumerate(price_data.items()):
            cum = d["Cum_Return"].squeeze()
            fcum.add_trace(go.Scatter(
                x=cum.index, y=cum.values,
                name=sym,
                line=dict(color=palette[i % len(palette)], width=2),
            ))

        fcum.update_layout(**BL(
            height=420,
            title=dict(text="Cumulative Return (normalised)",
                       font=dict(family="Bricolage Grotesque", size=15, color="#fff")),
            yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                       linecolor="#1c1f2e", tickfont=dict(size=10), title="Growth (×1)"),
        ))
        st.plotly_chart(fcum,width="stretch")

        # Correlation heatmap
        if len(price_data) > 1:
            st.markdown('<p class="sec-title">Correlation Matrix</p>'
                        '<p class="sec-sub">Daily return correlations</p>', unsafe_allow_html=True)
            ret_df = pd.DataFrame({
                sym: d["Daily_Ret"] for sym, d in price_data.items()
            }).dropna()
            corr = ret_df.corr()
            z    = corr.values
            syms = corr.columns.tolist()

            fhm = go.Figure(go.Heatmap(
                z=z, x=syms, y=syms,
                colorscale=[[0, RED], [0.5, "#111420"], [1, GREEN]],
                zmin=-1, zmax=1,
                text=np.round(z, 2),
                texttemplate="%{text}",
                textfont=dict(size=11),
                showscale=True,
                colorbar=dict(thickness=12, len=0.8,
                              tickfont=dict(family="JetBrains Mono", size=10)),
            ))
            fhm.update_layout(**BL(
                height=380,
                title=dict(text="Correlation Matrix",
                           font=dict(family="Bricolage Grotesque", size=15, color="#fff")),
                xaxis=dict(showgrid=False, tickfont=dict(size=10)),
                yaxis=dict(showgrid=False, autorange="reversed", tickfont=dict(size=10)),
            ))
            st.plotly_chart(fhm,width="stretch")

    else:
        st.info("Add comparison tickers in the sidebar.")

# ─────────────────────────────────────────────
# TAB 4 — NEWS & SENTIMENT
# ─────────────────────────────────────────────
with tabs[3]:
    st.markdown(f'<p class="sec-title">News Feed · {ticker}</p>'
                '<p class="sec-sub">Latest headlines from Yahoo Finance</p>',
                unsafe_allow_html=True)

    if news:
        # Simple keyword-based sentiment scoring
        bull_kw = ["surge", "rally", "beat", "profit", "growth", "gain", "record",
                   "upgrade", "buy", "bullish", "soar", "jump", "rise", "strong"]
        bear_kw = ["drop", "fall", "miss", "loss", "decline", "cut", "downgrade",
                   "sell", "bearish", "crash", "slump", "warn", "weak", "risk"]

        bull_count = bear_count = neut_count = 0

        for item in news[:20]:
            # yfinance >= 0.2.40 wraps news in a 'content' sub-dict
            content = item.get("content", item)
            title = content.get("title", item.get("title", "No headline"))
            pub   = content.get("provider", {}).get("displayName", "") or item.get("publisher", "")
            ts_raw = content.get("pubDate", "") or item.get("providerPublishTime", 0)
            link  = content.get("canonicalUrl", {}).get("url", "") or item.get("link", "#")

            # Parse timestamp — could be int (unix) or ISO string
            try:
                if isinstance(ts_raw, (int, float)) and ts_raw > 0:
                    ts_fmt = datetime.fromtimestamp(ts_raw).strftime("%b %d, %Y  %H:%M")
                elif isinstance(ts_raw, str) and ts_raw:
                    ts_fmt = ts_raw[:16].replace("T", "  ")
                else:
                    ts_fmt = "—"
            except Exception:
                ts_fmt = "—"
            title_low = title.lower()

            score = sum(1 for w in bull_kw if w in title_low) - \
                    sum(1 for w in bear_kw if w in title_low)

            if score > 0:
                sentiment = '<span class="news-bull">● BULLISH</span>'
                bull_count += 1
            elif score < 0:
                sentiment = '<span class="news-bear">● BEARISH</span>'
                bear_count += 1
            else:
                sentiment = '<span class="news-neut">● NEUTRAL</span>'
                neut_count += 1

            st.markdown(f"""
            <a href="{link}" target="_blank" style="text-decoration:none;">
              <div class="news-card">
                <p class="news-headline">{title}</p>
                <p class="news-meta">{sentiment} &nbsp;·&nbsp; {pub} &nbsp;·&nbsp; {ts_fmt}</p>
              </div>
            </a>
            """, unsafe_allow_html=True)

        # Sentiment summary donut
        st.markdown('<hr class="divider"/>'
                    '<p class="sec-title">Sentiment Summary</p>'
                    '<p class="sec-sub">Keyword-based classification of headlines</p>',
                    unsafe_allow_html=True)

        col_donut, col_stats = st.columns([1, 1])
        with col_donut:
            total = bull_count + bear_count + neut_count or 1
            fdon  = go.Figure(go.Pie(
                labels=["Bullish", "Bearish", "Neutral"],
                values=[bull_count, bear_count, neut_count],
                hole=0.6,
                marker=dict(colors=[GREEN, RED, "#4a5068"],
                            line=dict(color="#07080c", width=2)),
                textfont=dict(family="JetBrains Mono", size=11),
                hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
            ))
            fdon.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                legend=dict(font=dict(family="JetBrains Mono", size=11),
                            bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=20, b=0),
                height=280,
                annotations=[dict(
                    text=f"<b>{total}</b><br>articles",
                    x=0.5, y=0.5, font=dict(size=14, family="Bricolage Grotesque", color="#fff"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fdon,width="stretch")

        with col_stats:
            st.markdown(f"""
            <div style="padding:1rem 0;">
              <div style="margin-bottom:1.2rem;">
                <p style="color:#4a5068;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">Bullish Signals</p>
                <p style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.2rem;font-weight:800;color:{GREEN};margin:0;">{bull_count}</p>
              </div>
              <div style="margin-bottom:1.2rem;">
                <p style="color:#4a5068;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">Bearish Signals</p>
                <p style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.2rem;font-weight:800;color:{RED};margin:0;">{bear_count}</p>
              </div>
              <div>
                <p style="color:#4a5068;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.2rem;">Sentiment Score</p>
                <p style="font-family:'Bricolage Grotesque',sans-serif;font-size:2.2rem;font-weight:800;
                   color:{'#00e676' if bull_count >= bear_count else '#ff5252'};margin:0;">
                  {'+' if bull_count >= bear_count else ''}{bull_count - bear_count:+d}
                </p>
              </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No recent news found for {ticker}.")

# ─────────────────────────────────────────────
# TAB 5 — PORTFOLIO
# ─────────────────────────────────────────────
with tabs[4]:
    st.markdown('<p class="sec-title">Portfolio Tracker</p>'
                '<p class="sec-sub">Enter holdings in sidebar as  TICKER:SHARES</p>',
                unsafe_allow_html=True)

    # Parse holdings
    holdings = {}
    if portfolio_input.strip():
        for line in portfolio_input.strip().splitlines():
            line = line.strip()
            if ":" in line:
                sym, sh = line.split(":", 1)
                try:
                    holdings[sym.strip().upper()] = float(sh.strip())
                except ValueError:
                    pass

    if not holdings:
        st.info("Add holdings in the sidebar (e.g. `AAPL:10`, `MSFT:5`).")
    else:
        port_rows = []
        port_hist = {}

        with st.spinner("Loading portfolio data…"):
            for sym, shares in holdings.items():
                d = load_stock(sym, start_date, end_date)
                if d is None or d.empty:
                    continue
                d = enrich(d)
                latest_p = scalar(d["Close"].iloc[-1])
                first_p  = scalar(d["Close"].iloc[0])
                value    = latest_p * shares
                cost     = first_p  * shares
                pnl      = value - cost
                pnl_pct  = (pnl / cost * 100) if cost else 0
                inf_sym  = load_info(sym)
                rm_sym   = risk_metrics(d)
                port_hist[sym] = d["Close"].squeeze() * shares
                port_rows.append({
                    "Ticker":   sym,
                    "Shares":   shares,
                    "Price":    f"${latest_p:,.2f}",
                    "Value":    f"${value:,.2f}",
                    "P&L":      f"{'+'if pnl>=0 else ''}{pnl:,.2f}",
                    "P&L %":    f"{'+'if pnl_pct>=0 else ''}{pnl_pct:.1f}%",
                    "Sharpe":   f"{rm_sym['Sharpe Ratio']:.2f}",
                    "Max DD":   f"{rm_sym['Max Drawdown']*100:.1f}%",
                    "Sector":   inf_sym.get("sector", "—")[:18],
                })

        if port_rows:
            df_port = pd.DataFrame(port_rows)
            st.dataframe(df_port.set_index("Ticker"),width="stretch", height=300)

            # Summary metrics
            total_val  = sum(scalar(load_stock(s, start_date, end_date)["Close"].iloc[-1]) * h
                             for s, h in holdings.items()
                             if load_stock(s, start_date, end_date) is not None
                             and not load_stock(s, start_date, end_date).empty)

            pcol1, pcol2, pcol3 = st.columns(3)
            with pcol1: st.metric("Total Positions", len(holdings))
            with pcol2: st.metric("Portfolio Value",  f"${total_val:,.2f}")

            # Portfolio value over time
            if port_hist:
                port_series = pd.DataFrame(port_hist).sum(axis=1).dropna()
                fpv = go.Figure()
                fpv.add_trace(go.Scatter(
                    x=port_series.index, y=port_series.values,
                    fill="tozeroy", fillcolor="rgba(77,158,255,0.07)",
                    line=dict(color=BLUE, width=2), name="Portfolio Value",
                ))
                fpv.update_layout(**BL(
                    height=340,
                    title=dict(text="Portfolio Value Over Time",
                               font=dict(family="Bricolage Grotesque", size=15, color="#fff")),
                    yaxis=dict(gridcolor="#1c1f2e", showgrid=True, zeroline=False,
                               linecolor="#1c1f2e", tickfont=dict(size=10), title="Value (USD)"),
                ))
                st.plotly_chart(fpv,width="stretch")

            # Allocation pie
            alloc_labels = list(holdings.keys())
            alloc_values = []
            for sym in alloc_labels:
                d = load_stock(sym, start_date, end_date)
                if d is not None and not d.empty:
                    alloc_values.append(scalar(d["Close"].iloc[-1]) * holdings[sym])
                else:
                    alloc_values.append(0)

            col_pie, col_meta = st.columns([1, 1])
            with col_pie:
                palette_port = [ACCENT, BLUE, GREEN, ORANGE, PURPLE, RED, "#e91e63", "#00bcd4"]
                fp = go.Figure(go.Pie(
                    labels=alloc_labels, values=alloc_values,
                    hole=0.55,
                    marker=dict(colors=palette_port[:len(alloc_labels)],
                                line=dict(color="#07080c", width=2)),
                    textfont=dict(family="JetBrains Mono", size=11),
                    hovertemplate="%{label}: $%{value:,.0f} (%{percent})<extra></extra>",
                ))
                fp.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    legend=dict(font=dict(family="JetBrains Mono", size=10),
                                bgcolor="rgba(0,0,0,0)"),
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=300,
                    annotations=[dict(
                        text="<b>Allocation</b>",
                        x=0.5, y=0.5,
                        font=dict(size=12, family="Bricolage Grotesque", color="#fff"),
                        showarrow=False,
                    )],
                )
                st.plotly_chart(fp, width="stretch")

# ══════════════════════════════════════════════
#  FOOTER — DATA TABLE + EXPORT
# ══════════════════════════════════════════════

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
st.markdown('<p class="sec-title">Raw Data Export</p>'
            '<p class="sec-sub">Enriched OHLCV with all technical indicators</p>',
            unsafe_allow_html=True)

export_cols = ["Open", "High", "Low", "Close", "Volume",
               "Daily_Ret", "Cum_Return", "MA_20", "MA_50",
               "RSI", "MACD", "ATR", "BB_Upper", "BB_Lower"]
export_df = stock[[c for c in export_cols if c in stock.columns]].round(4)

col_dl, col_info2 = st.columns([1, 5])
with col_dl:
    st.download_button(
        "📥 Export CSV",
        data=export_df.to_csv().encode("utf-8"),
        file_name=f"{ticker}_alphalens_{datetime.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
with col_info2:
    st.markdown(
        f'<p style="color:#4a5068;font-size:0.7rem;padding-top:0.6rem;">'
        f'{len(export_df):,} rows · {start_date} → {end_date} · '
        f'{len(export_cols)} indicators</p>',
        unsafe_allow_html=True
    )

st.dataframe(export_df.tail(100), width="stretch", height=300)
