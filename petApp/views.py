import datetime
import traceback

from django.db import IntegrityError
from django.shortcuts import render, redirect

from .models import PetModel


def index(request):
    list = PetModel.objects.all()
    return render(request, "pet/index.html", {"list": list})


def new(request):
    if request.method == "POST":
        name = request.POST["name"]
        age = request.POST["age"]
        sex_string = request.POST["sex"]
        if sex_string:
            sex = True
        else:
            sex = False
        charmPoint = request.POST["charmPoint"]
        postCord = request.POST["postCord"]
        address = request.POST["address"]
        image = request.FILES["upload_file"]

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        try:
            PetModel.objects.create(
                name=name,
                age=age,
                sex=sex,
                charmPoint=charmPoint,
                postCord=postCord,
                address=address,
                image=image,
                created_at=today,
                updated_at=today,
            )
            return redirect("/pet/index")
        except IntegrityError as e:
            traceback.format_exc()

            # ToDo バリデーションメッセージの確認
            return render(
                request,
                "pet/new.html",
                {"error_message": "ペット登録に問題が発生しました"},
            )
    return render(request, "pet/new.html")
