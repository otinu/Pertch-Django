import traceback
from datetime import datetime

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_authenticated_user
from django.forms.models import ModelChoiceField
from django.utils import timezone

from .models import PetModel, PetCommentModel
from .forms import PetCommentForm

"""
def new(request):
    event_time = request.POST.get("event_time")
    event_place = request.POST.get("event_place")
    event_information = request.POST.get("event_information")

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
            "pet/new.html",
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
"""


def new(request):
    form = PetCommentForm(request.POST)

    # created_at,updated_at用
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    # PetとPetComentの紐づけ
    pet_id = request.POST.get("pet_id")
    try:
        pet = PetModel.objects.get(pk=pet_id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    # form.event_time = request.POST.get("event_time")
    # form.event_place = request.POST.get("event_place")
    # form.event_information = request.POST.get("event_information")

    form.fields["event_time"] = request.POST.get("event_time")
    form.fields["event_place"] = request.POST.get("event_place")
    form.fields["event_information"] = request.POST.get("event_information")
    form.fields["created_at"] = now
    form.fields["updated_at"] = now
    form.fields["pet"] = pet

    pet_comment = form.save(commit=False)

    # form.fields["pet"] = ModelChoiceField(queryset=PetModel.objects.filter(id=pet_id))
    # form.fields["pet"] = PetModel.objects.get(pk=pet_id)

    # form.fields["pet"].queryset = PetModel.objects.filter(id=pet_id)
    # form.fields["pet_id"] = pet_id

    pet_comment.event_time = request.POST.get("event_time")
    pet_comment.event_place = request.POST.get("event_place")
    pet_comment.event_information = request.POST.get("event_information")
    pet_comment.created_at = today
    pet_comment.updated_at = today
    pet_comment.pet = pet

    # if not pet_comment.is_valid():
    #     return render(
    #         request,
    #         "pet/new.html",
    #         {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
    #     )

    pet_comment.save()
    return redirect("/pet/show/" + pet_id)

    # ToDo バリデーションメッセージの確認
    # return render(
    #     request,
    #     "petComent/new.html",
    #     {"error_message": "目撃情報の登録に問題が発生しました"},
    # )
