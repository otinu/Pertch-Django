import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


# Djangoのログイン(認証)機能を使えるよう、AbstractUserを継承
class Owner(AbstractUser):
    """
    継承フィールド一覧

    username：CharField
    first_name：CharField
    last_name：CharField
    email：EmailField
    is_staff ：BooleanField
    is_active：BooleanField
    date_joined：DateTimeField
    """

    username = models.CharField(max_length=20, unique=True)
    password = models.TextField()
    message = models.TextField()
    contact = models.EmailField(max_length=30, unique=True)
    sub_contact = models.CharField(max_length=30)

    now = datetime.datetime.now()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    USERNAME_FIELD = "username"

    # superuserを作る際、入力に含める
    REQUIRED_FIELDS = ["contact", "created_at", "updated_at"]
