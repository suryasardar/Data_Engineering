from fastapi import FastAPI

from app.schemas import SalesTransaction
from app.transform import transform_transaction


app = FastAPI(title="Sales ETL Microservice")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/transactions")
def create_transaction(transaction: SalesTransaction):
    transformed = transform_transaction(transaction)

    return {
        "status": "success",
        "data": transformed,
    }