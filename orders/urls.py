from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^checkout/$', views.checkout, name='checkout'),
    # url(r'^$', views.orders_list, name='orders_list'),
    url(r'^(?P<order_id>\d+)/$', views.order, name='order'),
]


