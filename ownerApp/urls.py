from django.urls import path
from ownerApp.views import (
    top,
    registration,
    login_func,
    logout_func,
    mypage,
    detail,
    update,
    delete,
)

app_name = "owner"
urlpatterns = [
    path("top/", top, name="top"),
    path("registration/", registration, name="registration"),
    path("login/", login_func, name="login"),
    path("logout/", logout_func, name="logout"),
    path("mypage/", mypage, name="mypage"),
    path("detail/<int:id>", detail, name="detail"),
    path("update/", update, name="update"),
    path("delete/", delete, name="delete"),
]
