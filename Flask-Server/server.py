from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit
import time, json, uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)


time_now = 0
msg = "Hello User. Please wait other users to join. Survey will start once minimum users will join. Max waiting time " \
      "is 5 min "

client_count = 0
user_list = []


@app.route('/')
def hello_world():
    return 'Hello PRODIGI!'


@socketio.on('message')
def handle_message(msg):
    print("Connected with the client with data " + msg)


@socketio.on('connect')
def test_connect():
    print("Connected")
    f = open('data.json')
    data = json.load(f)
    global client_count, time_now
    minUserCount = data['minimumNoOfUser']

    if client_count == 0:
        time_now = int(time.time())

    if str(request.remote_addr) not in user_list:
        print("New user")
        user_list.append(str(request.remote_addr))
        client_count += 1
    else:
        print("Old_user")
        user_list.append(str(request.remote_addr))

    print("Total no of connected client " + str(client_count))
    # send(connected_msg_json, json=True)
    print("About to send the time when first user connected " + str(time_now))
    send(time_now)
    emit('my event', str(time_now))
    # if(client_count > 5):
    if client_count > minUserCount:
        send("Continue", broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    global client_count
    user_list.remove(str(request.remote_addr))
    set_user_list = set(user_list)
    client_count = len(set_user_list)
    print("Total no of connected client " + str(client_count))


@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)


if __name__ == '__main__':
    app.run(debug=True)
