import sqlite3 as sql


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
        return "VTuber not found", 404
    else:
        return vtuber


def insertContact(email, name):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute("INSERT INTO contact_list (email,name) VALUES (?,?)", (email, name))
    con.commit()
    con.close()
