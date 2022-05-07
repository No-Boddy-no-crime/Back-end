var socket;
var asyncIDTurn;
var asyncIDState;

const MILLISECONDS_IN_A = Object.freeze({SEC: 1000, MIN: 60000, HOUR: 3600000});

/* sockets listening post */
const initListeners = () => {
	socket.on('connect', (msg) => {
		console.log('Connect'); 
		appendServerResponse(msg);
	});
	socket.on('gameTurn', (msg) => {
		console.log('GameTurn'); 
		console.log(msg);
	});
	socket.on('GameState', (msg) => {
		console.log('GameState'); 
		updateGameState(msg);
	})
	socket.on('noRebuttal', (msg) => {
		console.log('No Rebuttal'); 
		appendServerResponse(msg);
	})
	socket.on('chooseRebuttalCard', (msg, cb) => {
		console.log('chooseRebuttalCard'); 
		chooseRebuttal(msg['cards'])
		setTimeout( () => { cb(cleanUpCb()); }, 11000);
		
	})
	socket.on('rebuttal', (msg) => {
		console.log('rebuttal'); 
		appendServerResponse(msg);
	})
	socket.on('rebuttalAll', (msg) => {
		console.log('rebuttal'); 
		appendServerResponse(msg);
	})
	socket.on('GameOver', (msg) => {
		console.log('GameOver'); 
		appendServerResponse(msg);
	})
	socket.on('falseAccusation', (msg) => {
		console.log('falseAccusation'); 
		appendServerResponse(msg);
	})
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

	if(msg['status'] == 'in-play'){
		updateBoard(msg);
		getCards();
	}
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

//send('chooseRebuttalCard', {'wrench'})