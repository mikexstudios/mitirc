from django.conf import settings
from django import template
from django.template.defaultfilters import stringfilter
#from django.utils.safestring import mark_safe

import urllib

register = template.Library()

#NOTE: This tag is currently not used. Marked for deletion.
@register.simple_tag(takes_context = True)
def webchat_url(context, channel = None):
    '''
    Given a channel string (eg. '#general'), returns a url to webchat that auto-
    matically joins that channel. If no channel string is provided, then
    returns the webchat_url without a channel.
    '''
    request = context['request']

    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    webchat_url = getattr(settings, 'WEBCHAT_URL', 
            'http://%s:%s/' % (request.get_host().split(':')[0], 9090))
    #Get user's IRC authentication information
    ia = request.user.ircauth

    #Now add user-specific connection parameters on the url
    params = {
        'nick': request.user.username,
        'key': ia.password,
    }
    if channel:
        params['channels'] = channel
    webchat_url += '?%s' % urllib.urlencode(params)

    return webchat_url

@register.filter
@stringfilter
def urlquote(val):
    '''
    Given a string, returns it quoted through urllib.
    '''
    
    return urllib.quote_plus(val)
