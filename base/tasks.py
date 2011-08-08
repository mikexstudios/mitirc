from django.conf import settings

from celery.task import task

import irclib
from pprint import pprint

@task
def add(x, y):
    return x + y

@task
def update_irc_room_list():
    '''
    Issues the /LIST command on the IRC server to get a list of rooms. Updates 
    the database with this room list information.

    NOTE: This method does not scale well.
    '''

    irc = irclib.IRC()
    try:
        c = irc.server().connect(settings.IRC_SERVER, settings.IRC_SERVER_PORT, 
                                 settings.IRC_TASK_NICKNAME)
    except irclib.ServerConnectionError, x:
        return False #task failed

    def on_connect(connection, event):
        connection.list() #issue /LIST

    def on_list(connection, event):
        pprint(event)

    c.add_global_handler('list', on_list)
    irc.process_once()
