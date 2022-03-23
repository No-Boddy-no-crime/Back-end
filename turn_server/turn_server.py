from flask import request

from flask_socketio import  emit, join_room
from turn_server import socketio


game_state = {} # placeholder for game state json
room_id = None


@socketio.event
def connect(message):
    """Handle incoming connection. Requires room_id which will be the game board unique identifier.
    This may not be necessary, it might be nice to map players/characters to session ids, but we might never use anyway."""
    global room_id
    room_id = message['game_board_id'] # creates a room with same id as game board.
    join_room(room_id)
    player_id = request.sid
    #TODO update player id with session id from socketio.
    emit('connect','New Player Joined', to=room_id)

@socketio.event
def gameTurn(): 
    """Handles request for gameTurn"""
    emit('gameTurn', 'It is your turn', to=request.sid)

@socketio.event
def gameState():
    """ Handles request for game state."""
    emit('GameState', game_state, to=request.sid)

