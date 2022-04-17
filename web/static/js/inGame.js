var gameState = {}
var player = { id: undefined, name: undefined, pos: undefined };
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

	if(gameId == 0 && startGame == true ){
        console.log('creating game')
        createGame();

    } else{
        createPlayer();
    }

    setTimeout(function(){
        initListeners()
        initAsyncComms();
        joinGame();
    }, 500);



    document.getElementById('move_player_button').onclick = function(){ movePlayerUI() };
});

const createPlayer = () => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/player`, 
            type: 'POST',
            success: function(response) { 
                console.log(`${JSON.stringify(response)}`);
                //TODO: set player
                player.name = response['character_name'];
                player.id = response['player_id'];
                startingPos(player);
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
                gameId = response['game_board_id'];
                startGame = false;
                console.log('creating player')
                createPlayer();
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
            url: `/v1/games/${{gameId}}/players/${{playerId}}/accusation`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                appendServerResponse2(`Made accusation: ` + JSON.stringify(response))
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
            url: `/v1/games/${{gameId}}/players/${{playerId}}/suggestion`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                appendServerResponse2(`Made suggestion: ` + JSON.stringify(response))
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
            url: `/v1/games/${{gameId}}/players/${{playerId}}/move`, 
            data: payload, 
            type: 'POST',
            success: function(response) { 
                appendServerResponse2(`Moved player: ` + JSON.stringify(response))
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const appendServerResponse2 = (msg) => {
	if(msg == undefined) return
	const div = document.createElement('div')
	div.innerText = msg
	document.getElementById('syncServerMessages').append(div)
}

const allowableMoves = (pos) => {
    $("#move_player_select").empty();
    const allowed = [];

    if(pos == 0) {
        allowed.push('Right');
        allowed.push('Down');
        allowed.push('Secret Passage');
    } else if(pos == 1) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 2) {
        allowed.push('Right');
        allowed.push('Left');
        allowed.push('Down');
    } else if(pos == 3) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 4) {
        allowed.push('Left');
        allowed.push('Down');
        allowed.push('Secret Passage');
    }

    else if(pos == 5) {
        allowed.push('Up');
        allowed.push('Down');
    } else if(pos == 6) {
        allowed.push('Up');
        allowed.push('Down');
    }
    else if(pos == 7) {
        allowed.push('Up');
        allowed.push('Down');
    }

    else if(pos == 8) {
        allowed.push('Up');
        allowed.push('Down');
        allowed.push('Right');
    } else if(pos == 9) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 10) {
        allowed.push('Up');
        allowed.push('Down');
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 11) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 12) {
        allowed.push('Up');
        allowed.push('Down');
        allowed.push('Left');
    }

    else if(pos == 13) {
        allowed.push('Up');
        allowed.push('Down');
    } else if(pos == 14) {
        allowed.push('Up');
        allowed.push('Down');
    }
    else if(pos == 15) {
        allowed.push('Up');
        allowed.push('Down');
    }

    else if(pos == 16) {
        allowed.push('Up');
        allowed.push('Right');
        allowed.push('Secret Passage');
    } else if(pos == 17) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 18) {
        allowed.push('Right');
        allowed.push('Left');
        allowed.push('Up');
    } else if(pos == 19) {
        allowed.push('Right');
        allowed.push('Left');
    } else if(pos == 20) {
        allowed.push('Left');
        allowed.push('Up');
        allowed.push('Secret Passage');
    }

    else if(typeof pos == 'string'){
        allowed.push('hallway');
    }

    allowed.forEach((item) => {
        $('#move_player_select').append($('<option>', {
            value: item,
            text: item
        }));
    })
}

const getEndPosFromMove = (move, start) => {

    if(move == 'hallway'){
        if(start == 'scarlet') return 3;
        else if(start == 'green') return 17;
        else if(start == 'white') return 19;
        else if(start == 'plum') return 5;
        else if(start == 'mustard') return 7;
        else if(start == 'peacock') return 13;
    }


    if(move == 'Right') return start + 1; 
    else if(move == 'Left') return start - 1;
    else if(move == 'Up') {
        if(start == 5 || start == 13) return start - 5;
        else if(start == 6 || start == 14) return start - 4;
        else if(start == 7 || start == 15) return start - 3;
        else if(start == 8 || start == 16) return start - 3;
        else if(start == 10 || start == 18) return start - 4;
        else if(start == 12 || start == 20) return start - 5;
    }
    else if(move == 'Down'){
        if(start == 5 || start == 13) return start + 3;
        else if(start == 6 || start == 14) return start + 4;
        else if(start == 7 || start == 15) return start + 5;
        else if(start == 8 || start == 0) return start + 5;
        else if(start == 10 || start == 2) return start + 4;
        else if(start == 12 || start == 4) return start + 3;
    }
    else if(move == 'Secret Passage'){
        if(start == 0) return 20;
        else if(start == 4) return 16;
        else if(start == 16) return 4;
        else if(start == 20) return 0;
    }
}

const movePlayerUI = () => {
    const start = player.pos;
    const move = document.getElementById('move_player_select').value;

    const endPos = getEndPosFromMove(move, start);

    const playerBox = document.createElement('div');
    playerBox.innerText = player.name;
    playerBox.id = `${player.name}`;

    const oldLoc = document.getElementById(`${player.name}`);
    if(oldLoc != null){
        oldLoc.remove();
    }

    const newLoc = document.getElementById(`${endPos}`);
    newLoc.append(playerBox);

    allowableMoves(endPos);

    player.pos = endPos;
}

function startingPos(character){
    
    const playerBox = document.createElement('div');
    playerBox.innerText = character.name;
    playerBox.id = `${character.name}`;

    let startId = undefined;

    if(character.name == 'Miss Scarlet') {
        player.pos = 'scarlet';
        startId = 'sS'
    }
    else if(character.name == 'Mr Green'){
        player.pos = 'green';
        startId = 'gS';
    }
    else if(character.name == 'Mrs White'){
        player.pos = 'white';
        startId = 'wS';
    }
    else if(character.name == 'Professor Plum'){
        player.pos = 'plum';
        startId = 'plumS';
    }
    else if(character.name == 'Colonel Mustard'){
        player.pos = 'mustard';
        startId = 'mS';
    }
    else if(character.name == 'Mrs Peacock'){
        player.pos = 'peacock';
        startId = 'peaS';
    }

    const startBox = document.getElementById(startId)
    startBox.append(playerBox);

    allowableMoves(player.pos);
}
