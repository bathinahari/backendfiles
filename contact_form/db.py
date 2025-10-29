import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME") # replace with your MySQL password

# Function to get connection
def get_connection():
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,              # change if needed
        password=DB_PASSWORD,  # replace with your MySQL password
        database=DB_NAME     # your database name
    )
    return connection


# Function to save contact form data
def save_contact_form(name, email, contact_no, message):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO contact_form (name, email, contact_no, message, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (name, email, contact_no, message, datetime.now())
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Contact form saved successfully!")