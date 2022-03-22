from flask import Flask, render_template, request

from flask_socketio import SocketIO, emit, join_room
import random


async_mode = None

app = Flask(__name__)


socketio = SocketIO(app, async_mode=async_mode)

# lists of items for characters, weapons, rooms. To be replaced by respective classes.
characters = ['Miss Scarlet', 'Col. Mustard', 'Mrs. White',
              'Mr. Green', 'Mrs. Peacock', 'Prof. Plum']
weapons = ['Revolver', 'Dagger', 'Lead Pipe', 'Rope', 'Candlestick', 'Wrench']
rooms = ['Study', 'Library', 'Conservatory', 'Hall',
         'Billiard Room', 'Ballroom', 'Lounge', 'Dining Room', 'Kitchen']

# global variables in lieu of database queries.
game_state = {} # placeholder for game state json
ids = {} # get character name by session id
turn = 0 # turn counter. incremented by end_turn
active_player = None # character name of player currently executing their turn
room_id = None # placeholder for room id


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.event
def join(message):
    """Handles new player joining room. Creates new game board or adds player information to existing game."""
    global characters, game_state, room_id, ids
    if request.sid not in ids.keys(): #If player is already in room, subsequent calls to join do nothing.
        room_id = message['room']  # get room id from text box
        join_room(room_id)
        # players do not currently have ability to chose character. Pulls next character name from the list.
        char = characters[len(ids)]

        # Checks whether player is creating the room or joining an existing one.
        try:
            game_state[room_id][char] = {
                'player_id': request.sid, 'position': 'home', 'cards': []}
        except KeyError:
            game_state[room_id] = {}
            game_state[room_id][char] = {
                'player_id': request.sid, 'position': 'home', 'cards': []}
        # Handles ability to query player by character name or id (will be replace by DB access).
        ids[request.sid] = char
        emit('joinGame',
            {'data': char + ' has joined the game'}, to=room_id)


@socketio.event
def move(message):
    """Handles player movement. Update game state to reflect new player position. Broadcast new position."""
    global game_state, active_player, room_id
    if ids[request.sid] == active_player:
        # Update game state with new player positiion.
        game_state[room_id][active_player]['position'] = message['move']
        emit('playerMove',
             {'data': active_player + ' has moved to ' + message['move']}, to=room_id)


@socketio.on('gameTurn')
def gameTurn():
    """Handles changing of player turn triggered by starting a game or a player ending their turn."""
    global turn, active_player, game_state, room_id
    if turn == 0:
        deal_cards()
    try:
        # Loop through list of players to maintain turn order.
        active_player_index = (
            turn + len(game_state[room_id])) % len(game_state[room_id])
    # setting index to 0 to avoid divide by 0 error for player's first turn.
    except ZeroDivisionError:
        active_player_index = 0
    char = characters[active_player_index]
    active_player = char
    # Only sends message to active player that it is their turn.
    emit('gameTurn', {'data': 'It is your turn'},
         to=game_state[room_id][char]['player_id'])


@socketio.on('end_turn')
def end_turn():
    """Handles player electing to end their turn. will update the turn counter and call gameTurn()"""
    global turn, active_player
    if ids[request.sid] == active_player:
        turn += 1
        gameTurn()


@socketio.on('showCards')
def show_cards():
    """Handles request from player to view their cards. Will send list of cards to player who sent the request."""
    char = ids[request.sid]
    cards = game_state[room_id][char]['cards']
    emit('showCards', {'data': str(cards)},
         to=request.sid)


@socketio.on('gameState')
def show_cards():
    """Handles player request for updated game status excluding card viewing. Currently simulated by sending message with al player positions."""
    positions = ''
    for chars in game_state[room_id].keys():
        pos = game_state[room_id][chars]['position']
        positions += f'{chars} : {pos}, '
    emit('gameState', {'data': str(game_state)},
         to=request.sid)


def deal_cards():
    """Upon game start, shuffle cards and send 6 to each player."""
    cards = characters + weapons + rooms
    random.shuffle(cards)
    for char in game_state[room_id].keys():
        game_state[room_id][char]['cards'] = cards[0:6]
        cards = cards[6:]


if __name__ == '__main__':
    socketio.run(app)
