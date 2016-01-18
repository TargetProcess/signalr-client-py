using System;
using System.Security.Principal;
using System.Text;
using Microsoft.AspNet.Http;
using Microsoft.AspNet.SignalR;
using Microsoft.AspNet.SignalR.Hubs;

namespace Chat.Hubs
{
    public class KnowUserBasicAuthenticationAttribute : AuthorizeAttribute
	{
		private readonly string _password = "user";
		private readonly string _realm = "Chat";
		private readonly string _role = "user";
		private readonly string _username = "known";

	    public override bool AuthorizeHubConnection(HubDescriptor hubDescriptor, HttpRequest request)
	    {
			return AuthenticateCore(request);
		}

	    public override bool AuthorizeHubMethodInvocation(IHubIncomingInvokerContext hubIncomingInvokerContext, bool appliesToMethod)
	    {
		    return AuthenticateCore(hubIncomingInvokerContext.Hub.Context.Request);
	    }

	    private bool AuthenticateCore(HttpRequest request)
	    {
		    var httpContext = request.HttpContext;
		    var authorization = request.Headers["Authorization"];

		    if (!string.IsNullOrEmpty(authorization))
		    {
			    var cred = Encoding.ASCII.GetString(Convert.FromBase64String(authorization.ToString().Substring(6))).Split(':');
			    var user = new {Name = cred[0], Pass = cred[1]};

			    if (user.Name == _username && user.Pass == _password)
			    {
				    httpContext.User = new GenericPrincipal(new GenericIdentity(_username), new[] {_role});

				    return true;
			    }
		    }

		    return false;
	    }
	}
}