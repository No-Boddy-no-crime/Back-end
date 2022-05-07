from flask import request
from flask_socketio import SocketIO, emit, join_room
import game_server.db.database as db
from bson import json_util
import json
from game_server.controllers import board_controller as bc

socketio = SocketIO()

turn = {}
turn_order = ['Miss Scarlet', 'Colonel Mustard', 'Mrs White', 'Mr Green', 'Mrs Peacock', 'Professor Plum']
rebuttal = None
active_player = None


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
    msg = f"{char_name} has joined the game."
    #update the player information in the db with the player's session id.
    db.get_games_collection().find_one_and_update({"game_board_id": room_id, 'players.character_name':char_name}, {"$set" : {"players.$.sid": id}})
    emit("connect", msg, to=room_id)


@socketio.event
def gameTurn(message): 
    """Handles request for gameTurn. Initial call to gameTurn should come from a game start. Subsequent calls will be when a player's turn has ended.
       Does not currently check if player had been moved to room by a suggestion or if player moved voluntarily."""
    global active_player
    if isinstance(message, dict):
        room_id = message['game_board_id']
    else:
        room_id = int(message.pop())
    try: # Check to see if the game has already initiated a turn.
        turn[room_id] +=1
    except:
        turn[room_id] = 0
    players = [player['character_name'] for player in db.get_game(room_id)['players']] # retrieve all players in the game.
    indexes = [turn_order.index(player) for player in players] 
    sorted_players = [p for _,p in sorted(zip(indexes, players))] # sort players by designated turn order.
    idx = (turn[room_id] + len(sorted_players)) % len(sorted_players) # get the index of the next active player.

    # retrieve the session id of the active player.
    active_player = db.get_games_collection().find_one({"game_board_id": room_id}, 
                                       {"players": {"$elemMatch" : {"character_name": sorted_players[idx]}}})["players"][0]
    print(f"Active Player: {active_player}")
    try:
        id = active_player['sid']
        board = db.get_game(room_id)['board']
    except KeyError:
        return
  
    current_position=None    
    for index, room in enumerate(board):
        for player in room:
            if player == active_player['player_id']:
                current_position = index
                
    options = check_possible_moves(board, current_position)
    print(options)
  
    socketio.emit('gameTurn', {'moves':options}, to=id)
    # except:
    #     print(f"Unable to query session id of active player")
    
    


@socketio.event
def gameState(message):
    """ Handles request for game state. Functions as event handler for client request for game state or function to broadcast updated game state called by game_server."""
    if isinstance(message, dict):
        try: #request came from client.
            request.sid
            room_id = message['game_board_id']
            game_state = json.loads(json_util.dumps(db.get_game(game_board_id=room_id)))
            
        except: #request came from game_server
            game_state = message
            room_id = game_state['game_board_id']
    else:
        room_id = message  
        game_state = json.loads(json_util.dumps(db.get_game(game_board_id=room_id)))
    try:
        socketio.emit('GameState', game_state, to=room_id)
    except:
        print(f"Attempted to emit game state. No room_id: {room_id}")
    


def notify_players_of_winner(game_id, player_id):
    character = db.get_games_collection().find_one({"game_board_id": int(game_id)}, 
                                       {"players": {"$elemMatch" : {"player_id": int(player_id)}}})['players'][0]['character_name']
    print(f"Notifying Room: {game_id} that {character} has won the Game.")
    msg = f"{character} has won the game!!!"
    try:
        socketio.emit('gameOver', msg, to=game_id)
    except:
        print(f"Attempted to notify players of game over. No room_id: {game_id}")



def notify_players_of_rebutall(game_id, other_player_id):
    character = db.get_games_collection().find_one({"game_board_id": int(game_id)}, 
                                       {"players": {"$elemMatch" : {"player_id": int(other_player_id)}}})["players"][0]['character_name']
    print(f"Notifying Room: {game_id} that {character} has made a rebuttal.")
    msg = f"{character} has made a rebuttal."
    try:
        socketio.emit('rebuttal', msg, to=game_id)
    except:
        print(f"Attempted to notify all players of rebuttal. No room_id: {game_id}")

    

def notify_player_to_rebute(game_id, other_player_id, matching_cards):
    global rebuttal
    rebuttal = None
    """Notify player to select a rebuttal card from a list of possible options. Requires client side callback to return selected card.
       If player does not make a choice within 10 seconds, returns first card in matches."""
    try:
        id = db.get_games_collection().find_one({"game_board_id": int(game_id)}, 
                                        {"players": {"$elemMatch" : {"player_id": int(other_player_id)}}})["players"][0]['sid']
    except KeyError:
        return
    character = db.get_games_collection().find_one({"game_board_id": int(game_id)}, 
                                       {"players": {"$elemMatch" : {"player_id": int(other_player_id)}}})["players"][0]['character_name']
    msg = {'cards':matching_cards}
    print(matching_cards)
    socketio.emit('chooseRebuttalCard', msg, to=id, callback=update_rebuttal)
    socketio.sleep(20)
    if rebuttal is None:
        rebuttal = matching_cards[0]
         
    return {"player":{"player_id": other_player_id, "character_name": character}, "card": rebuttal}

def notify_players_no_rebute(game_id, card_set):
    msg = {"msg": "No Player was able to rebute the suggestion", "card_set":card_set}
    try:
        socketio.emit("noRebuttal", msg, to=game_id)
    except:
        print(f"Attempted to broadcast no rebute. No room_id: {game_id}")


def check_possible_moves(board, position):
    print(f"Checking Moves. position: {position}")
    potential_moves = bc.valid_transitions[position]
    for room in potential_moves:
        if len(board[room]) > 0 and len(bc.valid_transitions[room]) == 2: # Checks if potential move is a hallway that is occupied by another player.
            potential_moves.remove(room)
    return potential_moves


def is_active_player(player_id):
    return player_id == active_player['player_id']


def update_rebuttal(card):
    global rebuttal
    rebuttal = card