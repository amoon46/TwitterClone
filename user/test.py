from django.test import TestCase
from django.urls import reverse

from .models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url_home = reverse('user:home')
        self.url_signup = reverse('user:signup')

        self.data = {
            'email': 'test@gmail.com',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }

        self.response_get = self.client.get(self.url_signup)
        self.response_post = self.client.post(self.url_signup, self.data)

    def test_success_get(self):
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'user/signup.html')

    def test_success_post(self):
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

        # ハッシュ化で値が一致しない？
        # self.assertEqual(user_object.password, self.data['password1'])


class TestFailSignUpView(TestCase):
    def setUp(self):
        self.url_home = reverse('user:home')
        self.url_signup = reverse('user:signup')

        self.data_blank = {
            'email': '',
            'password1': '',
            'password2': '',
        }
        self.data_email_empty = {
            'email': '',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }
        self.data_password_empty = {
            'email': 'test@gmail.com',
            'password1': '',
            'password2': '',
        }
        self.data_invalid_email = {
            'email': 'a',
            'password1': 'Hogehoge777',
            'password2': 'Hogehoge777',
        }
        self.data_too_short_password = {
            'email': 'test@gmail.com',
            'password1': 'hoge',
            'password2': 'hoge'
        }
        self.data_similar_to = {
            'email': 'hogehoeg777@gmail.com',
            'password1': 'hogehoge777',
            'password2': 'hogehoge777'
        }
        self.data_only_numbers_password = {
            'email': 'test@gmail.com',
            'password1': '7777777777',
            'password2': '7777777777',
        }
        self.data_not_equal_password = {
            'email': 'test@gmail.com',
            'password1': 'hogehoge777',
            'password2': 'gehogeho777',
        }

        self.response_blank = self.client.post(self.url_signup, self.data_blank)
        self.response_email_empty = self.client.post(self.url_signup, self.data_email_empty)
        self.response_password_empty = self.client.post(self.url_signup, self.data_password_empty)
        self.response_invalid_email = self.client.post(self.url_signup, self.data_invalid_email)

        self.response_too_short_password = self.client.post(
            self.url_signup, self.data_too_short_password
        )

        self.response_similar_to = self.client.post(self.url_signup, self.data_similar_to)

        self.response_only_numbers_password = self.client.post(
            self.url_signup, self.data_only_numbers_password
        )

        self.response_not_equal_password = self.client.post(
            self.url_signup, self.data_not_equal_password
        )

    def test_failure_post_with_empty_form(self):
        self.assertEquals(self.response_blank.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_blank.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_empty_email(self):
        self.assertEquals(self.response_email_empty.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_email_empty.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_empty_password(self):
        self.assertEquals(self.response_password_empty.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_password_empty.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_invalid_email(self):
        self.assertEquals(self.response_invalid_email.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_invalid_email.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_too_short_password(self):
        self.assertEquals(self.response_too_short_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_too_short_password.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_password_similar_to_username(self):
        self.assertEquals(self.response_similar_to.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_similar_to.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_only_numbers_password(self):
        self.assertEquals(self.response_only_numbers_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_only_numbers_password.context.get('form')
        self.assertTrue(form.errors)

    def test_failure_post_with_mismatch_password(self):
        self.assertEquals(self.response_not_equal_password.status_code, 200)

        self.assertFalse(User.objects.exists())

        form = self.response_not_equal_password.context.get('form')
        self.assertTrue(form.errors)


class TestHomeView(TestCase):
    def setUp(self):
        self.url_home = reverse('user:home')

    def test_success_get(self):
        self.response = self.client.get(self.url_home)
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'user/home.html')
