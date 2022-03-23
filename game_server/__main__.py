#!/usr/bin/env python3

import connexion

from game_server import encoder
from turn_server import create_socketio, socketio


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Clue Game Server'},
                pythonic_params=True)
    create_socketio(app.app)
    socketio.run(app,port=8080)


if __name__ == '__main__':
    main()
