from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

@render_to('base/home.html')
def home(request):

    return {}


@login_required
@render_to('base/dashboard.html')
def dashboard(request):

    return {}


@login_required
#@render_to('base/chat.html')
def chat(request):
    webchat_url = getattr(settings, 'WEBCHAT_URL', 
            'http://%s:%s/' % (request.META['SERVER_NAME'], 9090))

    return redirect(webchat_url)

