from django.urls import path
from .views import testfunc

urlpatterns = [
    path('test/', testfunc, name='test')
]