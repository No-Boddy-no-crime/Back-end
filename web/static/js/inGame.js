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
    socket = io();

	if(gameId == 0 && startGame == true ){
        console.log('creating game')
        createGame();

    } else{
        createPlayer();
        document.getElementById("startGameForReal").remove();
    }

    setTimeout(function(){
        initListeners()
        initAsyncComms();
        joinGame();
    }, 500);



    document.getElementById('move_player_button').onclick = function(){ movePlayerUI() };
    document.getElementById('make_suggestion_button').onclick = function(){ suggestPlayer(); };
    document.getElementById('make_accusation_button').onclick = function(){ accusePlayer(); };
});

const startGameBoard = () =>{
    $.ajax(
        {
            url: `/v1/games/${gameId}`, 
            type: 'POST',
            success: function(response) { 
                console.log('startGame')
                document.getElementById("startGameForReal").remove();
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
            url: `/v1/games/${gameId}/player`, 
            type: 'POST',
            success: function(response) { 
                console.log(`${JSON.stringify(response)}`);
                //TODO: set player
                player.name = response['character_name'];
                player.id = response['player_id'];
                startingPos(player, true);
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
                document.getElementById("startGameForReal").disabled = false;
                document.getElementById("startGameForReal").onclick = function(){ startGameBoard(); }
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const compileMovePayload = (from, to) => ({
  "from_room": from,
  "to_room": to
})

const movePlayer = (from, to) => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/player/${player.id}/move`, 
            data: JSON.stringify(compileMovePayload(from, to)), 
            type: 'POST',
            contentType: 'application/json',
            success: function(response) { 
                console.log("Moved Player");
                console.log(JSON.stringify(response));
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const compileAccusePayload = () => ({
    "character_name": `${document.getElementById('who_select').value}`,
    "player": {
        "character_name": `${player.name}`,
        "player_id": `${player.id}`
    },
    "room": `${document.getElementById('where_select').value}`,
    "weapon": `${document.getElementById('what_select').value}`
})

const compileSuggestPayload = () => ({
    "character_name": `${document.getElementById('who_select').value}`,
    "player": {
        "character_name": `${player.name}`,
        "player_id": `${player.id}`
    },
    "room": `${document.getElementById('where_select').value}`,
    "weapon": `${document.getElementById('what_select').value}`
})

const accusePlayer = () => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/player/${player.id}/accusation`, 
            data: JSON.stringify(compileSuggestPayload()), 
            type: 'POST',
            contentType: 'application/json',
            success: function(response) { 
                console.log("Accused Player");
                console.log(JSON.stringify(response));

                if(JSON.stringify(response) == 'true')
                    alert('Correct Accusation - Winner');
                else
                    alert('Incorrect Accusation - Loser');
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const suggestPlayer = () => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/player/${player.id}/suggestion`, 
            data: JSON.stringify(compileAccusePayload()), 
            type: 'POST',
            contentType: 'application/json',
            success: function(response) { 
                console.log("Suggested Player");
                console.log(JSON.stringify(response));
                //alert(JSON.stringify(response))
                appendServerResponse(`${response["player"]["character_name"]} rebutted with ${response["card"]}`)
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const getCards = () => {
    $.ajax(
        {
            url: `/v1/games/${gameId}/player/${player.id}`,
            type: 'GET',
            contentType: 'application/json',
            success: function(response) { 
                console.log("Get Cards");
                console.log(JSON.stringify(response));
                displayCards(response['cards'])
            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        }
   );
}

const displayCards = (cardArr) => {
    const cardCont = document.getElementById('playerCards');

    cardArr.forEach((cardName, index) => {
        if(document.getElementById((cardName + 'Card')) == null){
            const card = document.createElement('div');
            card.id = cardName + 'Card';
            card.innerText = `${index}: ${cardName}`;
            cardCont.append(card);
        }
    })
}

const appendServerResponse = (msg) => {
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
    playerBox.innerText = player.name + '(You)';
    playerBox.id = `${player.name}`;

    const oldLoc = document.getElementById(`${player.name}`);
    if(oldLoc != null){
        oldLoc.remove();
    }

    const newLoc = document.getElementById(`${endPos}`);
    newLoc.append(playerBox);

    allowableMoves(endPos);

    player.pos = endPos;

    //server call
    movePlayer(start, endPos);
}

function startingPos(character, directUser){
    
    //skip over already added people
    const old = document.getElementById(`${character.name}`);
    if(old != undefined) return;

    const playerBox = document.createElement('div');
    playerBox.innerText = character.name;

    if(directUser){
        playerBox.innerText = playerBox.innerText + ' (You)';
    }

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

function updatePlayers(playerArr){
    playerArr
    .filter((otherPlayer) => otherPlayer['player_id'] != player.id )
    .forEach((otherPlayer) => {
        const character = {};
        character.name = otherPlayer['character_name'] //TODO: fix this garbage
        startingPos(character, false)
    });
}

function updateBoard(msg){
    const board = msg['board'];
    const players = msg['players']

    updateBoardLoc(board, players);
}

function updateBoardLoc(board, players){

    for(let i = 0; i < board.length; i++){
        if(board[i].length == 0) continue;

        const spot = board[i];
        const playersAtSpot = spot.length;

        for(let k = 0; k < playersAtSpot; k++){
            const playerId = spot[k];
            const cName = getPlayerName(players, playerId);

            const playerBox = document.createElement('div');
            playerBox.innerText = cName;
            playerBox.id = `${cName}`;

            const oldLoc = document.getElementById(`${cName}`);
            if(oldLoc != null){
                oldLoc.remove();  
            }
            const newLoc = document.getElementById(`${i}`);
            newLoc.append(playerBox);

            if(playerId == player.id){
                allowableMoves(i);
                player.pos = i;
                playerBox.innerText = playerBox.innerText + '(You)';
            }
        }
    }
}

function getPlayerName(players, playerId){
    for(let i = 0; i < players.length; i++){
        if(playerId == players[i]['player_id']){
            return players[i]['character_name']
        }
    }
}

async function chooseRebuttal(arr){

    document.getElementById('chooseRebutDiv').innerText = 'Choose a card to rebut with';

    for(let i = 0; i < arr.length; i++){
        $('#rebutDropDown').append($('<option>', {
            value: `${arr[i]}`,
            text: `${arr[i]}`
        }));
    }
    await new Promise(r => setTimeout(r, 10000));
    document.getElementById('chooseRebutDiv').innerText = 'No card to rebut';
    const ret = $('#rebutDropDown').val()
    $('#rebutDropDown').empty()
    return {card: ret};
}