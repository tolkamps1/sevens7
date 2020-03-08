#
# db.py
#
import os
import sqlite3
import time
import datetime
from flask import g
import db_init

def test_db_conn():
    """ Check if db connection can open, create and init db if doesn't already exist """
    dbname = os.environ.get("SEVENS_DB_NAME")
    assert dbname is not None

    # If db file doesn't exist call the initialize module to create and init
    if not os.path.isfile(dbname):
        db_init.init(dbname)

def get_db():
    dbname = os.environ.get("SEVENS_DB_NAME")
    assert dbname is not None
    
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db = sqlite3.connect(dbname)
    return g.sqlite_db

def close_db():
    if hasattr(g,'sqlite_db'):
	    g.sqlite_db.close()

# CREATE TABLE accesslog (id INTEGER, function STRING, method STRING, date DATE, ipaddress INTEGER, useragent STRING, user STRING);
def game_row_to_dict(row):
    game = {}
    game['id'] = row[0]
    game['rngseed'] = row[1]
    game['score'] = row[2]
    game['lines'] = row[3]
    game['date'] = datetime.datetime.utcfromtimestamp(row[4])
    game['user'] = row[5]
    game['haveResult'] = row[6]
    return game

# CREATE TABLE games (id INTEGER PRIMARY KEY AUTOINCREMENT, rngseed INTEGER, score INTEGER, lines INTEGER, date DATE, user STRING, haveResult BOOLEAN);
def accesslog_row_to_dict(row):
    access = {}
    access['id'] = row[0]
    access['function'] = row[1]
    access['method'] = row[2]
    access['date'] = datetime.datetime.utcfromtimestamp(row[3])
    access['ipaddress'] = row[4]
    access['useragent'] = row[5]
    access['user'] = row[6]
    return access

def get_games():
    conn = get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM games ORDER BY date").fetchall()
    games = []
    for row in rows:
        game = game_row_to_dict(row)
        games.append(game)
    return games

def create_new_game():
    conn = get_db()
    curs = conn.cursor()
    curs.execute("INSERT INTO games (rngseed, score, lines, date, user, haveResult) VALUES (?,?,?,?,?,?);", 
                (get_rng_seed(), 0, 0, time.time(),"",False))
    conn.commit()
    res = curs.execute("SELECT * FROM games WHERE id=last_insert_rowid()").fetchall()
    return game_row_to_dict(res[0])

def update_game(gameid,score,lines,user):
    conn = get_db()
    curs = conn.cursor()
    curs.execute("UPDATE games SET score=?, lines=?, user=?, haveResult=? WHERE id=?;", 
                (score, lines, user, True, gameid))
    conn.commit()
    res = curs.execute("SELECT * FROM games WHERE id=?;",(gameid,)).fetchall()
    if len(res) != 0:
       return game_row_to_dict(res[0])
    else:
       return None

def add_access_log(game_id, func, method, auth, ip, user_agent):
    """ Add access log to global access_log list """
    conn = get_db()
    curs = conn.cursor()

    curs.execute("INSERT INTO accesslog (id, function, method, date, ipaddress, useragent, user) VALUES (?,?,?,?,?,?,?);", (game_id, func, method, time.time(),ip, user_agent, auth))
    conn.commit()

def get_access_logs():
    conn = get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM accesslog ORDER BY date").fetchall()
    access_log = []
    for row in rows:
        access = accesslog_row_to_dict(row)
        access_log.append(access)
    return access_log

def get_rng_seed():
    """ Generate rng seed """
    return 0xDEADBEEF
