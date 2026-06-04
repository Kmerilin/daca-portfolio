"""
UrbanStyle Investor Dashboard
===============================
Interaktiivne dashboard investoritele — Plotly + Streamlit.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track B.
"""
 
import streamlit as st
import pandas as pd
from data_loader import load_sales_with_details
from charts import (
    create_revenue_trend,
    create_top_products,
    create_sales_by_city
)
 
# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================
 
st.set_page_config(
    page_title="UrbanStyle Dashboard",     # brauseri vahekaardi pealkiri
    page_icon="📊",                         # brauseri vahekaardi ikoon
    layout="wide"                           # kasuta kogu laiust
)
 
# ============================================================
# 2. ANDMETE LAADIMINE (cache'iga)
# ============================================================
 
@st.cache_data(ttl=300)  # Cache 5 minutiks (300 sekundit)
def get_data():
    """Laadi andmed Supabase'ist ja cache'i need."""
    return load_sales_with_details()
 
# Laadi andmed
df = get_data()
 
# Teisenda kuupäev
df["sale_date"] = pd.to_datetime(df["sale_date"])
 
# ============================================================
# 3. KÜLGPANEEL (FILTRID)
# ============================================================
 
st.sidebar.header("🔍 Filtrid")
 
# Linnade filter
all_cities = sorted(df["city"].dropna().unique())
selected_cities = st.sidebar.multiselect(
    "Linnad",
    options=all_cities,
    default=all_cities,                     # vaikimisi kõik valitud
    help="Vali linnad, mille andmeid tahad näha"
)
 
# Kuupäeva filter
min_date = df["sale_date"].min().date()
max_date = df["sale_date"].max().date()
date_range = st.sidebar.date_input(
    "Ajavahemik",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Vali algus- ja lõppkuupäev"
)
 
# Kanalite filter
all_channels = sorted(df["channel"].dropna().unique())
selected_channels = st.sidebar.multiselect(
    "Müügikanalid",
    options=all_channels,
    default=all_channels,
    help="online = e-pood, pood = füüsiline kauplus"
)
 
# ============================================================
# 4. ANDMETE FILTREERIMINE
# ============================================================
 
# Rakenda filtrid
df_filtered = df[
    (df["city"].isin(selected_cities)) &
    (df["sale_date"].dt.date >= date_range[0]) &
    (df["sale_date"].dt.date <= date_range[1]) &
    (df["channel"].isin(selected_channels))
].copy()
 
# ============================================================
# 5. PÄIS JA KPI KAARDID
# ============================================================
 
st.title("📊 UrbanStyle Investor Dashboard")
st.markdown("*Reaalajas müügiandmed investorkoosoleku ettevalmistuseks*")
st.divider()
 
# Arvuta KPI-d
total_revenue = df_filtered["total_price"].sum()
total_orders = len(df_filtered)
unique_customers = df_filtered["customer_id"].nunique()
avg_order_value = df_filtered["total_price"].mean() if len(df_filtered) > 0 else 0
 
# KPI kaardid kolmes veerus
col1, col2, col3, col4 = st.columns(4)
 
col1.metric(
    label="Kogumüügitulu",
    value=f"€{total_revenue:,.0f}",
    help="Valitud perioodi kogu müügitulu"
)
 
col2.metric(
    label="Tellimusi",
    value=f"{total_orders:,}",
    help="Valitud perioodi tellimuste arv"
)
 
col3.metric(
    label="Unikaalseid kliente",
    value=f"{unique_customers:,}",
    help="Erinevate klientide arv valitud perioodil"
)
 
col4.metric(
    label="Keskmine tellimus",
    value=f"€{avg_order_value:,.2f}",
    help="Keskmine tellimuse summa"
)
 
st.divider()
 
# ============================================================
# 6. DIAGRAMMID
# ============================================================
 
# Esimene rida: müügitrend (täislaiuses)
st.header("📈 Müügitrendid")
fig_trend = create_revenue_trend(df_filtered)
st.plotly_chart(fig_trend, use_container_width=True)
 
# Teine rida: top tooted ja linnade jaotus kõrvuti
col_left, col_right = st.columns(2)
 
with col_left:
    st.header("🏆 Top Tooted")
    fig_products = create_top_products(df_filtered)
    st.plotly_chart(fig_products, use_container_width=True)
 
with col_right:
    st.header("🏙️ Müük Linnade Kaupa")
    fig_cities = create_sales_by_city(df_filtered)
    st.plotly_chart(fig_cities, use_container_width=True)
 
# ============================================================
# 7. JALUS
# ============================================================
 
st.divider()
st.caption(
    "UrbanStyle.ltd — Investor Dashboard | "
    "DACA Programm, Nädal 5 | "
    f"Andmeid: {len(df_filtered):,} rida"
)
