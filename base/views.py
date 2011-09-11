from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

from base import models

import urllib
import datetime

@render_to('base/home.html')
def home(request):

    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    host = request.get_host().split(':')[0]

    return {'host': host}


@login_required
@render_to('base/dashboard.html')
def dashboard(request):
    #Get all rooms that have been updated greater or equal to t minutes ago.
    #By using a filter, we don't have to garbage collect stale rooms in the data-
    #base.
    rooms = models.Room.objects.filter(
             Q(always_display = True) | Q(updated__gte = datetime.datetime.now() -\
             datetime.timedelta(minutes = getattr(settings, 'ROOM_AGE_FILTER', 10)))
            ).order_by('-num_users')
    try:
        total_users = models.Statistic.objects.get(key = 'total_users').value
        max_users = models.Statistic.objects.get(key = 'max_users').value
    except models.Statistic.DoesNotExist:
        total_users = 0
        max_users = 0

    return {'rooms': rooms, 'total_users': total_users, 'max_users': max_users}


@login_required
#@render_to('base/chat.html')
def chat(request, channel = None):
    #NOTE: Using get_host() also pulls in the port number. So if a non-80
    #port is used, break it apart into just the server name.
    webchat_url = getattr(settings, 'WEBCHAT_URL', 
            'http://%s:%s/' % (request.get_host().split(':')[0], 9090))

    #Get user's IRC authentication information
    ia = request.user.ircauth

    #Now add user-specific connection parameters on the url
    webchat_url += '?%s' % urllib.urlencode({
        'nick': request.user.username,
        #NOTE: We set the channel GET param to highest precedence followed by 
        #      channel encoded in the url. The GET param is submitted by new
        #      room creation form.
        'channels': request.GET.get('channels', None) or channel or getattr(settings, 'DEFAULT_ROOM', '#general'),
        'key': ia.password,
    })

    return redirect(webchat_url)

