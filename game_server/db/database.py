from flask import Flask
from flask_pymongo import PyMongo

MONGO = None

def setup_db(flask_app):
    global MONGO
    flask_app.config["MONGO_URI"] = "mongodb://localhost:27017/clueDB"
    MONGO = PyMongo(flask_app)

def get_db():
    return MONGO

def get_games_collection():
    assert MONGO is not None
    return MONGO.db.get_collection("Games")

def get_players_collection():
    assert MONGO is not None
    return MONGO.db.get_collection("Players")

def get_games():
    return get_games_collection().find()

def get_players():
    return get_players_collection().find()

def main():
    pass

if __name__ == '__main__':
    main()