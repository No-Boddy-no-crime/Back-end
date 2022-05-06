import turn_server.turn_server as turn_server
import game_server.db.database as db

room_mapping = {"study" : 0, 
        "study_to_hall": 1,
        "study_to_library": 5,
        "hall": 2, 
        "hall_to_lounge":3,
        "hall_to_billard": 6,
        "lounge": 4,
        "lounge_to_dining": 7, 
        "library": 8,
        "library_to_billard": 9,
        "library_to_conservatory": 13, 
        "billard room": 10, 
        "billard_to_dining": 11,
        "billard_to_ballroom": 14,
        "dining room": 12, 
        "dining_to_kitchen": 15,
        "conservatory": 16, 
        "conservatory_to_ballroom": 17,
        "ballroom": 18, 
        "ballroom_to_kitchen": 19,
        "kitchen": 20}

valid_transitions = [[1, 5, 20], 
                        [0, 2],  
                        [1, 3, 6], 
                        [2, 4],  
                        [3, 7, 16],
                        [0, 8],
                        [2, 10], 
                        [4, 12], 
                        [5, 9, 13], 
                        [8, 10],
                        [9, 6, 11, 14], 
                        [10, 12],
                        [7, 11, 15], 
                        [8, 16],
                        [10, 18], 
                        [12, 20], 
                        [13, 17, 4], 
                        [16, 18], 
                        [17, 14, 19],  
                        [18, 20],
                        [19, 15, 0]]

def start_game_board(game):
    board = game["board"]
    players = game["players"]
    if board is None or not board:
        board = [[] for _ in range(21)]

    for player in players:
        if player["character_name"] == "Miss Scarlet" and player["player_id"] not in board[room_mapping["hall_to_lounge"]]:
                board[room_mapping["hall_to_lounge"]].append(player["player_id"])
        elif player["character_name"] == "Mrs White" and player["player_id"] not in board[room_mapping["ballroom_to_kitchen"]]:
            board[room_mapping["ballroom_to_kitchen"]].append(player["player_id"])
        elif player["character_name"] == "Mrs Peacock" and player["player_id"] not in board[room_mapping["library_to_conservatory"]]:
            board[room_mapping["library_to_conservatory"]].append(player["player_id"])
        elif player["character_name"] == "Mr Green" and player["player_id"] not in board[room_mapping["conservatory_to_ballroom"]]:
            board[room_mapping["conservatory_to_ballroom"]].append(player["player_id"])
        elif player["character_name"] == "Professor Plum" and player["player_id"] not in board[room_mapping["study_to_library"]]:
            board[room_mapping["study_to_library"]].append(player["player_id"])
        elif player["character_name"] == "Colonel Mustard" and player["player_id"] not in board[room_mapping["lounge_to_dining"]]:
            board[room_mapping["lounge_to_dining"]].append(player["player_id"])
    return board

def check_move(from_room, to_room):
    print("Checking the move")
    if to_room in valid_transitions[from_room]:
        return True
    return False

def update_game_board_with_move(game, moved_player_id, moved_from_room, moved_to_room):
    board = game["board"]

    if type(moved_to_room) is str:
        moved_to_room = room_mapping[moved_to_room]

    # find where the player was located, and remove them
    board[moved_from_room].remove(moved_player_id)
    board[moved_to_room].append(int(moved_player_id))
    game["board"] = board
    db.update_game(game["game_board_id"], game)
    # TODO: not a real function yet
    turn_server.gameState(game)