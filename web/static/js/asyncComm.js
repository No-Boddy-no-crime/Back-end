var socket;
var asyncIDTurn;
var asyncIDState;

const MILLISECONDS_IN_A = Object.freeze({SEC: 1000, MIN: 60000, HOUR: 3600000});

/* sockets listening post */
const initListeners = () => {
	socket.on('connect', (msg) => appendServerResponse(msg))
	socket.on('gameTurn', (msg) => appendServerResponse(msg))
	socket.on('GameState', (msg) => updateGameState(msg))
}

/* query server periodically */
const initAsyncComms = () => {
	asyncIDTurn = setInterval(checkForTurn, MILLISECONDS_IN_A.SEC * 24)
	asyncIDState = setInterval(requestGameState, MILLISECONDS_IN_A.SEC * 10)
}

/* append message as they come in */
const appendServerResponse = (msg) => {
	if(msg == undefined) return
	const div = document.createElement('div')
	div.innerText = msg
	document.getElementById('asyncServerMessages').append(div)
}

/* internal state */
const updateGameState = (msg) => {
	if(msg == undefined) return
	gameState = msg
	appendServerResponse('Updated GameState')
}

/* requests to server */
const joinGame = () => send('joinGame', {game_board_id: 452, character_name: 'Colonel Mustard'})
const checkForTurn = () => send('gameTurn', {game_board_id: 452})
const requestGameState = () => send('gameState')

/* main query point */
const send = (eventName, payload) => socket.emit(eventName, payload)