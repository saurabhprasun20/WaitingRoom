from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True)


@app.route('/')
def start():
    return 'Chat room activated'


@socketio.on('connect')
def handle_connect():
    print('connected')


@socketio.on('message')
def handle_msg(msg):
    print("Process the received message " + msg)
    reply = ''
    if msg == 'Hi!':
        reply = "Hello!"
    elif msg == 'Connected':
        reply = 'Welcome user!'
    elif msg == 'How are you?':
        reply = 'I am good and how are you'
    else:
        reply = 'I am not intelligent enough to talk more'

    send("Bot: " + reply, broadcast=True)


if __name__ == '__main__':
    app.run(debug=True)
