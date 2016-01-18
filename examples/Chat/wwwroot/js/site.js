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
	
	chat.client.topicChanged = function(topic, user) {
		$('#topic').text(topic + ' set by ' + user);
	};
	
	$.connection.hub.error(function(error) {
		text = text + 'Houston, we have a problem! ' + error + '\n';
		$textArea.text(text);
	});
	
	$.connection.hub.start({transport: 'auto'}, function() {
		chat.server.send('Incoming!');
		chat.server.requestError().fail(function(error) {
			text = text + 'Houston, we have a problem! ' + error + '\n';
			$textArea.text(text);
		});
	});
});