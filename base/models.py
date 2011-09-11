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
    #If always_display is set to True, then the room will always be listed in
    #dashboard even if it does not exist on the IRC server. This is useful for
    #constantly used rooms and acts as a failsafe if the room polling script
    #fails.
    always_display = models.BooleanField(default = False)
    #We use the updated field to filter out old rooms that are probably empty
    #(since they haven't been updated by the room listing bot).
    updated = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return '%s %s %s' % (self.name, self.num_users, self.topic)


class Statistic(models.Model):
    '''
    Keeps track of IRC statistics (like number of users, number of channels).
    Simply a key-value store for now.
    NOTE: This is a pretty crude way of storing stats. Got a better idea?
    '''
    key = models.CharField(max_length = 50, primary_key = True)
    value = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return '%s: %s' % (self.key, self.value)

# We handle signals in handlers.py. Make sure they are registered by importing:
import handlers
