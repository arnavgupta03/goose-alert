from flask import Flask, render_template, session
import requests, os
from flask_socketio import SocketIO, leave_room, send, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/messages")
def messages():
    rooms = ["South - UWaterloo Campus", "East - UWaterloo Campus", "West - UWaterloo Campus", "North - UWaterloo Campus"]
    return render_template("messages.html", rooms = rooms)

if __name__ == "__main__":
    socketio.run(app, debug = True)