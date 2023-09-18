import datetime
import traceback

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError

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

        username = request.POST["username"]
        password = request.POST["password"]
        message = request.POST["message"]
        contact = request.POST["contact"]

        # created_at,updated_at用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        try:
            Owner.objects.create(
                username=username,
                password=password,
                message=message,
                contact=contact,
                created_at=today,
                updated_at=today,
            )
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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "pet/index.html")
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
            request, "owner/login.html", {"error_message": "予期せエラーが発生しました\n管理者にご確認ください"}
        )
    else:
        return redirect(separation_string)


def logout_func(request):
    logout(request)
    return redirect("/owner/top")


def screen_separation(request):
    try:
        next_url = request.GET["hidden_value"]
        return next_url
    except KeyError as e:
        error_message = traceback.format_exception_only(type(e), e)[0]
        if "django.utils.datastructures.MultiValueDictKeyError" in error_message:
            return "normal"

        traceback.format_exc()
        return "abnormal"
