from django.urls import path, include
from . import views

urlpatterns = [
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_register, name="signup"),
    path("logout/", views.user_logout, name="logout"),
]
