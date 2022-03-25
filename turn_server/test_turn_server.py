from flask import session
from flask_socketio import emit
from . import socketio

@socketio.on('connect', namespace='/test')
def test_connect():
    print("Server says: A client has connected")
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('join room', namespace='/test')
def test_join_room(data):
    join_room(data['room'])

@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('leave room', namespace='/test')
def test_leave_room(data):
    leave_room(data['room'])

@socketio.on('my room namespace event', namespace='/test')
def test_room_event(data):
    room = data.pop('room')
    send('room message', room=room)
