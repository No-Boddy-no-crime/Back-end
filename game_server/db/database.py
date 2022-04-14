from multiprocessing.sharedctypes import Value
import random
from flask import Flask, json
from flask_pymongo import PyMongo
import pymongo
from pymongo import ReturnDocument
from bson import json_util

MONGO_DB = None
characters = set(["Miss Scarlet",
                    "Mrs White",
                    "Mrs Peacock",
                    "Professor Plum",
                    "Mr Green",
                    "Colonel Mustard"])
CURRENT_GAMES = set()

def setup_db(flask_app):
    global MONGO_DB
    flask_app.config["MONGO_URI"] = "mongodb://localhost:27017/clueDB"
    MONGO_DB = PyMongo(flask_app).db

def get_db():
    return MONGO_DB

def get_games_collection():
    assert MONGO_DB is not None
    return MONGO_DB.get_collection("Games")


def create_game(init = False):
    if len(CURRENT_GAMES):
        raise ValueError("Too many games")
    game_id = random.randint(0, 500)
    while game_id in CURRENT_GAMES:
        game_id = random.randint(0, 500)
    CURRENT_GAMES.add(game_id)
    game = {"game_board_id": game_id, 
            "board": [[] for _ in range(20)],
            "status": "new",
            "players": []}
    get_games_collection().insert_one(game)
    return game.pop("_id")


def get_games(limit = None):
    if limit:
        games = list(get_games_collection().find({},{'_id': False}).limit(limit))
    else:
        games = list(get_games_collection().find({}, {'_id': False}))
    if len(games) == 0:
        raise ValueError("No existing games")
    return games

def get_game(game_board_id = None):
    if game_board_id:
        game = get_games_collection().find_one({"game_board_id": game_board_id}, {'_id': False})
    else:
        game = get_games_collection().find_one()
    if game is None:
        raise ValueError('Game not found')
    return game

def delete_game(game_board_id):
    deleted = get_games_collection().delete_one({"game_board_id": game_board_id})
    if deleted.deleted_count == 0:
        raise ValueError("No game found")
    
def update_game(game_board_id, new_game_state):
    new_game = get_games_collection().find_one_and_update({"game_board_id": game_board_id}, 
                                                            {'$set': new_game_state},
                                                            projection={'_id': False}, 
                                                            return_document=ReturnDocument.AFTER)
    if new_game is None:
        raise ValueError("No game found")
    return new_game

def update_player(game_board_id, player_id, update):
    # {userID:1, "solutions.textID":2}, {$set: {"solutions.$.solution": "the new text"}}
    get_games_collection().find_one_and_update({"game_id": game_board_id, "players.player_id": player_id}, {"$set": update})


def create_player(game_board_id):
    # TODO: race condition here
    game = get_games_collection().find_one({"game_board_id": game_board_id}, {"_id": 0})
    
    if game is None:
        raise ValueError("No game found")
    if game["status"] == "in-play":
        raise IndexError("Game will not accept new players")
    
    try:
        taken_characters = set([player["character_name"] for player in game["players"]])
        available_characters = characters.difference(taken_characters)
    except KeyError:
        available_characters = characters

    player_id = len(game["players"])
    player = {
        "player_id": player_id,
        "character_name": list(available_characters)[0],
        "cards": None
    }
    get_games_collection().find_one_and_update({"game_board_id": game_board_id}, {"$push" : {"players": player}})
    return player
    
def get_players(game_board_id):
    return list(get_games_collection().find_one({"game_board_id": game_board_id}, 
                                            {"players": 1, "_id": 0})["players"])

def get_player(game_board_id, player_id):
    player = get_games_collection().find_one({"game_board_id": game_board_id}, 
                                       {"players": {"$elemMatch" : {"player_id": player_id}}})["players"][0]
    return player

def __test_mongo():
    global MONGO_DB
    MONGO_DB = pymongo.MongoClient("mongodb://localhost:27017/").clueDB

def __insert_a_few_games():
    for i in range(3):
        print(create_game())

def main():
    import pprint
    pp = pprint.PrettyPrinter()
    __test_mongo()
    games = get_games()
    game = create_game(True)
    game_id = game["game_board_id"]
    player = create_player(game_board_id=game_id)
    player_id = player["player_id"]
    players = get_players(game_board_id=game_id)
    print("Game")
    pp.pprint(get_game(game_board_id=game_id))
    print("Player")
    pp.pprint(get_player(game_board_id=game_id, player_id=player_id))

if __name__ == '__main__':
    main()