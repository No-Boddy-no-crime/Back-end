from flask import request
from flask_socketio import SocketIO, emit, join_room
import game_server.db.database as db
from bson import json_util
import json

socketio = SocketIO()

turn = {}
turn_order = ['Miss Scarlet', 'Colonel Mustard', 'Mrs White', 'Mr Green', 'Mrs Peacock', 'Professor Plum']


def create_socketio(app):
    print('Server: init socketio')
    async_mode = None
    socketio.init_app(app, async_mode=async_mode)

    return app


@socketio.on('connect')
def test_connect():
    print('Client Connected...')


@socketio.on('disconnect')
def test_disconnect():
    print('Client Disconnected...')


@socketio.event
def joinGame(message):
    """Handle incoming connection. Requires room_id which will be the game board unique identifier. Also requires the player's chosen character."""

    room_id = message['game_board_id'] # creates a room with same id as game board.
    char_name = message['character_name'] # gets the player's chosen character
    id = request.sid
    join_room(room_id)

    #update the player information in the db with the player's session id.
    db.get_games_collection().find_one_and_update({"game_board_id": room_id, 'players.character_name':char_name}, {"$set" : {"players.$.sid": id}})
    emit("connect","New Player Joined", to=room_id)


@socketio.event
def gameTurn(message): 
    """Handles request for gameTurn. Initial call to gameTurn should come from a game start. Subsequent calls will be when a player's turn has ended."""

    room_id = message['game_board_id']
    try: # Check to see if the game has already initiated a turn.
        turn[room_id] +=1
    except:
        turn[room_id] = 0
    players = [item['character_name'] for item in db.get_players(room_id)] # retrieve all players in the game.
    indexes = [turn_order.index(player) for player in players] 
    sorted_players = [p for _,p in sorted(zip(indexes, players))] # sort players by designated turn order.
    idx = (turn[room_id] + len(sorted_players)) % len(sorted_players) # get the index of the next active player.

    # retrieve the session id of the active player.
    id = db.get_games_collection().find_one({"game_board_id": room_id}, 
                                       {"players": {"$elemMatch" : {"character_name": sorted_players[idx]}}})["players"][0]['sid']
    # inform the active player that it is their turn.
    emit('gameTurn', 'It is your turn', to=id)


@socketio.event
def gameState(message):
    """ Handles request for game state."""

    room_id = message['game_board_id']
    game_state = json.loads(json_util.dumps(db.get_game(game_board_id=room_id)))
    print(game_state)
    emit('GameState', game_state, to=request.sid)
    