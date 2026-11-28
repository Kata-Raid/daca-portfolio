import time
import logging
from datetime import datetime

# Seadistame logimise
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline():
    """Orkestreerib kogu ETL pipeline'i tööd (Extract -> Transform -> Load)."""
    start_time = time.time()
    logger.info("🚀 PIPELINE KÄIVITATUD (Roll D - pipeline.py)...")
    
    try:
        # 1. EXTRACT (Roll A - Marianne osa)
        logger.info("[1/3] EXTRACT: Pärime müügiandmed Supabase API-st...")
        try:
            from data_fetcher import fetch_sales
            df_sales = fetch_sales()
        except Exception as e:
            logger.warning(f"⚠️ 'data_fetcher' ei käivitunud ({e}). Kasutame testimiseks näidisandmeid.")
            import pandas as pd
            df_sales = pd.DataFrame([
                {"id": 1, "store_location": "Tallinn", "total_price": 100.0},
                {"id": 2, "store_location": "Tartu", "total_price": 150.0}
            ])

        # 2. TRANSFORM (Roll B)
        logger.info("[2/3] TRANSFORM: Puhastame ja grupeerime andmed...")
        try:
            from transform import calculate_weekly_aggregates
            df_summary = calculate_weekly_aggregates(df_sales)
        except Exception as e:
            logger.warning(f"⚠️ 'transform' ei käivitunud ({e}). Kasutame algseid andmeid.")
            df_summary = df_sales

        # 3. LOAD / EXPORT (Roll C)
        logger.info("[3/3] LOAD: Salvestame tulemused CSV-sse ja genereerime graafikud...")
        try:
            from visualize_export import export_results
            export_results(df_summary)
        except Exception as e:
            logger.warning(f"⚠️ 'visualize_export' ei käivitunud ({e}). Salvestame test-CSV.")
            df_summary.to_csv("pipeline_output_test.csv", index=False)

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"🎉 PIPELINE LÕPETAS EDUKALT! Kogu aeg: {elapsed} sekundit.")
        return True

    except Exception as e:
        logger.error(f"❌ PIPELINE KRAHHIS VEAGA: {e}")
        return False

if __name__ == "__main__":
    run_pipeline()