from logging import debug
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
    rooms = [{"text": "South - UWaterloo Campus", "name": "south-uwaterloo"}, {"text": "East - UWaterloo Campus", "name": "east-uwaterloo"}, {"text": "West - UWaterloo Campus", "name": "west-uwaterloo"}, {"text": "North - UWaterloo Campus", "name": "north-uwaterloo"}]
    return render_template("messages.html", rooms = rooms)

@socketio.on("connect")
def connect():
    print("Connected!")

@socketio.on("sendMessage")
def sendMessage(data):
    emit("receiveMessage", {"message": data["message"], "user": data["user"]}, to=data["room"])

@socketio.on("changeRoom")
def changeRoom(data):
    join_room(data["name"])

if __name__ == "__main__":
    socketio.run(app, debug = True)