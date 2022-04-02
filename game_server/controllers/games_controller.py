from multiprocessing.sharedctypes import Value
import connexion
import six

from game_server.models.error import Error  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server import util
import game_server.db.database as db
from flask import abort


def create_game():  # noqa: E501
    """Create a game

     # noqa: E501


    :rtype: Game
    """
    try:
        game = db.create_game()
    except ValueError as e:
        abort(503, str(e))
    return jsonify(game)


def list_games(limit=None):  # noqa: E501
    """List all games

     # noqa: E501

    :param limit: How many items to return at one time (max 100)
    :type limit: int

    :rtype: List[Game]
    """
    try:
        games = db.get_games(limit=limit)
        print(games)
    except ValueError as e:
        abort(404, str(e))
    return games

def show_game_by_id(game_id):  # noqa: E501
    """Info for a specific game

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Game
    """
    try:
        game = db.get_game(game_board_id=game_id)
        print(game)
    except ValueError as e:
        abort(404, str(e))
    return game

def end_game(game_id):  # noqa: E501
    """Delete a specific Game

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: None
    """
    try:
        db.delete_game(game_id)
    except ValueError as e:
        abort(404, str(e))
    return True