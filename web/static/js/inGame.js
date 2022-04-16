var gameState = {}
var playerId = undefined;
/*
    const gameId 
        - found in html
        game_id of current game board

    const startGame
        - bool whether or not to start game
*/

/* executes once DOM is ready; 
 * this will be the only jquery used; only vanilla from here 
 */
$(document).ready(function(){
    socket = io()
    initListeners()

	if(gameId == 0 && startGame == true ){
        console.log('creating game')
        createGame();
    }
    console.log('creating player')
    createPlayer();

    joinGame();
    initAsyncComms();
});

const createPlayer = () => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/players`, 
            type: 'POST',
            success: function(response) { 
                console.log(`${JSON.stringify(response)}`);
                //TODO: set player
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
                console.log('response' + JSON.stringify(response))
                gameId = response['id'];
                startGame = false;
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}