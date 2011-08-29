from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

from base import models

import urllib

@render_to('base/home.html')
def home(request):

    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    host = request.get_host().split(':')[0]

    return {'host': host}


@login_required
@render_to('base/dashboard.html')
def dashboard(request):
    rooms = models.Room.objects.all().order_by('-num_users')    

    return {'rooms': rooms}


@login_required
#@render_to('base/chat.html')
def chat(request):
    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    webchat_url = getattr(settings, 'WEBCHAT_URL', 
            'http://%s:%s/' % (request.get_host().split(':')[0], 9090))

    #Get user's IRC authentication information
    ia = request.user.ircauth

    #Now add user-specific connection parameters on the url
    webchat_url += '?%s' % urllib.urlencode({
        'nick': request.user.username,
        'channels': getattr(settings, 'DEFAULT_ROOM', '#general'),
        'key': ia.password,
    })

    return redirect(webchat_url)

