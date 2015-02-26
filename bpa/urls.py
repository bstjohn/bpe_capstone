from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.views import UserProfileDetailView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bpe_capstone.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', 'django.contrib.auth.views.login'),
                       url(r'^login/$', 'django.contrib.auth.views.login'),
                       url(r'^logout/$', 'registration.views.logout'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^info/', include('info.urls', namespace="info")),
                       url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
                       url(r'^query/', include('query.urls', namespace="query")),
                       url(r'^registration/$', 'registration.views.register_user'),
                       url(r'^registration_success/$', 'registration.views.register_success'),
                       url(r'^registration_fail/$', 'registration.views.register_fail'),
                       url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset',
                           {'post_reset_redirect': 'passwordsent/'}, name='password_reset'),
                       url(r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done',
                           name='password_reset_done'),
                       url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm', {'post_reset_redirect': 'reset/done/'},
                           name='password_reset_confirm'),
                       url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete',
                           name='password_reset_complete'),
                       url(r'^stations/', include('stations.urls', namespace="station")),
                       url(r'^profile/$', 'registration.views.user_profile'),
                       url(r"^users/(?P<slug>\w+)/$", UserProfileDetailView.as_view(), name="profile"),

)
