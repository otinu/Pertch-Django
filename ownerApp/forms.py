from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

Owner = get_user_model()


class registration_form(UserCreationForm):
    # ToDo バリデーション機能の追加
    # ⇒現状、ユーザー名未記載・HTMLのrequired抜き の場合にバリデーションがかからない
    class Meta:
        model = Owner
        fields = Owner.REQUIRED_FIELDS + ["password1", "password2"]


class login_form(AuthenticationForm):
    pass
