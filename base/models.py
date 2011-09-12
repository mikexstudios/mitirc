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
    is_oper = models.BooleanField(default = False)
    updated = models.DateTimeField(auto_now = True)

    def generate_password(self):
        '''
        Populates the password attribute with a random password.
        '''
        self.password = ''.join(SystemRandom().sample(string.ascii_lowercase + \
                                string.digits, 8)) #match password model length!
        self.sync_to_oper()

    def sync_to_oper(self):
        '''
        If user is oper, then need to check if Oper model is associated with
        the username and also check that the passwords are synced.
        '''
        if self.is_oper:
            o, is_created = Oper.objects.get_or_create(username = self.username, 
                             defaults = {'password': self.password})
            #If object exists but is not synced, then resync the password
            if o.password != self.password:
                o.password = self.password
                o.save()

    def save(self, *args, **kwargs):
        self.sync_to_oper()
        super(IRCAuth, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.username, )


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


class Oper(models.Model):
    '''
    Sets up the schema used by the sqloper module from inspIRCd. 
    See: http://wiki.inspircd.org/Modules/sqloper
    '''
    class Meta:
        db_table = 'ircd_opers'

    #id is automatically created and auto-incremented.
    username = models.CharField(max_length = 31, unique = True)
    password = models.CharField(max_length = 32) #allow possibility for md5 or sha
    #hostname should be in 'glob' format (e.g. *@*).
    hostname = models.CharField(max_length = 255, default = '*@*')
    #Defines the admin class of the op: NetAdmin, GlobalOp, or Helper. These
    #classes are defined in config/opers.conf file in InspIRCd.
    type = models.CharField(max_length = 20, default = 'GlobalOp')

    def __unicode__(self):
        return '%s: %s' % (self.username, self.type)


# We handle signals in handlers.py. Make sure they are registered by importing:
import handlers
