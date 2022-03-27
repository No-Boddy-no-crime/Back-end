import connexion
import six

from game_server.models.error import Error  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server import util
import game_server.db.database as db


def create_game():  # noqa: E501
    """Create a game

     # noqa: E501


    :rtype: Game
    """
    return db.create_game()


def list_games(limit=None):  # noqa: E501
    """List all games

     # noqa: E501

    :param limit: How many items to return at one time (max 100)
    :type limit: int

    :rtype: List[Game]
    """
    print(db.get_games(limit=limit))
    return db.get_games(limit=limit)

def show_game_by_id(game_id):  # noqa: E501
    """Info for a specific game

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Game
    """
    print(db.get_game(game_board_id=game_id))
    return db.get_game(game_board_id=game_id)
