import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("join")
def join(data):
    print("JOIN EVENT:", data)

    username = data["username"]
    room = data["room"]

    join_room(room)

    emit("message", {
        "user": "System",
        "msg": f"{username} joined {room}"
    }, to=room)


@socketio.on("send_message")
def send(data):
    print("MESSAGE EVENT:", data)

    emit("message", {
        "user": data["username"],
        "msg": data["message"]
    }, to=data["room"])


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
