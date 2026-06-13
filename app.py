from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("join")
def join(data):
    join_room(data["room"])
    emit("message", {
        "user": "System",
        "msg": f"{data['username']} joined {data['room']}"
    }, to=data["room"])

@socketio.on("send_message")
def send(data):
    emit("message", {
        "user": data["username"],
        "msg": data["message"]
    }, to=data["room"])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
