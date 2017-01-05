from django.conf.urls import url

urlpatterns =[
    url(r'^$', 'megazine.views.index', name='index'),
    url(r'^index_old/$', 'megazine.views.index_old', name='index_old'),
    url(r'^(?P<pk>\d+)/$', 'megazine.views.detail', name='detail'),
    url(r'^new/$', 'megazine.views.new', name='new'),
     url(r'^(?P<pk>\d+)/edit/$', 'megazine.views.edit', name='edit'),
    url(r'^(?P<pk>\d+)/delete/$', 'megazine.views.delete', name='delete'),
    url(r'^(?P<pk>\d+)/comment_new/$', 'megazine.views.comment_new', name='comment_new'),
     url(r'^comment_edit/(?P<pk_comment>\d+)/$', 'megazine.views.comment_edit', name='comment_edit'),
    url(r'^comment_delete/(?P<pk_comment>\d+)/$', 'megazine.views.comment_delete', name='comment_delete'),
    url(r'^signup_old/$', 'megazine.views.signup_old', name='signup_old'),
    url(r'^test/$', 'megazine.views.test'),
]
