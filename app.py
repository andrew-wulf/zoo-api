from flask import Flask, request
import animals

app = Flask(__name__)

@app.route("/animals.json")
def index():
    return animals.animals_all()

