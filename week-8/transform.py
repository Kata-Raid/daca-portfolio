# Roll B: Data Processing (andmete töötlemine)

# Impordime Pandase teegi andmete töötlemiseks ja analüüsimiseks
import pandas as pd


# Defineerime funktsiooni müügiandmete puhastamiseks
def clean_data(df):
    # Proovime andmeid puhastada
    try:
        # Loome andmetest koopia, et algsed andmed ei muutuks
        df_clean = df.copy()

        # Eemaldame duplikaadid
        df_clean = df_clean.drop_duplicates()

        # Teisendame kuupäeva õigesse formaati
        df_clean['sale_date'] = pd.to_datetime(
            df_clean['sale_date'], errors='coerce'
        )

        # Eemaldame read, kus puudub kuupäev või hind.
        # Puuduva customer_id-ga müügiread jätame alles, sest need võivad siiski olla kehtivad müügitehingud.
        df_clean = df_clean.dropna(
            subset=['sale_date', 'total_price']
        )

        # Tagastame puhastatud DataFrame'i
        return df_clean

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga andmete puhastamisel: {e}")
        raise


# Defineerime funktsiooni nädalapõhise müügikokkuvõtte arvutamiseks
def calculate_weekly_aggregates(df):
    # Proovime arvutada nädalapõhise kokkuvõtte
    try:
        # Grupeerime andmed nädalate kaupa ning arvutame tulu, tellimuste arvu ja keskmise ostuväärtuse
        weekly = df.resample('W', on='sale_date').agg(
            total_revenue=('total_price', 'sum'),
            order_count=('total_price', 'count'),
            avg_order_value=('total_price', 'mean')
        )

        # Muudame indeksi tavaliseks veeruks ja tagastame nädalapõhise kokkuvõttetabeli
        return weekly.reset_index()
    
    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga nädalapõhise kokkuvõtte arvutamisel: {e}")
        raise


# Defineerime funktsiooni KPI-de arvutamiseks
def calculate_kpis(df):
    # Proovime arvutada KPI-d
    try:
        # Arvutame KPI-d: kogukäive, unikaalsete klientide arv ja keskmise tellimuse väärtus
        kpis = {
            'total_revenue': round(float(df['total_price'].sum()), 2),
            'unique_customers': int(df['customer_id'].nunique()),
            'avg_order_value': round(float(df['total_price'].mean()), 2)
        }

        # Tagastame KPI-de väärtused
        return kpis

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga KPI-de arvutamisel: {e}")
        raise


# Defineerime funktsiooni müügi-ja kliendiandmete ühendamiseks
def merge_datasets(df_sales, df_customers):
    # Proovime ühendada müügi- ja kliendiandmed
    try:   
        # Ühendame müügi- ja kliendiandmed nii, et säiliks kõik müügiread
        df_merged = pd.merge(
            df_sales,
            df_customers,
            on='customer_id',
            how='left'
        )

        # Tagastame ühendatud DataFrame'i 
        return df_merged

    # Püüame kinni tekkinud vead ja kuvame veateate
    except Exception as e:
        print(f"Viga andmete ühendamisel: {e}")
        raise
