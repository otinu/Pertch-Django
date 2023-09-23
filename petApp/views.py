import datetime
import traceback

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user

from petApp.models import PetModel


def index(request):
    list = PetModel.objects.all()
    return render(request, "pet/index.html", {"list": list})


def new(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex_string = request.POST.get("sex")
        if sex_string:
            sex = True
        else:
            sex = False
        charmPoint = request.POST.get("charmPoint")
        postCord = request.POST.get("postCord")
        address = request.POST.get("address")

        image = get_media_or_empty(request, "upload_file")

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
        age = request.POST.get("age")
        charmPoint = request.POST.get("charmPoint")
        postCord = request.POST.get("postCord")
        address = request.POST.get("address")

        image = get_media_or_empty(request, "upload_file")

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        try:
            pet.age = age
            pet.charmPoint = charmPoint
            pet.postCord = postCord
            pet.address = address
            if image:
                pet.image = image  # type: ignore
            pet.updated_at = today  # type: ignore
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


def delete(request, id):
    pet = get_one_pet(id)
    if pet is None:
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    try:
        pet.delete()
        return redirect("/pet/index")
    except Exception as e:
        traceback.format_exc()
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )


def get_one_pet(id):
    try:
        return PetModel.objects.get(pk=id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return None


def get_media_or_empty(request, name):
    if (name, "") in request.POST.items():
        return ""
    else:
        return request.FILES[name]
