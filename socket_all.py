from flask_socketio import SocketIO
from flask_socketio import send, emit

socketio = SocketIO(app)

@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)

from flask_socketio import join_room, leave_room

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)