import base64
import json
import io
import pandas as pd
from google.cloud import storage, firestore
import functions_framework

# Initialize clients globally
storage_client = storage.Client()
# Pointing to your specific database!
db = firestore.Client(database="surya-database")

@functions_framework.http
def process_csv(request):
    envelope = request.get_json()
    if not envelope or 'message' not in envelope:
        return 'Bad Request: invalid Pub/Sub message format', 400

    pubsub_message = envelope['message']
    
    if isinstance(pubsub_message, dict) and 'data' in pubsub_message:
        message_data = base64.b64decode(pubsub_message['data']).decode('utf-8')
        file_event = json.loads(message_data)
    else:
        return 'Bad Request: no data', 400

    bucket_name = file_event['bucket']
    file_name = file_event['name']

    # 1. Handle only .csv files in raw-data/
    if not file_name.startswith('raw-data/') or not file_name.endswith('.csv'):
        return f'Ignored: {file_name} is not a CSV in raw-data/', 400

    # 2. Idempotency Check (Don't process twice)
    doc_ref = db.collection('processed_files').document(file_name.replace('/', '_'))
    if doc_ref.get().exists:
        return f'Already processed: {file_name}', 200

    try:
        # 3. Download and parse the CSV
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        csv_data = blob.download_as_string()
        
        df = pd.read_csv(io.BytesIO(csv_data))

        # 4. Compute metrics
        metrics = {
            "file_name": file_name,
            "row_count": len(df),
            "null_counts": df.isnull().sum().to_dict()
        }

        # 5. Save JSON report
        report_file_name = file_name.replace('raw-data/', 'reports/').replace('.csv', '_report.json')
        report_blob = bucket.blob(report_file_name)
        report_blob.upload_from_string(
            data=json.dumps(metrics, indent=2),
            content_type='application/json'
        )

        # 6. Mark as processed in Firestore
        doc_ref.set({"status": "completed", "file": file_name})

        return 'Success', 200

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return "Internal Server Error", 500