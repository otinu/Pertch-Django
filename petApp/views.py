from django.shortcuts import render, redirect
from .models import PetModel


def index(request):
    list = PetModel.objects.all()
    return render(request, "pet/index.html", {"list": list})
