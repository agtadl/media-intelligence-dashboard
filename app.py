import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Interactive Media Intelligence Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

OPENROUTER_API_KEY = st.secrets.get("OPENROUTER_API_KEY", "")

# =========================================================
# FIXED COLOR SYSTEM (tidak ikut tema gelap/terang Chrome/OS)
# =========================================================
BG_MAIN     = "#FFFFFF"
BG_CARD     = "#FFFFFF"
TEXT_MAIN   = "#171A2B"
TEXT_SOFT   = "#5B6072"
BORDER      = "#E6E8F0"
ACCENT      = "#4A56E2"
ACCENT_SOFT = "#EEF0FD"
POSITIVE    = "#2FAE79"
NEUTRAL     = "#F0A93C"
NEGATIVE    = "#E15A5A"
BRAND_A_COLOR = "#4A56E2"
BRAND_B_COLOR = "#F0A93C"
PLOT_FONT = "Inter, 'Segoe UI', sans-serif"

CUSTOM_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', 'Segoe UI', sans-serif !important; }}

.stApp {{ background-color: {BG_MAIN} !important; }}

/* sembunyikan total chrome bawaan Streamlit (toolbar/menu/footer) */
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stStatusWidget"],
[data-testid="stToolbar"] {{ display: none !important; }}

[data-testid="stHeader"] {{
    background: transparent !important;
    height: 2.5rem !important;
}}

.block-container {{ padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1400px; }}

/* ---- Bar upload CSV di paling atas ---- */
.upload-label {{ font-size: 0.88rem; font-weight: 600; color: {TEXT_MAIN} !important; }}
.upload-sub {{ font-size: 0.78rem; color: {TEXT_SOFT} !important; }}

/* ---- Quick Overview ---- */
.qo-title {{ font-size: 1.1rem; font-weight: 700; color: {TEXT_MAIN} !important; margin-bottom: 0.1rem; }}
.qo-sub {{ font-size: 0.85rem; color: {TEXT_SOFT} !important; margin-bottom: 1rem; }}
.qo-item {{ padding-top: 0.5rem; padding-bottom: 1.2rem; }}
.qo-bar {{
    height: 5px;
    width: 100%;
    border-radius: 999px;
    background-color: var(--qo-color);
    margin-bottom: 0.9rem;
}}
.qo-value {{ font-size: 1.7rem; font-weight: 800; color: {TEXT_MAIN} !important; line-height: 1.15; }}
.qo-value small {{ font-size: 0.95rem; font-weight: 600; color: {TEXT_SOFT} !important; }}
.qo-label {{ font-size: 0.85rem; color: {TEXT_SOFT} !important; margin-top: 0.2rem; }}

