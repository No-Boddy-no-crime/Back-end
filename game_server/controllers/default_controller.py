import connexion
import six

from game_server.models.card_set import CardSet  # noqa: E501
from game_server.models.game import Game  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server import util


def create_game():  # noqa: E501
    """Create a new game

    Create a new game # noqa: E501


    :rtype: Game
    """
    return 'do some magic!'


def create_player(game_id):  # noqa: E501
    """Create a new player

    Create a new player # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str

    :rtype: Player
    """
    return 'do some magic!'


def find_player(game_id, player_id):  # noqa: E501
    """Find a player

    Find a  player # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str
    :param player_id: ID of player to return
    :type player_id: str

    :rtype: Player
    """
    return 'do some magic!'


def get_game_by_id(game_id):  # noqa: E501
    """Find game by ID

    Returns a game # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str

    :rtype: Game
    """
    return 'do some magic!'


def make_accusation(game_id, player_id, accusation):  # noqa: E501
    """Make an accusation

    Create a new player accusation # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str
    :param player_id: ID of player to return
    :type player_id: str
    :param accusation: the player&#39;s accusation
    :type accusation: dict | bytes

    :rtype: CardSet
    """
    if connexion.request.is_json:
        accusation =  CardSet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def make_suggestion(game_id, player_id, suggestion):  # noqa: E501
    """Make a suggestion

    Create a new player suggestion # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str
    :param player_id: ID of player to return
    :type player_id: str
    :param suggestion: the player&#39;s suggestion
    :type suggestion: dict | bytes

    :rtype: RebuttalCard
    """
    if connexion.request.is_json:
        suggestion =  CardSet.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def move_player(game_id, player_id, move):  # noqa: E501
    """Create a new player move

    Create a new player move # noqa: E501

    :param game_id: ID of game to return
    :type game_id: str
    :param player_id: ID of player to return
    :type player_id: str
    :param move: attempted move
    :type move: 

    :rtype: Game
    """
    return 'do some magic!'
