from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'blog.views.index', name="index"),
    url(r'^new/$', 'blog.views.new', name='new'),
    url(r'^(?P<pk>\d+)/$', 'blog.views.detail', name='detail'),
    url(r'^(?P<pk>\d+)/comments/new/$', 'blog.views.comment_new',
    name='comment_new'),
    url(r'^edit/(?P<pk>\d+)/$', 'blog.views.edit', name='edit'),
    url(r'^signup/joke/$', 'blog.views.signup_joke'),
    ]
