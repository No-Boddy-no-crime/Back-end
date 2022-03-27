#!/usr/bin/env python3

import connexion

from game_server import encoder
from game_server.db.database import setup_db
from flask import g, json, render_template
from flask_pymongo import PyMongo
from turn_server.turn_server import create_socketio, socketio

app = connexion.App(__name__, specification_dir='./openapi/')

app.app.static_url_path = "../web/static"
app.app.static_folder = '../web/static'
app.app.template_folder = '../web/templates'

@app.route('/')
def hello():
    print('Server: serving index.html')
    return render_template('index.html', async_mode=socketio.async_mode)

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