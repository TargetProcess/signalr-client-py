using System;
using System.Threading.Tasks;
using Microsoft.AspNet.SignalR;
using Microsoft.AspNet.SignalR.Hubs;

namespace Chat.Hubs
{
    [HubName("chat")]

	public class ChatHub : Hub
	{
		public Task Send(string message)
		{
			return Clients.All.newMessageReceived(message, DateTime.Now);
		}

		[KnowUserBasicAuthentication]
		public Task SetTopic(string topic)
		{
			return Clients.All.topicChanged(topic);
		}
	}
}