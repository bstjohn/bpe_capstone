from django.conf.urls import patterns, url

from query import views

urlpatterns = patterns('',
                       url(r'^query-builder/', views.query_builder, name='query-builder')
)