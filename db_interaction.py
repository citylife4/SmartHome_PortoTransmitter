import sqlite3 as sql
from datetime import datetime
import hashlib

path_db = "/home/jdv/Project/SmartHome_Webserver/homedash/Database/database.db"


def insert_state(state):
    con = sql.connect(path_db, isolation_level=None)
    cur = con.cursor()
    state_to_add = 1 if state == 'True' else 0
    with con:
        cur.execute('INSERT INTO door (date, door_status) VALUES (?, ?)', (datetime.now(), str(state_to_add)))
    con.close()
    return con, cur


def insert_porto_door(state):
    con = sql.connect(path_db, isolation_level=None)
    cur = con.cursor()
    bool_to_add = 1 if state == 1 or 3 else 0
    with con:
        cur.execute('INSERT INTO porto_door_status (date, door_opened,door_status) VALUES (?, ?,?)', (datetime.now(),
                                                                                                      str(bool_to_add),
                                                                                                      str(state)))
    con.close()
    return con, cur