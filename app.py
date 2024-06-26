from flask import Flask, request
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