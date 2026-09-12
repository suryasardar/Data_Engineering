from unittest.mock import patch

from app.connect_bq import insert_transaction


def test_insert_transaction_success():
    transaction = {
        "transaction_id": "TXN001",
        "product_id": "P001",
        "quantity": 5,
        "unit_price": 100,
        "subtotal": 500,
        "tax": 90,
        "total": 590,
        "customer_id": "C001",
        "processed_timestamp": "2026-09-12T00:00:00Z",
    }

    with patch(
        "app.bigquery_client.client.insert_rows_json",
        return_value=[]
    ):
        result = insert_transaction(transaction)

    assert result is True