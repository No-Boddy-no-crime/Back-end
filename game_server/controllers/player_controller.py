import connexion
import six

from game_server.models.error import Error  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server import util
from game_server.db.database import get_db

def create_player(game_id):  # noqa: E501
    """Join a game as a player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Player
    """
    return 'do some magic!'


def make_accusation(game_id, player_id):  # noqa: E501
    """Create a new player accusation

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    return 'do some magic!'


def make_suggestion(game_id, player_id):  # noqa: E501
    """Create a new player suggestion

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: RebuttalCard
    """
    return 'do some magic!'


def move_player(game_id, player_id):  # noqa: E501
    """Create a new player move

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    return 'do some magic!'


def show_player_by_id(game_id, player_id):  # noqa: E501
    """Info for a specific player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    return 'do some magic!'
