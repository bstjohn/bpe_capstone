from django.conf.urls import patterns, url

from queryBuilder import views

urlpatterns = patterns('',
                       url(r'^$', views.query_builder, name='query-builder')
)