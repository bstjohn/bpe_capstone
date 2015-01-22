from django.conf.urls import patterns, url

from registration import views

urlpatterns = patterns('',
    #url(r'^$', views.registration, name='registration'),
    # call the function from 'registration.views.register'
    url(r'^$', 'registration.views.register'),  
)
