from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={"*": {"origins": "http://localhost:5173"}})

@app.route('/')
def hello():
    return 'Hello, World!'