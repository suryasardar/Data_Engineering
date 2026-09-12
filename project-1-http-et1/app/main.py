from fastapi import FastAPI, HTTPException
from app.schemas import SalesTransaction
from app.transform import transform_transaction
from app.connect_bq import insert_transaction

app = FastAPI(title="Sales ETL Microservice")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/transactions")
def create_transaction(transaction: SalesTransaction):
    try:
        transformed = transform_transaction(transaction)

        # Load into BigQuery
        insert_transaction(transformed)

        # Convert datetime to JSON-serializable string
        response_data = transformed.copy()
        response_data["processed_timestamp"] = (
            transformed["processed_timestamp"].isoformat()
        )

        return {
            "status": "success",
            "message": "Transaction processed and loaded into BigQuery",
            "data": response_data,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process transaction: {str(e)}"
        )