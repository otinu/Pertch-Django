import re
from datetime import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

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
        with open("media/pet/test.png", "rb") as f:
            file = SimpleUploadedFile(f.name, f.read(), content_type="image/png")
        image = {"image": file}

        form = PetForm(self.data, image)
        self.assertTrue(form.is_valid())
        pet = form.save(commit=False)
        pet.owner = test_pet.owner
        pet.save()

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

    # 異常登録
    def test_registration_abnormal(self):
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


class ShowTest(TestCase):
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

        test_pet_comment = PetCommentModel.objects.create(
            pk=999,
            event_time=datetime.now(),
            event_place="test_place",
            event_information="test_information",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            pet=pet,
        )

        self.data = {
            "event_time": test_pet_comment.event_time,
            "event_place": test_pet_comment.event_place,
            "event_information": test_pet_comment.event_information,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "pet": test_pet_comment.pet,
        }

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

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        test_pet = PetModel.objects.get(pk=999)
        response = self.client.get("/pet/show/999", follow=True)

        sex = "♂" if test_pet.sex else "♀"

        owner_a_tag = (
            '<a id="owner-show-link" href="/owner/detail/'
            + str(test_pet.owner.pk)
            + '">'
        )
        owner_link = owner_a_tag + test_pet.owner.username + "</a>"

        ## 画面(ペット)
        test_case_list = [
            '<h2 style="margin: 0;">' + test_pet.name + "</h2>",
            '<img id="pet-image" src="/static/image/no-image.png">',
            "年齢",
            "<p>" + str(test_pet.age) + "歳</p>",
            "性別",
            "<p>" + sex + "</p>",
            "オーナー",
            owner_link,
            "特徴",
            "<textarea readonly>" + test_pet.charm_point + "</textarea>",
            "郵便番号",
            "<p>" + str(test_pet.post_cord) + "</p>",
            "住所",
            "<p>" + test_pet.address + "</p>",
            "<small>©Otinu</small>"
            # breakpoint()でpet.imageが入っている状態でも、
            # response.content内はno-image.pngになってしまう
            # ⇒写真の自動テストは負荷
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

        ## 画面(目撃情報)
        test_case_list = [
            '<h2 id="eye-witness-title">目撃情報</h2>',
            "日時",
            '<input type="datetime-local" name="event_time"',
            "場所",
            '<input type="text" name="event_place"',
            "情報",
            '<textarea name="event_information"',
            '<input type="submit" id="eyewitness-button" value="投稿"',
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

    # 通常登録
    def test_registration_normal(self):
        pet_comment_form = PetCommentForm(self.data)
        self.assertTrue(pet_comment_form.is_valid())

    # 異常登録
    ## 日時(20231001)
    def test_registration_abnormal(self):
        self.data["event_time"] = datetime(2023, 10, 1).strftime("%Y%m%d")
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_time" in form.errors)
        self.assertFalse(form.is_valid())

        ## 日時(2023年10月1日)
        self.data["event_time"] = datetime(2023, 10, 1).strftime("%Y年%m月%d日")
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_time" in form.errors)
        self.assertFalse(form.is_valid())

        ## 日時(2023/15/01)
        self.data["event_time"] = "2023/15/01"  # datetimeでは作成不可のため、文字列で代用
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_time" in form.errors)
        self.assertFalse(form.is_valid())

        ## 日時未入力
        self.data["event_time"] = None
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_time" in form.errors)
        self.assertFalse(form.is_valid())

        ### 次テストの準備
        self.data["event_time"] = datetime.now()

        ## 場所(81文字)
        self.data["event_place"] = "t" * 81
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_place" in form.errors)
        self.assertFalse(form.is_valid())

        ## 場所未入力
        self.data["event_place"] = None
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_place" in form.errors)
        self.assertFalse(form.is_valid())

        ### 次テストの準備
        self.data["event_place"] = "test_place"

        ## 情報(201文字)
        self.data["event_information"] = "t" * 201
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_information" in form.errors)
        self.assertFalse(form.is_valid())

        ## 情報未入力
        self.data["event_information"] = None
        form = PetCommentForm(self.data)
        if form.errors is not None:
            self.assertTrue("event_information" in form.errors)
        self.assertFalse(form.is_valid())
