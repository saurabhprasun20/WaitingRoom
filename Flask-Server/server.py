from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit
import time, json, uuid, logging
from random import randrange
from randomChat import select_chat_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)
logger = logging.getLogger()

time_first_connection = 0
random_chatroom_selection = -1
msg = "Hello User. Please wait other users to join. Survey will start once minimum users will join. Max waiting time " \
      "is 5 min "

client_count = 0
user_list = []
previous_user_list = []


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
    global client_count, time_first_connection, random_chatroom_selection, previous_user_list, user_list
    minUserCount = data['minimumNoOfUser']
    cycle_change = data['cycleChange']
    f.close()
    print("minimum user count is: " + str(minUserCount))
    print("request remote address is: " + str(request.headers["X-Forwarded-For"]))
    if client_count == 0 or cycle_change == 1:
        time_first_connection = int(time.time())
        random_chatroom_selection = select_chat_room()
        if cycle_change == 1:
            previous_user_list = user_list
            with open("data.json", "r+") as jsonFile:
                data = json.load(jsonFile)
                data['cycleChange'] = 0
                jsonFile.seek(0)  # rewind
                json.dump(data, jsonFile)
                jsonFile.truncate()

    if str(request.headers["X-Forwarded-For"]) not in user_list:
        print("New user")
        user_list.append(str(request.headers["X-Forwarded-For"]))
        client_count += 1
    else:
        print("Old_user")
        user_list.append(str(request.headers["X-Forwarded-For"]))

    print("Total no of connected client " + str(client_count))
    # send(connected_msg_json, json=True)
    print("About to send the time when first user connected " + str(time_first_connection))
    send(str(time_first_connection)+'&'+str(random_chatroom_selection))
    emit('my event', str(time_first_connection))
    # if(client_count > 5):
    if client_count > minUserCount+len(previous_user_list):
        send("Continue", broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    global client_count, previous_user_list
    if str(request.headers["X-Forwarded-For"]) in previous_user_list:
        previous_user_list.remove(str(request.headers["X-Forwarded-For"]))
    user_list.remove(str(request.headers["X-Forwarded-For"]))
    set_user_list = set(user_list)
    client_count = len(set_user_list)
    print("Total no of connected client " + str(client_count))


@socketio.on('my event')
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)


def initialize():
    emit("disconnect", broadcast=True)


if __name__ == '__main__':
    app.run(debug=True)
