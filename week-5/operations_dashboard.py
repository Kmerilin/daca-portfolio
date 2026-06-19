"""
UrbanStyle Operations Dashboard
================================
Inventuuri olukord ja müük kaupluste lõikes operatsioonijuht Liisile.
DACA Programm, Nädal 5: Visualiseerimise Disain, Track C.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import load_sales, load_inventory, load_products

# ============================================================
# 1. LEHE SEADISTAMINE
# ============================================================

st.set_page_config(
    page_title="UrbanStyle Operations Dashboard",
    page_icon="🏪",
    layout="wide"
)

# ============================================================
# 2. ANDMETE LAADIMINE
# ============================================================

@st.cache_data(ttl=300)
def get_sales_data():
    return load_sales()

@st.cache_data(ttl=300)
def get_inventory_data():
    df_inv = load_inventory()
    df_prod = load_products()

    if df_inv.empty or "product_id" not in df_inv.columns:
        return df_inv

    df = df_inv.merge(
        df_prod[["product_id", "category"]],
        on="product_id",
        how="left"
    )
    return df

df_sales = get_sales_data()
df_inventory = get_inventory_data()

# ============================================================
# 3. PÄIS JA KPI KAARDID
# ============================================================

st.title("🏪 UrbanStyle Operations Dashboard")
st.markdown("*Laoseisud ja müük kaupluste lõikes — ülevaade Liisile*")
st.divider()

total_stores = df_sales["store_location"].fillna("Online").nunique() if "store_location" in df_sales.columns else 0
total_inventory = int(df_inventory["quantity_available"].sum()) if not df_inventory.empty else 0
total_transactions = len(df_sales)

fig_kpi = make_subplots(
    rows=1, cols=3,
    specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]]
)

fig_kpi.add_trace(go.Indicator(
    mode="number",
    value=total_stores,
    title={"text": "Müügikohti", "font": {"size": 16}},
    number={"valueformat": ",", "font": {"size": 40, "color": "#009B8D"}}
), row=1, col=1)

fig_kpi.add_trace(go.Indicator(
    mode="number",
    value=total_inventory,
    title={"text": "Laos kokku (tk)", "font": {"size": 16}},
    number={"valueformat": ",", "font": {"size": 40, "color": "#009B8D"}}
), row=1, col=2)

fig_kpi.add_trace(go.Indicator(
    mode="number",
    value=total_transactions,
    title={"text": "Tehinguid kokku", "font": {"size": 16}},
    number={"valueformat": ",", "font": {"size": 40, "color": "#009B8D"}}
), row=1, col=3)

fig_kpi.update_layout(
    title="UrbanStyle Operations KPI ülevaade",
    title_font_size=20,
    font_family="Arial",
    height=240,
    paper_bgcolor="white"
)

st.plotly_chart(fig_kpi, use_container_width=True)

st.divider()

col_left, col_right = st.columns(2)

# ============================================================
# 4. MÜÜK KAUPLUSTE LÕIKES (SEKTORDIAGRAMM)
# ============================================================

with col_left:
    st.header("Müük kaupluste lõikes")

    # Online orders have null store_location — label them explicitly
    sales_with_location = df_sales.copy()
    sales_with_location["store_location"] = sales_with_location["store_location"].fillna("Online")

    store_revenue = (
        sales_with_location.groupby("store_location")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
    )

    fig_stores = px.pie(
        store_revenue,
        values="total_price",
        names="store_location",
        title="Müük kaupluste lõikes",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_stores.update_traces(
        textposition="inside",
        texttemplate="%{label}<br>%{percent:.0%}",
        hovertemplate="<b>%{label}</b><br>"
                      "Tulu: €%{value:,.0f}<br>"
                      "Osakaal: %{percent:.0%}<extra></extra>"
    )

    fig_stores.update_layout(
        font_family="Arial",
        title_font_size=18,
        showlegend=True
    )

    st.plotly_chart(fig_stores, use_container_width=True)

    if not store_revenue.empty:
        top_store = store_revenue.iloc[0]
        top_pct = top_store["total_price"] / store_revenue["total_price"].sum() * 100
        st.markdown(
            f"> **Äritõlgendus:** {top_store['store_location']} moodustab {top_pct:.0f}% "
            f"kogu müügitulust — see on selgelt tugevaim müügikanal. "
            "Äriliselt tähendab see, et ressursside jaotamisel tuleks arvestada "
            "iga müügikoha panust kogutullu."
        )

# ============================================================
# 5. LAOSEISUD KATEGOORIA JÄRGI (TULPDIAGRAMM)
# ============================================================

with col_right:
    st.header("Laoseisud kategooria järgi")

    if not df_inventory.empty and "category" in df_inventory.columns:
        inv_by_cat = (
            df_inventory.groupby("category")["quantity_available"]
            .sum()
            .reset_index()
            .sort_values("quantity_available", ascending=False)
        )

        # Sorteeri väikseimast suurimani horisontaaldisplayl visuaalselt paremaks
        inv_by_cat_plot = inv_by_cat.sort_values("quantity_available", ascending=True)

        fig_inv = px.bar(
            inv_by_cat_plot,
            x="quantity_available",
            y="category",
            orientation="h",
            title="Laoseisud kategooria järgi",
            labels={
                "quantity_available": "Kogus (tk)",
                "category": "Kategooria"
            },
            color="quantity_available",
            color_continuous_scale="Teal",
            text="quantity_available"
        )

        fig_inv.update_traces(
            texttemplate="%{text:,}",
            textposition="inside",
            insidetextanchor="end"
        )

        fig_inv.update_layout(
            font_family="Arial",
            title_font_size=18,
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_tickformat=",",
            uniformtext_minsize=10,
            uniformtext_mode="hide"
        )

        st.plotly_chart(fig_inv, use_container_width=True)

        if not inv_by_cat.empty:
            low_cat = inv_by_cat.iloc[-1]
            high_cat = inv_by_cat.iloc[0]
            st.markdown(
                f"> **Äritõlgendus:** Kõige rohkem laovaru on kategoorias **{high_cat['category']}** "
                f"({int(high_cat['quantity_available']):,} tk), kõige vähem **{low_cat['category']}** "
                f"({int(low_cat['quantity_available']):,} tk). "
                "Äriliselt tähendab see, et madalate laoseisudega kategooriad vajavad "
                "kiiret täiendamist, et vältida müügivõimaluste kaotust."
            )
    else:
        st.info("Inventuuri andmed puuduvad või kategooria info ei ole saadaval.")

# ============================================================
# 6. JALUS
# ============================================================

st.divider()
st.caption(
    "UrbanStyle.ltd — Operations Dashboard | "
    "DACA Programm, Nädal 5 | "
    f"Müügitehinguid: {total_transactions:,} | "
    f"Laokogus: {total_inventory:,} tk"
)
