import re
from django import forms
from .models import Owner
from django.contrib.auth import get_user_model


class OwnerForm(forms.ModelForm):
    username = forms.CharField(
        label="ユーザー名",
        min_length=2,
        max_length=20,
        widget=forms.TextInput(attrs={"id": "username", "placeholder": "お名前"}),
    )

    password = forms.CharField(
        label="パスワード",
        min_length=4,
        max_length=12,
        widget=forms.PasswordInput(
            attrs={"id": "password", "placeholder": "4～12文字 英語小文字・大文字"}
        ),
    )

    contact = forms.CharField(
        label="連絡先1",
        max_length=30,
        widget=forms.EmailInput(attrs={"id": "contact", "placeholder": "メールアドレス"}),
    )

    sub_contact = forms.CharField(label="連絡先2", max_length=30, required=False)

    message = forms.CharField(
        label="メッセージ",
        max_length=1000,
        widget=forms.TextInput(attrs={"id": "message"}),
        required=False,
    )

    class Meta:
        model = Owner
        fields = ("username", "password", "contact", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data["password"]
        pattern = r"(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{4,12}$"

        if re.match(pattern, password):
            return password
        raise forms.ValidationError("エラーが発生しました。パスワードは4～12文字、英語小文字・大文字を含めて入力が必要です")


class MypageForm(forms.ModelForm):
    contact = forms.CharField(
        label="連絡先1",
        max_length=30,
        widget=forms.EmailInput(
            attrs={"class": "owner-contact", "placeholder": "メールアドレス"}
        ),
    )

    sub_contact = forms.CharField(
        label="連絡先2",
        max_length=30,
        widget=forms.TextInput(
            attrs={"class": "owner-contact", "placeholder": "予備の連絡先"}
        ),
        required=False,
    )

    message = forms.CharField(
        label="メッセージ",
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                "id": "message",
                "class": "owner-message",
                "placeholder": "目撃者へのメッセージ",
            }
        ),
        required=False,
    )

    class Meta:
        model = Owner
        fields = ("contact", "sub_contact", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
