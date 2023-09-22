from django.urls import path
from .views import index, new, show

urlpatterns = [
    path("index/", index, name="index"),
    path("new/", new, name="new"),
    path("show/<int:id>", show, name="show"),
]
