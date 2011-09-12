from django.contrib.auth.models import User
from django.db.models.signals import post_save

import models

def create_ircauth(sender, **kw):
    '''
    Creates an IRCAuth entry for the user if this is the first time that the user
    is created.

    WARNING: Because we use South to manage base-related tables, when superuser is
    created through syncdb, this handler gets called and errors because IRCAuth
    does not exist. Thus, the workaround is to create the superuser *after* running
    both syncdb and migrations.
    '''
    user = kw["instance"]
    if kw["created"]:
        ia = models.IRCAuth(user = user, username = user.username)
        ia.generate_password()
        ia.save()
post_save.connect(create_ircauth, sender = User)

