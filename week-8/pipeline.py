"""
ROLL D: Automatiseerimisskript

Ühendab rollide A, B ja C moodulid üheks pipeline'iks:
    extract -> transform -> visualize -> export

Käivitamine:
    python pipeline.py
"""

import logging                         # logimiseks (näitab, mis igal sammul toimub)
import time                            # koguaja mõõtmiseks

# Impordime teiste rollide funktsioonid otse nende failidest:
# Roll A — andmete pärimine
from data_fetcher import fetch_sales
# Roll B — andmete puhastamine ja koondamine
from transform import (
    clean_data,
    calculate_weekly_aggregates,
    calculate_kpis,
)
# Roll C — visualiseerimine ja salvestamine
from visualize_export import (
    create_weekly_chart,
    create_kpi_summary,
    export_results,
    export_charts,
)

# Logimise seadistus: tase INFO ja kuvab aja + taseme + sõnumi
logging.basicConfig(
    level=logging.INFO,                # näitab INFO ja kõrgema taseme teateid
    format="%(asctime)s - %(levelname)s - %(message)s",  # nt: 2026-06-26 11:45 - INFO - ...
)


def run_pipeline(start_date="2024-01-01", end_date="2024-12-31"):
    """
    Käivitab etapid järjekorras ja logib iga sammu.
    Tagastab kokkuvõtte töödeldud andmetest.
    """
    # 1. EXTRACT (Roll A) — pärime müügiandmed andmebaasist
    logging.info("1/4 Extract: pärin müügiandmeid...")
    sales = fetch_sales(start_date, end_date)             # tagastab DataFrame'i
    logging.info(f"Extract valmis: {len(sales)} rida")    # logime, mitu rida saime
    if sales.empty:
        # kui andmeid ei tulnud, viskame selge vea (parem kui hiljem segane crash)
        raise ValueError(
            "Extract ei tagastanud andmeid — kontrolli .env ühendust ja kuupäevi."
        )

    # 2. TRANSFORM (Roll B) — puhastame ja arvutame koondnäitajad
    logging.info("2/4 Transform: puhastan ja koondan...")
    clean = clean_data(sales)                             # eemaldab duplikaadid, NULL-id
    weekly = calculate_weekly_aggregates(clean)           # nädalane tulu, tellimuste arv jne
    kpis = calculate_kpis(clean)                          # kogukäive, kliendid, keskmine tellimus
    logging.info(
        f"Transform valmis: {len(clean)} puhast rida, {len(weekly)} nädalat"
    )

    # 3. VISUALIZE (Roll C) — loome diagrammid mälus
    logging.info("3/4 Visualize: loon diagrammid...")
    fig_weekly = create_weekly_chart(weekly)
    fig_kpi = create_kpi_summary(kpis)

    # 4. EXPORT (Roll C) — salvestame tulemused output/ kausta
    logging.info("4/4 Export: salvestan failid output/ kausta...")
    csv_path = export_results(weekly, "output")           # CSV ajatempliga
    chart_paths = export_charts(                          # diagrammid HTML-ina
        {"weekly_revenue": fig_weekly, "kpi_summary": fig_kpi},
        "output",
    )

    # tagastame kokkuvõtte, et __main__ saaks selle välja printida
    return {
        "rows": len(clean),
        "weeks": len(weekly),
        "kpis": kpis,
        "csv": csv_path,
        "charts": chart_paths,
    }


if __name__ == "__main__":
    # See plokk käivitub ainult otse jooksutamisel: python pipeline.py
    start_time = time.time()                              # märgime algusaja
    logging.info("Pipeline started")

    try:
        # kogu pipeline ühe try sees — kui mõni etapp ebaõnnestub, püüame vea kinni
        summary = run_pipeline()
        elapsed = time.time() - start_time                # kui kaua kokku kulus (sekundites)
        logging.info(
            f"Pipeline complete: {summary['rows']} rida, "
            f"{summary['weeks']} nädalat, KPI-d={summary['kpis']} "
            f"({elapsed:.1f}s)"
        )
    except Exception as e:
        # logime vea selgelt; raise hoiab veateate alles (näitab, kus täpselt katki läks)
        logging.error(f"Pipeline ebaõnnestus: {e}")
        raise
