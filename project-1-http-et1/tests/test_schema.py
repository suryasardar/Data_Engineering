import pytest

from app.schemas import SalesTransaction


def test_valid_transaction():
    transaction = SalesTransaction(
        transaction_id="TXN001",
        product_id="P001",
        quantity=5,
        unit_price=100,
        customer_id="C001",
    )

    assert transaction.quantity == 5
    assert transaction.unit_price == 100


def test_negative_quantity_is_invalid():
    with pytest.raises(Exception):
        SalesTransaction(
            transaction_id="TXN001",
            product_id="P001",
            quantity=-5,
            unit_price=100,
            customer_id="C001",
        )


def test_missing_required_field_is_invalid():
    with pytest.raises(Exception):
        SalesTransaction(
            transaction_id="TXN001",
            product_id="P001",
            quantity=5,
            unit_price=100,
        )