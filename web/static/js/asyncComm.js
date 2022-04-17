var socket;
var asyncIDTurn;
var asyncIDState;

const MILLISECONDS_IN_A = Object.freeze({SEC: 1000, MIN: 60000, HOUR: 3600000});

/* sockets listening post */
const initListeners = () => {
	socket.on('connect', (msg) => console.log(msg))
	socket.on('gameTurn', (msg) => console.log(msg))
	socket.on('GameState', (msg) => updateGameState(msg))
}

/* query server periodically */
const initAsyncComms = () => {
	asyncIDTurn = setInterval(function(){
		console.log('jere')
		checkForTurn(gameId)
	}, MILLISECONDS_IN_A.SEC * 10)

	asyncIDState = setInterval(requestGameState, MILLISECONDS_IN_A.SEC * 10)
}

/* internal state */
const updateGameState = (msg) => {
	if(msg == undefined) return
	
	if(msg['status'] == 'new') updatePlayers(msg['players']);
}

/* requests to server */
const joinGame = (gameId) => send('joinGame', {game_board_id: gameId, character_id: player.id})
const checkForTurn = (gameId) => send('gameTurn', {game_board_id: gameId})
const requestGameState = () => send('gameState')

/* main query point */
const send = (eventName, payload) => socket.emit(eventName, payload)