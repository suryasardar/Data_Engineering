from google.cloud import bigquery
import os

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "sales_dataset"
TABLE_ID = "sales_transactions"


client = bigquery.Client(project=PROJECT_ID)


def insert_transaction(transaction: dict):
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    rows_to_insert = [transaction]

    errors = client.insert_rows_json(
        table_ref,
        rows_to_insert
    )

    if errors:
        raise RuntimeError(f"BigQuery insert failed: {errors}")

    return True