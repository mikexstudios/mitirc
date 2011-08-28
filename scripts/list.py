#Scaffolding to setup standalone django script
import os, sys

# Path of this "site" (no trailing /):
#THIS_ROOT = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(os.path.join(THIS_ROOT, '../../'))
#sys.path.append(os.path.join(THIS_ROOT, '../'))
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
#from django.conf import settings

sys.path[0] = os.path.normpath(os.path.join(sys.path[0], '..'))
from django.core.management import setup_environ
import settings
setup_environ(settings)

#From base app:
from base import models

import irclib
import time #for sleep


irc = irclib.IRC()
try:
    c = irc.server().connect('mxh.xvm.mit.edu', 6667, 'guest-task')
except irclib.ServerConnectionError, x:
    print x
    sys.exit(1)

def on_connect(connection, event):
    print 'Connected!'
    connection.list() #issue /LIST

def on_list(connection, event):
    '''
    This gets called for each entry in LIST.
    '''
    #ex. ['#general', '3', '[+nt] Chat about anything!']
    name, num_users, topic = event.arguments()

    #Remove the [+nt], etc. mode part from the topic
    topic = topic.split(']', 1)[1] #we split only once at the first ]
    topic = topic.strip()

    room = models.Room()
    room.name = name #this is the primary key
    room.num_users = num_users
    room.topic = topic
    #Because we defined the primary key, saving will automatically select
    #between UPDATE or INSERT.
    room.save()

    print room

def on_listend(connection, event):
    #Since this script runs forever, we wait a certain period of time before
    #listing the rooms again. Default wait is 1 minute.
    print '----------------'
    timeout = getattr(settings, 'UPDATE_ROOMS_INTERVAL', 60) #seconds
    time.sleep(timeout)
    connection.list()

def on_disconnect(connection, event):
    sys.exit(0)

c.add_global_handler('welcome', on_connect)
c.add_global_handler('list', on_list)
c.add_global_handler('listend', on_listend)
c.add_global_handler("disconnect", on_disconnect)
irc.process_forever()
