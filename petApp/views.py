from datetime import datetime
import traceback

from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib import messages

from petApp.models import PetModel
from petApp.forms import PetForm
from petCommentApp.forms import PetCommentForm


def index(request):
    list = PetModel.objects.all()
    return render(request, "pet/index.html", {"list": list})


def new(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, "ご入力の際にエラーが発生しました。管理者にご確認ください")
            return redirect("/pet/new/")

        pet = form.save(commit=False)

        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        pet.created_at = today
        pet.updated_at = today
        pet.owner = get_current_authenticated_user()

        pet.save()
        messages.success(request, "ペットの登録が完了しました")
        return redirect("/pet/index")

    form = PetForm()
    return render(request, "pet/new.html", context={"form": form})


def show(request, id):
    pet = get_one_pet(id)
    if pet is None:
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    pet_comment_list = pet.petcommentmodel_set.all()  # type: ignore
    form = PetCommentForm()
    return render(
        request,
        "pet/show.html",
        context={"pet": pet, "pet_comment_list": pet_comment_list, "form": form},
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
        charm_point = request.POST.get("charm-point")
        post_cord = request.POST.get("post-cord")
        address = request.POST.get("address")

        image = get_media_or_empty(request, "upload_file")

        # created_at,updated_at用
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")

        try:
            pet.age = age
            pet.charm_point = charm_point
            pet.post_cord = post_cord
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


def search(request):
    if request.method == "POST":
        name = request.POST.get("name")
        age = request.POST.get("age")
        sex_string = request.POST.get("sex")
        if sex_string:
            sex = True
        else:
            sex = False
        charm_point = request.POST.get("charm-point")
        post_cord = request.POST.get("post-cord")
        address = request.POST.get("address")
        owner = request.POST.get("owner")

        # 検索実行
        list = PetModel.objects
        if name:
            list = list.filter(name__icontains=name)
        if age:
            list = list.filter(age=age)
        if sex:
            list = list.filter(sex=sex)
        if charm_point:
            list = list.filter(charm_point__icontains=charm_point)
        if post_cord:
            list = list.filter(post_cord=post_cord)
        if address:
            list = list.filter(address__icontains=address)
        if owner:
            list = list.filter(owner__username=owner)

        if type(list) == QuerySet:
            return render(request, "pet/index.html", {"list": list})
        else:
            return render(request, "pet/index.html", {"search_message": "検索結果は0件でした"})

    return render(
        request, "pet/index.html", {"search_message": "予期せぬエラーが発生しました\n管理者にご確認ください"}
    )


def get_one_pet(id):
    try:
        return PetModel.objects.get(pk=id)
    except PetModel.DoesNotExist:
        print(traceback.format_exc())
        return None


def get_media_or_empty(request, name):
    if (name, "") in request.POST.items():
        return ""
    else:
        return request.FILES[name]
