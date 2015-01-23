from django.conf.urls import patterns, url

from info import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^contact/$', views.contact, name='contact'),
                       url(r'^faq/$', views.faq, name='faq'),
                       url(r'^about/$', views.about, name='about'),
)