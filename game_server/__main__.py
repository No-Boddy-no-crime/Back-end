#!/usr/bin/env python3

import connexion

from game_server import encoder
from game_server.db.database import setup_db
from flask import g
from flask_pymongo import PyMongo


def main():
    global app
    global mongo
    app = connexion.App(__name__, specification_dir='./openapi/')
    setup_db(app.app)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Clue Game Server'},
                pythonic_params=True)
    app.run(port=8080)


if __name__ == '__main__':
    main()
