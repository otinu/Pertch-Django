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
        name = get_value_or_empty(request, "name")
        age = get_value_or_empty(request, "age")
        sex_string = get_value_or_empty(request, "sex")
        if sex_string:
            sex = True
        else:
            sex = False
        charmPoint = get_value_or_empty(request, "charmPoint")
        postCord = get_value_or_empty(request, "postCord")
        address = get_value_or_empty(request, "address")

        image = get_value_or_empty(request, "upload_file")

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
    pet = get_one_pet(id)
    if pet is None:
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


def edit(request, id):
    pet = get_one_pet(id)
    if pet is None:
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    if request.method == "POST":
        age = get_value_or_empty(request, "age")
        charmPoint = get_value_or_empty(request, "charmPoint")
        postCord = get_value_or_empty(request, "postCord")
        address = get_value_or_empty(request, "address")

        image = get_value_or_empty(request, "upload_file")

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        # ログインユーザーとPetの投稿を紐づけ
        owner = get_current_authenticated_user()

        try:
            pet.age = age
            pet.charmPoint = charmPoint
            pet.postCord = postCord
            pet.address = address
            pet.save()
            return redirect("/pet/index")
        except Exception as e:
            traceback.format_exc()

            # ToDo バリデーションメッセージの確認
            return render(
                request,
                "pet/new.html",
                {"error_message": "ペット登録に問題が発生しました"},
            )

    return render(request, "pet/edit.html", context={"pet": pet})


def get_one_pet(id):
    try:
        return PetModel.objects.get(pk=id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return None


def get_value_or_empty(request, name):
    if (name, "") in request.POST.items():
        return ""

    if name == "upload_file":
        return request.FILES[name]
    else:
        return request.POST[name]
