from datetime import datetime
import traceback

from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from petApp.models import PetModel
from petApp.forms import PetForm
from petCommentApp.forms import PetCommentForm


@login_required
def index(request):
    list = PetModel.objects.all()
    list = list.order_by("created_at").reverse()
    return render(request, "pet/index.html", {"list": list})


@login_required
def new(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if not form.is_valid():
            # clean_post_cord()でバリデーションにかかった場合
            if "post_cord" in form.errors:
                messages.error(request, form.errors["post_cord"][0])
            else:
                messages.error(request, "ご入力の際にエラーが発生しました。管理者にご確認ください")
            return redirect("/pet/new/")

        pet = form.save(commit=False)

        now = datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")

        pet.created_at = today
        pet.updated_at = today
        pet.owner = get_current_authenticated_user()

        pet.save()
        messages.success(request, "ペットの登録が完了しました")
        return redirect("/pet/index")

    form = PetForm()
    return render(request, "pet/new.html", context={"form": form})


@login_required
def show(request, id):
    pet = get_one_pet(id)
    if pet is None:
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    pet_comment_list = pet.petcommentmodel_set.all()  # type: ignore
    pet_comment_list = pet_comment_list.order_by("created_at").reverse()
    form = PetCommentForm()
    return render(
        request,
        "pet/show.html",
        context={"pet": pet, "pet_comment_list": pet_comment_list, "form": form},
    )


@login_required
def edit(request, id):
    pet = get_one_pet(id)
    if pet is None:
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if not form.is_valid():
            # clean_post_cord()でバリデーションにかかった場合
            if "post_cord" in form.errors:
                messages.error(request, form.errors["post_cord"][0])
            else:
                messages.error(request, "ご入力の際にエラーが発生しました。管理者にご確認ください")
            return redirect("edit", id=id)

        edit_pet = form.save(commit=False)

        # 写真が未選択の場合、更新前の写真を設定
        if len(request.FILES) == 0:
            edit_pet.image = pet.image

        now = datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")

        edit_pet.created_at = pet.created_at
        edit_pet.updated_at = today
        edit_pet.owner = get_current_authenticated_user()

        edit_pet.save()
        pet.delete()  # save()完了後、更新前のデータは削除
        messages.success(request, "ペットの更新が完了しました")
        return redirect("/pet/index")

    form = PetForm(instance=pet)
    pet_id = pet.id  # type: ignore
    # nameから画像添付の有無を確認
    if pet.image.name:
        pet_image_url = pet.image.url
    else:
        pet_image_url = "/static/image/no-image.png"
    return render(
        request,
        "pet/edit.html",
        context={"form": form, "pet_id": pet_id, "pet_image_url": pet_image_url},
    )


@login_required
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


@login_required
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
