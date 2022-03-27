import connexion
import unittest

from turn_server.turn_server import socketio, gameTurn, gameState, joinGame, create_socketio

app = connexion.App(__name__, specification_dir='./openapi/')

app.app.static_url_path = "../web/static"
app.app.static_folder = '../web/static'
app.app.template_folder = '../web/templates'

create_socketio(app.app)

@socketio.on('join game', namespace='/test')
def on_join_game(message):
    joinGame(message)

@socketio.on('game turn', namespace='/test')
def on_game_turn(arg):
    gameTurn(arg)

@socketio.on('game state', namespace='/test')
def on_game_state(arg):
    gameState(arg)

class TestTurnServer(unittest.TestCase):
    def test_connect(self):
        client = socketio.test_client(app.app, namespace='/test')
        self.assertTrue(client.is_connected('/test'))
        received = client.get_received('/test')
        self.assertEqual(len(received), 3)
        self.assertEqual(received[0]['args'], 'connected-test')
        self.assertEqual(received[1]['args'], '{}')
        self.assertEqual(received[2]['args'], '{}')
        client.disconnect(namespace='/test')
        self.assertFalse(client.is_connected('/test'))

    def test_join_game(self):
        client1 = socketio.test_client(app.app, namespace='/test')
        client2 = socketio.test_client(app.app, namespace='/test')

        client1.get_received('/test')
        client2.get_received('/test')

        client1.emit('join game', {'game_board_id': 239}, namespace='/test')
        client2.emit('join game', {'game_board_id': 239}, namespace='/test')

        self.assertDictEqual(client1.get_received('/test')[0], client2.get_received('/test')[0]) # client1 receives 2 messages, client2 only receives 1

    def test_game_turn(self):
        client = socketio.test_client(app.app, namespace='/test')
        client.get_received('/test')
        client.emit('game turn', 'testing', namespace='/test')
        received = client.get_received('/test')
        self.assertEqual(len(received), 1) # should only recieve 1 message.
        self.assertEqual(len(received[0]['args']), 1) # gameTurn currently emits string "It is your turn."

    def test_game_state(self):
        client = socketio.test_client(app.app, namespace='/test')
        client.get_received('/test')
        client.emit('game state', 'testing', namespace='/test')
        received = client.get_received('/test')
        self.assertEqual(len(received), 1) # should only receive 1 message.
        self.assertEqual(len(received[0]['args']), 1) # returns entire game state or empty dict.

if __name__=="__main__":
    unittest.main()
