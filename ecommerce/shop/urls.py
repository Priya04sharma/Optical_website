# from django.conf.urls import url
# from . import views

# app_name = 'shop'

# urlpatterns = [
#     url(r'^$', views.product_list, name='product_list'),
#     url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
#     url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
# ]


from django.urls import path
from . import views
from .views import signup_view

from django.contrib.auth import views as auth_views
app_name = 'shop'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
