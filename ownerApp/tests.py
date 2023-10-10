from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve

from ownerApp.views import registration
from ownerApp.forms import OwnerForm

client = Client()
url = reverse("owner:registration")
response = client.get(url)


class RegistrationTest(TestCase):
    # 初回アクセス
    def test_enter(self):
        # URLの確認
        self.assertEqual(resolve(url).func, registration)

        # ステータスコードの確認
        self.assertEqual(response.status_code, 200)

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
                self.assertContains(response, test_case)

    # 通常登録
    def test_registration_normal(self):
        data = {
            "username": "tester",
            "password": "Tttt1",
            "contact": "test@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

        data = {
            "username": "tester2",
            "password": "Tttt2",
            "contact": "test2@sample.jp",
            "mesage": "",
        }
        form = OwnerForm(data)
        self.assertTrue(form.is_valid())

    # 異常登録(Name)
    def test_registration_name_abnormal(self):
        data = {
            "username": "t",
            "password": "Tttt3",
            "contact": "test3@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester444444444444444",
            "password": "Tttt2",
            "contact": "test2@sample.jp",
            "mesage": "",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

    # 異常登録(Password)
    def test_registration_password_abnormal(self):
        data = {
            "username": "tester5",
            "password": "Tt5",
            "contact": "test5@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester5",
            "password": "Tt5",
            "contact": "test5@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester5",
            "password": "Tttt555555555",
            "contact": "test5@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester6",
            "password": "TTTTTTT6",
            "contact": "test6@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester7",
            "password": "ttttttt7",
            "contact": "test7@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester8",
            "password": "Tttttttt",
            "contact": "test8@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester9",
            "password": "99999999",
            "contact": "test9@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester10",
            "password": "",
            "contact": "test10@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

    # 異常登録(Email)
    def test_registration_contact_abnormal(self):
        data = {
            "username": "tester11",
            "password": "Tttt11",
            "contact": "test@test",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester12",
            "password": "Tttt12",
            "contact": "testttttttttttttttttttt@test.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

        data = {
            "username": "tester13",
            "password": "Tttt13",
            "contact": "",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

    # 異常登録(Message)
    def test_registration_message_abnormal(self):
        over_message = "a" * 1001
        data = {
            "username": "tester14",
            "password": "Tttt14",
            "contact": "test14@sample.jp",
            "message": over_message,
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())

    # 異常登録(重複)
    def test_registration_duplicate_abnormal(self):
        data = {
            "username": "tester",
            "password": "Tttt1",
            "contact": "test@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        form.save()
        data = {
            "username": "tester",
            "password": "Tttt15",
            "contact": "test15@sample.jp",
            "mesage": "登録テスト",
        }
        form = OwnerForm(data)
        self.assertFalse(form.is_valid())
