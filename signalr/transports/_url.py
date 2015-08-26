import urllib

client_protocol = 1.5


def get_url(url, action, **kwargs):
    args = kwargs.copy()
    args['clientProtocol'] = str(client_protocol)
    query = '&'.join(map(lambda key: '{key}={value}'.format(key=key, value=urllib.quote_plus(args[key])), args))

    return '{url}/{action}?{query}'.format(url=url,
                                           action=action,
                                           query=query)
