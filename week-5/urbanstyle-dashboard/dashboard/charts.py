"""
UrbanStyle Dashboard — Diagrammide Loomine
============================================
Kolm põhidiagrammi: müügitrend, top tooted, müük linnade kaupa.
"""
 
import pandas as pd
import plotly.express as px
from data_loader import load_sales_with_details
 
 
def prepare_data():
    """Laadi ja ettevalmista andmed diagrammide jaoks."""
    df = load_sales_with_details()
 
    # Teisenda sale_date kuupäevatüübiks
    df["sale_date"] = pd.to_datetime(df["sale_date"])
 
    return df

def create_revenue_trend(df):
    """
    Joondiagramm: igakuine müügitulu.
    Näitab UrbanStyle müügitrendi ajas.
    """
    # Samm 1: Grupeeri müügid kuu kaupa (nagu SQL GROUP BY)
    monthly = (
        df.groupby(df["sale_date"].dt.to_period("M"))["total_price"]
        .sum()
        .reset_index()
    )
 
    # Samm 2: Teisenda periood tagasi kuupäevaks (Plotly vajab)
    monthly["sale_date"] = monthly["sale_date"].dt.to_timestamp()
 
    # Samm 3: Loo joondiagramm
    fig = px.line(
        monthly,                              # andmed
        x="sale_date",                        # x-telg: kuupäev
        y="total_price",                      # y-telg: müügitulu
        title="UrbanStyle igakuine müügitulu", # diagrammi pealkiri
        labels={                              # telgede sildid
            "sale_date": "Kuu",
            "total_price": "Müügitulu (EUR)"
        }
    )
 
    # Samm 4: Kohanda välimust
    fig.update_layout(
        font_family="Arial",         # font
        title_font_size=20,          # pealkirja suurus
        hovermode="x unified",       # hover näitab kõiki punkte samal x-väärtusel
        yaxis_tickformat=",.0f",     # y-telg: tuhandete eraldaja, 0 kohta peale koma
        yaxis_tickprefix="€",        # y-telg: euro sümbol ette
    )
 
    # Samm 5: Lisa joon, mis näitab keskmist
    avg_revenue = monthly["total_price"].mean()
    fig.add_hline(
        y=avg_revenue,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Keskmine: €{avg_revenue:,.0f}",
        annotation_position="top right"
    )
 
    return fig

def create_top_products(df, top_n=10):
    """
    Horisontaalne tulpdiagramm: top N toodet müügitulu järgi.
    """
    # Samm 1: Grupeeri toote nime järgi ja summeeri
    product_revenue = (
        df.groupby("product_name")["total_price"]
        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)  # Sorteeri langev
        .head(top_n)                                    # Võta top N
    )
 
    # Samm 2: Sorteeri tagasi kasvavasse järjekorda (visuaaliks parem)
    product_revenue = product_revenue.sort_values("total_price", ascending=True)
 
    # Samm 3: Loo horisontaalne tulpdiagramm
    fig = px.bar(
        product_revenue,
        x="total_price",                              # tulba pikkus
        y="product_name",                              # tootenimi
        orientation="h",                               # horisontaalne
        title=f"Top {top_n} toodet müügitulu järgi",
        labels={
            "total_price": "Müügitulu (EUR)",
            "product_name": "Toode"
        },

        color="total_price",                           # värvi tulbad väärtuse järgi
        color_continuous_scale="Teal"                  # värviskeem
    )
 
    # Samm 4: Kohanda välimust
    fig.update_layout(
        font_family="Arial",
        title_font_size=20,
        showlegend=False,                              # peida legend (pole vajalik)
        xaxis_tickformat=",.0f",
        xaxis_tickprefix="€",
        coloraxis_showscale=False                      # peida värviskala
    )
 
    return fig

def create_sales_by_city(df):
    """
    Sektordiagramm: müügitulu jaotus linnade kaupa.
    Näitab, milline linn genereerib kõige rohkem tulu.
    """
    # Samm 1: Grupeeri linna järgi
    city_revenue = (
        df.groupby("city")["total_price"]

        .sum()
        .reset_index()
        .sort_values("total_price", ascending=False)
    )
 
    # Samm 2: Grupeeri väiksemad linnad kokku ("Muud")
    # Linnad, mis annavad alla 3% kogutulust, koondatakse
    total = city_revenue["total_price"].sum()
    city_revenue["osakaal"] = city_revenue["total_price"] / total
    main_cities = city_revenue[city_revenue["osakaal"] >= 0.03].copy()
    other_total = city_revenue[city_revenue["osakaal"] < 0.03]["total_price"].sum()
 
    if other_total > 0:
        other_row = pd.DataFrame({
            "city": ["Muud linnad"],
            "total_price": [other_total],
            "osakaal": [other_total / total]
        })
        main_cities = pd.concat([main_cities, other_row], ignore_index=True)
 
    # Samm 3: Loo sektordiagramm
    fig = px.pie(
        main_cities,
        values="total_price",                          # sektori suurus
        names="city",                                  # sektori nimi
        title="Müügitulu jaotus linnade kaupa",
        color_discrete_sequence=px.colors.qualitative.Set2  # värviskeem
    )
 
    # Samm 4: Kohanda välimust
    fig.update_traces(
        textposition="inside",                         # tekst sektori sees
        textinfo="percent+label",                      # näita protsenti ja nime
        hovertemplate="<b>%{label}</b><br>"
                      "Tulu: €%{value:,.0f}<br>"
                      "Osakaal: %{percent}<extra></extra>"
    )
 
    fig.update_layout(
        font_family="Arial",
        title_font_size=20
    )
 
    return fig

if __name__ == "__main__":
    print("Andmete laadimine...")
    df = prepare_data()
    print(f"Laaditud: {len(df)} rida")
 
    print("\n1. Müügitrendi diagramm...")
    fig1 = create_revenue_trend(df)
    fig1.show()
 
    print("2. Top tooted diagramm...")
    fig2 = create_top_products(df)
    fig2.show()
 
    print("3. Müük linnade kaupa...")
    fig3 = create_sales_by_city(df)
    fig3.show()
 
    print("\nKõik diagrammid loodud!")

