#Scaffolding to setup standalone django script
import os, sys
sys.path[0] = os.path.normpath(os.path.join(sys.path[0], '..'))
from django.core.management import setup_environ
import settings
setup_environ(settings)

#From base app:
from base import models

import irclib
import time #for sleep
import re


irc = irclib.IRC()
try:
    c = irc.server().connect('mxh.xvm.mit.edu', 6667, 'guest-task')
except irclib.ServerConnectionError, x:
    print x
    sys.exit(1)

def on_connect(connection, event):
    print 'Connected!'
    connection.list() #issue /LIST
    #We do NOT invoke /LUSERS because upon connect, the server automatically
    #issues the output of the /LUSERS command.

def on_disconnect(connection, event):
    sys.exit(0)


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
    room.num_users = int(num_users)
    room.topic = topic
    #Because we defined the primary key, saving will automatically select
    #between UPDATE or INSERT.
    room.save()

    print room

def on_listend(connection, event):
    #Since this script runs forever, we wait a certain period of time before
    #listing the rooms again. Default wait is 1 minute.
    #TODO: Fix this crude timeout stuff
    print '----------------'
    timeout = getattr(settings, 'IRC_UPDATE_INTERVAL', 60) #seconds
    time.sleep(timeout) #WARNING: This is blocking. Effects everything.
    connection.list()
    connection.lusers()


def on_luserchannels(connection, event):
    '''Gets the total number of channels on the server.'''
    #ex. ['2', 'channels formed']
    total_channels = event.arguments()[0]

    stat = models.Statistic()
    stat.key = 'total_channels'
    stat.value = int(total_channels)
    stat.save()
    print stat


def on_n_global(connection, event):
    '''Gets the total and max number of global users.'''
    #ex. ['Current Global Users: 2  Max: 3']
    m = re.match(r'Current Global Users: (\d+)  Max: (\d+)', event.arguments()[0])
    if m:
        stat = models.Statistic()
        stat.key = 'total_users'
        stat.value = int(m.group(1)) - 1 #We subtract one to correct for this script
        stat.save()
        print stat

        stat = models.Statistic()
        stat.key = 'max_users'
        stat.value = int(m.group(2)) - 1
        stat.save()
        print stat


#See https://github.com/jbalogh/python-irclib/blob/master/irclib.py for list
#of events. The number to the left of those events are what the IRC server returns:
c.add_global_handler('welcome', on_connect)
c.add_global_handler("disconnect", on_disconnect)
#For LIST
c.add_global_handler('list', on_list)
c.add_global_handler('listend', on_listend)
#For LUSERS
c.add_global_handler('luserchannels', on_luserchannels)
c.add_global_handler('n_global', on_n_global)

irc.process_forever()
