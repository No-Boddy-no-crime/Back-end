/* executes once DOM is ready; 
 * this will be the only jquery used; only vanilla from here 
 */
$(document).ready(function(){
    listAllGames(compileListAllGamesPayload())
});

const limitGames = 100;

const compileListAllGamesPayload = () => {limit: limitGames};

const listAllGames = (payload) =>{
    $.ajax(
        {
            url: '/v1/games', 
            type: 'GET',
            data: payload, 
            success: function(response) { 
                displayGames(response);
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const displayGames = (response) => response.forEach((game) => appendGame(game));

const appendGame = (game) => {
    const gameId = game['game_board_id'];
    const numPlayers = game['players'].length;

    const availGamesDiv = document.getElementById('availGames');

    const newGameDiv = document.createElement('div');
    newGameDiv.innerText = `Game number ${gameId} has ${numPlayers} players.`;

    availGamesDiv.append(newGameDiv);
}


