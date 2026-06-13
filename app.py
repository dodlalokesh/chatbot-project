from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)

# Safer async mode (no eventlet needed)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)


@app.route("/")
def home():
    return render_template("index.html")


@socketio.on("join")
def handle_join(data):
    try:
        username = data.get("username")
        room = data.get("room")

        if not username or not room:
            emit("error", {"msg": "username or room missing"})
            return

        join_room(room)

        emit("message", {
            "user": "System",
            "msg": f"{username} joined {room}"
        }, to=room)

    except Exception as e:
        emit("error", {"msg": str(e)})


@socketio.on("send_message")
def handle_message(data):
    try:
        username = data.get("username")
        message = data.get("message")
        room = data.get("room")

        if not all([username, message, room]):
            emit("error", {"msg": "Invalid message data"})
            return

        emit("message", {
            "user": username,
            "msg": message
        }, to=room)

    except Exception as e:
        emit("error", {"msg": str(e)})


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True
    )
