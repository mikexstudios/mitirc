from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.utils import DatabaseError

import models
import helpers

def create_ircauth(sender, **kw):
    '''
    Creates an IRCAuth entry for the user if this is the first time that the user
    is created.
    '''
    user = kw["instance"]
    if kw["created"]:
        try:
            helpers.create_ircauth_for_user(user)
        except DatabaseError:
            #Because we use South to manage base-related tables, when
            #superuser is created through syncdb, this handler gets called and
            #errors because IRCAuth does not exist. Thus, we catch that problem
            #here. We bank on having IRCAuth created when the chat view is
            #called.
            pass
post_save.connect(create_ircauth, sender = User)

