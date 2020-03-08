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
    tab = curs.execute ("SELECT * FROM sqlite_master WHERE type='table' AND name='games'").fetchall()
    if len(tab) > 0:
        print("table games exists in current directory.")
        print("Please delete ", dbname, " before running this script.")
        sys.exit(0)

    tab = curs.execute ("SELECT * FROM sqlite_master WHERE type='table' AND name='accesslog'").fetchall()
    if len(tab) > 0:
        print("table accesslog exists in current directory.")
        print("Please delete ", dbname, " before running this script.")
        sys.exit(0)

    # Create tables
    curs.executescript("""
    CREATE TABLE games (id INTEGER PRIMARY KEY AUTOINCREMENT, rngseed INTEGER, score INTEGER, lines INTEGER, date DATE, user STRING, haveResult BOOLEAN);
    """)
    curs.executescript("""
    CREATE TABLE accesslog (id INTEGER, function STRING, method STRING, date DATE, ipaddress INTEGER, useragent STRING, user STRING);
    """)

def drop_database(dbname):
    assert 'test' in dbname  # dont delete prod data! 
    try:
        os.remove(dbname)
    except OSError:
        pass
