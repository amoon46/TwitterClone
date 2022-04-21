from django.test import TestCase
from django.urls import reverse, resolve

from user.models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url_home = reverse('home')
        self.url_signup = reverse('user:signup')

    def test_success_get(self):
        self.response_get = self.client.get(self.url_signup)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'user/signup.html')

    def test_success_post(self):

        self.data = {
            'email': 'test@gmail.com',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }
        self.response_post = self.client.post(self.url_signup, self.data)
        self.assertRedirects(
            self.response_post,
            self.url_home,
            status_code=302,
            target_status_code=200
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        user_object = User.objects.get(pk=1)
        self.assertEqual(user_object.email, self.data['email'])


class TestFailSignUpView(TestCase):
    def setUp(self):
        self.url_home = reverse('home')
        self.url_signup = reverse('user:signup')

    def test_failure_post_with_empty_form(self):
        self.data_blank = {
            'email': '',
            'password1': '',
            'password2': '',
        }
        self.response_blank = self.client.post(self.url_signup, self.data_blank)

        self.assertEquals(self.response_blank.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_blank.context.get('form')
        self.assertTrue(form.errors['email'])
        self.assertTrue(form.errors['password1'])
        self.assertTrue(form.errors['password2'])

    def test_failure_post_with_empty_email(self):

        self.data_email_empty = {
            'email': '',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }
        self.response_email_empty = self.client.post(self.url_signup, self.data_email_empty)

        self.assertEquals(self.response_email_empty.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_email_empty.context.get('form')
        self.assertTrue(form.errors['email'])

    def test_failure_post_with_empty_password(self):

        self.data_password_empty = {
            'email': 'test@gmail.com',
            'password1': '',
            'password2': '',
        }
        self.response_password_empty = self.client.post(self.url_signup, self.data_password_empty)

        self.assertEquals(self.response_password_empty.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_password_empty.context.get('form')
        self.assertTrue(form.errors['password1'])
        self.assertTrue(form.errors['password2'])

    def test_failure_post_with_invalid_email(self):

        self.data_invalid_email = {
            'email': 'a',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }

        self.response_invalid_email = self.client.post(self.url_signup, self.data_invalid_email)

        self.assertEquals(self.response_invalid_email.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_invalid_email.context.get('form')
        self.assertTrue(form.errors['email'])

    def test_failure_post_with_too_short_password(self):
        self.data_too_short_password = {
            'email': 'test@gmail.com',
            'password1': 'hoge',
            'password2': 'hoge'
        }
        self.response_too_short_password = self.client.post(
            self.url_signup, self.data_too_short_password
        )
        self.assertEquals(self.response_too_short_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_too_short_password.context.get('form')
        self.assertTrue(form.errors['password2'])
        self.assertTrue(
            'このパスワードは短すぎます。最低 8 文字以上必要です。' in form.errors['password2']
        )

    def test_failure_post_with_password_similar_to_username(self):
        self.data_similar_to = {
            'email': 'hogehoeg777@gmail.com',
            'password1': 'hogehoge777',
            'password2': 'hogehoge777'
        }
        self.response_similar_to = self.client.post(self.url_signup, self.data_similar_to)

        self.assertEquals(self.response_similar_to.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_similar_to.context.get('form')
        self.assertTrue(form.errors['password2'])
        self.assertTrue(
            'このパスワードは email address と似すぎています。' in form.errors['password2']
        )

    def test_failure_post_with_only_numbers_password(self):
        self.data_only_numbers_password = {
            'email': 'test@gmail.com',
            'password1': '7777777777',
            'password2': '7777777777',
        }
        self.response_only_numbers_password = self.client.post(
            self.url_signup, self.data_only_numbers_password
        )
        self.assertEquals(self.response_only_numbers_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_only_numbers_password.context.get('form')
        self.assertTrue(form.errors['password2'])
        self.assertTrue(
            'このパスワードは数字しか使われていません。' in form.errors['password2']
        )

    def test_failure_post_with_mismatch_password(self):
        self.data_not_equal_password = {
            'email': 'test@gmail.com',
            'password1': 'hogehoge777',
            'password2': 'gehogeho777',
        }

        self.response_not_equal_password = self.client.post(
            self.url_signup, self.data_not_equal_password
        )
        self.assertEquals(self.response_not_equal_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_not_equal_password.context.get('form')
        self.assertTrue(form.errors['password2'])
        self.assertTrue(
            '確認用パスワードが一致しません。' in form.errors['password2']
        )
        print(form.errors)


class TestHomeView(TestCase):
    def setUp(self):
        self.url_home = reverse('home')

    def test_success_get(self):
        self.response = self.client.get(self.url_home)
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')
