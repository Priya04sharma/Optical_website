from django.urls import path
from . import views
from .views import signup_view

app_name = 'shop'

urlpatterns = [



    # path('base/', views.base_view, name='base'),

    # User-related
    path('signup/', signup_view, name='signup'),

    # Appointment-related
    path('appointment/', views.appointment_view, name='appointment'),
    path('submit-appointment/', views.submit_appointment, name='submit_appointment'),
    path('thank-you/', views.thank_you, name='thank_you'),

    # About Us-related
    path('aboutdetails/', views.about_details, name='aboutdetails'),  # Place this before product URLs

    # Product-related
path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),  # Put this first
path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
path('', views.product_list, name='product_list'),

]
