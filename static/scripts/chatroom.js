//connect to Socket.IO server
const socket = io();
// get elements
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const chatMessages = document.getElementById('chat-messages');
const msgheader = document.getElementById('message-header');
const userheader = document.getElementById('user-header');


socket.on('message', function(data) {
    u=""
    for(i=0;i<data.userlist.length;i++){
      u+=data.userlist[i] +","
    }     
    msgheader.innerHTML=data.groupname
    userheader.innerHTML= u
    var p = document.createElement('p');
    p.innerText =  data.username + ":" + data.message;
    chatMessages.appendChild(p);
    
});

// send message to server when button is clicked
sendButton.addEventListener('click', function() {
    var message = messageInput.value.trim();
    if (message !== '') {
      socket.emit('message', { message: message ,title : msgheader.textContent});
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


socket.on('grp_button', function(data) {
  function func(data){
    var button = document.createElement('button');
    button.innerText = data.grp;
    button.id = data.grp;
    button.className = "grpclass";
    button.type = "submit";
    button.addEventListener('click', function() {
      const btn = button.id
      chatMessages.innerHTML=''
      socket.emit('grp_button', {btn : btn});
    });
    groupContainer.appendChild(button);
  }
  const groupContainer = document.getElementById('group-container'); 
  func(data);
  
});