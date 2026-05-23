import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",     # 👈 leave empty (since Workbench doesn't ask)
        database="university_chatbot"
    )
    return conn
