from django.db import models
from django.contrib.auth.models import User

#import datetime
from random import SystemRandom
import string #for letters and digits

class IRCAuth(models.Model):
    '''
    Table that contains username and randomly-generated password pairs for 
    authentication through IRCd.
    '''
    user = models.OneToOneField(User, primary_key = True)
    username = models.CharField(max_length = 31, db_index = True, unique = True)
    password = models.CharField(max_length = 8) 
    updated = models.DateTimeField(auto_now = True)

    def generate_password(self):
        '''
        Populates the password attribute with a random password.
        '''
        self.password = ''.join(SystemRandom().sample(string.ascii_lowercase + \
                                string.digits, 8)) #match password model length!


class Room(models.Model):
    '''
    Describes an IRC room.
    '''
    #We set the room name as the primary key so we do not have an integer auto-
    #increment field. The currently set maximum length of room names is 65 for
    #InspIRCd. The standard states a maximum length of 50 chars.
    #NOTE: primary_key=True implies null=False and unique=True. 
    name = models.CharField(max_length = 65, primary_key = True)
    num_users = models.PositiveIntegerField(default = 0)
    #The maximum topic length varies by IRCd, but InspIRCd has maximum length
    #of 308. 
    topic = models.CharField(max_length = 310, default = '', blank = True)
    #We use the updated field to filter out old rooms that are probably empty
    #(since they haven't been updated by the room listing bot).
    updated = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.num_users, self.topic)


# We handle signals in handlers.py. Make sure they are registered by importing:
import handlers
