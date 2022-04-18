import turn_server
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
    print(room_mapping["ballroom_to_kitchen"])
    for player in players:
        if player["character_name"] == "Miss Scarlet":
            board[room_mapping["hall_to_lounge"]].append(player["player_id"])
        elif player["character_name"] == "Mrs White":
            board[room_mapping["ballroom_to_kitchen"]].append(player["player_id"])
        elif player["character_name"] == "Mrs Peacock":
            board[room_mapping["library_to_conservatory"]].append(player["player_id"])
        elif player["character_name"] == "Mr Green":
            board[room_mapping["conservatory_to_ballroom"]].append(player["player_id"])
        elif player["character_name"] == "Professor Plum":
            board[room_mapping["study_to_library"]].append(player["player_id"])
        elif player["character_name"] == "Colonel Mustard":
            board[room_mapping["lounge_to_dining"]].append(player["player_id"])
        else:
            board[room_mapping["billard_to_dining"]].append(player["player_id"])
    return board

def check_move(from_room, to_room):
    if to_room in valid_transitions[from_room]:
        return True
    return False

def update_game_board_with_move(game, moved_player_id, moved_to_room):
    board = game["board"]
    moved_player = None
    
    # find where the player was located, and remove them
    for room in board:
        for player in room:
            if player == moved_player_id:
                moved_player = player
                room.remove(player)
    
    # place the player in the new room
    print(moved_to_room, type(moved_to_room))
    if type(moved_to_room) is str:
        board[room_mapping[moved_to_room]].append(moved_player)
    elif type(moved_to_room) is int:
        board[moved_to_room].append(moved_player)
    game["board"] = board
    db.update_game(game["game_board_id"], game)
    # TODO: not a real function yet
    turn_server.notify_update_game_state(game)