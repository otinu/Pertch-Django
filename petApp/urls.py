from django.urls import path, include
from .views import index, new, show, edit

urlpatterns = [
    path("index/", index, name="index"),
    path("new/", new, name="new"),
    path("show/<int:id>", show, name="show"),
    path("edit/<int:id>", edit, name="edit"),
    path("petComment/", include("petCommentApp.urls")),
]
