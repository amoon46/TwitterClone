from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import SESSION_KEY

from .models import User


class TestSignUpView(TestCase):
    def setUp(self):
        self.url_home = reverse('twitter:home')
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
        self.assertIn(SESSION_KEY, self.client.session)

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


class TestHomeView(TestCase):
    def setUp(self):
        self.url_home = reverse('twitter:home')
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.login_user = self.client.login(email='test@gmail.com', password='Hogehoge777')

    def test_success_get(self):
        self.response = self.client.get(self.url_home)
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'twitter/home.html')


class TestLoginView(TestCase):
    def setUp(self):
        self.url_login = reverse('user:login')
        self.url_home = reverse('twitter:home')
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')

    def test_success_get(self):
        self.response_get = self.client.get(self.url_login)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'user/login.html')

    def test_success_post(self):
        self.data = {
            'username': 'test@gmail.com',
            'password': 'Hogehoge777',
        }
        self.response_post = self.client.post(self.url_login, self.data)

        self.assertRedirects(
            self.response_post,
            self.url_home,
            status_code=302,
            target_status_code=200
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        self.data = {
            'username': '000@gmail.com',
            'password': 'Hogehoge777',
        }
        self.response_with_not_exists_user = self.client.post(self.url_login, self.data)

        self.assertEquals(self.response_with_not_exists_user.status_code, 200)

        form = self.response_with_not_exists_user.context.get('form')
        self.assertTrue(form.non_field_errors)

        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        self.data = {
            'username': 'test@gmail.com',
            'password': '',
        }
        self.response_with_empty_password = self.client.post(self.url_login, self.data)

        self.assertEquals(self.response_with_empty_password.status_code, 200)

        form = self.response_with_empty_password.context.get('form')
        self.assertTrue(form.non_field_errors)

        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.url_logout = reverse('user:logout')
        self.url_confirm = reverse('user:logout_confirm')
        User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.client.login(email='test@gmail.com', password='Hogehoge777')

    def test_logout_confirm_success_get(self):
        self.response_confirm = self.client.get(self.url_confirm)
        self.assertEqual(self.response_confirm.status_code, 200)

    def test_logout_success_get(self):
        self.response_logout = self.client.get(self.url_logout)
        self.assertEqual(self.response_logout.status_code, 302)

        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProflieView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.url_profile = reverse('user:profile', args=[1])

    def test_success_get(self):
        self.response_get = self.client.get(self.url_profile)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'user/profile.html')


class TestUserProfileEditView(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(
            email='test@gmail.com', password='Hogehoge777'
        )
        self.user_2 = User.objects.create_user(
            email='Hogehoge@gmail.com', password='Hogehoge777'
        )
        self.login_user = self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.url_profile_1 = reverse('user:profile', args=[1])
        self.url_update_1 = reverse('user:profile_update', args=[1])
        self.url_profile_2 = reverse('user:profile', args=[2])
        self.url_update_2 = reverse('user:profile_update', args=[2])
        self.url_profile_none = reverse('user:profile', kwargs={'pk': 99})
        self.url_update_none = reverse('user:profile_update', kwargs={'pk': 99})

    def test_success_get(self):
        self.response_get = self.client.get(self.url_update_1)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'user/profile_update.html')

    def test_success_post(self):
        self.data = {
            'nickname': 'yesman',
            'introduction': 'jimcarrey',
        }
        self.response_post = self.client.post(self.url_update_1, self.data)

        self.assertRedirects(
            self.response_post,
            self.url_profile_1,
            status_code=302,
            target_status_code=200
        )
        user_object = User.objects.get(pk=1)
        self.assertEqual(user_object.nickname, self.data['nickname'])
        self.assertEqual(user_object.introduction, self.data['introduction'])

    def test_failure_post_with_not_exists_user(self):
        self.data = {
            'nickname': 'yesman',
            'introduction': 'jimcarrey',
        }
        response = self.client.get(self.url_update_none)
        self.assertEqual(response.status_code, 404)

    def test_failure_post_with_incorrect_user(self):
        self.data = {
            'nickname': 'yesman',
            'introduction': 'jimcarrey',
        }
        self.response_post_incorrect_user = self.client.post(self.url_update_2, self.data)

        self.assertEqual(self.response_post_incorrect_user.status_code, 403)
        user_object = User.objects.get(pk=2)
        self.assertFalse(user_object.nickname, self.data['nickname'])
        self.assertFalse(user_object.introduction, self.data['introduction'])
