import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Djangoのログイン(認証)機能を使えるよう、AbstractUserを継承
class Owner(AbstractUser, models.Model):
    USERNAME_FIELD = "username"

    # superuserを作る際、入力に含める
    REQUIRED_FIELDS = ["contact", "created_at", "updated_at"]

    class Meta:
        db_table = "owner"

    # ユーザー名(飼い主名)
    username = models.CharField(max_length=20, unique=True)
    # パスワード
    password = models.TextField()
    # 連絡先1
    contact = models.EmailField(max_length=30, unique=True)
    # 連絡先2
    sub_contact = models.CharField(max_length=30)
    # メッセージ
    message = models.TextField()

    now = datetime.datetime.now()
    # 登録日時
    created_at = models.DateTimeField(default=now)
    # 更新日時
    updated_at = models.DateTimeField(default=now)
