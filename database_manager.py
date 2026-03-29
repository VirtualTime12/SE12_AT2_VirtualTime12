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


def listVtubers():
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM vtubers").fetchall()
    con.close()
    return data


def insertContact(email, name):
    con = sql.connect("database/data_source.db")
    cur = con.cursor()
    cur.execute("INSERT INTO contact_list (email,name) VALUES (?,?)", (email, name))
    con.commit()
    con.close()
