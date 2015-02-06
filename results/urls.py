from django.conf.urls import patterns, url

from results import views

urlpatterns = patterns('',
                       url(r'^get-results/', views.get_results, name='get-results')
)



