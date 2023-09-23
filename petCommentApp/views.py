from datetime import datetime
import traceback

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user

from .models import PetModel, PetCommentModel


def new(request):
    event_time = request.POST.get("event-time")
    event_place = request.POST.get("event-place")
    event_information = request.POST.get("event-information")

    # created_at,updated_at用
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    # PetとPetComentの紐づけ
    pet_id = request.POST.get("pet-id")
    try:
        pet = PetModel.objects.get(pk=pet_id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return render(
            request,
            "petComment/new.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    try:
        PetCommentModel.objects.create(
            event_time=event_time,
            event_place=event_place,
            event_information=event_information,
            created_at=today,
            updated_at=today,
            pet=pet,
        )
        return redirect("/pet/show/" + pet_id)
    except IntegrityError as e:
        traceback.format_exc()

        # ToDo バリデーションメッセージの確認
        return render(
            request,
            "petComent/new.html",
            {"error_message": "目撃情報の登録に問題が発生しました"},
        )
