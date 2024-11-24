import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google.cloud import storage
import pyodbc
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set template and static folder paths
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Enable CORS for specific origin
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# GCS Authentication
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'class-activity-435807-1abd91357b8d.json')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
BUCKET_NAME = "my-flask"  # Ensure this is the correct GCS bucket name

# Establish a connection to the database
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=35.231.64.34;'
            'DATABASE=myappdb;'
            'UID=sqlserver;'
            'PWD=root;'
            'Encrypt=no;'
            'Connection Timeout=30;'  # 30 seconds timeout

        )
        logging.info("Database connection established.")
        return conn
    except pyodbc.Error as e:
        logging.error(f"Database Connection Error: {e}")
        return None

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle submission and insert data into the database
@app.route('/submit', methods=['POST'])
def submit_values():
    data = request.get_json()
    value1 = data.get('value1')
    value2 = data.get('value2')

    logging.info(f"Received Value 1: {value1}, Value 2: {value2}")

    if not value1 or not value2:
        return jsonify(error="Both values are required"), 400

    combined_message = f"Value 1: {value1}, Value 2: {value2}"

    # Insert the message into the database
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO my_table (message) VALUES (?)', (combined_message,))
            conn.commit()
            logging.info("Values submitted successfully.")
            return jsonify(success=True, message="Values submitted successfully"), 201
        except Exception as e:
            conn.rollback()
            logging.error(f"Error occurred while submitting values: {e}")
            return jsonify(error="Failed to submit values"), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify(error="Database connection failed"), 500

# Initialize Google Cloud Storage client
def get_gcs_client():
    return storage.Client(credentials=credentials)

# Function to upload a file to Google Cloud Storage
def upload_to_gcs(file, bucket_name, blob_name):
    try:
        client = get_gcs_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_file(file)
        logging.info(f"File {blob_name} uploaded to {bucket_name}.")
        return f"File {blob_name} uploaded to {bucket_name}"
    except Exception as e:
        logging.error(f"Error uploading file to GCS: {e}")
        raise

# Route to handle file uploads
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file:
        try:
            blob_name = file.filename
            upload_to_gcs(file, BUCKET_NAME, blob_name)
            return jsonify(success=True, message=f"File '{blob_name}' uploaded successfully"), 201
        except Exception as e:
            return jsonify(error=f"Failed to upload file: {str(e)}"), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
