import logging
from fastapi import FastAPI, HTTPException
from app.schemas import SalesTransaction
from app.transform import transform_transaction
from app.connect_bq import insert_transaction

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sales ETL Microservice")


@app.get("/")
def health_check():
    logger.info("Health check endpoint pinged.")
    return {"status": "ok"}


@app.post("/transactions")
def create_transaction(transaction: SalesTransaction):
    # We use transaction.dict() or transaction.transaction_id depending on your Pydantic schema
    # Assuming transaction_id is a direct attribute of your Pydantic model:
    txn_id = getattr(transaction, "transaction_id", "Unknown")
    
    try:
        logger.info(f"Received new transaction payload for ID: {txn_id}")
        
        # Transform data
        transformed = transform_transaction(transaction)
        logger.info(f"Successfully transformed transaction ID: {txn_id}")

        # Convert datetime to JSON-serializable string BEFORE BigQuery insertion
        transformed["processed_timestamp"] = transformed["processed_timestamp"].isoformat()

        # Load into BigQuery
        insert_transaction(transformed)
        logger.info(f"Successfully inserted transaction ID: {txn_id} into BigQuery")

        return {
            "status": "success",
            "message": "Transaction processed and loaded into BigQuery",
            "data": transformed,
        }

    except Exception as e:
        # exc_info=True attaches the full stack trace to your Cloud Logging for easier debugging
        logger.error(f"Failed to process transaction ID: {txn_id}. Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process transaction: {str(e)}"
        )