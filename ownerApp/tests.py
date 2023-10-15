import re
from datetime import datetime
from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve

from ownerApp.views import registration, login_func, mypage, detail
from ownerApp.forms import OwnerForm, MypageForm
from ownerApp.models import Owner
from petApp.models import PetModel


class RegistrationTest(TestCase):
    client = Client()
    url = reverse("owner:registration")
    response = client.get(url)

    # 初回アクセス
    def test_enter(self):
        # URLの確認
        self.assertEqual(resolve(self.url).func, registration)

        # ステータスコードの確認
        self.assertEqual(self.response.status_code, 200)

    # 画面
    def test_layout(self):
        test_case_list = [
            "Name",
            '<input type="text" name="username"',
            "Password",
            '<input type="password" name="password"',
            "Email",
            '<input type="email" name="contact"',
            "Message",
            '<textarea placeholder="目撃者へのメッセージ" id="message" name="message">',
            "登録",
            '<input class="submit-button registration-button" type="submit" value="登録"',
            "Top",
            '<input class="submit-button" type="submit" value="Top"',
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(self.response, test_case)

    # 通常登録
    def test_registration_normal(self):
        ## 全入力
        data = {
            "username": "tester",
            "password": "Tttt0",
            "contact": "test@sample.jp",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        ## Message未入力
        data["message"] = ""
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        ### 次テストの準備
        data["message"] = "登録テスト"

        ## Name(2文字)
        data["username"] = "t" * 2
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        ## Name(20文字)
        data["username"] = "t" * 20
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        ### 次テストの準備
        data["username"] = "tester"

        ## Password(4文字-半角英数字,大文字,小文字)
        data["password"] = "Tt" + "0" * 2
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        ## Password(12文字-半角英数字,大文字,小文字)
        data["password"] = "Tt" + "0" * 10
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

    # 異常登録(Name)
    def test_registration_name_abnormal(self):
        ## Name(1文字)
        data = {
            "username": "t",
            "password": "Tttt0",
            "contact": "test@sample.jp",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        ## Name(21文字)
        data["username"] = "t" * 21
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        ## Name未入力
        data["username"] = ""
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

    # 異常登録(Password)
    def test_registration_password_abnormal(self):
        ## Password(3文字)
        data = {
            "username": "tester",
            "password": "Tt0",
            "contact": "test@sample.jp",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password(13文字-半角英数字,大文字,小文字)
        data["password"] = "Tttt" + "0" * 9
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password(8文字-半角英数字,大文字)
        data["password"] = "T" * 7 + "0"
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password(8文字-半角英数字,小文字)
        data["password"] = "t" * 7 + "0"
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password(8文字-大文字,小文字)
        data["password"] = "T" * 7 + "t"
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password(8文字-半角英数字)
        data["password"] = "9" * 8
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

        ## Password未入力
        data["password"] = ""
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("password" in form.errors)
        self.assertFalse(form.is_valid())

    # 異常登録(Email)
    def test_registration_contact_abnormal(self):
        ## Email(ドットなし)
        data = {
            "username": "tester",
            "password": "Tttt0",
            "contact": "test@test",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("contact" in form.errors)
        self.assertFalse(form.is_valid())

        ## Email(31文字)
        data["contact"] = "tes" + "t" * 20 + "@test.jp"
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("contact" in form.errors)
        self.assertFalse(form.is_valid())

        ## Email未入力
        data["contact"] = ""
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("contact" in form.errors)
        self.assertFalse(form.is_valid())

    # 異常登録(Message)
    def test_registration_message_abnormal(self):
        ## Message(1001文字)
        over_message = "a" * 1001
        data = {
            "username": "tester",
            "password": "Tttt0",
            "contact": "test@sample.jp",
            "message": over_message,
        }
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("message" in form.errors)
        self.assertFalse(form.is_valid())

    # 異常登録(重複)
    def test_registration_duplicate_abnormal(self):
        ## 既存ユーザー(username)
        data = {
            "username": "tester",
            "password": "Tttt1",
            "contact": "test@sample.jp",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        form.save()
        data = {
            "username": "tester",
            "password": "Tttt15",
            "contact": "test15@sample.jp",
            "message": "登録テスト",
        }
        form = OwnerForm(data)
        if form.errors is not None:
            self.assertTrue("username" in form.errors)
        self.assertFalse(form.is_valid())


class LoginTest(TestCase):
    client = Client()
    url = reverse("owner:login")
    response = client.get(url)

    def setUp(self):
        Owner.objects.create(
            username="tester", password="Test1", contact="test@test.co.jp"
        )

    # 初回アクセス
    def test_enter(self):
        # URLの確認
        self.assertEqual(resolve(self.url).func, login_func)

        # ステータスコードの確認
        self.assertEqual(self.response.status_code, 200)

    # 画面
    def test_layout(self):
        test_case_list = [
            '<img id="profile-img"',
            '<input type="text" id="username" class="form-control" name="username"',
            '<input type="password" id="inputPassword" class="form-control" name="password"',
            "ログイン",
            '<form class="form-signin" method="post" action="/owner/login/"',
            "登録",
            '<form class="form-signin" action="/owner/registration/"',
            "TOP",
            '<form class="form-signin" action="/owner/top/"',
            '<button class="btn btn-lg btn-primary btn-block btn-signin" type="submit"',
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(self.response, test_case)

    # 通常ログイン
    def test_login_normal(self):
        user = Owner.objects.get(username="tester")
        client = Client()
        client.force_login(user)
        response = client.get("/pet/index", follow=True)
        self.assertEqual(len(response.redirect_chain), 1)  # リダイレクトなしのため、要素数1

    # 不正ログイン(ユーザー名,パスワード)
    def test_login_both_abnormal(self):
        user = Owner.objects.get(username="tester")
        user.username = "otherTester"
        user.password = "otherPassword11"
        client = Client()
        client.force_login(user)
        response = client.get("/pet/index", follow=True)

        redirect_pattern = r"/owner/top/.*"
        self.assertTrue(re.match(redirect_pattern, response.redirect_chain[1][0]))

    # 不正ログイン(ユーザー名)
    def test_login_username_abnormal(self):
        user = Owner.objects.get(username="tester")
        user.username = "otherTester"
        client = Client()

        # force_login()では、username誤りでもログイン成功状態になってしまった
        # ⇒login()で解決
        client.login(username=user.username, password=user.password)

        response = client.get("/pet/index", follow=True)
        redirect_pattern = r"/owner/top/.*"
        self.assertTrue(re.match(redirect_pattern, response.redirect_chain[1][0]))

    # 不正ログイン(パスワード)
    def test_login_password_abnormal(self):
        user = Owner.objects.get(username="tester")
        user.password = "otherPassword11"
        client = Client()
        client.login(username=user.username, password=user.password)

        response = client.get("/pet/index", follow=True)
        redirect_pattern = r"/owner/top/.*"
        self.assertTrue(re.match(redirect_pattern, response.redirect_chain[1][0]))


class MypageTest(TestCase):
    def setUp(self) -> None:
        user = Owner.objects.create(
            username="tester",
            password="Test1",
            contact="test@test.co.jp",
            sub_contact="080-1111-1111",
            message="test_message",
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
            owner=user,
        )

    # 初回アクセス
    def test_enter(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        # URLの確認
        url = reverse("owner:mypage")
        self.assertEqual(resolve(url).func, mypage)

        # ステータスコードの確認
        response = self.client.get("/owner/mypage", follow=True)
        self.assertEqual(response.status_code, 200)

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)
        response = self.client.get("/owner/mypage", follow=True)

        message = (
            '<textarea name="message" cols="40" rows="10" id="message" class="owner-message" placeholder="目撃者へのメッセージ" maxlength="1000">'
            + "\n"
            + user.message
        )

        test_case_list = [
            '<i class="fa-solid fa-user fa-3x">',
            '<h2 id="owner-name">' + user.username,
            "連絡先1",
            '<input type="email" name="contact" value="' + user.contact + '"',
            "連絡先2",
            '<input type="text" name="sub_contact" value="' + user.sub_contact + '"',
            "目撃者へのメッセージ",
            message,
            "更新",
            '<input type="submit" class="submit-button" value="更新"',
            '<form method="post" action="/owner/update/"',
            "退会",
            '<input type="submit" class="deleteBtn" value="退会"',
            '<form method="post" action="/owner/delete/"',
            "<small>©Otinu</small>",
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)

    # 通常更新
    def test_registration_normal(self):
        origin_user = Owner.objects.get(username="tester")
        edit_user = Owner.objects.get(username="tester")

        ## 連絡先1更新(30文字)
        edit_user.contact = "newTest" + "t" * 12 + "@test.co.jp"
        edit_user.save()
        edit_user.contact = origin_user.contact

        ## 連絡先2更新(30文字)
        edit_user.sub_contact = "070-2222-2222" + "-" + "9" * 16
        edit_user.save()
        edit_user.sub_contact = origin_user.sub_contact

        ## 目撃者へのメッセージ更新(値変更)
        edit_user.message = "new_test_message"
        edit_user.save()

        ## 目撃者へのメッセージ更新(あり⇒なし)
        edit_user.message = ""
        edit_user.save()

        ## 全更新
        edit_user.contact = "newTest@test.co.jp"
        edit_user.sub_contact = "070-2222-2222"
        edit_user.message = "new_test_message"
        edit_user.save()

    # 異常更新
    def test_registration_abnormal(self):
        data = {
            "contact": "test@test.co.jp",
            "sub_contact": "080-1111-1111",
            "message": "test_message",
        }

        ## 連絡先1(31文字)
        data["contact"] = "t" * 17 + "est@test.co.jp"
        form = MypageForm(data)
        if form.errors is not None:
            self.assertTrue("contact" in form.errors)
        self.assertFalse(form.is_valid())

        ## 連絡先1未入力
        data["contact"] = ""
        form = MypageForm(data)
        if form.errors is not None:
            self.assertTrue("contact" in form.errors)
        self.assertFalse(form.is_valid())

        ## 連絡先2(31文字)
        data["sub_contact"] = "t" * 17 + "est@test.co.jp"
        form = MypageForm(data)
        if form.errors is not None:
            self.assertTrue("sub_contact" in form.errors)
        self.assertFalse(form.is_valid())

        ## 目撃者へのメッセージ(1001文字)
        data["message"] = "t" * 1001
        form = MypageForm(data)
        if form.errors is not None:
            self.assertTrue("message" in form.errors)
        self.assertFalse(form.is_valid())

    # 退会
    def test_resign(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)
        self.client.get("/owner/delete", follow=True)
        response = self.client.get("/pet/index", follow=True)

        ## ログイン制御
        redirect_pattern = r"/owner/top/.*"
        self.assertTrue(re.match(redirect_pattern, response.redirect_chain[1][0]))

        ## データ確認
        try:
            Owner.objects.get(username="tester")
            self.assertTrue(False)
        except Owner.DoesNotExist:
            self.assertTrue(True)

        ## ペットリレーション
        try:
            PetModel.objects.get(pk=999)
            self.assertTrue(False)
        except PetModel.DoesNotExist:
            self.assertTrue(True)


class DetailTest(TestCase):
    def setUp(self) -> None:
        user = Owner.objects.create(
            id=999,
            username="tester",
            password="Test1",
            contact="test@test.co.jp",
            sub_contact="080-1111-1111",
            message="test_message",
        )

        PetModel.objects.create(
            id=999,
            name="testPet",
            age=99,
            sex=True,
            charm_point="test",
            post_cord="9999999",
            address="test",
            image="test_image.png",
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

    # 初回アクセス
    def test_enter(self):
        user = Owner.objects.get(username="tester")
        self.client.force_login(user)

        # URLの確認
        url = reverse("owner:detail", kwargs={"id": 999})
        self.assertEqual(resolve(url).func, detail)

        # ステータスコードの確認
        response = self.client.get("/owner/detail/999", follow=True)
        self.assertEqual(response.status_code, 200)

    # 画面
    def test_layout(self):
        user = Owner.objects.get(username="tester")
        pet = PetModel.objects.get(pk=999)
        other_pet = PetModel.objects.get(pk=1000)
        self.client.force_login(user)
        response = self.client.get("/owner/detail/999", follow=True)

        test_case_list = [
            '<i class="fa-solid fa-user fa-3x"></i>',
            '<h2 id="owner-name">' + user.username,
            '<p id="owner-contact">' + user.contact,
            '<p id="owner-contact">' + user.sub_contact,
            "<textarea readonly>" + user.message,
            '<h2 style="margin: 0;">' + pet.name,
            '<img class="card-img_06" src="/media/' + str(pet.image) + '">',
            '<a id="pet-img" href="/pet/show/' + str(pet.pk) + '"',
            '<h2 style="margin: 0;">' + other_pet.name,
            '<img class="card-img_06" src="/media/' + str(other_pet.image) + '">',
            '<a id="pet-img" href="/pet/show/' + str(other_pet.pk) + '"',
            "<small>©Otinu</small>",
        ]
        for test_case in test_case_list:
            with self.subTest(test_case):
                self.assertContains(response, test_case)
