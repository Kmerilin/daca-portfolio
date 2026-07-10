"""
ROLL B: Andmete puhastamine ja koondamine (Transform)

Puhastab Roll A väljundi ning arvutab nädalased koondnäitajad ja KPI-d.

Väljund (Roll C sisend):
  - calculate_weekly_aggregates(): veerud sale_date, weekly_revenue,
    order_count, avg_order_value
  - calculate_kpis(): dict võtmetega total_revenue, unique_customers,
    avg_order_value
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Eemaldab täisrea duplikaadid ja read, kus puudub kriitiline väli
    (sale_id või total_price). NULL customer_id säilitatakse (külalisostud) —
    sama põhimõte, mis Nädal 7 puhastuses.
    """
    if df.empty:
        return df

    clean = df.drop_duplicates()

    if "sale_id" in clean.columns:
        clean = clean.drop_duplicates(subset="sale_id")

    if "total_price" in clean.columns:
        clean = clean.dropna(subset=["total_price"])

    if "sale_date" in clean.columns:
        clean["sale_date"] = pd.to_datetime(clean["sale_date"], errors="coerce")
        clean = clean.dropna(subset=["sale_date"])

    return clean.reset_index(drop=True)


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Koondab müügiandmed nädalate kaupa.
    Tagastab veerud: sale_date (nädala algus), weekly_revenue, order_count,
    avg_order_value — need nimed on kohustuslikud, Roll C loeb neid täpselt.
    """
    if df.empty:
        return pd.DataFrame(columns=["sale_date", "weekly_revenue", "order_count", "avg_order_value"])

    weekly = (
        df.set_index("sale_date")
        .resample("W")["total_price"]
        .agg(weekly_revenue="sum", order_count="count")
        .reset_index()
    )
    weekly["avg_order_value"] = (
        weekly["weekly_revenue"] / weekly["order_count"].replace(0, pd.NA)
    ).round(2)

    return weekly


def calculate_kpis(df: pd.DataFrame) -> dict:
    """
    Arvutab kolm peamist KPI-d kogu perioodi kohta.
    Tagastab dict võtmetega total_revenue, unique_customers, avg_order_value —
    need nimed on kohustuslikud, Roll C loeb neid täpselt.
    """
    if df.empty:
        return {"total_revenue": 0, "unique_customers": 0, "avg_order_value": 0}

    return {
        "total_revenue": round(df["total_price"].sum(), 2),
        "unique_customers": df["customer_id"].nunique() if "customer_id" in df.columns else 0,
        "avg_order_value": round(df["total_price"].mean(), 2),
    }
