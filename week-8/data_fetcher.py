
# Roll A - API Query

# %% 1. TEEKIDE IMPORTIMINE

import pandas as pd
import os
import time

from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client


# %% 2. SUPABASE'I ÜHENDUSE LOOMINE

# Leiame projekti põhikaustas asuva .env faili.
env_path = Path(__file__).resolve().parents[2] / ".env"

# Laeme keskkonnamuutujad .env failist.
load_dotenv(env_path, override=True)

# Loeme Supabase'i ühenduse andmed.
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Kontrollime, kas ühenduse andmed on olemas.
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase'i ühenduse andmed puuduvad .env failist!")

# Loome Supabase'i ühenduse.
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

print("Supabase'i ühendus on loodud!")



# %% 3. RETRY-FUNKTSIOON – EXPONENTIAL BACKOFF

def retry_request(request_function, max_attempts=4):
    """
    Proovib ebaõnnestunud API päringut automaatselt uuesti.

    Maksimaalselt 4 katset:
    1 sekund, 2 sekundit ja 4 sekundit ooteaega.
    """

    for attempt in range(1, max_attempts + 1):

        try:
            return request_function()

        except Exception as e:

            # Kui kõik katsed on tehtud, anname vea edasi.
            if attempt == max_attempts:
                print(
                    f"API päring ebaõnnestus pärast "
                    f"{max_attempts} katset: {e}"
                )
                raise

            # Arvutame järgmise katse ooteaja.
            wait_time = 2 ** (attempt - 1)

            print(
                f"Päring ebaõnnestus. "
                f"Järgmine katse {attempt + 1}/{max_attempts}. "
                f"Ootame {wait_time} sekundit."
            )

            time.sleep(wait_time)



# %% 4. MÜÜGIANDMETE PÄRIMINE – PAGINATION JA RETRY

def fetch_sales(start_date, end_date):
    """
    Pärib Supabase'i sales tabelist müügiandmed
    etteantud kuupäevavahemiku kohta.

    Kasutab pagination'it ja retry-funktsiooni.
    """

    try:
        page_size = 1000
        all_data = []
        offset = 0

        while True:
            response = retry_request(
                lambda: (
                    supabase.table("sales")
                    .select("*")
                    .gte("sale_date", start_date)
                    .lte("sale_date", end_date)
                    .order("id")
                    .range(offset, offset + page_size - 1)
                    .execute()
                )
            )

            batch = response.data
            all_data.extend(batch)

            if len(batch) < page_size:
                break

            offset += page_size

        df = pd.DataFrame(all_data)

        print(f"Kokku müügiandmeid: {len(df)} rida")
        return df

    except Exception as e:
        print(f"Viga müügiandmete pärimisel: {e}")
        return pd.DataFrame()


# %% 5. KLIENTIDE ANDMETE PÄRIMISE FUNKTSIOON

def fetch_customers():
    """
    Pärib Supabase'i customers tabelist kõik kliendiandmed.

    Kasutab pagination'it ja retry-funktsiooni.
    """

    try:
        page_size = 1000
        all_data = []
        offset = 0

        while True:

            response = retry_request(
                lambda: (
                    supabase.table("customers")
                    .select("*")
                    .order("customer_id")
                    .range(offset, offset + page_size - 1)
                    .execute()
                )
            )

            batch = response.data
            all_data.extend(batch)

            if len(batch) < page_size:
                break

            offset += page_size

        df = pd.DataFrame(all_data)

        print(f"Kokku klientide andmeid: {len(df)} rida")
        return df

    except Exception as e:
        print(f"Viga kliendiandmete pärimisel: {e}")
        return pd.DataFrame()


# %% 6. TOODETE ANDMETE PÄRIMISE FUNKTSIOON

def fetch_products():
    """
    Pärib Supabase'i products tabelist kõik tooteandmed.

    Kasutab pagination'it ja retry-funktsiooni.
    """

    try:
        page_size = 1000
        all_data = []
        offset = 0

        while True:

            response = retry_request(
                lambda: (
                    supabase.table("products")
                    .select("*")
                    .order("product_id")
                    .range(offset, offset + page_size - 1)
                    .execute()
                )
            )

            batch = response.data
            all_data.extend(batch)

            if len(batch) < page_size:
                break

            offset += page_size

        df = pd.DataFrame(all_data)

        print(f"Kokku toodete andmeid: {len(df)} rida")
        return df

    except Exception as e:
        print(f"Viga tooteandmete pärimisel: {e}")
        return pd.DataFrame()

# Käivitame testid ainult siis, kui data_fetcher.py käivitatakse eraldi
if __name__ == "__main__":


    # %%  Kontrollime müügiandmete kuupäevade vahemikku
    date_response = (
        supabase.table("sales")
        .select("sale_date")
        .order("sale_date")
        .limit(1)
        .execute()
    )

    print("Varaseim müügikuupäev:", date_response.data)

    date_response = (
        supabase.table("sales")
        .select("sale_date")
        .order("sale_date", desc=True)
        .limit(1)
        .execute()
    )

    print("Hiliseim müügikuupäev:", date_response.data)



    # %% 7. MÜÜGIANDMETE PÄRIMISE TEST

    sales_df = fetch_sales(
        start_date="2023-01-01",
        end_date="2026-06-28"
    )

    print("\nMüügiandmete ülevaade:")
    print(sales_df.shape)
    print(sales_df.head())

    # %% 8. KLIENTIDE ANDMETE PÄRIMISE TEST

    customers_df = fetch_customers()

    print("\nKlientide andmete ülevaade:")
    print(customers_df.shape)
    print(customers_df.head())


    # %% 9. TOODETE ANDMETE PÄRIMISE TEST

    products_df = fetch_products()

    print("\nToodete andmete ülevaade:")
    print(products_df.shape)
    print(products_df.head())


    # %% 10. ANDMETE SALVESTAMINE CSV-FAILIDENA

    sales_df.to_csv("sales.csv", index=False, encoding="utf-8-sig")
    customers_df.to_csv("customers.csv", index=False, encoding="utf-8-sig")
    products_df.to_csv("products.csv", index=False, encoding="utf-8-sig")

    print("Kõik kolm CSV-faili on salvestatud!")

    # %% 11. CSV-FAILIDE KONTROLL

    sales_check = pd.read_csv("sales.csv")
    customers_check = pd.read_csv("customers.csv")
    products_check = pd.read_csv("products.csv")

    print("Müügiandmed:", sales_check.shape)
    print("Kliendiandmed:", customers_check.shape)
    print("Tooteandmed:", products_check.shape)

    # %% 12. KLIENTIDE E-POSTI AADRESSIDE KONTROLL

    total_customers = len(customers_df)

    emails_available = customers_df["email"].notna().sum()
    emails_missing = customers_df["email"].isna().sum()

    print("Kliente kokku:", total_customers)
    print("E-posti aadress olemas:", emails_available)
    print("E-posti aadress puudub:", emails_missing)

    print(
        "E-posti aadresside olemasolu:",
        round(emails_available / total_customers * 100, 2),
        "%"
)


# %%
