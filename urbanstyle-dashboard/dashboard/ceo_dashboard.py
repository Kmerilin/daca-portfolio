"""
UrbanStyle CEO Dashboard
========================
Kõrgtaseme KPI-d ja müügitulu trend CEO Kristile.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track A.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import load_sales_with_details

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

df = get_data()

# ============================================================
# 3. PÄIS
# ============================================================

st.title("📈 UrbanStyle CEO Dashboard")
st.markdown("*Kõrgtaseme ülevaade — kas ettevõte kasvab?*")
st.divider()

# ============================================================
# 4. KPI KAARDID
# ============================================================

total_revenue = df["total_price"].sum()
unique_customers = df["customer_id"].nunique()

# Kuupõhine kasv: viimane täis kuu vs eelmine kuu
monthly = (
    df.groupby(df["sale_date"].dt.to_period("M"))["total_price"]
    .sum()
    .sort_index()
)

if len(monthly) >= 2:
    last_month = monthly.iloc[-1]
    prev_month = monthly.iloc[-2]
    growth_pct = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
    growth_label = f"{growth_pct:+.1f}%"
    growth_help = "Viimase kuu kasv võrreldes eelmise kuuga"
else:
    growth_label = "N/A"
    growth_help = "Kasvuandmete arvutamiseks on vaja vähemalt 2 kuu andmeid"

col1, col2, col3 = st.columns(3)

col1.metric(
    label="Kogumüügitulu",
    value=f"€{total_revenue:,.0f}",
    help="Kogu ajaloo müügitulu"
)

col2.metric(
    label="Unikaalseid kliente",
    value=f"{unique_customers:,}",
    help="Erinevate klientide koguarv"
)

col3.metric(
    label="Viimase kuu kasv",
    value=growth_label,
    help=growth_help
)

st.divider()

# ============================================================
# 5. MÜÜGITULU TREND (JOONDIAGRAMM)
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

fig.update_traces(
    line_color=BRAND_TEAL,
    line_width=3,
    mode="lines+markers",
    marker=dict(size=7, color=BRAND_TEAL)
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
# 6. JALUS
# ============================================================

st.divider()
st.caption(
    "UrbanStyle.ltd — CEO Dashboard | "
    "DACA Programm, Nädal 5 | "
    f"Andmeid: {len(df):,} müügitehingut"
)
