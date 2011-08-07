from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('base.views',
    # Examples:
    url(r'^$', 'home', name='home'),
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^chat/$', 'chat', name='chat'),
)
