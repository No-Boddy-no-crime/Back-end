import connexion
import six

from game_server.models.error import Error  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server import util


def create_game():  # noqa: E501
    """Create a game

     # noqa: E501


    :rtype: Game
    """
    return 'do some magic!'


def list_games(limit=None):  # noqa: E501
    """List all games

     # noqa: E501

    :param limit: How many items to return at one time (max 100)
    :type limit: int

    :rtype: List[Game]
    """
    return 'do some magic!'


def show_game_by_id(game_id):  # noqa: E501
    """Info for a specific game

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Game
    """
    return 'do some magic!'
