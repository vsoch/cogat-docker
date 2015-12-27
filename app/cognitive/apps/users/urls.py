from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login,name="login"),
    url(r'^logout/$', auth_views.logout, name="logout"),
    url(r'^create/$',views.create_user,name="create_user"),
    url(r'^profile/password/$',auth_views.password_change,name='password_change'),
    url(r'^password/change/done/$',auth_views.password_change_done,name='password_change_done'),
    url(r'^password/reset/$',auth_views.password_reset,name='password_reset'),
    url(r'^password/reset/done/$',auth_views.password_reset_done,name='password_reset_done'),
    url(r'^password/reset/complete/$',auth_views.password_reset_complete,name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm,name='password_reset_confirm'),
    url(r'^profile/edit$',views.edit_user,name="edit_user"),
    url(r'^profile/.*$',views.view_profile,name="my_profile"),
    url(r'^(?P<username>[A-Za-z0-9@/./+/-/_]+)/$',views.view_profile,name="profile")
]
