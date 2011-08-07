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


# We handle signals in handlers.py. Make sure they are registered by importing:
import handlers
