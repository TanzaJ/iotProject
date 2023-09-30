//const socket = io('http://localhost:5000');
const socket = require('socket.io')(server, {
    cors: {
        origin: "http://localhost:5000",
        methods: ["GET", "POST"],
        transports: ['websocket', 'polling'],
        credentials: true
    },
    allowEIO3: true
});

socket.on('my_event', function(data) {
    console.log(data.sensor_type + ': ' + data.data);
});