import datetime
import traceback

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.db import IntegrityError
from django.contrib import messages

from .forms import registration_form
from .models import Owner


def top(request):
    return render(request, "owner/top.html")


def registration(request):
    if request.method == "POST":
        """
        # ToDo バリデーション追加
        form = registration_form(request.POST)
        if form.is_valid():
            return render(
                request,
                "owner/registration.html",
                {"errorMessages": "Name,Password,Emailの入力は必須です"},
            )
        """

        username = request.POST.get("username")
        message = request.POST.get("message")
        contact = request.POST.get("contact")

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")

        try:
            owner = Owner.objects.create(
                username=username,
                message=message,
                contact=contact,
                created_at=today,
                updated_at=today,
            )
            password = request.POST.get("password")
            owner.set_password(password)
            owner.save()
            return redirect("/owner/login")
        except IntegrityError as e:
            traceback.format_exc()
            return render(
                request,
                "owner/registration.html",
                {"error_message": "ユーザー登録に問題が発生しました"},
            )

    separation_string = screen_separation(request)
    if separation_string == "normal":
        return render(request, "owner/registration.html")
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
