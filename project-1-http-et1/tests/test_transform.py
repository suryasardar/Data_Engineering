from app.schemas import SalesTransaction
from app.transform import transform_transaction


def test_transaction_transformation():
    transaction = SalesTransaction(
        transaction_id="TXN001",
        product_id="P001",
        quantity=5,
        unit_price=100,
        customer_id="C001",
    )

    result = transform_transaction(transaction)

    assert result["subtotal"] == 500
    assert result["tax"] == 90
    assert result["total"] == 590
    assert result["transaction_id"] == "TXN001"
    assert result["customer_id"] == "C001"
    assert result["processed_timestamp"] is not None