function onLoad() {
    var socket = io.connect("http://127.0.0.1:5000");
    socket.onconnect(() => {
        socket.emit("connect");
    });
}