import random
from flask import Flask
from flask_pymongo import PyMongo
import pymongo

MONGO_DB = None
characters = set(["Miss Scarlet",
                    "Mrs White",
                    "Mrs Peacock",
                    "Professor Plum",
                    "Mr Green",
                    "Colonel Mustard"])

def setup_db(flask_app):
    global MONGO_DB
    flask_app.config["MONGO_URI"] = "mongodb://localhost:27017/clueDB"
    MONGO_DB = PyMongo(flask_app).db

def get_db():
    return MONGO_DB

def get_games_collection():
    assert MONGO_DB is not None
    return MONGO_DB.get_collection("Games")


def create_game():
    game_id = random.randint(0, 500)
    game = {"game_board_id": game_id, 
            "name": "This is our game name",
            "board": [],
            "status": "new",
            "players": []}
    get_games_collection().insert_one(game)
    return game.pop("_id")

def get_games(limit = None):
    if limit:
        return list(get_games_collection().find({},{'_id': False}).limit(limit))
    return list(get_games_collection().find({}, {'_id': False}))

def get_game(game_board_id = None):
    if game_board_id:
        return get_games_collection().find_one({"game_board_id": game_board_id}, {'_id': False})
    return get_games_collection().find_one()


def create_player(game_board_id):
    # TODO: race condition here
    try:
        taken_characters = set([player["character_name"] for player in get_games_collection().find_one({"game_board_id": game_board_id}, {"players": 1, "_id": 0})["players"]])
        available_characters = characters.difference(taken_characters)
    except KeyError:
        available_characters = characters
    # TODO: player ID should be real
    player_id = random.randint(0, 7)
    player = {
        "player_id": player_id,
        "character_name": list(available_characters)[0]
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
    game = create_game()
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