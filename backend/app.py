import os
from flask import Flask, render_template, request, jsonify
from google.cloud import storage
import pyodbc
from google.oauth2 import service_account

# Set the full path to your 'frontend' folder
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

app = Flask(__name__, template_folder=template_dir, static_folder=os.path.join(template_dir, 'static'))

print(f"Template directory: {template_dir}")

# Establish a connection to the database
def get_db_connection():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=34.139.95.137;'
            'DATABASE=myappdb;'
            'UID=sqlserver;'
            'PWD=root;'
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

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()  # Use get_json to get the incoming JSON data
        value1 = data.get('value1')
        value2 = data.get('value2')

        if not value1 or not value2:
            return jsonify(error="Both values are required"), 400

        print(f"Received values: Value 1 - {value1}, Value 2 - {value2}")

        # Create a message from the received values
        message = f"Value 1: {value1}, Value 2: {value2}"

        # Save the message to the database
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Insert the combined message into the database
                cur.execute('INSERT INTO my_table (message) VALUES (?)', (message,))
                conn.commit()
                return jsonify(success=True, message="Values submitted successfully"), 201
            except Exception as e:
                conn.rollback()
                print(f"Error occurred while inserting values: {e}")
                return jsonify(error="Failed to insert values"), 500
            finally:
                cur.close()
                conn.close()
        else:
            return jsonify(error="Database connection failed"), 500

    except Exception as e:
        print(f"Error processing submission: {e}")
        return jsonify(error="An error occurred while processing your request"), 500

# Other routes remain unchanged...

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
