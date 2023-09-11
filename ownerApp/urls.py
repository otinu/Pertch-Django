from django.urls import path
from .views import get_registration

urlpatterns = [
    path('registration/', get_registration, name='test')
]