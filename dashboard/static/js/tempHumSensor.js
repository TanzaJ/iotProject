//const socket = io('http://localhost:5000');
const socket = io('http://localhost:5000', {
    withCredentials: true,
    extraHeaders: {
      "my-custom-header": "abcd"
    }
  });

socket.on('my_event', function(data) {
    console.log(data.sensor_type + ': ' + data.data);
});