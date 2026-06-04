"""
UrbanStyle CEO Dashboard
========================
Kõrgtaseme KPI-d ja müügitulu trend CEO Kristile.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track A.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import load_sales_with_details, load_customers

BRAND_TEAL = "#009B8D"

# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================

st.set_page_config(
    page_title="UrbanStyle CEO Dashboard",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# 2. ANDMETE LAADIMINE
# ============================================================

@st.cache_data(ttl=300)
def get_data():
    df = load_sales_with_details()
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

@st.cache_data(ttl=300)
def get_total_customers():
    return len(load_customers())

df = get_data()
total_registered_customers = get_total_customers()

# ============================================================
# 3. PÄIS
# ============================================================

st.title("📈 UrbanStyle CEO Dashboard")
st.markdown("*Kõrgtaseme ülevaade — kas ettevõte kasvab?*")
st.divider()

# ============================================================
# 4. ARVUTUSED
# ============================================================

total_revenue = df["total_price"].sum()

monthly = (
    df.groupby(df["sale_date"].dt.to_period("M"))["total_price"]
    .sum()
    .sort_index()
)

# MoM growth: compare last two months with meaningful revenue (>5000 EUR)
# to avoid distortion from sparse/incomplete months at the tail of the dataset
meaningful = monthly[monthly > 5000]
if len(meaningful) >= 2:
    last_month = meaningful.iloc[-1]
    prev_month = meaningful.iloc[-2]
    growth_pct = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
    growth_period = f"{meaningful.index[-2]} → {meaningful.index[-1]}"
else:
    growth_pct = 0
    growth_period = ""

# ============================================================
# 5. DIAGRAMM 1 — KPI INDIKAATORID (eksporditav)
# ============================================================

st.header("Peamised tulemusnäitajad (KPI)")

fig_kpi = make_subplots(
    rows=1, cols=3,
    specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
)

fig_kpi.add_trace(go.Indicator(
    mode="number",
    value=total_revenue,
    title={"text": "Kogumüügitulu", "font": {"size": 16}},
    number={"prefix": "€", "valueformat": ",.0f", "font": {"size": 40, "color": BRAND_TEAL}}
), row=1, col=1)

fig_kpi.add_trace(go.Indicator(
    mode="number",
    value=total_registered_customers,
    title={"text": "Registreeritud kliente", "font": {"size": 16}},
    number={"valueformat": ",", "font": {"size": 40, "color": BRAND_TEAL}}
), row=1, col=2)

fig_kpi.add_trace(go.Indicator(
    mode="number+delta",
    value=growth_pct,
    title={"text": f"Kuukasv ({growth_period})", "font": {"size": 14}},
    number={"suffix": "%", "valueformat": ".1f", "font": {"size": 40, "color": BRAND_TEAL}},
    delta={"reference": 0, "valueformat": ".1f", "suffix": "%"}
), row=1, col=3)

fig_kpi.update_layout(
    title="UrbanStyle KPI ülevaade",
    title_font_size=20,
    font_family="Arial",
    height=240,
    paper_bgcolor="white"
)

st.plotly_chart(fig_kpi, use_container_width=True)

st.markdown(
    "> **Äritõlgendus:** Kolm põhinäitajat annavad CEO-le kohese vastuse — "
    "kui palju tulu teenisime, kui suur on kliendibaas ja kas viimane kuu kasvas. "
    "Äriliselt tähendab positiivne kasvuprotsent, et ettevõte liigub õiges suunas."
)

st.divider()

# ============================================================
# 6. DIAGRAMM 2 — MÜÜGITULU TREND (JOONDIAGRAMM)
# ============================================================

st.header("Müügitulu trend kuude lõikes")

monthly_df = monthly.reset_index()
monthly_df.columns = ["kuu", "tulu"]
monthly_df["kuu"] = monthly_df["kuu"].dt.to_timestamp()

fig = px.line(
    monthly_df,
    x="kuu",
    y="tulu",
    title="UrbanStyle müügitulu trend",
    labels={"kuu": "Kuu", "tulu": "Müügitulu (EUR)"}
)

idx_max = monthly_df["tulu"].idxmax()
idx_min = monthly_df["tulu"].idxmin()
monthly_df["label"] = ""
monthly_df.loc[idx_max, "label"] = f"€{monthly_df.loc[idx_max, 'tulu']:,.0f}"
monthly_df.loc[idx_min, "label"] = f"€{monthly_df.loc[idx_min, 'tulu']:,.0f}"

fig.update_traces(
    line_color=BRAND_TEAL,
    line_width=3,
    mode="lines+markers+text",
    marker=dict(size=7, color=BRAND_TEAL),
    text=monthly_df["label"],
    textposition="top center",
    textfont=dict(size=11, color=BRAND_TEAL)
)

avg_revenue = monthly_df["tulu"].mean()
fig.add_hline(
    y=avg_revenue,
    line_dash="dash",
    line_color="gray",
    annotation_text=f"Keskmine: €{avg_revenue:,.0f}",
    annotation_position="top right"
)

fig.update_layout(
    font_family="Arial",
    title_font_size=20,
    hovermode="x unified",
    yaxis_tickformat=",.0f",
    yaxis_tickprefix="€",
    plot_bgcolor="white",
    paper_bgcolor="white",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown(
    "> **Äritõlgendus:** See diagramm näitab UrbanStyle igakuist müügitulu ajas — "
    "tõusev trend tähendab kasvu, langev trend nõuab tähelepanu. "
    "Äriliselt tähendab see, et saame hinnata, kas äri kasvab ootuspäraselt "
    "ja kas on vaja müügistrateegiat kohandada."
)

# ============================================================
# 7. JALUS
# ============================================================

st.divider()
st.caption(
    "UrbanStyle.ltd — CEO Dashboard | "
    "DACA Programm, Nädal 5 | "
    f"Andmeid: {len(df):,} müügitehingut"
)
