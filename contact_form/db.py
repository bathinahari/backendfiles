import mysql.connector
from datetime import datetime

# Function to get connection
def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",              # change if needed
        password="12345",  # replace with your MySQL password
        database="luvetha"      # your database name
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