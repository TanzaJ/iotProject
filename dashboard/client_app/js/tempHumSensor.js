const socket = io('http://localhost:5000');

socket.on('my_event', function(data) {
    console.log(data.propertyName);  // Replace 'propertyName' with the name of the property you want to access
});