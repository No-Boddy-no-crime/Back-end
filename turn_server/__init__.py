from flask_socketio import SocketIO



socketio = SocketIO()

def create_socketio(app):
    async_mode = None
    socketio.init_app(app, async_mode=async_mode)

    return app