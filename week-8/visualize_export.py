"""
ROLL C: Visualiseerimine ja salvestamine

Loob Plotly diagrammid Roll B töödeldud andmetest ja ekspordib
tulemused failidesse (CSV + HTML) kausta output/.

Sisend (Roll B väljund):
  - df_weekly: calculate_weekly_aggregates() tulemus
      veerud: sale_date, weekly_revenue, order_count, avg_order_value
  - kpis: calculate_kpis() tulemus
      võtmed: total_revenue, unique_customers, avg_order_value
"""

import os                              # failiteede ja kaustade haldamiseks
from datetime import datetime          # ajatempli loomiseks failinimes

import plotly.express as px            # px = kiire viis tavadiagramme teha (nt joondiagramm)
import plotly.graph_objects as go      # go = madalama taseme, täpsem kontroll (nt KPI-kaardid)


def create_weekly_chart(df_weekly):
    """
    Loob Plotly joondiagrammi nädalastest tululiikumistest.

    NB! Roll B veerunimed on 'sale_date' ja 'weekly_revenue'
    (mitte 'week'/'revenue', nagu ülesande vihjes).
    """
    try:
        # px.line loob joondiagrammi: x-teljel aeg, y-teljel tulu
        fig = px.line(
            df_weekly,
            x="sale_date",             # x-telg = nädala kuupäev (Roll B veerg)
            y="weekly_revenue",        # y-telg = selle nädala tulu (Roll B veerg)
            title="Nädalane tulu",     # diagrammi pealkiri
            markers=True,              # näitab iga nädala kohta täpi joonel
        )
        # update_layout muudab välimust — siin paneme telgedele selged nimed
        fig.update_layout(
            xaxis_title="Nädal",
            yaxis_title="Tulu (€)",
        )
        return fig                     # tagastame valmis diagrammi (ei salvesta veel siin)

    except Exception as e:
        # kui midagi läheb valesti (nt vale veerunimi), prindime vea
        print(f"Viga nädalase diagrammi loomisel: {e}")
        return go.Figure()             # tagastame tühja diagrammi, et programm ei jookseks kokku


def create_kpi_summary(kpis):
    """
    Loob Plotly indicator-kaardid peamistest KPI-dest.

    kpis = {"total_revenue": ..., "unique_customers": ...,
            "avg_order_value": ...}
    """
    try:
        fig = go.Figure()              # alustame tühja diagrammiga, lisame kaardid ükshaaval

        # Esimene kaart: kogukäive
        fig.add_trace(go.Indicator(
            mode="number",                                  # näitab ainult suurt numbrit
            value=kpis.get("total_revenue", 0),             # .get(...,0) = vaikeväärtus 0, kui võti puudub
            number={"prefix": "€", "valueformat": ",.2f"},  # € ette, 2 kohta peale koma, tuhandete eraldaja
            title={"text": "Kogukäive"},                    # kaardi pealkiri
            domain={"row": 0, "column": 0},                 # asukoht ruudustikus: rida 0, veerg 0 (vasakul)
        ))

        # Teine kaart: unikaalsete klientide arv
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get("unique_customers", 0),
            title={"text": "Unikaalsed kliendid"},
            domain={"row": 0, "column": 1},                 # keskmine veerg
        ))

        # Kolmas kaart: keskmine tellimuse väärtus
        fig.add_trace(go.Indicator(
            mode="number",
            value=kpis.get("avg_order_value", 0),
            number={"prefix": "€", "valueformat": ",.2f"},
            title={"text": "Keskmine tellimus"},
            domain={"row": 0, "column": 2},                 # parem veerg
        ))

        # ütleme Plotlyle, et tegu on 1 rea ja 3 veeruga ruudustikuga
        fig.update_layout(
            grid={"rows": 1, "columns": 3, "pattern": "independent"},
            title="Peamised KPI-d",
        )
        return fig

    except Exception as e:
        print(f"Viga KPI kokkuvõtte loomisel: {e}")
        return go.Figure()


def export_results(df, output_dir="output"):
    """
    Salvestab DataFrame'i CSV-sse ajatempliga failinimega.
    Loob output/ kausta, kui see ei eksisteeri.
    Tagastab salvestatud faili tee.
    """
    try:
        # loob kausta; exist_ok=True tähendab "ära anna viga, kui juba olemas"
        os.makedirs(output_dir, exist_ok=True)

        # tänane kuupäev kujul AAAAKKPP, nt 20260626
        date_str = datetime.now().strftime("%Y%m%d")
        # os.path.join liidab kausta + failinime õigesti (õige kaldkriipsuga)
        csv_path = os.path.join(output_dir, f"results_{date_str}.csv")

        # salvestab DataFrame'i CSV-sse; index=False = ära kirjuta reanumbrite veergu
        df.to_csv(csv_path, index=False)
        print(f"Salvestatud CSV: {csv_path}")
        return csv_path                # tagastame tee, et Roll D saaks teada, kuhu salvestati

    except Exception as e:
        print(f"Viga tulemuste salvestamisel: {e}")
        return None


def export_charts(figures, output_dir="output"):
    """
    Salvestab Plotly diagrammid HTML-failidesse.
    figures = {"weekly_revenue": fig1, "kpi_summary": fig2}
    Tagastab salvestatud failide teede nimekirja.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        paths = []                     # kogume siia salvestatud failide teed
        # .items() annab korraga nii nime (failinime jaoks) kui ka diagrammi
        for name, fig in figures.items():
            path = os.path.join(output_dir, f"{name}.html")
            fig.write_html(path)       # salvestab diagrammi iseseisva HTML-failina (avaneb brauseris)
            paths.append(path)
            print(f"Salvestatud diagramm: {path}")

        return paths

    except Exception as e:
        print(f"Viga diagrammide salvestamisel: {e}")
        return []


if __name__ == "__main__":
    # See plokk käivitub ainult siis, kui faili otse jooksutada
    # (python visualize_export.py) — mitte siis, kui seda imporditakse.
    # Testime ilma andmebaasita, kasutades Roll B funktsioone näidisandmetel.
    import pandas as pd
    from transform import (
        clean_data,
        calculate_weekly_aggregates,
        calculate_kpis,
    )

    # väike käsitsi tehtud näidisandmestik (nagu tuleks Roll A-st)
    sample_sales = pd.DataFrame({
        "sale_id": [1, 2, 3, 4, 5, 6],
        "customer_id": [101, 102, 103, 101, 104, 102],
        "sale_date": [
            "2024-01-03", "2024-01-05", "2024-01-12",
            "2024-01-15", "2024-01-22", "2024-01-29",
        ],
        "total_price": [120.0, 200.0, 150.0, 90.0, 300.0, 175.0],
    })

    # Roll B samm-sammult: puhasta -> koonda nädalateks -> arvuta KPI-d
    clean = clean_data(sample_sales)
    weekly = calculate_weekly_aggregates(clean)
    kpis = calculate_kpis(clean)

    # Roll C: loo diagrammid
    fig_weekly = create_weekly_chart(weekly)
    fig_kpi = create_kpi_summary(kpis)

    # Roll C: ekspordi tulemused
    export_results(weekly, "output")
    export_charts(
        {"weekly_revenue": fig_weekly, "kpi_summary": fig_kpi},
        "output",
    )

    print("Valmis — kontrolli output/ kausta.")
