#from django.conf import settings

import models

def create_ircauth_for_user(user):
    '''
    Given a user without an associated IRCAuth model, creates one.
    '''
    #Check if user already has an IRCAuth object
    try:
        user.ircauth
    except models.IRCAuth.DoesNotExist:
        ia = models.IRCAuth(user = user, username = user.username)
        ia.generate_password()
        ia.save()
