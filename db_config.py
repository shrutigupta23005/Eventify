# import mysql.connector

# def get_db_connection():
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",     # 👈 leave empty (since Workbench doesn't ask)
#         database="university_chatbot"
#     )
#     return conn

import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn
