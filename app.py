#!flask/bin/python
import sys
import datetime
import os
import itertools, random

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
    return '<b> SUCCESS!!!!</b>'


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
    #print("HELLOOWWW")
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
    if board.check_board(suit,number):
        hands.lay_card_down(suit, number, player_id)
    return '<b> SUCCESS!!!!</b>'




'''
@app.route('/tetris/accesslogs/static', methods=['GET'])
def static_logs():
    return render_template('access_logs.html', logs=db.get_access_logs())

@app.route('/tetris/gamestate', methods=['GET'])
def list_access():
    """ JSONify global access_log list """
    return jsonify(db.get_game_state())

@app.route('/tetris/games', methods=['GET'])
def list_games():
    """ JSONify global games list """
    user_id = request.args.get('user_id')
    print(user_id)
    if user_id is not None and user_id is not '':
        user_games = [game for game in db.get_games() if game['user'] == user_id]
        return jsonify(user_games)
    return jsonify(db.get_games())


@app.route('/tetris/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    """ Update & store game object """
    global authorized_tokens
    if not request.get_json():
        print("no request.json")
        abort(400)
    if not 'score' in request.json or not 'lines' in request.json:
        print("no score or lines")
        abort(400)
    if type(request.json['score']) is not int:
        print("score is not int")
        abort(400)
    if type(request.json['lines']) is not int:
        print("lines is not int")
        abort(400)
    if not request.headers.get('X-SENG275-Authentication'):
        abort(400)

    auth = request.headers.get('X-SENG275-Authentication')
    if auth not in authorized_tokens:
        abort(401)

    updated_game = db.update_game(game_id,
        request.json.get('score'),
        request.json.get('lines'),
        display_user(auth))

    if updated_game:
        db.add_access_log(game_id, 
            sys._getframe().f_code.co_name,
            "PUT",
            display_user(auth),
            request.environ.get('HTTP_X_REAL_IP',request.remote_addr),
            request.headers.get('User-Agent')) 
        return jsonify(updated_game)
    else:
        abort(404)

@app.errorhandler(400)
def bad_request(error):
    """ Respond to bad request """
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.errorhandler(401)
def not_authorized(error):
    """ Respond to non-authorized request """
    return make_response(jsonify({'error': 'Not Authorized'}), 401)

@app.errorhandler(404)
def not_found(error):
    """ Respond to unfound request """
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed(error):
    """ Respond to disallowed request """
    return make_response(jsonify({'error': 'Not allowed'}), 405)


@app.teardown_appcontext
def db_cleanup(error):
    db.close_db()
    # print("App Teardown Triggered")
    # print(error)

@app.template_filter('dt')
def filter_datetime(date, fmt=None):
    date = date + (datetime.datetime.now() - datetime.datetime.utcnow())
    return date.strftime("%Y/%m/%d %H:%M:%S")

'''

if __name__ == '__main__':
    # Set TETRIS_DB_NAME env var if not already set
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
