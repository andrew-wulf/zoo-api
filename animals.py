from db import connect_to_db


def animals_all():
    conn = connect_to_db()
    rows = conn.execute(
        """
        SELECT * FROM animals
        """
    ).fetchall()
    return [dict(row) for row in rows]



def animals_create(name, description, image):
    conn = connect_to_db()
    row = conn.execute(
        """
        INSERT INTO animals (name, description, image)
        VALUES (?, ?, ?)
        RETURNING *
        """,
        (name, description, image),
    ).fetchone()
    conn.commit()
    return dict(row)



def animals_find_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        SELECT * FROM animals
        WHERE id = ?
        """,
        (id,),
    ).fetchone()
    return dict(row)



def animals_update_by_id(id, name, description, image):
    conn = connect_to_db()
    row = conn.execute(
        """
        UPDATE animals SET name = ?, description = ?, image = ?
        WHERE id = ?
        RETURNING *
        """,
        (name, description, image, id),
    ).fetchone()
    conn.commit()
    return dict(row)




def animals_destroy_by_id(id):
    conn = connect_to_db()
    row = conn.execute(
        """
        DELETE from animals
        WHERE id = ?
        """,
        (id,),
    )
    conn.commit()
    return {"message": "Animal entry removed successfully"}