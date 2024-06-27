import sqlite3
import bcrypt


def connect_to_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def initial_setup():
    conn = connect_to_db()
    conn.execute("DROP TABLE IF EXISTS animals;")
    conn.execute("DROP TABLE IF EXISTS users;")
    conn.execute("DROP TABLE IF EXISTS secret;")

    conn.execute(
        """
        CREATE TABLE animals (
          id INTEGER PRIMARY KEY NOT NULL,
          name TEXT,
          description TEXT,
          image TEXT
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE users (
          id INTEGER PRIMARY KEY NOT NULL,
          username TEXT,
          password_digest TEXT,
          email TEXT
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE secret (
          id INTEGER PRIMARY KEY NOT NULL,
          key TEXT
        );
        """
    )

    conn.commit()
    print("Tables created successfully")


    # SEEDS

    conn.execute("""
    INSERT INTO secret (key)
    VALUES (?)
    """,
    (secret_key_generator(),),
    )

    # Admin user (admin, admin@gmail.com, password)
    password = 'password'
    hashed = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())

    conn.execute(
    """
    INSERT INTO users (username, email, password_digest)
    VALUES (?, ?, ?)
    """,
    ('admin', 'admin@gmail.com', hashed),
    )
    conn.commit()

    animals_seed_data = [
        ("tiger", "male mid size Bengal tiger", "https://www.cattales.org/wp-content/uploads/sites/499/2022/10/Tigger-in-pool-cropped-JO-1024x1024.jpg"),
        ("lions", "large female African lioness", "https://upload.wikimedia.org/wikipedia/commons/5/59/Female_African_Lion_%28Panthera_leo%29_%280347%29_-_Relic38.jpg"),
        
    ]
    conn.executemany(
        """
        INSERT INTO animals (name, description, image)
        VALUES (?,?,?)
        """,
        animals_seed_data,
    )
    conn.commit()
    print("Seed data created successfully")

    conn.close()



def secret_key_generator():
    import secrets
    return secrets.token_urlsafe(16)


def get_key():
    conn = connect_to_db()
    res = conn.execute('SELECT * from secret').fetchone()
    return res[1]


if __name__ == "__main__":
    initial_setup()