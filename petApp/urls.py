from django.urls import path, include
from .views import index, new, show, edit, delete, search

app_name = "pet"
urlpatterns = [
    path("index/", index, name="index"),
    path("new/", new, name="new"),
    path("show/<int:id>", show, name="show"),
    path("edit/<int:id>", edit, name="edit"),
    path("delete/<int:id>", delete, name="delete"),
    path("search/", search, name="search"),
    path("petComment/", include("petCommentApp.urls")),
]
