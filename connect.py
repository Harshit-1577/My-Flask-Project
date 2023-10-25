# connect.py
import mysql.connector

def create_connection():
    config = {
        'user': 'admin',
        'password': 'harshit7781',
        'host': 'mydbflask.c0e3z3me5aad.us-east-1.rds.amazonaws.com',
        'database': 'mydbflask',
        'raise_on_warnings': True,
    }

    try:
        conn = mysql.connector.connect(**config)
        print("Database Connection Opened")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_connection(conn):
    if conn:
        conn.close()
        print("Database Connection Closed")
