"""
ROLL A: Andmete pärimine (Extract)

Pärib müügiandmed Supabase'ist etteantud kuupäevavahemikus.
Kasutab sama .env struktuuri, mis Nädal 5 dashboard'id (SUPABASE_URL, SUPABASE_KEY).
"""

import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY"),
)


def fetch_sales(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Pärib sales tabeli read, mille sale_date jääb [start_date, end_date] vahemikku.

    Args:
        start_date: kuupäev formaadis "YYYY-MM-DD"
        end_date: kuupäev formaadis "YYYY-MM-DD"

    Returns:
        pandas DataFrame müügiandmetega. Tühi DataFrame, kui midagi ei leitud
        või ühendus ebaõnnestus (Roll D pipeline viskab sel juhul selge vea).
    """
    try:
        PAGE = 1000
        rows = []
        start = 0
        while True:
            response = (
                supabase.table("sales")
                .select("*")
                .gte("sale_date", start_date)
                .lte("sale_date", end_date)
                .range(start, start + PAGE - 1)
                .execute()
            )
            rows.extend(response.data)
            if len(response.data) < PAGE:
                break
            start += PAGE

        df = pd.DataFrame(rows)
        if not df.empty:
            df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
        return df

    except Exception as e:
        print(f"Viga andmete pärimisel: {e}")
        return pd.DataFrame()
