import traceback
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import PetModel
from .forms import PetCommentForm


def new(request):
    form = PetCommentForm(request.POST)
    pet_id = request.POST.get("pet_id")

    if not form.is_valid():
        messages.error(request, "ご入力の際にエラーが発生しました。管理者にご確認ください")
        return redirect("/pet/show/" + pet_id)

    try:
        pet = PetModel.objects.get(pk=pet_id)
    except PetModel.DoesNotExist as e:
        print(traceback.format_exc())
        messages.error(request, "予期せぬエラーが発生しました。管理者にご確認ください")
        return redirect("/pet/index/")

    pet_comment = form.save(commit=False)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    pet_comment.created_at = today
    pet_comment.updated_at = today
    pet_comment.pet = pet

    pet_comment.save()
    return redirect("/pet/show/" + pet_id)
