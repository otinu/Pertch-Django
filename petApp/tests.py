import re
from datetime import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.core.files import File
from django.db.models.fields.files import ImageFieldFile

from petApp.views import index, new, show
from petApp.forms import PetForm
from petCommentApp.forms import PetCommentForm
from ownerApp.models import Owner
from petApp.models import PetModel
from petCommentApp.models import PetCommentModel


class NewTest(TestCase):
    def setUp(self) -> None:
        user = Owner.objects.create(
            username="tester", password="Test1", contact="test@test.co.jp"
        )

        pet = PetModel.objects.create(
            id=999,
            name="testPet",
            age=99,
            sex=True,
            charm_point="test",
            post_cord="9999999",
            address="test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=user,
        )

        self.data = {
            "id": pet.pk,
            "name": pet.name,
            "age": pet.age,
            "sex": True,
            "image": File(open("media/pet/test.png")),
            "charm_point": pet.charm_point,
            "post_cord": pet.post_cord,
            "address": pet.address,
            "created_at": pet.created_at,
            "updated_at": pet.updated_at,
        }

    # 初回アクセス
    def test_enter(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        # URLの確認
        url = reverse("pet:new")
        self.assertEqual(resolve(url).func, new)

        # ステータスコードの確認
        response = self.client.get("/pet/new", follow=True)
        self.assertEqual(response.status_code, 200)

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)
        response = self.client.get("/pet/new", follow=True)

        test_case_list = [
            "ペット登録",
            # FontAwesomeによって、デベロッパーツールで開く際はsvgタグになっている
            # ⇒テスト実行時、内部ではiタグのままコメントアウトされない状態になる
            '<i class="fa-solid fa-shield-dog',
            "名前",
            '<input type="text" name="name"',
            "年齢",
            '<input type="number" name="age"',
            "性別",
            "♂",
            '<input type="radio" name="sex" value="True"',
            "♀",
            '<input type="radio" name="sex" value="False"',
            "ペットの写真",
            "未選択",
            '<input type="file" name="image"',
            "特徴",
            '<textarea name="charm_point"',
            "郵便番号",
            '<input type="number" name="post_cord" id="post-cord" placeholder="7桁でご入力ください"',
            "住所",
            '<input type="text" name="address"',
            "登録",
            '<input type="submit" value="登録"',
            "<small>©Otinu</small>",
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

    # 通常登録
    def test_registration_normal(self):
        test_pet = PetModel.objects.get(pk=999)

        # Formクラスのバリデーションの代わりにsave()にてテスト実施
        form = PetForm(self.data)
        self.assertTrue(form.is_valid())
        pet = form.save(commit=False)
        pet.owner = test_pet.owner
        form.save()

        ## ペットの写真なし
        pet.image = None
        pet.save()

        ### 次テストの準備
        pet.delete()
        form = PetForm(self.data)
        pet = form.save(commit=False)
        pet.owner = test_pet.owner
        pet.save()

        ## 特徴なし
        pet.charm_point = ""
        pet.save()

        ### 次テストの準備
        pet.charm_point = test_pet.charm_point
        pet.save()

        ## 住所なし
        pet.address = ""
        pet.save()

        ### 次テストの準備
        pet.address = test_pet.address
        pet.save()

    # 異常登録(年齢)
    def test_registration_abnormal(self):
        test_pet = PetModel.objects.get(pk=999)

        ## 名前(1文字)
        self.data["name"] = "t"
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("name" in form.errors)
        self.assertFalse(form.is_valid())

        ## 名前(21文字)
        self.data["name"] = "t" * 21
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("name" in form.errors)
        self.assertFalse(form.is_valid())

        ## 名前なし
        self.data["name"] = ""
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("name" in form.errors)
        self.assertFalse(form.is_valid())

        ### 次テストの準備
        self.data["name"] = "testPet"

        ## 年齢(-1)
        self.data["age"] = -1
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("age" in form.errors)
        self.assertFalse(form.is_valid())

        ## 年齢(100)
        self.data["age"] = 100
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("age" in form.errors)
        self.assertFalse(form.is_valid())

        ## 年齢(test)
        self.data["age"] = "test"
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("age" in form.errors)
        self.assertFalse(form.is_valid())

        ## 年齢(test)
        self.data["age"] = "test"
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("age" in form.errors)
        self.assertFalse(form.is_valid())

        ## 年齢なし
        self.data["age"] = None
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("age" in form.errors)
        self.assertFalse(form.is_valid())

        ### 次テストの準備
        self.data["age"] = 99

        ## 特徴(1001文字)
        self.data["charm_point"] = "t" * 1001
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("charm_point" in form.errors)
        self.assertFalse(form.is_valid())

        ### 次テストの準備
        self.data["charm_point"] = "test"

        ## 郵便番号(数字1ケタ)
        self.data["post_cord"] = 9
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("post_cord" in form.errors)
        self.assertFalse(form.is_valid())

        ## 郵便番号(数字6ケタ)
        self.data["post_cord"] = 123456
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("post_cord" in form.errors)
        self.assertFalse(form.is_valid())

        ## 郵便番号未入力
        self.data["post_cord"] = None
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("post_cord" in form.errors)
        self.assertFalse(form.is_valid())


"""
# ログインに成功し、正常なリダイレクトのみか確認
redirect_pattern = r"/owner/top/.*"
self.assertFalse(re.match(redirect_pattern, response.redirect_chain[0][0]))
self.assertEqual(len(response.redirect_chain), 1)
"""


class ShowTest(TestCase):
    def setUp(self) -> None:
        self.user = Owner.objects.create(
            username="tester", password="Test1", contact="test@test.co.jp"
        )

        PetModel.objects.create(
            id=999,
            name="testPet",
            age=99,
            sex=True,
            charm_point="test",
            post_cord="9999999",
            address="test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=self.user,
        )

    # 初回アクセス
    def test_enter(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        # URLの確認
        url = reverse("pet:show", kwargs={"id": 999})
        self.assertEqual(resolve(url).func, show)

        # ステータスコードの確認
        response = self.client.get("/pet/show/999", follow=True)
        self.assertEqual(response.status_code, 200)