/* ---- Hero header, rasio 19:6 ---- */
.hero {{
    background: linear-gradient(100deg, {ACCENT} 0%, #6B74EE 100%);
    border-radius: 18px;
    padding: 1.9rem 2.3rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 1.2rem;
    box-shadow: 0 8px 24px rgba(74,86,226,0.18);
}}
.hero h1 {{ color: #FFFFFF !important; font-size: 1.55rem; font-weight: 800; margin: 0 0 0.35rem 0; letter-spacing: -0.02em; line-height: 1.25; }}
.hero p  {{ color: #E7E9FF !important; font-size: 0.9rem; margin: 0; }}

/* ---- Semua container(border=True) dijadikan tampilan "card" ---- */
div[data-testid="stVerticalBlockBorderWrapper"] * {{
    background-color: transparent !important;
}}
div[data-testid="stPlotlyChart"] {{
    background-color: {BG_CARD} !important;
}}
div[data-testid="stArrowVegaLiteChart"],
div[data-testid="stVegaLiteChart"] {{
    background-color: {BG_CARD} !important;
}}

.chart-title {{ font-size: 1.05rem; font-weight: 700; color: {TEXT_MAIN} !important; margin-bottom: 0.1rem; }}
.chart-sub   {{ font-size: 0.82rem; color: {TEXT_SOFT} !important; margin-bottom: 0.4rem; }}

.section-label {{
    font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    color: {ACCENT} !important; margin: 1.4rem 0 0.6rem 0;
}}

/* ---- Tombol insight ---- */
.stButton > button {{
    background-color: {ACCENT_SOFT}; color: {ACCENT} !important;
    border: 1px solid {ACCENT_SOFT}; border-radius: 8px;
    font-weight: 600; font-size: 0.8rem; padding: 0.35rem 0.7rem; width: 100%;
}}
.stButton > button:hover {{ background-color: {ACCENT}; color: #FFFFFF !important; border-color: {ACCENT}; }}

/* ---- Dialog popup insight ---- */
div[data-testid="stDialog"] * {{ color: {TEXT_MAIN} !important; }}
div[data-testid="stDialog"] > div {{ background-color: {BG_CARD} !important; }}
.insight-row {{ display: flex; gap: 0.7rem; padding: 0.6rem 0; border-bottom: 1px solid {BORDER}; }}
.insight-num {{
    background-color: {ACCENT}; color: #FFFFFF !important; min-width: 26px; height: 26px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 700; flex-shrink: 0;
}}
.insight-text {{ font-size: 0.92rem; color: {TEXT_MAIN} !important; line-height: 1.45; }}

/* ---- Tabs ---- */
.stTabs [data-baseweb="tab-list"] {{ gap: 0.4rem; border-bottom: 1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{ color: {TEXT_SOFT} !important; font-weight: 600; font-size: 0.92rem; }}
.stTabs [aria-selected="true"] {{ color: {ACCENT} !important; border-bottom: 3px solid {ACCENT} !important; }}

/* ---- Metric (KPI) ---- */
div[data-testid="stMetric"] {{ background-color: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 14px; padding: 0.9rem 1.1rem; }}
div[data-testid="stMetricLabel"] * {{ color: {TEXT_SOFT} !important; }}
div[data-testid="stMetricValue"] * {{ color: {TEXT_MAIN} !important; }}

.reco-item {{
    background-color: {ACCENT_SOFT}; border-left: 4px solid {ACCENT}; border-radius: 10px;
    padding: 0.85rem 1.1rem; margin-bottom: 0.7rem; font-size: 0.92rem; color: {TEXT_MAIN} !important; line-height: 1.5;
}}

/* ---- Video Analysis: tabel kronologis & framework ABCD ---- */
.breakdown-sub {{ font-size: 0.82rem; color: {TEXT_SOFT} !important; margin-bottom: 0.7rem; }}
.abcd-card {{
    background-color: {BG_CARD}; border: 1px solid {BG_MAIN}; border-left: 4px solid var(--abcd-color);
    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 1rem; height: 100%;
}}
.abcd-title {{ font-size: 0.92rem; font-weight: 700; color: {TEXT_MAIN} !important; margin-bottom: 0.55rem; line-height: 1.4; }}
.abcd-text {{ font-size: 0.86rem; color: {TEXT_SOFT} !important; line-height: 1.55; }}
    div[data-testid="stDataFrame"] {{
    background-color: {BG_CARD} !important;
}}
div[data-testid="stDataFrame"] > div {{
    background-color: {BG_CARD} !important;
}} 

/* ---- Sidebar navigasi ---- */
section[data-testid="stSidebar"] {{
    background-color: {ACCENT_SOFT} !important;
    border-right: 1px solid {BORDER};
}}
section[data-testid="stSidebar"] .block-container {{ padding-top: 1.6rem; }}
.sidebar-brand {{
    font-size: 1rem; font-weight: 800; color: {TEXT_MAIN} !important; margin-bottom: 1rem;
}}
section[data-testid="stSidebar"] .stRadio > label {{ display: none; }}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] {{ gap: 0.3rem; }}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {{
    background-color: {BG_MAIN}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 0.6rem 0.8rem; width: 100%; font-weight: 600; font-size: 0.92rem; color: {TEXT_SOFT} !important;
}}
section[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {{
    background-color: {ACCENT_SOFT}; border-color: {ACCENT}; color: {ACCENT} !important;
}}
.sidebar-key-label {{ font-size: 0.78rem; font-weight: 700; color: {TEXT_SOFT} !important; margin: 1.4rem 0 0.4rem 0; text-transform: uppercase; letter-spacing: 0.06em; }}

/* ---- Kesimpulan Bisnis badge & tombol AI primer ---- */
.kb-badge {{
    display: inline-block; background-color: {ACCENT_SOFT}; color: {ACCENT} !important;
    font-weight: 700; font-size: 0.85rem; padding: 0.45rem 0.9rem; border-radius: 999px; margin-bottom: 1rem;
}}
.stButton > button[kind="primary"] {{
    background-color: {TEXT_MAIN} !important; color: #FFFFFF !important; border: 1px solid {TEXT_MAIN} !important;
    border-radius: 10px; font-weight: 600; font-size: 0.85rem; padding: 0.6rem 1rem; width: 100%;
}}
.stButton > button[kind="primary"]:hover {{ background-color: #000000 !important; border-color: #000000 !important; }}

/* ---- Expander uploader ---- */
div[data-testid="stExpander"] {{ background-color: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 12px; }}

video, iframe {{ border-radius: 14px; }}
/* ---- Samakan tinggi container yang sejajar dalam 1 row ---- */
div[data-testid="stHorizontalBlock"] {{
    align-items: stretch !important;
}}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
    display: flex !important;
    flex-direction: column !important;
}}
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div {{
    display: flex !important;
    flex-direction: column !important;
    flex: 1 !important;
}}
div[data-testid="stVerticalBlockBorderWrapper"] {{
    height: 100% !important;
}}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data
def load_data(source):
    d = pd.read_csv(source)
    d["Date"] = pd.to_datetime(d["Date"], dayfirst=True, errors="coerce")
    return d

# ---------------------------------------------------------
# Data source: default demo dataset, atau upload CSV sendiri
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-key-label">📁 Data Source</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload CSV kamu (opsional)", type=["csv"])

if uploaded is not None:
    df = load_data(uploaded)
    st.sidebar.success("Menggunakan data yang kamu upload.")
else:
    df = load_data("data_default.csv")
    st.sidebar.info("Menampilkan data contoh (demo). Upload CSV untuk lihat data kamu sendiri.")

brands = sorted(df["Brand"].unique())
BRAND_COLOR_MAP = {brands[0]: BRAND_A_COLOR}
if len(brands) > 1:
    BRAND_COLOR_MAP[brands[1]] = BRAND_B_COLOR
SENTIMENT_COLOR_MAP = {"Positif": POSITIVE, "Netral": NEUTRAL, "Negatif": NEGATIVE}

def format_number(n):
    n = float(n)
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if abs(n) >= 1_000:
        return f"{n/1_000:.1f}K"
    return f"{n:.0f}"

# =========================================================
# SIDEBAR — NAVIGASI & OPENROUTER API KEY
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">📡 Menu</div>', unsafe_allow_html=True)
    nav_choice = st.radio("Menu", ["📊 Dashboard", "🎥 Video Analysis"], label_visibility="collapsed")
    st.markdown('<div class="sidebar-key-label">OpenRouter API Key</div>', unsafe_allow_html=True)
    sidebar_api_key = st.text_input(
        "OpenRouter API Key untuk insight AI",
        type="password",
        value=OPENROUTER_API_KEY,
        placeholder="sk-or-...",
        label_visibility="collapsed",
        key="sidebar_api_key",
        help="Sudah terisi otomatis dari kode. Bisa diganti manual kalau perlu pakai key lain.",
    )

# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <h1>📡 Interactive Media Intelligence Dashboard</h1>
        <p>Laporan audit komparatif performa media sosial & video antar merek — sentimen, engagement, platform, dan sebaran lokasi.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# QUICK OVERVIEW
# =========================================================
_total_eng = df["Engagements"].sum()
_total_posts = len(df)
_positif_rate = (df["Sentiment"] == "Positif").mean() * 100
_eng_by_brand = df.groupby("Brand")["Engagements"].sum().sort_values(ascending=False)
_leading_brand = _eng_by_brand.index[0]
_leading_share = _eng_by_brand.iloc[0] / _eng_by_brand.sum() * 100
_brand_vs = " vs ".join(brands)

QO_COLORS = [ACCENT, "#4C8DFF", POSITIVE, "#E8873A"]
qo_items = [
    (f"{format_number(_total_eng)}", "Total Engagements"),
    (f'{_total_posts} <small>posts</small>', "Total Postingan"),
    (f"{_positif_rate:.1f}%", "Sentimen Positif"),
    (f"{_leading_brand}", f"Leading Brand ({_leading_share:.0f}% share)"),
]

with st.container(border=True):
    st.markdown('<div class="qo-title">Quick Overview</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="qo-sub">Ringkasan performa gabungan {_brand_vs}</div>', unsafe_allow_html=True)
    qcols = st.columns(4)
    for qcol, (value, label), color in zip(qcols, qo_items, QO_COLORS):
        with qcol:
            st.markdown(
                f"""<div class="qo-item" style="--qo-color:{color};">
                        <div class="qo-bar"></div>
                        <div class="qo-value">{value}</div>
                        <div class="qo-label">{label}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

# =========================================================
# HELPERS
# =========================================================
@st.dialog("💡 Insight")
def show_insight(title, points):
    st.markdown(f"**{title}**")
    for i, p in enumerate(points, start=1):
        st.markdown(
            f"""<div class="insight-row">
                    <div class="insight-num">{i}</div>
                    <div class="insight-text">{p}</div>
                </div>""",
            unsafe_allow_html=True,
        )

OPENROUTER_MODEL = "anthropic/claude-sonnet-4.5"  # ganti model di sini kalau mau pakai model lain di OpenRouter

def generate_ai_insight(api_key, chart_title, context_text):
    import requests, json as _json
    prompt = (
        "Kamu adalah analis media intelligence yang menulis insight singkat untuk dashboard bisnis.\n"
        f"Chart: {chart_title}\n"
        f"Data pendukung:\n{context_text}\n\n"
        "Tulis TEPAT 3 poin insight (masing-masing 1 kalimat, Bahasa Indonesia) berdasarkan data di atas. "
        "Tandai angka atau istilah penting dengan tag <b>...</b>. "
        "Balas HANYA dengan JSON array berisi 3 string, tanpa markdown code fence, tanpa teks tambahan."
    )
    resp = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400,
        },
        timeout=60,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    pts = _json.loads(raw.strip())
    if not isinstance(pts, list) or not pts:
        raise ValueError("Format balasan AI tidak sesuai.")
    return [str(p) for p in pts[:3]]

def style_fig(fig, height=300, xaxis_title="", yaxis_title=""):
    fig.update_layout(
        font=dict(family=PLOT_FONT, color=TEXT_MAIN, size=12.5),
        plot_bgcolor=BG_CARD,
        paper_bgcolor=BG_CARD,
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        legend=dict(font=dict(color=TEXT_MAIN, size=12)),
    )
    fig.update_xaxes(title=dict(text=xaxis_title, font=dict(color=TEXT_MAIN, size=12)),
                      tickfont=dict(color=TEXT_SOFT, size=11.5), gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(title=dict(text=yaxis_title, font=dict(color=TEXT_MAIN, size=12)),
                      tickfont=dict(color=TEXT_SOFT, size=11.5), gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER)
    return fig

def render_chart(title, subtitle, key, fig):
    with st.container(border=True):
        c1, c2 = st.columns([5, 1.3])
        with c1:
            st.markdown(f'<div class="chart-title">{title}</div><div class="chart-sub">{subtitle}</div>', unsafe_allow_html=True)
        with c2:
            clicked = st.button("💡 Generate Insight", key=key, use_container_width=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    return clicked

# =========================================================
# NAVIGASI HALAMAN (via sidebar)
# =========================================================
if nav_choice == "📊 Dashboard":

    # ------------- ROW 1: Engagement Trend (full width) -------------
    valid_dates = df.dropna(subset=["Date"]).copy()
    if len(valid_dates):
        median_date = valid_dates["Date"].median()
        valid_dates = valid_dates[(valid_dates["Date"] - median_date).abs() <= pd.Timedelta(days=400)]
    trend = (
        valid_dates.groupby([pd.Grouper(key="Date", freq="MS"), "Brand"])["Engagements"]
        .sum().reset_index()
    )
    fig_trend = px.line(trend, x="Date", y="Engagements", color="Brand",
                         color_discrete_map=BRAND_COLOR_MAP, markers=True)
    fig_trend.update_traces(line=dict(width=3), marker=dict(size=7))
    fig_trend.update_xaxes(dtick="M1", tickformat="%b %Y")
    style_fig(fig_trend, height=320, yaxis_title="Total Engagements")

    clicked = render_chart("Engagement Trend Over Time", "Total engagement bulanan per merek", "btn_trend", fig_trend)
    if clicked:
        if not sidebar_api_key:
            st.warning("Masukkan Anthropic API Key di sidebar untuk generate insight.")
        else:
            with st.spinner("Menghasilkan insight..."):
                try:
                    pts = generate_ai_insight(sidebar_api_key, "Engagement Trend Over Time", trend.to_string(index=False))
                    show_insight("Engagement Trend Over Time", pts)
                except Exception as e:
                    st.error(f"Gagal generate insight: {e}")

    # ------------- ROW 2: Sentiment | Platform -------------
    col1, col2 = st.columns(2)

    with col1:
        sent_counts = df.groupby(["Brand", "Sentiment"]).size().reset_index(name="Count")
        fig_sent = make_subplots(
            rows=1, cols=len(brands),
            specs=[[{"type": "domain"}] * len(brands)],
            subplot_titles=brands,
        )
        for i, b in enumerate(brands, start=1):
            d = sent_counts[sent_counts["Brand"] == b]
            fig_sent.add_trace(
                go.Pie(
                    labels=d["Sentiment"], values=d["Count"], hole=0.55,
                    marker=dict(colors=[SENTIMENT_COLOR_MAP.get(s, ACCENT) for s in d["Sentiment"]]),
                    textinfo="percent", textfont=dict(color=TEXT_MAIN, size=11.5),
                    sort=False, showlegend=(i == 1),
                ),
                row=1, col=i,
            )
        style_fig(fig_sent, height=300)
        fig_sent.update_layout(margin=dict(t=40, l=10, r=10, b=10))
        fig_sent.update_annotations(font=dict(color=TEXT_MAIN, size=12.5, family=PLOT_FONT))
        fig_sent.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top", y=-0.05,
                xanchor="center", x=0.5,
                font=dict(color=TEXT_MAIN, size=12),
            ),
            margin=dict(t=40, l=10, r=10, b=50),
        )

        clicked_sent = render_chart("Sentiment Breakdown", "Distribusi sentimen per merek", "btn_sent", fig_sent)
        if clicked_sent:
            if not sidebar_api_key:
                st.warning("Masukkan Anthropic API Key di sidebar untuk generate insight.")
            else:
                with st.spinner("Menghasilkan insight..."):
                    try:
                        pts = generate_ai_insight(sidebar_api_key, "Sentiment Breakdown", sent_counts.to_string(index=False))
                        show_insight("Sentiment Breakdown", pts)
                    except Exception as e:
                        st.error(f"Gagal generate insight: {e}")

    with col2:
        plat = df.groupby(["Platform", "Brand"])["Engagements"].sum().reset_index()
        fig_plat = px.bar(plat, x="Platform", y="Engagements", color="Brand",
                           color_discrete_map=BRAND_COLOR_MAP, barmode="group")
        style_fig(fig_plat, height=300, yaxis_title="Engagements")

        clicked_plat = render_chart("Platform Engagements", "Total engagement per platform & merek", "btn_plat", fig_plat)
        if clicked_plat:
            if not sidebar_api_key:
                st.warning("Masukkan Anthropic API Key di sidebar untuk generate insight.")
            else:
                with st.spinner("Menghasilkan insight..."):
                    try:
                        pts = generate_ai_insight(sidebar_api_key, "Platform Engagements", plat.to_string(index=False))
                        show_insight("Platform Engagements", pts)
                    except Exception as e:
                        st.error(f"Gagal generate insight: {e}")

    # ------------- ROW 3: Media Type | Top Locations -------------
    col3, col4 = st.columns(2)

    with col3:
        media_types_all = df["Media_Type"].unique()
        MEDIA_COLORS = [ACCENT, "#8B92F0", "#C7CBFA", "#D9DCFB"]
        MEDIA_COLOR_MAP = {m: MEDIA_COLORS[i % len(MEDIA_COLORS)] for i, m in enumerate(media_types_all)}

        media_counts = df.groupby(["Brand", "Media_Type"]).size().reset_index(name="Count")
        fig_media = make_subplots(
            rows=1, cols=len(brands),
            specs=[[{"type": "domain"}] * len(brands)],
            subplot_titles=brands,
        )
        for i, b in enumerate(brands, start=1):
            d = media_counts[media_counts["Brand"] == b]
            fig_media.add_trace(
                go.Pie(
                    labels=d["Media_Type"], values=d["Count"], hole=0.55,
                    marker=dict(colors=[MEDIA_COLOR_MAP[m] for m in d["Media_Type"]]),
                    textinfo="percent", textfont=dict(color=TEXT_MAIN, size=11.5),
                    sort=False, showlegend=(i == 1),
                ),
                row=1, col=i,
            )
        style_fig(fig_media, height=330)
        fig_media.update_annotations(font=dict(color=TEXT_MAIN, size=12.5, family=PLOT_FONT))
        fig_media.update_layout(
            legend=dict(
                orientation="h",
                yanchor="top", y=-0.05,
                xanchor="center", x=0.5,
                font=dict(color=TEXT_MAIN, size=12),
            ),
            margin=dict(t=40, l=10, r=10, b=50),
        )

        clicked_media = render_chart("Media Type Mix", "Komposisi jenis konten per merek", "btn_media", fig_media)
        if clicked_media:
            if not sidebar_api_key:
                st.warning("Masukkan Anthropic API Key di sidebar untuk generate insight.")
            else:
                with st.spinner("Menghasilkan insight..."):
                    try:
                        pts = generate_ai_insight(sidebar_api_key, "Media Type Mix", media_counts.to_string(index=False))
                        show_insight("Media Type Mix", pts)
                    except Exception as e:
                        st.error(f"Gagal generate insight: {e}")

    with col4:
        top_locs = df.groupby("Location")["Engagements"].sum().sort_values(ascending=False).head(5).index
        loc = df[df["Location"].isin(top_locs)].groupby(["Location", "Brand"])["Engagements"].sum().reset_index()
        loc_order = df[df["Location"].isin(top_locs)].groupby("Location")["Engagements"].sum().sort_values().index
        fig_loc = px.bar(loc, x="Engagements", y="Location", color="Brand", orientation="h",
                          color_discrete_map=BRAND_COLOR_MAP, barmode="group",
                          category_orders={"Location": list(loc_order)})
        style_fig(fig_loc, height=330, xaxis_title="Engagements")

        clicked_loc = render_chart("Top 5 Locations", "Wilayah dengan kontribusi engagement tertinggi per merek", "btn_loc", fig_loc)
        if clicked_loc:
            if not sidebar_api_key:
                st.warning("Masukkan Anthropic API Key di sidebar untuk generate insight.")
            else:
                with st.spinner("Menghasilkan insight..."):
                    try:
                        pts = generate_ai_insight(sidebar_api_key, "Top 5 Locations", loc.to_string(index=False))
                        show_insight("Top 5 Locations", pts)
                    except Exception as e:
                        st.error(f"Gagal generate insight: {e}")

# =========================================================
# TAB 2 — VIDEO ANALYSIS
# =========================================================
elif nav_choice == "🎥 Video Analysis":
    st.markdown('<div class="section-label">Video Yang Dianalisis</div>', unsafe_allow_html=True)

    # TODO: ganti dengan link YouTube video yang dianalisis
    YOUTUBE_URL = "https://youtu.be/sv1XMvvKQTY?si=dpOrS51UP0hjQYjG"
    with st.container(border=True):
        st.video(YOUTUBE_URL)

    st.markdown('<div class="section-label">Tabel Kronologis (Breakdown per Menit)</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<div class="breakdown-sub">Isi hasil ekstraksi dari Google AI Studio (unggah video &rarr; prompt breakdown menit-per-menit).</div>',
            unsafe_allow_html=True,
        )
        # TODO: ganti dengan hasil breakdown video yang sebenarnya
        breakdown = pd.DataFrame({
    "Waktu": [
        "00:00", "00:05", "00:15", "00:18", "00:37", "00:58", "01:35", "01:55",
        "02:11", "03:00", "03:55", "04:20", "05:40", "06:30", "07:15", "08:25",
        "09:12", "10:30", "12:45", "13:08", "14:02", "15:42", "16:34", "17:08",
        "17:22", "18:41", "20:47", "21:25", "23:25", "25:35", "28:40", "29:50", "30:10"
    ],
    "Adegan": [
        "Emil dan host lainnya memperkenalkan Artha yang mahir bersalawat.",
        "Artha mulai menyanyikan lirik salawat dengan merdu.",
        "Emil mencoba menyambung nyanyian namun tidak tahu liriknya.",
        "Cuplikan pembuka acara \"Slay & Say\" menampilkan Artha beraktivitas di kamar mandi.",
        "Emil dan host menyambut penonton dan menyapa Artha sebagai bintang tamu.",
        "Artha meminta maaf karena baru bisa hadir karena jadwal yang padat.",
        "Artha memperkenalkan diri dengan gaya bicaranya yang sangat cepat.",
        "Pembahasan mengenai gaya bicara Artha yang sombong namun jujur.",
        "Artha menjelaskan asal usul gaya bicaranya yang cepat karena pengaruh lingkungan.",
        "Artha menceritakan masa lalunya yang tinggal di kontrakan.",
        "Artha bercerita tentang upayanya menutupi kemiskinan saat mulai menjadi influencer.",
        "Artha mengungkapkan alasan sebenarnya bicara cepat: menghindari suara ayam.",
        "Emil memuji Artha sebagai wanita yang memiliki nilai diri yang tinggi.",
        "Artha menceritakan inspirasi tren goyangan \"kedat-kedut\" miliknya.",
        "Cerita tentang fans Indonesia yang mengklaim tren tersebut milik Artha hingga ke luar negeri.",
        "Host menanyakan perasaan Artha yang kini sudah menjadi aktris film.",
        "Artha mengaku sempat risih karena harus akting menangis sesuai arahan.",
        "Artha menyebutkan beberapa aktor senior yang menjadi lawan mainnya.",
        "Emil menanyakan tentang keinginan Artha menjadi penyanyi mengikuti wasiat ayahnya.",
        "Artha menceritakan kenangan sedih bersama ayahnya yang memintanya jadi penyanyi.",
        "Artha menyanyikan sedikit cuplikan lagu yang dia buat khusus untuk ayahnya.",
        "Artha kembali diminta menunjukkan kemampuannya bersalawat.",
        "Artha menyanyikan salawat dengan penuh penghayatan (sama dengan pembukaan).",
        "Artha menyinggung tetangga yang suka membicarakannya karena pakaian seksinya.",
        "Pengakuan Artha bahwa ia sudah berkali-kali khatam Al-Qur'an.",
        "Klarifikasi mengenai rumor Artha pindah agama karena foto bersama pacar.",
        "Permainan \"Dar Dare Dor\" dimulai dengan pertanyaan untuk Artha.",
        "Artha menjawab tawaran brand yang memintanya cuci muka di depan tukang ayam.",
        "Pertanyaan untuk Emil tentang content creator yang aslinya sangat berbeda.",
        "Pertanyaan terakhir mengenai content creator yang aslinya beda (host lainnya ikut menimpali).",
        "Artha berbagi tips diet dan kebiasaan makannya.",
        "Artha mengungkapkan tujuan hidupnya untuk menyekolahkan adik-adiknya.",
        "Emil menutup acara dan mengucapkan terima kasih kepada Artha.",
    ],
    "Catatan": [
        "\"Tapi katanya Artha ini jago salawatan juga lho.\"",
        "\"Ilahilas tulil firdausi si-ala...\"",
        "\"Sambungin, sambungin! Gak tahu liriknya.\"",
        "(Musik pembuka dan efek suara grafis)",
        "\"Welcome back to Slay and Say! Bintang tamunya sudah lama gue undang, Artha!\"",
        "\"Sudah lama nunggu, maaf banget ya.\"",
        "\"Halo semua kenalin nama gue Artha... umur 21 tahun... sebulan dapat empat digit.\"",
        "\"Gue memang sombong, orang-orang tahu kok.\"",
        "\"Kenapa gue bisa ngomong secepat ini? Gue orang Betawi Sunda, tinggal di Kampung Raden.\"",
        "\"Dulu gue tinggal di kontrakan warisan nenek gue.\"",
        "\"Gue dulu gak mau orang tahu kalau gue orang miskin... gue harus cantik banget.\"",
        "\"Gue harus ribut sama ayam, harus dulu-duluan sebelum ayam berkokok pas lagi ambil video.\"",
        "\"Loe itu likeable banget tahu buat perempuan yang punya value.\"",
        "\"Sebenarnya ada orang bule yang bikin video kedat-kedut, terus gue ikutan.\"",
        "\"Orang Indo banyak yang komen 'anak buah Artha', bulenya sampai gak terima.\"",
        "\"Gimana rasanya sekarang loe sudah main di series?\"",
        "\"Gue disuruh 'Ayo nangis!', enak aja nyuruh-nyuruh gue.\"",
        "\"Pemainnya sudah senior-senior, ada Adipati Dolken, Winky Wiryawan.\"",
        "\"Dulu loe pengen jadi penyanyi karena mengikuti alur almarhum bokap?\"",
        "\"Bokap gue di IGD pas napasnya sudah susah bilang, 'Jadi penyanyi ya'.\"",
        "\"Lepaskanlah ikatanku...\"",
        "\"Coba dong kita pengen denger nih Kak.\"",
        "\"Ilahilas tulil firdausi si-ala...\"",
        "\"Anaknya pakai baju seksi... tapi loe tahu gak? Loe ngaji sama gue, loe kalah!\"",
        "\"Gue hafal semua juz 30, gue sudah pernah khatam berapa kali.\"",
        "\"Netizen Indonesia itu tolol otaknya, gue cuma foto adat di Bali bukan pindah agama.\"",
        "\"Apa tawaran kerja sama brand teraneh yang pernah loe dapat?\"",
        "\"Ada brand suruh gue ke tukang seblak sama tukang ayam buat hapus make up pakai oil mereka.\"",
        "\"Siapa content creator yang image-nya bagus tapi aslinya beda banget?\"",
        "\"Sebenarnya Emil sih, soalnya mukanya kalau di depan orang jutek parah.\"",
        "\"Gue jarang banget olahraga, gue benar-benar gak makan nasi.\"",
        "\"Gue pengen ngeratuin keluarga gue... adik-adik gue semuanya harus kuliah di London.\"",
        "\"Thank you Artha sudah datang ke Slay and Say! See you guys next week!\"",
    ],
})
    st.dataframe(breakdown, use_container_width=True, hide_index=True)
    
    st.markdown('<div class="section-label">Evaluasi Framework ABCD</div>', unsafe_allow_html=True)
    # TODO: ganti dengan hasil evaluasi ABCD yang sebenarnya
    abcd_items = [
        ("#4A56E2", "Attention", "Apakah 3 detik pertama menarik perhatian?",
         "Video dibuka dengan Arthada menyanyikan salawat, bukan konten komedi/viral seperti biasa dikenal dari "
         "dirinya. Pembukaan ini justru jadi hook yang kontras dan mengejutkan karena tidak sesuai ekspektasi "
         "penonton terhadap image \"sombong cepat ngomong\" yang selama ini melekat, sehingga cukup efektif "
         "menahan penonton untuk terus menonton."),
        ("#4C8DFF", "Connection", "Apakah video membangun koneksi emosional?",
         "Ya, cukup kuat. Ada momen personal yang emosional (cerita ayah yang minta dinyanyikan lagu saat di IGD), "
         "cerita masa lalu di-bully, serta klarifikasi rumor pindah agama yang membuat penonton melihat sisi "
         "vulnerable Arthada di balik citra publiknya yang \"sombong\". Ini membangun simpati dan hubungan "
         "emosional yang lebih dalam dengan audiens."),
        ("#2FAE79", "Branding", "Seberapa jelas & konsisten brand ditampilkan?",
         "Branding program \"Slay & Say\" ditampilkan lewat intro animasi di detik ke-18 dan identitas visual "
         "(nama program, host Mochamado) konsisten muncul di sepanjang video. Namun branding brand Arthada "
         "sendiri lebih terbangun lewat personal storytelling (ciri khas bicara cepat, gaya \"sombong\") "
         "ketimbang elemen visual/logo formal."),
        ("#E8873A", "Direction", "Apakah CTA jelas & mengarahkan aksi?",
         "CTA di video ini cenderung lemah/implisit — tidak ada ajakan eksplisit untuk follow, subscribe, atau "
         "action tertentu di akhir video. Penutupan hanya berupa ucapan terima kasih dan credit title, sehingga "
         "dari sisi konversi/direction framework ABCD, bagian ini jadi titik lemah dibanding 3 elemen lainnya."),
    ]
    abcd_row1 = st.columns(2)
    abcd_row2 = st.columns(2)
    for col, (color, title, question, answer) in zip(abcd_row1 + abcd_row2, abcd_items):
        with col:
            st.markdown(
                f"""<div class="abcd-card" style="--abcd-color:{color};">
                        <div class="abcd-title">{title} — {question}</div>
                        <div class="abcd-text">{answer}</div>
                    </div>""",
                unsafe_allow_html=True,
            )

    st.markdown('<div class="section-label">Screenshot Adegan Kunci</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<div class="breakdown-sub">Tempel link Google Drive (pastikan sharing diatur \'Anyone with the link\') untuk menampilkan gambar.</div>',
            unsafe_allow_html=True,
        )
        # TODO: ganti dengan link Google Drive (format: https://drive.google.com/uc?id=FILE_ID)
        screenshot_link = st.text_input("Link gambar Google Drive (opsional)")
        if screenshot_link:
            try:
                st.image(screenshot_link, use_container_width=True)
            except Exception:
                st.markdown("*Gambar belum tersedia — pastikan link Google Drive sudah 'Anyone with the link'.*")

# =========================================================
# KESIMPULAN BISNIS & REKOMENDASI STRATEGIS
# =========================================================
st.markdown('<div class="section-label">Kesimpulan Bisnis & Rekomendasi Strategis</div>', unsafe_allow_html=True)

kb_summary = df.groupby("Brand").agg(
    Total_Engagement=("Engagements", "sum"),
    Rata_rata_Engagement=("Engagements", "mean"),
    Jumlah_Post=("Engagements", "count"),
).reset_index()
kb_summary["Total_Engagement"] = kb_summary["Total_Engagement"].round(0).astype(int)
kb_summary["Rata_rata_Engagement"] = kb_summary["Rata_rata_Engagement"].round(0).astype(int)
kb_ranked = kb_summary.sort_values("Total_Engagement", ascending=False).reset_index(drop=True)
kb_winner = kb_ranked.loc[0, "Brand"]

with st.container(border=True):
    st.markdown(f'<div class="kb-badge">{kb_winner} unggul dalam total engagement</div>', unsafe_allow_html=True)
    kb_display = kb_ranked.copy()
    kb_display["Total_Engagement"] = kb_display["Total_Engagement"].apply(lambda x: f"{x:,}".replace(",", "."))
    kb_display["Rata_rata_Engagement"] = kb_display["Rata_rata_Engagement"].apply(lambda x: f"{x:,}".replace(",", "."))
    st.dataframe(kb_display, use_container_width=True, hide_index=True)

st.markdown('<div class="section-label">AI-Generated Business Conclusion</div>', unsafe_allow_html=True)
with st.container(border=True):
    generate_clicked = st.button("✨ Generate AI Insight", type="primary")

    if generate_clicked:
        if not OPENROUTER_API_KEY:
            st.warning("Isi dulu OPENROUTER_API_KEY di bagian atas kode dengan API key OpenRouter kamu.")
        else:
            with st.spinner("Menghasilkan kesimpulan bisnis..."):
                try:
                    import requests
                    data_summary = kb_ranked.to_string(index=False)
                    prompt = (
                        "Kamu adalah analis media intelligence. Berdasarkan ringkasan data berikut, tulis "
                        "kesimpulan bisnis singkat (3-5 kalimat) dalam Bahasa Indonesia yang menjelaskan brand "
                        "mana yang unggul dan kenapa, lalu tutup dengan 1 rekomendasi strategis untuk brand yang "
                        "tertinggal.\n\n" + data_summary
                    )
                    resp = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
                        json={
                            "model": OPENROUTER_MODEL,
                            "messages": [{"role": "user", "content": prompt}],
                            "max_tokens": 500,
                        },
                        timeout=60,
                    )
                    resp.raise_for_status()
                    st.session_state["ai_business_conclusion"] = resp.json()["choices"][0]["message"]["content"]
                except Exception as e:
                    st.error(f"Gagal generate insight: {e}")

    if st.session_state.get("ai_business_conclusion"):
        st.markdown(f'<div class="reco-item">{st.session_state["ai_business_conclusion"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="qo-sub">Klik tombol di atas untuk menghasilkan kesimpulan bisnis otomatis dari Claude.</div>',
            unsafe_allow_html=True,
        )
