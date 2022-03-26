var gameState = {}

/* executes once DOM is ready; 
 * this will be the only jquery used; only vanilla from here 
 */
$(document).ready(function(){
	socket = io()
	
	initListeners()
	initAsyncComms()

	joinGame()
	
	initSyncCommButton()
});