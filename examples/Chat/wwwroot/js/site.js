// Write your Javascript code.
$(function(){
	$.connection.hub.logging = true;
	
	var chat = $.connection.chat;
	var $textArea = $('#chat');
	var text = '';
	
	chat.client.newMessageReceived = function(message) {
		text = text + 'Someone said: ' + message + '\n';
		$textArea.text(text);
	};
	
	chat.client.topicChanged = function(topic) {
		$('#topic').text(topic);
	};
	
	$.connection.hub.error(function(error) {
		text = text + 'Someone failed: ' + error + '\n';
		$textArea.text(text);
	});
	
	$.connection.hub.start({transport: 'auto'}, function() {
		chat.server.send('Incoming!');
	});
});