# from django.conf.urls import url
# from . import views

# app_name = 'orders'

# urlpatterns = [
#     url(r'^create/$', views.order_create, name='order_create')
# ]



from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='create'),
]
