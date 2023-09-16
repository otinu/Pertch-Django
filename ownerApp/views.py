import datetime
import traceback

from django.shortcuts import render
from django.db import IntegrityError

from .forms import registrationForm
from .models import Owner


def registration(request):
    if request.method == "POST":
        form = registrationForm(request.POST)

        """
        # ToDo バリデーション追加
        
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

        # createdAt,updatedAt用
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d")

        try:
            Owner.objects.create(
                username=username,
                password=password,
                message=message,
                contact=contact,
                createdAt=today,
                updatedAt=today,
            )
        except IntegrityError as e:
            traceback.format_exc()
            return render(
                request,
                "owner/registration.html",
                {"errorMessages": "ユーザー登録に問題が発生しました"},
            )

    return render(request, "owner/registration.html", {"errorMessages": None})
