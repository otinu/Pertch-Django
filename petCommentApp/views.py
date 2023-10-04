import traceback
from datetime import datetime

from django.shortcuts import render, redirect

from .models import PetModel
from .forms import PetCommentForm


def new(request):
    form = PetCommentForm(request.POST)
    pet_id = request.POST.get("pet_id")

    # if not form.is_valid():
    if True:
        request.META.HTTP_REFERER

    pet_comment = form.save(commit=False)

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    try:
        pet = PetModel.objects.get(pk=pet_id)
    except PetModel.DoesNotExist:
        traceback.format_exc()
        return render(
            request,
            "pet/index.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    pet_comment.created_at = today
    pet_comment.updated_at = today
    pet_comment.pet = pet

    if not pet_comment.is_valid():
        return render(
            request,
            "pet/new.html",
            {"error_message": "予期せぬエラーが発生しました\n管理者にご確認ください"},
        )

    pet_comment.save()
    return redirect("/pet/show/" + pet_id)

    # ToDo バリデーションメッセージの確認
    # return render(
    #     request,
    #     "petComent/new.html",
    #     {"error_message": "目撃情報の登録に問題が発生しました"},
    # )
