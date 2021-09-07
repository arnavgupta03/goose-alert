from flask import Flask, render_template, session, request, redirect, url_for
import requests, os
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, leave_room, send, emit, join_room
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
socketio = SocketIO(app, cors_allowed_origins="*")
mysql=MySQL(app)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="arnav"
app.config['MYSQL_DB']="flask"

API_KEY = os.environ.get("API_KEY")

@app.route("/", methods=['GET','POST'])
def func2():
    return render_template('index.html')

@app.route("/login", methods=['GET','POST'])
def func():
    if request.method=='POST':
        userdetails=request.form
        name=userdetails['name']
        password=userdetails['password']
        mycursor=mysql.connection.cursor()
        q="select * from flasktable"
        mydata=mycursor.execute(q)
        user=mycursor.fetchall()
        for i in user:
            if i[0]==name and i[2]==password:
                print("worked!")
                session["username"] = name
                return redirect(url_for("messages"))
    return render_template('login.html')

@app.route("/register", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        print("reached")
        userdetails=request.form
        name=userdetails['name']
        email=userdetails['email']
        password=userdetails['password']
        mycursor=mysql.connection.cursor()
        q="insert into flasktable values('{}','{}','{}')".format(name,email,password)
        mycursor.execute(q)
        mysql.connection.commit()
        mycursor.close()
        print("success")
    return render_template('register.html')

@app.route("/messages")
def messages():
    username = session.get("username")
    rooms = [{"text": "South - UWaterloo Campus", "name": "south-uwaterloo"}, {"text": "East - UWaterloo Campus", "name": "east-uwaterloo"}, {"text": "West - UWaterloo Campus", "name": "west-uwaterloo"}, {"text": "North - UWaterloo Campus", "name": "north-uwaterloo"}]
    return render_template("messages.html", rooms = rooms, username = username)

@app.route("/map")
def map():
    return render_template("map.html", API_KEY = API_KEY)

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