const initSyncCommButton = () => {
    document.getElementById('get_games_id_button').onclick = function(){ listAllGames(compileListAllGamesPayload()); };
    document.getElementById('join_game_id_button').onclick = function(){ getGame(); }
    document.getElementById('create_game_button').onclick = function(){ createGame(); }

    document.getElementById('create_player_button').onclick = function(){ createPlayer(); }
    document.getElementById('make_accusation_button').onclick = function(){ makeAccusation(compilePlayerGuessPayload()); }
    document.getElementById('make_suggestion_button').onclick = function(){ makeSuggestion(compilePlayerGuessPayload()); }
    document.getElementById('move_player_button').onclick = function(){ movePlayer(compilePlayerMovementPayload()); }
    document.getElementById('player_info_button').onclick = function(){ getPlayerInfo(); }
}

const compileListAllGamesPayload = () => {limit: document.getElementById('get_games_limit').value}

const compilePlayerGuessPayload = () => {
    character_name: document.getElementById('who_select').value;
    weapon: document.getElementById('what_select').value;
    room: document.getElementById('where_select').value;
}

const compilePlayerMovementPayload = () => {move: document.getElementById('move_player_select').value}

const getGame = () => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('join_game_id').value}`, 
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const listAllGames = (payload) =>{
    $.ajax(
        {
            url: '/v1/games', 
            data: payload, 
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const createGame = () =>{
    $.ajax(
        {
            url: '/v1/games', 
            type: 'POST',
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const createPlayer = () => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('game_id_string_create_player').value}/players`, 
            type: 'POST',
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const getPlayerInfo = () => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('game_id_string_get_player').value}/players/${document.getElementById('player_id_string_get_player').value}`, 
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const makeAccusation = (payload) => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('game_id_accSug').value}/players/${document.getElementById('player_id_accSug').value}/accusation`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const makeSuggestion = (payload) => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('game_id_accSug').value}/players/${document.getElementById('player_id_accSug').value}/suggestion`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const movePlayer = (payload) => {
    $.ajax(
        {
            url: `/v1/games/${document.getElementById('game_id_move').value}/players/${document.getElementById('player_id_move').value}/move`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                console.log(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}
