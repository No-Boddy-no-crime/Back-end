from flask import json
from flask_socketio import SocketIO, emit, join_room

socketio = SocketIO()

game_state = {} # placeholder for game state json
room_id = None

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
    print("Join Game: " + json.dumps(message))
    """Handle incoming connection. Requires room_id which will be the game board unique identifier.
    This may not be necessary, it might be nice to map players/characters to session ids, but we might never use anyway."""
    global room_id
    room_id = message['game_board_id'] # creates a room with same id as game board.
    join_room(room_id)
    #TODO: define quest ---> player_id = request.sid
    #TODO update player id with session id from socketio.
    emit('connect','New Player Joined', to=room_id)

@socketio.event
def gameTurn(arg1): 
    print('Server: in gameTurn');
    """Handles request for gameTurn"""
    #TODO: define request ---> to=request.sid
    emit('gameTurn', 'It is your turn')

@socketio.event
def gameState(arg2):
    print('Server: in gameState');
    """ Handles request for game state."""
    #TODO: define request ---> to=request.sid
    emit('GameState', game_state)
    