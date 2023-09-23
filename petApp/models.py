import datetime

from django.db import models
from django.core.validators import MinLengthValidator

from ownerApp.models import Owner

# ToDo サブクラス(Meta)を使ってテーブル名指定
# ToDo 非NULL制約 などの制約 + Fieldクラスのblankなどフィールドオプションの利用


class PetModel(models.Model):
    class Meta:
        db_table = "pet"

    # ペット名
    # (name)最小文字数2,最大文字数20
    name = models.CharField(validators=[MinLengthValidator(2)], max_length=20)
    # 年齢
    age = models.CharField(validators=[MinLengthValidator(0)], max_length=99)
    # 性別
    sex = models.BooleanField()
    # 特徴
    charmPoint = models.CharField(max_length=1000)
    # 郵便番号
    # ToDo 住所のバリデーション(正規表現)
    # ToDo 7文字ちょうどを指定したい
    postCord = models.CharField(validators=[MinLengthValidator(7)], max_length=8)
    # 住所
    address = models.CharField(max_length=50)
    # 写真
    image = models.ImageField(upload_to="pet/")

    now = datetime.datetime.now()
    # 登録日時
    created_at = models.DateTimeField(default=now)
    # 更新日時
    updated_at = models.DateTimeField(default=now)

    # Owner:Pet で 1:N の関係
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
