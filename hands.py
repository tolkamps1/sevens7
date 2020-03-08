import db
import players
import board

def create_hand(hand, player_id):
    clubs = []
    diamonds = []
    spades = []
    hearts = []
    for [num, suite] in hand:
        print("HAND!!! num{} suite {}".format(num, suite))
        if(suite == "clubs"):
            clubs.append(str(num))
        if(suite == "spades"):
            spades.append(str(num))
        if(suite == "hearts"):
            hearts.append(str(num))
        if(suite == "diamonds"):
            diamonds.append(str(num))
    clubs = " ".join(clubs)
    spades = " ".join(spades)
    hearts = " ".join(hearts)
    diamonds = " ".join(diamonds)
    print(clubs)
    print(spades)
    print(hearts)
    print(diamonds)

    conn = db.get_db()
    curs = conn.cursor()
    curs.execute("INSERT INTO hands (player_id, clubs, hearts, diamonds, spades) VALUES (?,?,?,?,?);", 
                (player_id, clubs, hearts, diamonds, spades))
    conn.commit()
    res = curs.execute("SELECT * FROM hands WHERE player_id=last_insert_rowid()").fetchall()
    return db.hands_row_to_dict(res[0])


def find_7_clubs():
    conn = db.get_db()
    curs = conn.cursor()
    rows = curs.execute ("SELECT * FROM hands").fetchall()
    for row in rows:
        b = db.hands_row_to_dict(row)
        print(b)
        clubs = str(b["clubs"]).split(" ")
        for club in clubs:
            if int(club) == 7:
                return b["player_id"]
    return -1


def lay_card_down(suit, num, player_id):
    count = players.get_player_count()
    next_turn = player_id % count + 1
    conn = db.get_db()
    curs = conn.cursor()
    rows = curs.execute("SELECT {} FROM board".format(suit)).fetchone()
    new_row = ''
    if rows[0]:
        new_row = rows[0].split(" ")
        new_row.append(num)
        new_row = " ".join(new_row)
    else: 
        new_row = str(num)
    curs.execute("UPDATE board SET {}={}, cur_player_id={};".format(suit, str(new_row), str(next_turn)))
    conn.commit()
    '''if suit == 'spades':
        curs.execute("INSERT INTO board (suit) VALUES (?);", 
                (str(player_id)))
        conn.commit()
    if suit == 'hearts':
        curs.execute("INSERT INTO board (suit) VALUES (?);", 
                (str(player_id)))
        conn.commit()
    if suit == 'diamonds':
    curs.execute("INSERT INTO board (suit) VALUES (?);", 
                (str(player_id)))
        conn.commit()
    '''
    rows = curs.execute("SELECT * FROM board;").fetchone()
    print("NEWBOARD "+str(rows[0]))
    rows = curs.execute("SELECT {} FROM hands WHERE player_id={};".format(suit, player_id)).fetchone()
    conn.commit()
    if rows[0]:
        prev_row = rows[0].split(" ")
        new_row = []
        for c in prev_row:
            if c == num:
                continue
            new_row.append(c)
        new_row = " ".join(new_row)
        print(new_row)
        print(suit)
        print(player_id)
        curs.execute("UPDATE hands SET {}='{}' WHERE player_id={};".format(suit, str(new_row), str(player_id)))
        conn.commit()
    else:
        raise Exception("Excuse me, wut")
    

