from django.contrib import admin

from base import models

class IRCAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'username', 'password', 'updated')
    list_display_links = ('user', )
admin.site.register(models.IRCAuth, IRCAuthAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'num_users', 'topic', 'updated')
    list_display_links = ('name', )
admin.site.register(models.Room, RoomAdmin)

class StatisticAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', )
    list_display_links = ('key', )
admin.site.register(models.Statistic, StatisticAdmin)
