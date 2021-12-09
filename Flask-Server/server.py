from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import time, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

time_now = 0
msg = "Hello User. Please wait other users to join. Survey will start once minimum users will join. Max waiting time " \
      "is 5 min "

# connected_msg_json = json.dumps(connected_msg, indent=4)
client_count = 0


@socketio.on('message')
def handle_message(msg):
    print("Connected with the client with data " + msg)


@socketio.on('connect')
def test_connect():
    print("Connected")
    f = open('data.json')
    data = json.load(f)
    minUserCount = data['minimumNoOfUser']
    global client_count, time_now
    if client_count == 0:
        time_now = int(time.time())
    client_count += 1
    print("Total no of connected client " + str(client_count))
    # send(connected_msg_json, json=True)
    send(time_now)
    # if(client_count > 5):
    if client_count > minUserCount:
        send("Continue", broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    global client_count
    client_count -= 1
    print("Total no of connected client " + str(client_count))


@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
