from django.contrib.auth.decorators import login_required

from annoying.decorators import render_to, ajax_request
#from annoying.functions import get_object_or_None

@render_to('base/home.html')
def home(request):

    return {}


@login_required
@render_to('base/dashboard.html')
def dashboard(request):

    return {}
