import db
import players

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
    club_check = False
    conn = db.get_db()
    curs = conn.cursor()
    res = curs.execute("SELECT * FROM board").fetchone()
    print("###### "+str(res))
    board = db.board_row_to_dict(res)
    
    if (suit == "clubs" and number == "7"):
        return True
    if board["clubs"] and suit != "clubs":
        if len(str(board["clubs"])) > 1:
            board["clubs"] = board["clubs"].split(" ")
        else: 
            board["clubs"] = str(board["clubs"])
        for card in board["clubs"]:
            if (card == number):
                club_check = True
    if number == "7" and club_check == True:
        return True
    print("CLUB CHECK: "+str(club_check))
    if board[suit]:
        if len(str(board[suit])) > 1:
            board[suit] = board[suit].split(" ")
        else: 
            board[suit] = str(board[suit])
        number1 = int(number) + 1
        number2 = int(number) - 1
        for card in board[suit]:
            if ((card == str(number1) or card == str(number2)) and (club_check == True or suit == "clubs")):
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

def update_player(player_id):
    count = players.get_player_count()
    prev_player = -1
    mod = player_id % count
    if mod == 0:
        prev_player = count - 1
    else:
        prev_player = mod - 1
    if prev_player == 0:
        prev_player = count

    conn = db.get_db()
    curs = conn.cursor()
    curs.execute("UPDATE board SET cur_player_id={};".format(str(prev_player)))
    conn.commit()
    return prev_player

def jump_forward(player_id):
    count = players.get_player_count()
    prev_player = player_id % count  + 1
    prev_player = prev_player % count + 1

    conn = db.get_db()
    curs = conn.cursor()
    curs.execute("UPDATE board SET cur_player_id={};".format(str(prev_player)))
    conn.commit()
    return prev_player
