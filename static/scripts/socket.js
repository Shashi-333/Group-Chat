// connect to Socket.IO server
const socket = io();

// get elements
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.getElementById('chat-messages');

//listen for messages from the server
//socket.connect("http://localhost:5000")

socket.on('message', function(data) {
  var message = document.createElement('p');
  message.innerText =  data.username +":"+data.message;
  chatMessages.appendChild(message);
});

// send message to server when button is clicked
sendButton.addEventListener('click', function() {
  var message = messageInput.value.trim();
  if (message !== '') {
    socket.emit('message', { message: message });
    messageInput.value = '';
  }
});

// send message to server when Enter key is pressed
messageInput.addEventListener('keypress', function(event) {
  if (event.key == 13) {
    sendButton.click();
    event.preventDefault();
  }
});