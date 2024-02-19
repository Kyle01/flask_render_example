import os
from flask import Flask, jsonify
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv() 

def get_db_connection():
    DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
    conn = psycopg2.connect(DB_CONNECTION_URL)
    return conn

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bar')
def second_endpoint():
    return jsonify(
        foo="bar",
    )


@app.route('/get_books')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books