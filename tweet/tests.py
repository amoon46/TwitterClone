from django.test import TestCase
from django.urls import reverse


from user.models import User
from .models import Post


class HomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_post_create = reverse('tweet:post_create')
        self.data1 = {
            'text': 'test1。',
        }
        self.data2 = {
            'text': 'test2',
        }
        self.data3 = {
            'text': 'test3',
        }

    def test_success_get(self):
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.response_post1 = self.client.post(self.url_post_create, self.data1)
        self.assertTrue(Post.objects.exists())

        post_object = Post.objects.get(pk=1)
        self.assertEqual(post_object.text, self.data1['text'])


class UserProfiileView(TestCase):
    pass


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_post_create = reverse('tweet:post_create')

    def test_success_get(self):
        self.response_get = self.client.get(self.url_post_create)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'tweet/post_create.html')

    def test_success_post(self):
        self.data = {
            'text': 'テストを試しています。',
        }
        self.response_post = self.client.post(self.url_post_create, self.data)
        self.assertRedirects(
            self.response_post,
            self.url_home,
            status_code=302,
            target_status_code=200
        )

        self.assertTrue(Post.objects.exists())

        post_object = Post.objects.get(pk=1)
        self.assertEqual(post_object.text, self.data['text'])

    def test_failure_post_with_empty_content(self):
        self.data_blank = {
            'text': '',
        }
        self.response_blank = self.client.post(self.url_post_create, self.data_blank)

        self.assertEquals(self.response_blank.status_code, 200)

        self.assertFalse(Post.objects.exists())

        form = self.response_blank.context.get('form')
        self.assertTrue(form.errors['text'])

    def test_failure_post_with_too_long_content(self):
        self.data_too_long = {
            'text':
            '130文字まではtextを書くことができるため長々とどうでもいい文章を書いていく。書くことがない。親譲りの無鉄砲で子供の時から損ばかりしている。小学校に居る時分学校の2階から飛び降りて一週間ほど腰を抜かしたことがある。まだまだ書かないと130文字に辿りつかない。',
        }
        self.response_too_long = self.client.post(self.url_post_create, self.data_too_long)

        self.assertEquals(self.response_too_long.status_code, 200)

        self.assertFalse(Post.objects.exists())

        form = self.response_too_long.context.get('form')
        self.assertTrue(form.errors['text'])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_profile = reverse('user:profile', args=[1])
        self.url_post_create = reverse('tweet:post_create')
        self.data = {
            'text': 'テストを試しています。',
        }

    def test_success_post(self):
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.response_post = self.client.post(self.url_post_create, self.data)
        self.assertRedirects(
            self.response_post,
            self.url_home,
            status_code=302,
            target_status_code=200
        )

        post_object = Post.objects.get(pk=1)
        self.assertEqual(post_object.text, self.data['text'])

        self.url_post_delete = reverse('tweet:post_delete', args=[1])
        self.response_delete = self.client.post(self.url_post_delete)
        self.assertRedirects(
            self.response_delete,
            self.url_profile,
            status_code=302,
            target_status_code=200
        )

    def test_failure_post_with_not_exist_tweet(self):
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.url_post_delete = reverse('tweet:post_delete', args=[99])
        self.response_delete = self.client.get(self.url_post_delete)
        self.assertEqual(self.response_delete.status_code, 404)

    def test_failure_post_with_incorrect_user(self):
        # 新しい投稿
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.response_post = self.client.post(self.url_post_create, self.data)
        post_object = Post.objects.get(pk=1)
        self.assertEqual(post_object.text, self.data['text'])

        # 別のユーザーで削除
        self.client.logout()
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.url_post_delete = reverse('tweet:post_delete', args=[1])
        self.response_delete = self.client.post(self.url_post_delete)
        self.assertEqual(self.response_delete.status_code, 403)


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_profile1 = reverse('user:profile', kwargs={'pk': self.user1.pk})
        self.url_profile2 = reverse('user:profile', kwargs={'pk': self.user2.pk})
        self.url_post_follow1 = reverse('tweet:follow',  kwargs={'pk': self.user1.pk})
        self.url_post_follow2 = reverse('tweet:follow',  kwargs={'pk': self.user2.pk})

    def test_success_post(self):
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        response = self.client.post(self.url_post_follow2)
        self.assertEqual(response.status_code, 302)

        """
            self.assertRedirects(
            self.response_follow,
            self.url_profile,
            status_code=302,
            target_status_code=200
            )
        """

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


"""
class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
"""


class TestFavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user = User.objects.create_user(email='@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_post_create = reverse('tweet:post_create')

    def test_success_get(self):
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.data = {
            'text': 'テストを試しています。',
        }
        self.response_post = self.client.post(self.url_post_create, self.data)
        post_object = Post.objects.get(pk=1)
        self.assertEqual(post_object.text, self.data['text'])

        self.url_follow = reverse('tweet:like_home', args=[1])

        self.response_follow = self.client.get(self.url_follow)
        # self.assertEquals(self.response_follow.status_code, 200)


class TestUnFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
