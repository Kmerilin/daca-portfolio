"""
UrbanStyle — Tartu Kaupluse Dashboard & Andmelugu
==================================================
Interaktiivne dashboard, mis keskendub AINULT Tartu kauplusele. Tartu on
UrbanStyle'i teine kauplus, kuid andmed näitavad langustrendi — eesmärk on
leida MIKS ja pakkuda lahendusi (Knaflic Ch 5-6 storytelling).

DACA Programm, Nädal 6: Andmelugu (Roll B), Track B.


"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ============================================================
# 0. NÄDAL 5 ANDMEKIHI TAASKASUTUS
# ============================================================
# Lisame Nädal 5 dashboard-kausta importteele ja laeme sama .env enne
# data_loader importi (data_loader loob Supabase kliendi import-ajal).

_WEEK5_DIR = Path(__file__).resolve().parent.parent / "week-5"
load_dotenv(_WEEK5_DIR / ".env")
sys.path.insert(0, str(_WEEK5_DIR))

# Lisame kohaliku kausta importteele (theme.py ja charts_tartu.py jaoks).
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd  # noqa: E402
import streamlit as st  # noqa: E402
from data_loader import load_sales_with_details, load_customers  # noqa: E402

from charts_tartu import (  # noqa: E402
    eur,
    tartu_kpi_cards,
    tartu_monthly_trend,
    tartu_top_products,
    tartu_segments,
    create_combined_figure,
)
from theme import COLORS  # noqa: E402  (dashboard/ on juba sys.path-il)

# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================

st.set_page_config(
    page_title="UrbanStyle — Tartu",
    page_icon="🏬",
    layout="wide",
)

# ============================================================
# 2. ANDMETE LAADIMINE (cache'iga)
# ============================================================

@st.cache_data(ttl=300)
def get_data():
    """Laadi müügiandmed, lisa kliendi loyalty_tier ja teisenda kuupäev."""
    df = load_sales_with_details()
    df["sale_date"] = pd.to_datetime(df["sale_date"])

    # Põhilaadija toob ainult city/nime — lisame segmendi (loyalty_tier).
    customers = load_customers()[["customer_id", "loyalty_tier"]]
    df = df.merge(customers, on="customer_id", how="left")
    return df

df = get_data()

# ============================================================
# 3. FILTREERIMINE: AINULT TARTU
# ============================================================

df_tartu = df[df["store_location"] == "Tartu"].copy()

# Tallinna kuukeskmine — viitejooneks (benchmark)
tln = df[df["store_location"] == "Tallinn"]
tallinn_monthly_avg = (
    tln.groupby(tln["sale_date"].dt.to_period("M"))["total_price"].sum().mean()
)

# ============================================================
# 4. PÄIS
# ============================================================

st.title("🏬 UrbanStyle — Tartu Kaupluse Dashboard")
st.markdown("*Andmelugu investorile: probleemne laps või võimalus?*")
st.divider()

# ============================================================
# 5. JUHTIDE KOKKUVÕTE (EXECUTIVE SUMMARY)
# ============================================================

# Arvutused kokkuvõtte ja loo jaoks (kõik dünaamiliselt andmetest)
monthly_tartu = (
    df_tartu.groupby(df_tartu["sale_date"].dt.to_period("M"))["total_price"]
    .sum()
)
monthly_tartu = monthly_tartu[monthly_tartu >= 5000].sort_index()  # eemalda hõre saba

tartu_monthly_avg = monthly_tartu.mean()
vs_tallinn_pct = tartu_monthly_avg / tallinn_monthly_avg * 100

peak_period = monthly_tartu.idxmax()
peak_value = monthly_tartu.max()
last_period = monthly_tartu.index[-1]
last_value = monthly_tartu.iloc[-1]
recent_drop_pct = (last_value - peak_value) / peak_value * 100  # tipust viimaseni

st.subheader("📋 Juhtide kokkuvõte")
st.error(
    f"**Tartu on langustrendis ja jääb selgelt Tallinnale alla.**\n\n"
    f"- **Kuukeskmine vaid {eur(tartu_monthly_avg)}** — ehk ~{vs_tallinn_pct:.0f}% "
    f"Tallinna keskmisest ({eur(tallinn_monthly_avg)}/kuu). Tartu teenib umbes poole vähem.\n"
    f"- **Järsk kukkumine tipust:** {eur(peak_value)} ({peak_period}) → "
    f"{eur(last_value)} ({last_period}), **{recent_drop_pct:+.0f}%**.\n"
    f"- **Võimalikud põhjused:** uue konkurendi avamine Tartu kesklinnas ja "
    f"online-kanali eelistus (online-müük ei kajastu poe käibes).\n"
    f"- **Tegevus:** soovitame kaupluse auditit, kohaliku turunduse hoogustamist "
    f"ja tootevaliku kohandamist Tartu nõudlusele."
)

st.divider()

# ============================================================
# 6. KPI KAARDID
# ============================================================

total_revenue = df_tartu["total_price"].sum()
total_orders = len(df_tartu)
avg_order_value = df_tartu["total_price"].mean() if total_orders else 0

# Euroopa vorming: tühik tuhandete eraldajana, koma EI ole eraldaja
total_orders_str = f"{total_orders:,}".replace(",", " ")
delta_vs_tln = tartu_monthly_avg - tallinn_monthly_avg
delta_vs_tln_str = f"{delta_vs_tln:,.0f}".replace(",", " ")

# KPI-kaardid: valge kaart + teal aktsent (slaidi stiil), värvid teemast.
st.markdown(
    f"""
    <style>
    .kpi-card {{
        background-color: {COLORS["white"]};
        border: 1px solid #dddddd;
        border-top: 4px solid {COLORS["teal"]};
        padding: 22px;
        border-radius: 10px;
        text-align: center;
        color: {COLORS["navy"]};
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        min-height: 135px;
    }}

    .kpi-label {{
        font-size: 15px;
        color: #555555;
        margin-bottom: 8px;
    }}

    .kpi-value {{
        font-size: 30px;
        font-weight: 700;
        color: {COLORS["navy"]};
        margin-bottom: 6px;
    }}

    .kpi-delta {{
        font-size: 13px;
        color: #555555;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Kogukäive (Tartu)</div>
            <div class="kpi-value">{eur(total_revenue)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Tellimusi</div>
            <div class="kpi-value">{total_orders_str}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Keskmine tellimus</div>
            <div class="kpi-value">{eur(avg_order_value)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Kuukeskmine vs Tallinn</div>
            <div class="kpi-value">{eur(tartu_monthly_avg)}</div>
            <div class="kpi-delta">
                {delta_vs_tln_str} € vs Tallinn
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# KPI-kaardid allalaaditava PNG-na
kpi_fig = tartu_kpi_cards(df_tartu, tallinn_monthly_avg, tartu_monthly_avg)
kpi_png = kpi_fig.to_image(format="png", width=1600, height=360, scale=2)
st.download_button(
    label="📥 Lae KPI-kaardid alla (PNG)",
    data=kpi_png,
    file_name="tartu_kpi_kaardid.png",
    mime="image/png",
)

st.divider()

# ============================================================
# 7. DIAGRAMMID
# ============================================================

st.header("📈 Müügitrend kuude lõikes")
st.plotly_chart(tartu_monthly_trend(df_tartu, tallinn_monthly_avg),
                use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    st.header("🏆 TOP 5 toodet")
    st.plotly_chart(tartu_top_products(df_tartu), use_container_width=True)

with col_right:
    st.header("👥 Kliendisegmendid")
    st.plotly_chart(tartu_segments(df_tartu), use_container_width=True)

st.divider()

# ============================================================
# 8. ANDMELUGU (NARRATIIV)
# ============================================================

st.header("📖 Andmelugu")
st.markdown(
    f"> **Ülesseade:** Tartu on UrbanStyle'i teine kauplus käibe poolest, "
    f"kuid teenib kuus keskmiselt vaid {eur(tartu_monthly_avg)} — ligikaudu "
    f"poole vähem kui Tallinn ({eur(tallinn_monthly_avg)}).\n\n"
    f"> **Konflikt:** Pärast tippkuud ({peak_period}, {eur(peak_value)}) on käive "
    f"kukkunud {abs(recent_drop_pct):.0f}% tasemele {eur(last_value)} ({last_period}) — "
    f"langus on kiire ja püsiv, mitte hooajaline kõikumine.\n\n"
    f"> **Soovitus:** Soovitame Tartu kaupluse auditit (asukoht, teenindus, laoseis), "
    f"tootevaliku kohandamist kohalikule nõudlusele ning kohaliku turunduskampaania "
    f"käivitamist. Langustrend + selge tegevuskava = tugev lugu investorile: "
    f"ettevõte **näeb** probleeme ja **tegeleb** nendega."
)
