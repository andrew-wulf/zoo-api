from flask import Flask, request, jsonify
from flask_cors import CORS
import bcrypt
from animals import *

app = Flask(__name__)

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
cors = CORS(app, resources={"*": {"origins": "http://localhost:5173"}})

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
            hashed = res[2]

            if bcrypt.checkpw(password, hashed):
                return {'id': res[0], 'username': res[1], 'email': res[3]}
    
        return "Invalid login supplied."
        