import connexion
import six

from game_server.models.error import Error  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server import util
import game_server.db.database as db

def create_player(game_id):  # noqa: E501
    """Join a game as a player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Player
    """
    return db.create_player(game_board_id=game_id)


def make_accusation(game_id, player_id):  # noqa: E501
    """Create a new player accusation

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    game = db.get_game(game_board_id=game_id)
    for player in game["players"]:
        
    return 'an accusation!'


def make_suggestion(game_id, player_id):  # noqa: E501
    """Create a new player suggestion

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: RebuttalCard
    """
    return 'a suggestion!'


def move_player(game_id, player_id):  # noqa: E501
    """Create a new player move

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    return 'a move!'


def show_player_by_id(game_id, player_id):  # noqa: E501
    """Info for a specific player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str

    :rtype: Player
    """
    return db.get_player(game_board_id=game_id, player_id=player_id)
