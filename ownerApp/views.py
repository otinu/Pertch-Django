from datetime import datetime
import traceback

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Owner
from .forms import OwnerForm, MypageForm


def top(request):
    return render(request, "owner/top.html")


def registration(request):
    if request.method == "POST":
        form = OwnerForm(request.POST)

        if "username" in form.errors and form.errors["username"] == [
            "Owner with this Username already exists."
        ]:
            messages.error(request, "エラーが発生しました。ご入力のユーザー名は既に登録済みでした")
            return redirect("/owner/registration/")

        if "password" in form.errors and len(form.errors["password"]) > 0:
            messages.error(request, "エラーが発生しました。パスワードは4～12文字、英語小文字・大文字を含めてご入力ください")
            return redirect("/owner/registration/")

        if "contact" in form.errors and len(form.errors["contact"]) > 0:
            messages.error(request, "エラーが発生しました。有効なメールアドレスをご入力ください")
            return redirect("/owner/registration/")

        owner = form.save(commit=False)
        owner.set_password(form.cleaned_data["password"])
        owner.save()
        messages.success(request, "ユーザー登録が完了しました")
        return redirect("/owner/login/")

    form = OwnerForm
    return render(request, "owner/registration.html", context={"form": form})


def login_func(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("pet:index")
        else:
            messages.error(request, "ログインに失敗しました。ユーザー名とパスワードをご確認ください")
            return redirect("/owner/login/")

    return render(request, "owner/login.html")


@login_required
def logout_func(request):
    logout(request)
    return redirect("/owner/top")


@login_required
def mypage(request):
    owner = get_current_authenticated_user()
    form = MypageForm(instance=owner)
    return render(
        request,
        "owner/mypage.html",
        {"owner": owner, "form": form},
    )


@login_required
def detail(request, id):
    try:
        owner = Owner.objects.get(pk=id)
        pet_list = owner.petmodel_set.all()  # type: ignore
        return render(
            request,
            "owner/detail.html",
            {"owner": owner, "pet_list": pet_list},
        )
    except Owner.DoesNotExist:
        print(traceback.format_exc())
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )


@login_required
def update(request):
    current_user = get_current_authenticated_user()
    owner = Owner.objects.get(id=current_user.id)  # type: ignore
    form = MypageForm(request.POST, instance=owner)

    if "contact" in form.errors and len(form.errors["contact"]) > 0:
        messages.error(request, "エラーが発生しました。有効なメールアドレスをご入力ください")
        return redirect("/owner/mypage/")

    form.save()
    messages.success(request, "マイページ情報の更新が完了しました")
    return redirect("/owner/mypage")


@login_required
def delete(request):
    current_user = get_current_authenticated_user()
    owner = Owner.objects.get(id=current_user.id)  # type: ignore
    try:
        owner.delete()
        logout(request)
        return redirect("/owner/top")
    except Exception as e:
        print(traceback.format_exc())
        return render(
            request,
            "owner/mypage.html",
            {"owner": owner, "error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )
