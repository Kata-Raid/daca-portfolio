from datetime import date
import logging
import time


import os
import json
import logging
from datetime import datetime

import plotly.graph_objects as go

from transform import (
    calculate_weekly_aggregates,
    calculate_kpis
)


import os
import logging
from datetime import datetime

import plotly.graph_objects as go

from data_fetcher import fetch_sales
from transform import (
    clean_data,
    calculate_weekly_aggregates,
    calculate_kpis
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 1. NÄDALAPÕHINE PLOTLY GRAAFIK
def create_weekly_chart(df_weekly):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_weekly["sale_date"],
            y=df_weekly["total_revenue"],
            mode="lines+markers",
            name="Nädala kogukäive"
        )
    )

    fig.update_layout(
        title="Nädalapõhine müügikäive",
        xaxis_title="Nädal",
        yaxis_title="Kogukäive (€)",
        template="plotly_white"
    )

    return fig


# 2. KPI-DE PLOTLY TABEL
def create_kpi_summary(kpis):

    fig = go.Figure(data=[
        go.Table(
            header=dict(
                values=["KPI", "Väärtus"],
                fill_color="lightblue",
                align="center"
            ),
            cells=dict(
                values=[
                    [
                        "Kogukäive (€)",
                        "Unikaalsed kliendid",
                        "Keskmine ostuväärtus (€)"
                    ],
                    [
                        round(float(kpis["total_revenue"]), 2),
                        kpis["unique_customers"],
                        round(float(kpis["avg_order_value"]), 2)
                    ]
                ],
                align="center"
            )
        )
    ])

    fig.update_layout(
        title="Müügi peamised KPI-d",
        template="plotly_white",
        height=350
    )

    return fig


# 3. TULEMUSTE EKSPORT
def export_results(df, output_dir="output"):

    try:

        if df.empty:
            raise ValueError("Eksporditavad andmed puuduvad!")

        # Loome output kausta
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Salvestame müügiandmed CSV-failina
        csv_path = os.path.join(
            output_dir,
            f"sales_results_{timestamp}.csv"
        )

        df.to_csv(
            csv_path,
            index=False,
            encoding="utf-8-sig"
        )

        # Arvutame KPI-d ja nädalakoondid
        kpis = calculate_kpis(df)
        df_weekly = calculate_weekly_aggregates(df)

        # Salvestame nädalakoondid CSV-failina
        weekly_csv_path = os.path.join(
            output_dir,
            f"weekly_sales_{timestamp}.csv"
        )

        df_weekly.to_csv(
            weekly_csv_path,
            index=False,
            encoding="utf-8-sig"
        )

        # Loome ja salvestame nädalagraafiku
        weekly_fig = create_weekly_chart(df_weekly)

        weekly_html_path = os.path.join(
            output_dir,
            f"weekly_chart_{timestamp}.html"
        )

        weekly_fig.write_html(weekly_html_path)

        # Loome ja salvestame KPI diagrammi
        kpi_fig = create_kpi_summary(kpis)

        kpi_html_path = os.path.join(
            output_dir,
            f"kpi_summary_{timestamp}.html"
        )

        kpi_fig.write_html(kpi_html_path)

        print("\nTULEMUSED EDUKALT EKSPORDITUD!")
        print("CSV:", os.path.abspath(csv_path))
        print("Nädala CSV:", os.path.abspath(weekly_csv_path))
        print("Nädala HTML:", os.path.abspath(weekly_html_path))
        print("KPI HTML:", os.path.abspath(kpi_html_path))

        return True

    except Exception:
        logger.exception("Eksport ebaõnnestus")
        raise


# 4. KOGU PROGRAMMI KÄIVITAMINE
if __name__ == "__main__":

    print("\nLaen Supabase'i müügiandmeid...")

    df = fetch_sales(
        start_date="2023-01-01",
        end_date="2026-06-28"
    )

    if df.empty:
        raise ValueError("Supabase ei tagastanud müügiandmeid!")

    print("Andmeid laaditud:", len(df))

    print("\nPuhastan andmeid...")

    df_clean = clean_data(df)

    
if __name__ == "__main__":
    print("Programm käivitus")

    df = fetch_sales(
        start_date="2023-01-01",
        end_date="2026-06-28"
    )
    print("Andmeid laaditi:", len(df))

    if df.empty:
        raise ValueError("Andmeid ei saadud Supabase'ist!")

    df_clean = clean_data(df)
    print("Puhastatud ridu:", len(df_clean))

    if df_clean.empty:
        raise ValueError("Puhastatud andmeid ei ole!")

    print("\nAlustan eksportimist...")

    export_results(df_clean, "output")

    print("\nRoll A, B ja C töö lõpetatud!")
    print("Failide asukoht:", os.path.abspath("output"))
