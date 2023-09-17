from django.urls import path
from ownerApp.views import top, registration, login_func

urlpatterns = [
    path("top/", top, name="top"),
    path("registration/", registration, name="registration"),
    path("login/", login_func, name="login"),
]
