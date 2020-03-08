import db
        
def get_all_players():
    conn = db.get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM players").fetchall()
    players = []
    for row in rows:
        b = db.players_row_to_dict(row)
        players.append(b)
    return players


def get_player_count():
    conn = db.get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT COUNT(*) FROM players").fetchone()
    return rows[0]


def get_player_hand(id):
    conn = db.get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT clubs, spades, hearts, diamonds FROM hands WHERE player_id={}".format(id)).fetchall()
    hands = []
    for row in rows:
        b = db.hands_row_to_dict(row)
        print(b)
        players.append(b)
    return players


def create_player(name):
    conn = db.get_db()
    curs = conn.cursor()
    curs.execute("INSERT INTO players (points, name) VALUES (?,?);", 
                (0, name))
    conn.commit()
    res = curs.execute("SELECT * FROM players WHERE id=last_insert_rowid()").fetchall()
    return db.players_row_to_dict(res[0])


def get_player_name(player_id):
    conn = db.get_db()
    curs = conn.cursor()
    res = curs.execute ("SELECT * FROM players WHERE id={}".format(player_id)).fetchone()
    return db.players_row_to_dict(res)["name"]
