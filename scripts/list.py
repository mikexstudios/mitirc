import irclib
import sys
from pprint import pprint

irc = irclib.IRC()
try:
    c = irc.server().connect('mxh.xvm.mit.edu', 6667, 'guest-task')
except irclib.ServerConnectionError, x:
    print x
    exit()

def on_connect(connection, event):
    print 'Connected...'
    connection.list() #issue /LIST

def on_list(connection, event):
    pprint(event.arguments())

def on_listend(connection, event):
    connection.quit('Got LIST')

def on_disconnect(connection, event):
    sys.exit(0)

c.add_global_handler('welcome', on_connect)
c.add_global_handler('list', on_list)
c.add_global_handler('listend', on_listend)
c.add_global_handler("disconnect", on_disconnect)
irc.process_forever()
