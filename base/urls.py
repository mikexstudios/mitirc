from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('base.views',
    url(r'^$', 'home', name='home'),
    url(r'^dashboard/$', 'dashboard', name='dashboard'),
    url(r'^chat/$', 'chat', name='chat'),
    #We want to match rooms of type: #myroom, myroom, etc. Need the %character in
    #there too for django quoted urls to be generated.
    url(r'^chat/([#%\w]+)/?$', 'chat', name='chat'),
)
