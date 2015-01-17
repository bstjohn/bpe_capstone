from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bpe_capstone.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^info/', include('info.urls', namespace="info")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard"))
)
