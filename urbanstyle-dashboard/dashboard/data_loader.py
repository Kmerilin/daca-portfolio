"""
UrbanStyle Dashboard — Andmelaadimine Supabase'ist
===================================================
See moodul laadib UrbanStyle andmed Supabase'ist
ja tagastab need pandas DataFrame'idena.
"""
 
import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd
 
# Laadi keskkonna muutujad .env failist
load_dotenv()
 
# Loo Supabase klient
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
 
def load_sales():
    """
    Laadi müügitabel (sales) Supabase'ist.
    Tagastab: pandas DataFrame müügiandmetega.
    Veerud: sale_id, invoice_id, sale_date, customer_id,
            product_id, quantity, unit_price, total_price,
            channel, store_location, payment_method
    """
    response = supabase.table("sales").select("*").execute()
    return pd.DataFrame(response.data)

def load_customers():
    """
    Laadi klienditabel (customers) Supabase'ist.
    Tagastab: pandas DataFrame kliendiandmetega.
    Veerud: customer_id, first_name, last_name, email,
            phone, city, registration_date, loyalty_tier, birth_year
    """
    response = supabase.table("customers").select("*").execute()
    return pd.DataFrame(response.data)
 
 
def load_products():
    """
    Laadi tootetabel (products) Supabase'ist.
    Tagastab: pandas DataFrame tooteteandmetega.
    Veerud: product_id, product_name, category, subcategory,
            unit_price, supplier, ...
    """
    response = supabase.table("products").select("*").execute()
    return pd.DataFrame(response.data)
 
 
def load_inventory():
    """
    Laadi inventuuritabel (inventory) Supabase'ist.
    Veerud: inventory_id, product_id, quantity_available, last_updated, ...
    """
    response = supabase.table("inventory").select("*").execute()
    return pd.DataFrame(response.data)


def load_sales_with_details():
    """
    Laadi müügiandmed koos toote- ja kliendiinfoga.
    Ühendab sales, products ja customers tabelid
    (sarnaselt SQL JOIN-ile, mille sa õppisid nädalal 3).
    """
    df_sales = load_sales()
    df_products = load_products()
    df_customers = load_customers()
 
    # JOIN: lisa tootenimi müügitabelile (nagu SQL LEFT JOIN)
    df = df_sales.merge(
        df_products[["product_id", "product_name", "category"]],
        on="product_id",
        how="left"
    )
 
    # JOIN: lisa kliendi linn müügitabelile
    df = df.merge(
        df_customers[["customer_id", "city", "first_name", "last_name"]],
        on="customer_id",
        how="left"
    )
 
    return df
