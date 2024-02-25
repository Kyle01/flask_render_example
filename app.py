import os
from flask import Flask, jsonify, request, json, abort
import hashlib
import psycopg2
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv() 

def verify_authentication():
    mode = os.environ.get('DEVELOPMENT_MODE')

    if mode == 'dev':
        return True
    
    try: 
        secret = os.environ.get('SECRET_HASH')

        parse_headers = json.loads(json.dumps({**request.headers}))
        csrf_token = parse_headers["Cookie"].split('; ')[0].split("=")[1]
        print(csrf_token)
        request_token = csrf_token.split("%7C")[0]
        request_hash = csrf_token.split("%7C")[1]
        
        hasher = hashlib.sha256()
        hasher.update(f'{request_token}{secret}'.encode('utf-8'))
        secret_hash = hasher.hexdigest()

        if secret_hash != request_hash:
            abort(403)
        else:
            return True
    except: 
        abort(403)

def get_db_connection():
    DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
    conn = psycopg2.connect(DB_CONNECTION_URL)
    return conn

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bar')
def second_endpoint():
    verify_authentication()
    return jsonify(
        foo="bar",
        kyle="mcv",
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