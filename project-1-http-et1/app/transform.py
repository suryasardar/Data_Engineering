from datetime import datetime, timezone

from app.schemas import SalesTransaction


TAX_RATE = 0.18


def transform_transaction(transaction: SalesTransaction) -> dict:
    subtotal = transaction.quantity * transaction.unit_price
    tax = subtotal * TAX_RATE
    total = subtotal + tax

    return {
        "transaction_id": transaction.transaction_id,
        "product_id": transaction.product_id,
        "quantity": transaction.quantity,
        "unit_price": transaction.unit_price,
        "subtotal": round(subtotal, 2),
        "tax": round(tax, 2),
        "total": round(total, 2),
        "customer_id": transaction.customer_id,
        "processed_timestamp": datetime.now(timezone.utc),
    }