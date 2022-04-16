from nis import match
import connexion
import six

from game_server.models.card_set import CardSet  # noqa: E501
from game_server.models.error import Error  # noqa: E501
from game_server.models.player import Player  # noqa: E501
from game_server.models.rebuttal_card import RebuttalCard  # noqa: E501
from game_server.models.move import Move
from game_server import util
from game_server.controllers.card_controller import CULPRIT, ROOM
import game_server.controllers.board_controller as board_controller
import turn_server.turn_server as turn_server 
import game_server.db.database as db


def create_player(game_id):  # noqa: E501
    """Join a game as a player

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str

    :rtype: Player
    """
    return db.create_player(game_board_id=game_id)


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
    game = db.get_game(game_id)
    case_file = set(game["casefile"])
    if case_file == set(card_set):
        # TODO: not a real function yet
        turn_server.notify_players_of_winner(player_id)
        return True
    # this is a positional update
    db.update_player(game_id, player_id, {"players.$.status": "post-accusation"})
    return {}


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
    # TODO : probably some error checking to make sure its a person place room 
    if connexion.request.is_json:
        card_set = CardSet.from_dict(connexion.request.get_json())  # noqa: E501
    
    game = db.get_game(game_id)
    suggestion_move_player(game, card_set)
    players = game["players"]
    # rotate to place the current player at the front (meaning put the list in order form who would be to the "left" of this player)
    # and remove that player
    rotated_player_list = players[player_id + 1:] + players[:player_id]

    for other_player in rotated_player_list:
        matching_cards =  set(other_player["cards"]).intersection(card_set)
        if len(matching_cards) == 0:
            continue
        elif len(matching_cards) == 1:
            # TODO: not a real function yet
            turn_server.notify_players_of_rebutall(other_player["player_id"])
            rebuttal = {"player_id": other_player["player_id"], "rebuttal_card": matching_cards.pop()}
            return rebuttal
        else:
            # TODO: not a real function yet
            rebuttal = turn_server.notify_player_to_rebute(other_player["player_id"], list(matching_cards))
            return rebuttal
    
    # if we are here, there was no rebute
    # TODO: not a real function yet
    turn_server.notify_players_no_rebute(card_set)
    return {}

def suggestion_move_player(game, card_set):
    moved_character = set(card_set).intersection(CULPRIT)
    moved_to_room = set(card_set).intersection(ROOM)
    moved_player_id = None

    for player in game["players"]:
        if player["character"] == moved_character:
            moved_player_id = player["player_id"]
            break
    
    board_controller.update_game_board_with_move(game, moved_player_id, moved_to_room)


def move_player(game_id, player_id, move):  # noqa: E501
    """Create a new player move

     # noqa: E501

    :param game_id: The id of the game to retrieve
    :type game_id: str
    :param player_id: The id of the player to retrieve
    :type player_id: str
    :param move: The move
    :type move: dict | bytes

    :rtype: Player
    """
    if connexion.request.is_json:
        move = Move.from_dict(connexion.request.get_json())  # noqa: E501
    if board_controller.check_move(move.from_room, move.to_room):
        board_controller.update_game_board_with_move(player_id)
    else:
        return 'illegal move'


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
