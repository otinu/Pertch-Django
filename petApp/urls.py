from django.urls import path
from .views import index

app_name = "petApp"
urlpatterns = [path("index/", index, name="index")]
