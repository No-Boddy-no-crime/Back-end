import game_server.db.database as db
import random

CULPRIT = ["Miss Scarlet",
                    "Mrs White",
                    "Mrs Peacock",
                    "Professor Plum",
                    "Mr Green",
                    "Colonel Mustard"]
WEAPON = ["rope", 
            "lead pipe", 
            "knife", 
            "wrench", 
            "candlestick", 
            "revolver"]
ROOM = ["study", 
        "hall", 
        "lounge", 
        "library", 
        "billard room", 
        "dining room", 
        "conservatory", 
        "ballroom", 
        "kitchen"]

CARDS = set([*ROOM, *WEAPON, *CULPRIT])

def pick_casefile(game_id):
    guilty_room = random.choice(ROOM)
    guilt_weapon = random.choice(WEAPON)
    guilty_person = random.choice(CULPRIT)
    casefile = set([guilty_room, guilt_weapon, guilty_person])
    db.update_game(game_board_id=game_id, new_game_state={"casefile": casefile})
    return casefile

def deal_remaining_cards(game_board_id, casefile):
    remaining_cards = list(CARDS.difference(casefile))
    game = db.get_game(game_board_id)
    players = game["players"]
    num_players = len(players)
    evenly_divisible = len(remaining_cards) // num_players
    visible_cards = len(remaining_cards) % num_players
    for player in players:
        player_cards = []
        for i in range(evenly_divisible):
            card = random.sample(remaining_cards, 1)[0]
            remaining_cards.remove(card)
            player_cards.append(card)
        player["cards"] = player_cards
    print(players)
    assert len(remaining_cards) == visible_cards
    db.update_game(game_board_id=game_board_id, new_game_state={"players": players, "visible_cards": visible_cards})
    return players, remaining_cards
