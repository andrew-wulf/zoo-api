from flask import Flask, request, jsonify
from flask_cors import CORS

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from animals import *
from db import get_key

app = Flask(__name__)

# Allow requests from frontend
cors = CORS(app, resources={"*": {"origins": "http://localhost:5173"}})

# JWT manager for sessions
app.config["JWT_SECRET_KEY"] = get_key()
jwt = JWTManager(app)


#animals routes

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


@app.route('/')
def hello():
    return 'Hello, World!'





# user/authentication routes

# CREATE

@app.route("/users.json", methods=["POST"])
def create_user():
    if request.method == 'POST':
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
    
        if username and email and password:
            # Declaring our password
            password = bytes(password, 'utf-8')
            
            # Adding the salt to password
            salt = bcrypt.gensalt()
            # Hashing the password
            hashed = bcrypt.hashpw(password, salt)
            
            # printing the salt
            print("Salt :")
            print(salt)
            
            # printing the hashed
            print("Hashed")
            print(hashed)
            
            print(bcrypt.checkpw(b'abcd', hashed))

            
            conn = connect_to_db()

            res = conn.execute(
            """
            SELECT * FROM users WHERE (username = ?) OR (email = ?)

            """, (username, email),
            ).fetchone()
            if res:
                return "Username or email already exists."

            row = conn.execute(
                """
                INSERT INTO users (username, email, password_digest)
                VALUES (?, ?, ?)
                RETURNING *
                """,
                (username, email, hashed),
            ).fetchone()
            conn.commit()
            if row:
                return "User created successfully."
            else:
                return "Failed to create user."

        else:
            return "missing one or more required params."




@app.route("/sessions.json", methods=["POST"])
def sessions_create():
    if request.method == 'POST':
        email = request.form["email"]
        password = bytes(request.form["password"], 'utf-8')
        
        conn = connect_to_db()

        res = conn.execute(
        """
        SELECT * FROM users WHERE (email = ?)

        """, (email,)
        ).fetchone()
        
        if res:
            username, hashed = res[1], res[2]

            if bcrypt.checkpw(password, hashed):
                access_token = create_access_token(identity=username)
                return jsonify(jwt=access_token)
    
        return "Invalid login supplied."
        