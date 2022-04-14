

default_board = [[] for _ in range(20)]

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
                        [0, 8], 
                        [1, 3, 6], 
                        [2, 4], 
                        [2, 10], 
                        [3, 7, 16], 
                        [4, 12], 
                        [5, 9, 13], 
                        [8, 10], 
                        [8, 16], 
                        [9, 6, 11, 14], 
                        [10, 12], 
                        [10, 18], 
                        [7, 11, 15], 
                        [12, 20], 
                        [13, 17, 4], 
                        [16, 18], 
                        [17, 14, 19],  
                        [18, 20],
                        [19, 15, 0]]

def check_move(from_room, to_room):
    pass

def update_game_board_with_move(game, moved_player_id, moved_to_room):
    board = game["board"]
    moved_player = None
    
    # find where the player was located, and remove them
    for room in board:
        for player in room:
            if player["player_id"] == moved_player_id:
                moved_player = player
                room.remove(player)
    
    # place the player in the new room
    room_id = ROOM.index(moved_to_room)
    board[room_id].append(moved_player)