"""
Initialize SQLite database.
Should only be called when one doesn't already exist
"""
import sys
import os
import sqlite3

def init(dbname):
    """ Initialize database with name dbname """
    assert dbname is not None

    # Connect & get db cursor
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()

    # Double check tables don't already exist, quit if so
    tab = curs.execute ("SELECT * FROM sqlite_master WHERE type='table' AND name='players'").fetchall()
    if len(tab) > 0:
        print("table players exists in current directory.")
        print("Please delete ", dbname, " before running this script.")
        sys.exit(0)

    tab = curs.execute ("SELECT * FROM sqlite_master WHERE type='table' AND name='hands'").fetchall()
    if len(tab) > 0:
        print("table hands exists in current directory.")
        print("Please delete ", dbname, " before running this script.")
        sys.exit(0)

    tab = curs.execute ("SELECT * FROM sqlite_master WHERE type='table' AND name='board'").fetchall()
    if len(tab) > 0:
        print("table board exists in current directory.")
        print("Please delete ", dbname, " before running this script.")
        sys.exit(0)

    # Create tables
    curs.executescript("""
    CREATE TABLE players (id INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER, name STRING);
    """)
    curs.executescript("""
    CREATE TABLE hands (player_id INTEGER , clubs STRING, hearts STRING, diamonds STRING, spades STRING, FOREIGN KEY (player_id) REFERENCES players(id));
    """)
    curs.executescript("""
    CREATE TABLE board (cur_player_id INTEGER, clubs STRING, hearts STRING, diamonds STRING, spades STRING, FOREIGN KEY (cur_player_id) REFERENCES players(id));
    """)

def drop_database(dbname):
    assert 'test' in dbname  # dont delete prod data! 
    try:
        os.remove(dbname)
    except OSError:
        pass
