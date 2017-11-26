from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.products_list, name='products_list'),
    url(r'^(?P<product_id>\d+)/$', views.product, name='product'),
    url(r'^(?P<category_name>[-\w]+)/$', views.products_list, name='products_list'),
]