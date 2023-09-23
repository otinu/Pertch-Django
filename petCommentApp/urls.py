from django.urls import path
from .views import new

app_name = "pet_comment"
urlpatterns = [path("new/", new, name="new")]
