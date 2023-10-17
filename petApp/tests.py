from datetime import datetime
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.core.files.uploadedfile import SimpleUploadedFile

from petApp.views import index, new, show, edit
from petApp.forms import PetForm
from petCommentApp.forms import PetCommentForm
from ownerApp.models import Owner
from petApp.models import PetModel
from petCommentApp.models import PetCommentModel


class IndexTest(TestCase):
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

        PetModel.objects.create(
            id=1000,
            name="otherPet",
            age=0,
            sex=False,
            charm_point="other",
            post_cord="1111111",
            address="other",
            image="other_image.png",
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
        url = reverse("pet:index")
        self.assertEqual(resolve(url).func, index)

        # ステータスコードの確認
        response = self.client.get("/pet/index", follow=True)
        self.assertEqual(response.status_code, 200)

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)
        response = self.client.get("/pet/index", follow=True)

        pet = PetModel.objects.get(pk=999)
        other_pet = PetModel.objects.get(pk=1000)

        pet_sex = "♂" if pet.sex else "♀"
        other_pet_sex = "♂" if other_pet.sex else "♀"

        other_pet_owner_link = (
            '<a href="/owner/detail/'
            + str(other_pet.owner.pk)
            + '">'
            + other_pet.owner.username
        )

        test_case_list = [
            ## ロゴ
            '<img id="title-logo-img" src="/static/image/title_logo.png">',
            '<a id="title-logo-link" href="/pet/index"',
            ## ハンバーガーメニュー
            '<button class="hamburger-menu"',
            "ペット一覧",
            '<i class="fa-solid fa-magnifying-glass-location fa-2x"></i>',
            "ペット登録",
            '<i class="fa-solid fa-shield-dog fa-2x"></i>',
            "マイページ",
            '<i class="fa-solid fa-shield-dog fa-2x"></i>',
            "ログアウト",
            '<i class="fa-solid fa-door-open fa-2x"></i>',
            ## 検索エリア
            "ペット一覧",
            '<h2 style="text-align: center;">',  # アイコンはハンバーガーメニューと重複のため省略
            "ペット名",
            '<input type="text" name="name"',
            "年齢",
            '<input type="number" class="search-input-age" name="age"',
            "性別",
            "♂",
            '<input type="radio" value="true" name="sex"',
            "♀",
            '<input type="radio" value="false" name="sex"',
            "特徴",
            '<input type="text" name="charm_point"',
            "郵便番号",
            '<input id="post-cord" type="text" name="post_cord"',
            "住所",
            '<input id="address" type="text" name="address"',
            "飼い主",
            '<input type="text" name="owner"',
            "検索",
            '<input type="submit" class="submit-button" value="検索"',
            '<form id="search" method="post" action="/pet/search/"',
            ## テーブル(ヘッダ)
            "ペット名",
            "<th>ペット名&nbsp;",
            "<th>年齢&nbsp;",
            "<th>性別&nbsp;",
            "<th>特徴&nbsp;",
            "<th>郵便番号&nbsp;",
            "<th>住所&nbsp;",
            "<th>飼い主&nbsp;",
            '<th id="no-sort-column">編集',
            '<th id="no-sort-column">削除',
            ## テーブル(ボディ)
            '<a href="/pet/show/' + str(pet.pk) + '">' + pet.name,
            '<td style="text-align: center;">' + str(pet.age),
            '<td style="text-align: center;">' + pet_sex,
            "<td>" + pet.charm_point,
            "<td>" + str(pet.post_cord),
            "<td>" + pet.address,
            '<a href="/owner/detail/' + str(pet.owner.pk) + '">' + pet.owner.username,
            '<a href="/pet/edit/' + str(pet.pk) + '">',
            '<a href="/pet/delete/' + str(pet.pk) + '">',
            '<a href="/pet/show/' + str(other_pet.pk) + '">' + other_pet.name,
            '<td style="text-align: center;">' + str(other_pet.age),
            '<td style="text-align: center;">' + other_pet_sex,
            "<td>" + other_pet.charm_point,
            "<td>" + str(other_pet.post_cord),
            "<td>" + other_pet.address,
            other_pet_owner_link,
            '<a href="/pet/edit/' + str(other_pet.pk) + '">',
            '<a href="/pet/delete/' + str(other_pet.pk) + '">',
            '<i class="fa-solid fa-pen-to-square"></i>',
            '<i class="fa-solid fa-trash"></i>',
            ## フッター
            "<small>©Otinu</small>",
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

    # 検索
    def test_search(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        owner1 = Owner.objects.create(
            username="search_owner", password="Test1", contact="search@test.co.jp"
        )
        owner2 = Owner.objects.create(
            username="検索owner", password="Test1", contact="search2@test.co.jp"
        )

        PetModel.objects.create(
            id=2000,
            name="search_dog",
            age=1,
            sex=True,
            charm_point="おおきい犬",
            post_cord="123456789",
            address="香川県高松市",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=owner1,
        )
        PetModel.objects.create(
            id=2001,
            name="検索dog",
            age=0,
            sex=False,
            charm_point="ちいさい犬",
            post_cord="127654389",
            address="香川県丸亀市",
            image="other_image.png",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=owner2,
        )
        PetModel.objects.create(
            id=2002,
            name="search_cat",
            age=3,
            sex=True,
            charm_point="おおきい猫",
            post_cord="213456798",
            address="高松市サンポート",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=owner1,
        )

        path = "/pet/search/"

        ## 6項目検索
        data = {
            "name": "search",
            "age": 3,
            "sex": "true",
            "charm_point": "おおきい",
            "post_cord": "34567",
            "address": "高松市",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "search_cat")
        self.assertNotContains(response, "search_dog")
        self.assertNotContains(response, "検索dog")

        ## 5項目検索
        data = {
            "name": "search",
            "sex": "true",
            "charm_point": "おおきい",
            "post_cord": "34567",
            "address": "高松市",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "search_dog")
        self.assertContains(response, "search_cat")
        self.assertNotContains(response, "検索dog")

        ## 4項目検索
        data = {
            "name": "検索",
            "sex": "false",
            "charm_point": "犬",
            "address": "香川県",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "検索dog")
        self.assertNotContains(response, "search_dog")
        self.assertNotContains(response, "search_cat")

        ## 3項目検索
        data = {
            "name": "検索",
            "charm_point": "犬",
            "address": "香川県",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "検索dog")
        self.assertNotContains(response, "search_dog")
        self.assertNotContains(response, "search_cat")

        ## 2項目検索
        data = {
            "age": 3,
            "address": "サンポート",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "search_cat")
        self.assertNotContains(response, "検索dog")
        self.assertNotContains(response, "search_dog")

        ## 1項目検索
        data = {
            "address": "市",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertContains(response, "search_dog")
        self.assertContains(response, "search_cat")
        self.assertContains(response, "検索dog")

        ## 結果なし
        data = {
            "post_cord": "22",
        }
        response = self.client.post(path, data=data, follow=True)
        self.assertNotContains(response, "search_dog")
        self.assertNotContains(response, "search_cat")
        self.assertNotContains(response, "検索dog")
        self.assertContains(response, "検索結果は0件でした")


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

    # 異常登録/更新
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

        ## 住所(51文字)
        self.data["address"] = "t" * 51
        form = PetForm(self.data)
        if form.errors is not None:
            self.assertTrue("address" in form.errors)
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


class EditTest(TestCase):
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
        url = reverse("pet:edit", kwargs={"id": 999})
        self.assertEqual(resolve(url).func, edit)

        # ステータスコードの確認
        response = self.client.get("/pet/edit/999", follow=True)
        self.assertEqual(response.status_code, 200)

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        test_pet = PetModel.objects.get(pk=999)
        response = self.client.get("/pet/edit/999", follow=True)

        sex = "♂" if test_pet.sex else "♀"

        charm_point = (
            '<textarea name="charm_point" cols="40" rows="10" maxlength="1000" id="id_charm_point">'
            + "\n"
            + test_pet.charm_point
        )

        post_cord = (
            '<input type="number" name="post_cord" value="'
            + str(test_pet.post_cord)
            + '"'
        )

        ## 画面(ペット)
        test_case_list = [
            '<input type="text" name="name" value="' + test_pet.name + '"',
            '<img id="pet-image" src="/static/image/no-image.png">',
            "年齢",
            '<input type="number" name="age" value="' + str(test_pet.age) + '"',
            "性別",
            "<p>" + sex + "</p>",
            "ペットの写真",
            "未選択",
            '<input type="file" name="image"',
            "特徴",
            charm_point,
            "郵便番号",
            post_cord,
            "住所",
            '<input type="text" name="address" value="' + test_pet.address + '"',
            "<small>©Otinu</small>",
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

    # 通常更新
    def test_registration_normal(self):
        origin_pet = PetModel.objects.get(pk=999)
        edit_pet = PetModel.objects.get(pk=999)

        ## 名前更新
        edit_pet.name = "new_name"
        edit_pet.save()
        edit_pet.name = origin_pet.name

        ##  年齢更新
        edit_pet.age = 5
        edit_pet.save()
        edit_pet.age = origin_pet.age

        ## ペットの写真(なし⇒あり)
        with open("media/pet/test.png", "rb") as f:
            file = SimpleUploadedFile(f.name, f.read(), content_type="image/png")
        image = {"image": file}
        form = PetForm(self.data, image)
        self.assertTrue(form.is_valid())

        ## ペットの写真(あり⇒なし)
        new_pet = PetModel.objects.create(
            id=1000,
            name="new_name",
            age=0,
            sex=True,
            image="new.png",
            charm_point="new_charm_point",
            post_cord="0000000",
            address="new_address",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            owner=origin_pet.owner,
        )
        new_pet.image = None  # type: ignore
        new_pet.save()

        ## 特徴更新
        edit_pet.charm_point = "new_charm_point"
        edit_pet.save()
        edit_pet.charm_point = origin_pet.charm_point

        ## 郵便番号更新
        edit_pet.post_cord = 2222222
        edit_pet.save()
        edit_pet.post_cord = origin_pet.post_cord

        ## 住所更新
        edit_pet.address = "new_address"
        edit_pet.save()
        edit_pet.address = origin_pet.address

        ## 全更新
        edit_pet.name = new_pet.name
        edit_pet.age = new_pet.age
        edit_pet.image = new_pet.image  # type: ignore
        edit_pet.charm_point = new_pet.charm_point
        edit_pet.post_cord = new_pet.post_cord
        edit_pet.address = new_pet.address
        edit_pet.save()

    # 異常更新
    # ⇒NewTest.test_registration_abnormal(self)にて確認
