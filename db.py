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
    dbname = os.environ.get("SEVENS_DB_NAME")

    try:
        os.remove(dbname)
    except OSError:
        pass
    """ Check if db connection can open, create and init db if doesn't already exist """
    print("********dbname: "+dbname)

    assert dbname is not None

    # If db file doesn't exist call the initialize module to create and init
    if not os.path.isfile(dbname):
        print("!!!!!!!!!dbname: "+dbname)
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

#     CREATE TABLE players (id INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER, name STRING);
def players_row_to_dict(row):
    players = {}
    players['id'] = row[0]
    players['points'] = row[1]
    players['name'] = row[2]
    return players

#CREATE TABLE hands (player_id INTEGER FOREIGN KEY, clubs STRING, hearts STRING, diamonds STRING, spades STRING);
def hands_row_to_dict(row):
    hands = {}
    hands['player_id'] = row[0]
    hands['clubs'] = str(row[1])
    hands['hearts'] = str(row[2])
    hands['diamonds'] = str(row[3])
    hands['spades'] = str(row[4])
    return hands


# CREATE TABLE board (cur_player_id INTEGER FOREIGN KEY, clubs STRING, hearts STRING, diamonds STRING, spades STRING);
def board_row_to_dict(row):
    board = {}
    board['cur_player_id'] = row[0]
    board['clubs'] = str(row[1])
    board['hearts'] = str(row[2])
    board['diamonds'] = str(row[3])
    board['spades'] = str(row[4])
    return board


def get_game_state():
    conn = get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM board").fetchall()
    board = []
    for row in rows:
        b = board_row_to_dict(row)
        board.append(b)
    return board

def get_games():
    conn = get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM games ORDER BY date").fetchall()
    games = []
    for row in rows:
        game = game_row_to_dict(row)
        games.append(game)
    return games



'''
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
'''