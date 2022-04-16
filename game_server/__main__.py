#!/usr/bin/env python3

import connexion

from game_server import encoder
from game_server.db.database import setup_db
from flask import g, json, render_template
from flask import jsonify, abort
from flask_pymongo import PyMongo
from turn_server.turn_server import create_socketio, socketio

app = connexion.App(__name__, specification_dir='./openapi/')

app.app.static_url_path = "../web/static"
app.app.static_folder = '../web/static'
app.app.template_folder = '../web/templates'

'''
@app.errorhandler(503)
def server_cannot_handle_request(e):
    return jsonify(error=str(e)), 503
'''
@app.route('/')
def home():
    print('Server: serving index.html')
    return render_template('index.html', gameId=67, async_mode=socketio.async_mode)

@app.route('/findGame', methods=('GET', 'POST'))
def findGame():
    print('Server: serving findGame.html')
    return render_template('findGame.html', async_mode=socketio.async_mode)

@app.route('/createGame', methods=('GET', 'POST'))
def createGame():
    print('Server: serving createGame.html')
    return render_template('createGame.html', async_mode=socketio.async_mode)

@app.route('/inGame/<gameId>', methods=('GET', 'POST'))
def inGame(gameId):
    print(gameId)
    gameId = gameId
    print('Server: serving inGame.html')
    return render_template('inGame.html', gameId=gameId, async_mode=socketio.async_mode)

def main():
    global app
    global mongo
    setup_db(app.app)
    print('Server: init main()')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Clue Game Server'},
                pythonic_params=True)
    create_socketio(app.app)
    socketio.run(app,port=8080)


if __name__ == '__main__':
    main()