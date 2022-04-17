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
	asyncIDTurn = setInterval(checkForTurn, MILLISECONDS_IN_A.SEC * 10)

	asyncIDState = setInterval(requestGameState, MILLISECONDS_IN_A.SEC * 10)
}

/* internal state */
const updateGameState = (msg) => {
	console.log(msg)
	if(msg == undefined) return
	if(msg['status'] == 'new') updatePlayers(msg['players']);

	if(msg['status'] == 'in-play') updateBoard(msg);
}

/* requests to server */
const joinGame = () => {
	console.log("joined game...")
	console.log(JSON.stringify(`{game_board_id: ${gameId}, character_name: ${player.name}}`))
	send('joinGame', {game_board_id: gameId, character_name: player.name})
}
const checkForTurn = () => send('gameTurn', {game_board_id: gameId})
const requestGameState = () => send('gameState')

/* main query point */
const send = (eventName, payload) => socket.emit(eventName, payload)