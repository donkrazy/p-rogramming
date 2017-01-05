from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'^$', 'project.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^magazine/', include('megazine.urls', namespace='megazine')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^refresh/$', 'project.views.refresh', name='refresh'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
