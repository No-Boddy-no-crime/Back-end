import connexion
import six

from game_server.models.card_set import CardSet  # noqa: E501
from game_server.models.error import Error  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server import util


def create_player(game_id):  # noqa: E501
    """Join a game as a player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Player
    """
    return 'do some magic!'


def make_accusation(game_id, player_id, card_set):  # noqa: E501
    """Create a new player accusation

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str
    :param card_set: The accusation card set
    :type card_set: dict | bytes

    :rtype: Player
    """
    if connexion.request.is_json:
        card_set = CardSet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def make_suggestion(game_id, player_id, card_set):  # noqa: E501
    """Create a new player suggestion

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str
    :param card_set: The suggestion card set
    :type card_set: dict | bytes

    :rtype: RebuttalCard
    """
    if connexion.request.is_json:
        card_set = CardSet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def move_player(game_id, player_id, body):  # noqa: E501
    """Create a new player move

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str
    :param body: The move
    :type body: int

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
