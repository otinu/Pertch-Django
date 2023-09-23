import datetime
import traceback

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user

from petApp.models import PetModel
from petCommentApp.models import PetCommentModel


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

        if ("upload_file", "") in request.POST.items():
            # ペット登録時に画像なし ⇒ 明示的にNoneを埋め込む
            image = None
        else:
            image = request.FILES["upload_file"]

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        # ログインユーザーとPetの投稿を紐づけ
        owner = get_current_authenticated_user()

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
                owner=owner,
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


def show(request, id):
    try:
        pet = PetModel.objects.get(pk=id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    pet_comment_list = pet.petcommentmodel_set.all()  # type: ignore
    return render(
        request,
        "pet/show.html",
        context={"pet": pet, "pet_comment_list": pet_comment_list},
    )
