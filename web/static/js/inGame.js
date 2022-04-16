var gameState = {}

/* executes once DOM is ready; 
 * this will be the only jquery used; only vanilla from here 
 */
$(document).ready(function(){

	if(gameId == 0 && startGame == true ){
        createGame();
    }
});

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