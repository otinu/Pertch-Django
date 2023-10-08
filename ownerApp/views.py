import datetime
import traceback

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.contrib import messages

from .models import Owner
from .forms import OwnerForm


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

    separation_string = screen_separation(request)
    if separation_string == "normal":
        form = OwnerForm
        return render(request, "owner/registration.html", context={"form": form})
    elif separation_string == "abnormal":
        return render(
            request,
            "owner/registration.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )
    else:
        return redirect(separation_string)


def login_func(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "owner/login.html", {"error_message": "ログインに失敗しました"})

    """
    # ログイン画面への遷移時
    hidden_list = ["registration", "top"]
    if not hidden_list in request.GET["hidden_value"]:
        return render(request, "owner/login.html")

    # ログイン画面から他の画面への遷移時
    next = request.GET["hidden_value"]
    next_page = "owner/" + next
    return render(request, next_page)
    """
    separation_string = screen_separation(request)
    if separation_string == "normal":
        return render(request, "owner/login.html")
    elif separation_string == "abnormal":
        return render(
            request,
            "owner/login.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )
    else:
        return redirect(separation_string)


def logout_func(request):
    logout(request)
    return redirect("/owner/top")


def mypage(request):
    owner = get_current_authenticated_user()
    return render(
        request,
        "owner/mypage.html",
        {"owner": owner},
    )


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
        traceback.format_exc()
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )


def update(request):
    current_user = get_current_authenticated_user()
    owner = Owner.objects.get(id=current_user.id)  # type: ignore

    owner.contact = request.POST.get("contact")
    owner.sub_contact = request.POST.get("sub-contact")
    owner.message = request.POST.get("owner-message")

    try:
        owner.save()
    except Exception as e:
        traceback.format_exc()
        return render(
            request,
            "owner/mypage.html",
            {"owner": owner, "error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    messages.success(request, "マイページ情報の更新が完了しました")
    return redirect("/owner/mypage")


def delete(request):
    current_user = get_current_authenticated_user()
    owner = Owner.objects.get(id=current_user.id)  # type: ignore
    try:
        owner.delete()
        logout(request)
        return redirect("/owner/top")
    except Exception as e:
        traceback.format_exc()
        return render(
            request,
            "owner/mypage.html",
            {"owner": owner, "error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )


def screen_separation(request):
    try:
        next_url = request.GET["hidden_value"]
        return "/owner/" + next_url
    except KeyError as e:
        error_message = traceback.format_exception_only(type(e), e)[0]
        if "django.utils.datastructures.MultiValueDictKeyError" in error_message:
            return "normal"

        traceback.format_exc()
        return "abnormal"
