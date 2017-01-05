from django.conf.urls import url


urlpatterns = [
    url(r'^login/$', 'accounts.views.login'),
    url(r'^login/email/$', 'accounts.views.login_email', name='login_email'),
    url(r'^login/req/(?P<token>[a-z0-9\-]+)$', 'accounts.views.login_email_req', name='login_req'),
    url(r'^signup/$', 'accounts.views.signup', name='signup'),
    url(r'^mysignup/$', 'accounts.views.mySignup', name='mySignup'),
    url(r'^info/$', 'accounts.views.info', name='info'),
]
