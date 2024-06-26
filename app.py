from flask import Flask, request
from flask_cors import CORS
from animals import *

app = Flask(__name__)

@app.route("/animals.json")
def index():
    return animals_all()

@app.route("/animals.json", methods=["POST"])
def create():
    name = request.form.get("name")
    description = request.form.get("description")
    image = request.form.get("image")
    return animals_create(name, description, image)

@app.route("/animals/<id>.json")
def show(id):
    return animals_find_by_id(id)

@app.route("/animals/<id>.json", methods=["PATCH"])
def update(id):
    name = request.form.get("name")
    description = request.form.get("description")
    image = request.form.get("image")
    return animals_update_by_id(id, name, description, image)

@app.route("/animals/<id>.json", methods=["DELETE"])
def destroy(id):
    return animals_destroy_by_id(id)
cors = CORS(app, resources={"*": {"origins": "http://localhost:5173"}})

@app.route('/')
def hello():
    return 'Hello, World!'