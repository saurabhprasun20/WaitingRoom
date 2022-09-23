from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit
import time, json, uuid, logging, psycopg2, logging
from random import randrange
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database="pre_tod",
                            user="prasun",
                            password="password")
    return conn


@app.route('/api/v1/user/assignment', methods=['GET'])
def get_assignment_time():
    conn = get_db_connection()
    curr = conn.cursor()
    args = request.args.to_dict()
    id = args.get("assignment_id")
    logging.info(f"args is {args}")
    logging.info(f"id is {id}")
    curr.execute("Select * from assignment_record where assignment_id=%s", (id,))
    assignment = curr.fetchall()
    insert_time = 0
    if len(assignment) == 0:
        insert_time = int(time.time())
        curr.execute('Insert into assignment_record (assignment_id,time)'
                     'values (%s, %s)',
                     (id, insert_time)
                     )
        conn.commit()
    curr.close()
    conn.close()
    if len(assignment) != 0:
        return str(assignment[0][1])
    else:
        return str(insert_time)


@app.route('/api/v1/first-user/time', methods=['GET'])
def get_active_time():
    f = open('data.json')
    data = json.load(f)
    activeTime = data['activeTime']
    return str(activeTime)


@app.route('/api/v1/url', methods=['GET'])
def get_url():
    f = open('data.json')
    data = json.load(f)
    chatRoom = data['chatRoom']
    return str(chatRoom)


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
    random_chatroom_selection = data['chatRoom']
    activeTime = data['activeTime']
    time_first_connection = data['firstUserTime']
    f.close()
    print("minimum user count is: " + str(minUserCount))
    print("request remote address is: " + str(request.headers["X-Forwarded-For"]))
    # if client_count == 0 or cycle_change == 1:
    # time_first_connection = int(time.time())
    if cycle_change == 1:
        previous_user_list = user_list.copy()
        with open("data.json", "r+") as jsonFile:
            data = json.load(jsonFile)
            time_first_connection = int(time.time())
            data['firstUserTime'] = time_first_connection
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

    print("User list after update")
    print(user_list)
    print("Total no of connected client " + str(client_count))
    # send(connected_msg_json, json=True)
    print("About to send the time when first user connected " + str(time_first_connection))
    send(str(time_first_connection) + '&' + str(activeTime) + '&' + str(random_chatroom_selection))
    emit('my event', str(time_first_connection))
    # if(client_count > 5):
    print("Previous user list & it's length")
    print(previous_user_list)
    print(len(previous_user_list))
    # if(client_count > 5):
    print("The minimum user required to open the chat room is:")
    print(minUserCount + len(previous_user_list))
    if client_count > minUserCount + len(previous_user_list):
        send("Continue" + str(round(time.time() * 1000)), broadcast=True)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    global client_count, previous_user_list, user_list
    if str(request.headers["X-Forwarded-For"]) in previous_user_list:
        previous_user_list.remove(str(request.headers["X-Forwarded-For"]))

    print("User list before removing the user")
    print(user_list)
    print("User being removed")
    print(request.headers["X-Forwarded-For"])
    if str(request.headers["X-Forwarded-For"]) in user_list:
        print("Yes")
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
