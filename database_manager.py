import sqlite3 as sql
from werkzeug.security import generate_password_hash, check_password_hash


def listVtuberbygeneration(generation):
    with sql.connect("database/data_source.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM vtubers WHERE generation LIKE ?", (f"%{generation}%",)
        ).fetchall()
    return data


def listVtuberbybranch(branch):
    with sql.connect("database/data_source.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM vtubers WHERE branch LIKE ?", (branch,)
        ).fetchall()
    return data


def listVtuberbygraduated(graduated):
    with sql.connect("database/data_source.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM vtubers WHERE graduated = ?", (graduated,)
        ).fetchall()
    return data


def listVtubers():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM vtubers").fetchall()
    con.close()
    return data


def get_vtuber(id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    vtuber = cur.execute("SELECT * FROM vtubers WHERE id = ?", (id,)).fetchone()

    if vtuber is None:
        con.close()
        return "VTuber not found", 404
    else:
        con.close()
        return vtuber


def insertUser(email, password):
    hashed_pw = generate_password_hash(password)

    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (email,password) VALUES (?,?)",
        (email, hashed_pw),
    )
    con.commit()
    con.close()


def checkUser(email, password):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    cur.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cur.fetchone()

    if user is None:
        con.close()
        return False

    stored_password = user[0]

    if check_password_hash(stored_password, password):
        con.close()
        return True
    else:
        con.close()
        return False


def get_user(email):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    user = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    con.close()
    return user


def add_favourite(user_id, vtuber_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    try:
        cur.execute(
            "INSERT INTO favourites (user_id, vtuber_id) VALUES (?, ?)",
            (user_id, vtuber_id),
        )
        con.commit()
    except:
        pass
    con.close()


def remove_favourite(user_id, vtuber_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    cur.execute(
        "DELETE FROM favourites WHERE user_id=? AND vtuber_id=?", (user_id, vtuber_id)
    )
    con.commit()
    con.close()


def is_favourite(user_id, vtuber_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    result = cur.execute(
        "SELECT 1 FROM favourites WHERE user_id=? AND vtuber_id=?", (user_id, vtuber_id)
    ).fetchone()

    con.close()

    return result is not None


def get_favourites(user_id):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()

    results = cur.execute(
        """
        SELECT vtubers.*
        FROM vtubers
        JOIN favourites ON vtubers.id = favourites.vtuber_id
        WHERE favourites.user_id = ?
    """,
        (user_id,),
    ).fetchall()

    con.close()

    return results
