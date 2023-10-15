import re
from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve

from ownerApp.views import registration, login_func
from ownerApp.forms import OwnerForm
from ownerApp.models import Owner


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
