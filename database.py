import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def log_interaction(user_id, username, action):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO logs (timestamp, user_id, username, action)
        VALUES (%s, %s, %s, %s)
    ''', (datetime.now(), user_id, username, action))
    conn.commit()
    cursor.close()
    conn.close()

def get_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM logs')
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return logs