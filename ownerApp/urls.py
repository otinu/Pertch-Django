from django.urls import path
from .views import registration, login_func

urlpatterns = [
    path("registration/", registration, name="registration"),
    path("login/", login_func, name="login"),
]
