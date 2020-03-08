#!flask/bin/python
import sys
import datetime
import os
import itertools, random
import json

from flask import Flask, jsonify, make_response, request, abort, render_template, g

import db
import players
import hands
import board

app = Flask(__name__)
authorized_tokens = {}

def display_user(auth):
    """ Create public user identifier """
    if auth is not None and len(auth) > 5:
        sys.stdout.flush()
        return auth[:3] + "__" + auth[-3:]
    else:
        sys.stdout.flush()
        return ""

@app.route('/')
def sanity_check():
    db.test_db_conn()
    return render_template('index.html')


@app.route('/newgame', methods=['POST'])
def new_game():
    data = request.form
    for player in data.values():
        print(players.create_player(player))
    print(data)
    create_hands(players.get_player_count())
    next_turn = hands.find_7_clubs()
    print(next_turn)
    if next_turn == -1:
        raise Exception(":(")
    print(board.create_game_board(next_turn))
    player_id = board.get_current_id()
    game = board.get_game_board()
    print(game)
    hand = hands.get_hand(player_id)
    print(hand)
    player_name = players.get_player_name(player_id)
    return render_template('gameboard.html', game=game, hand=hand, player_name=player_name)


def create_hands(count):
    print("COUNT: "+str(count))
    deck = list(itertools.product(range(1,14),['spades','hearts','diamonds','clubs']))
    random.shuffle(deck)

    per_player = (int) (52/count)
    i = 0
    leftover = count % 52
    for x in range(count):
        print("HII "+str(x))
        hand = deck[i:(i+per_player)]
        print(i)
        
        if leftover != 0:
            hand.append(deck[52-leftover])
            leftover -= 1
        print(hands.create_hand(hand, x+1))
        hand = []
        i = i+per_player


'''
card
'''
@app.route('/playcard', methods=['POST'])
def play_card():
    print("HELLOOWWW")
    give_card=False
    data = request.json
    suit = ''
    number = ''
    cantgo = "False"
    print(data)
    suit = data["card_suit"]
    number = data["card_value"]
    if data["cantgo"]:
        cantgo = data["cantgo"]
    player_id = board.get_current_id()
    if cantgo == "True":
        board.update_player(player_id)
        give_card=True
    elif board.check_board(suit,number):
        hands.lay_card_down(suit, number, player_id)
    else:
        print("You can't do that, sweetie.")

    game = board.get_game_board()
    player_id = board.get_current_id()

    print(game)
    #game = jsonify(game)
    print("NEWGAME !!!"+str(game))
    hand = hands.get_hand(player_id)
    print("Player")
    print(player_id)
    print(hand)
    player_name = players.get_player_name(player_id)
    return render_template('gameboard.html', game=game, hand=hand, player_name=player_name, give_card=give_card)

@app.route('/givecard', methods=['POST'])
def give_card():
    data = request.form
    suit = ''
    number = ''
    print(data)
    for k,i in enumerate(data.values()):
        print(i)
        if k == 0:
            suit = i
        else: 
            number = i
    player_id = board.get_current_id()
    hands.update_hands(suit, number, player_id)
    board.jump_forward(player_id)
    game = board.get_game_board()
    print(game)
    #game = jsonify(game)
    print("NEWGAME !!!"+str(game))
    hand = hands.get_hand(player_id)
    print(hand)
    player_name = players.get_player_name(player_id)
    return render_template('gameboard.html', game=game, hand=hand, player_name=player_name)

if __name__ == '__main__':
    # Set SEVENS_DB_NAME env var if not already set
    print("\n+ Setting up app prerequisites..")
    if not os.environ.get("SEVENS_DB_NAME"):
        print("Setting 'SEVENS_DB_NAME' env variable to: sevensdb")
        os.environ["SEVENS_DB_NAME"] = 'sevensdb'
    else:
        print("'SEVENS_DB_NAME' env variable already set to: ", os.environ["SEVENS_DB_NAME"])

    # Test db & build if doesn't exist
    db.test_db_conn()

    print("+ Setup Complete\n")
    # Run app
    app.run(debug=False, host='localhost', port=8080)
