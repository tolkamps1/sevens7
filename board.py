import db

def create_game_board(player_id):
    print(player_id)
    conn = db.get_db()
    curs = conn.cursor()
    curs.execute("INSERT INTO board (cur_player_id) VALUES (?);", 
                (str(player_id)))
    conn.commit()
    res = curs.execute("SELECT * FROM board").fetchone()
    print("###### "+str(res))
    return db.board_row_to_dict(res)


def check_board(suit, number):
    print(suit)
    print(number)
    conn = db.get_db()
    curs = conn.cursor()
    res = curs.execute("SELECT * FROM board").fetchone()
    print("###### "+str(res))
    board = db.board_row_to_dict(res)
    if (suit == "clubs" and number == "7"):
        return True
    if board["clubs"]:
        for card in board[suit]:
            if (int(card) != number):
                return False
    if board[suit]:
        for card in board[suit]:
            if (int(card) == (number + 1) or int(card) == (number - 1)):
                return True
    return False



def get_current_id():
    conn = db.get_db()
    curs = conn.cursor()
    res = curs.execute("SELECT * FROM board").fetchone()
    print(res)
    return db.board_row_to_dict(res)["cur_player_id"]


# Returns strings
def get_game_board():
    conn = db.get_db()
    curs = conn.cursor()
    res = curs.execute("SELECT * FROM board").fetchone()
    print("###### "+str(res))
    return db.board_row_to_dict(res)