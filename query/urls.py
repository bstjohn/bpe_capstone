from django.conf.urls import patterns, url

from query import views

urlpatterns = patterns('',
                       url(r'^$', views.query_index, name='query-index'),
                       url(r'^query-builder/', views.query_builder, name='query-builder'),
                       url(r'^query-result/', views.query_result, name='query-result'),
                       url(r'^status-result/', views.status_result, name='status-result')

)
