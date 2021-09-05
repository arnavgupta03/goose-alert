var socket = io.connect("http://127.0.0.1:5000");

function onLoad() {
    socket.onconnect(() => {
        socket.emit("connect");
    });
}

function sendMessage(data) {
    console.log(data);
    document.getElementById("message").value = "";
    socket.emit("sendMessage", {"message": data, "room": sessionStorage.getItem("room"), "user": sessionStorage.getItem("user")});
}

function changeRoom(data) {
    sessionStorage.setItem("room", data);
    document.getElementById("room-title").innerHTML = document.getElementById(data).innerHTML;
    socket.emit("changeRoom", {"name": data});
}

socket.on("receiveMessage", (data) => {
    var messageLine = document.createElement("p");
    var messageText = document.createTextNode(data.user + ": " + data.message);
    messageLine.appendChild(messageText);
    document.getElementById("chatbox").appendChild(messageLine);
})