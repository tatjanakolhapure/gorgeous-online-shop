from django.conf.urls import url
import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^details/$', views.account, name='account'),
    url(r'^details/edit_details/(?P<user_id>\d+)/$', views.edit_details, name='edit_details'),
    url(r'^details/edit_address/(?P<user_id>\d+)/$', views.edit_address, name='edit_address'),
]