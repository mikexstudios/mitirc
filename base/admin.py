from django.contrib import admin

from base import models

class IRCAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'password', 'updated')
    list_display_links = ('user')
admin.site.register(models.IRCAuth, IRCAuthAdmin)
