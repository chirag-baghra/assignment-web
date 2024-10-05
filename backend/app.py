import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.cloud import storage
import pyodbc
from google.oauth2 import service_account

app = Flask(__name__)


# Establish a connection to the database
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'  # ODBC driver
            'SERVER=34.139.95.137;'  # Replace with your server
            'DATABASE=myappdb;'  # Database name
            'UID=sqlserver;'  # Username
            'PWD=root;'  # Password
            'Encrypt=no;'
        )
        return conn
    except pyodbc.Error as e:
        print(f"Connection Error: {e}")
        return None


# Basic route to show the homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle the POST request for adding a message
@app.route('/add_message', methods=['POST'])
def add_message():
    message = request.form.get('message')

    if not message:
        return jsonify(error="Message is required"), 400

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO my_table (message) VALUES (?)', (message,))
            conn.commit()
            return jsonify(success=True, message="Message added successfully"), 201
        except Exception as e:
            conn.rollback()
            print(f"Error occurred while adding message: {e}")
            return jsonify(error="Failed to add message"), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify(error="Database connection failed"), 500

# Route to fetch messages from the database
@app.route('/messages', methods=['GET'])
def get_messages():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute('SELECT message FROM my_table')
            messages = cur.fetchall()
            return jsonify([msg[0] for msg in messages]), 200
        except Exception as e:
            print(f"Error retrieving messages: {e}")
            return jsonify(error="Failed to retrieve messages"), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify(error="Database connection failed"), 500


# Initialize Google Cloud Storage client
def get_gcs_client():
    return storage.Client()


# GCS authentication using service account file
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), 'class-activity-435807-1abd91357b8d.json')
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
BUCKET_NAME = "my-flask"


# Function to upload a file to Google Cloud Storage
def upload_to_gcs(file, bucket_name, blob_name):
    """Uploads the file to Google Cloud Storage."""
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file)
    return f"File {blob_name} uploaded to {bucket_name}"


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
    app.run(host='0.0.0.0', port=5000)
