from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_view, name='booking'),
    path('list/', views.booking_list_view, name='booking_list'),
]