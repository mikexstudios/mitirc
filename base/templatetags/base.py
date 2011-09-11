from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
#from django.utils.safestring import mark_safe

import urllib

register = template.Library()

@register.simple_tag(takes_context = True)
def webchat_url(context, channel = getattr(settings, 'DEFAULT_ROOM', '#general')):
    '''
    Given a channel string (eg. '#general'), returns a url to webchat that auto-
    matically joins that channel.
    '''
    request = context['request']

    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    webchat_url = getattr(settings, 'WEBCHAT_URL', 
            'http://%s:%s/' % (request.get_host().split(':')[0], 9090))
    #Get user's IRC authentication information
    ia = request.user.ircauth

    #Now add user-specific connection parameters on the url
    webchat_url += '?%s' % urllib.urlencode({
        'nick': request.user.username,
        'channels': channel,
        'key': ia.password,
    })

    return webchat_url
