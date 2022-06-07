from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
import json
import time


from user.models import User
from .models import Post


class HomeView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        time.sleep(0.1)
        self.post2 = Post.objects.create(text='別の人がテストを試しています。', user=self.user2)
        self.url_home = reverse('tweet:top')

    def test_success_get_tweet(self):
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.response_get = self.client.get(self.url_home)
        self.assertContains(self.response_get, self.post.text)
        self.assertContains(self.response_get, self.post2.text)
        self.assertQuerysetEqual(
            self.response_get.context['post_list'],
            ['<Post: 別の人がテストを試しています。>', '<Post: テストを試しています。>'],
            ordered=True,
        )


class UserProfiileView(TestCase):
    def setUp(self):
        # ツイート
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.user3 = User.objects.create_user(email='ho@gmail.com', password='Hogehoge777')
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        time.sleep(0.1)
        self.post2 = Post.objects.create(text='別の人がテストを試しています。', user=self.user2)
        time.sleep(0.1)
        self.post3 = Post.objects.create(text='user1がテストしています', user=self.user1)
        # フォロー数
        self.url_profile1 = reverse('user:profile', kwargs={'pk': self.user1.pk})
        self.url_following = reverse('tweet:following_list', kwargs={'pk': self.user1.pk})
        self.url_followers = reverse('tweet:followers_list', kwargs={'pk': self.user1.pk})
        self.url_post_follow3 = reverse('tweet:follow',  kwargs={'pk': self.user3.pk})
        self.url_post_follow2 = reverse('tweet:follow',  kwargs={'pk': self.user2.pk})
        self.url_post_follow1 = reverse('tweet:follow',  kwargs={'pk': self.user1.pk})

    def test_success_get_tweet(self):
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.response_get = self.client.get(self.url_profile1)

        self.assertContains(self.response_get, self.post.text)
        self.assertContains(self.response_get, self.post3.text)

        self.assertQuerysetEqual(
            self.response_get.context['post'],
            ['<Post: user1がテストしています>', '<Post: テストを試しています。>'],
            ordered=True,
        )

    def test_success_get_follow(self):
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.client.post(self.url_post_follow1)
        self.client.post(self.url_post_follow3)
        self.client.logout()
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.client.post(self.url_post_follow2)
        self.client.post(self.url_post_follow3)
        self.response_get_following = self.client.get(self.url_following)
        following_count = self.response_get_following.context['following'].all().count()
        self.assertEqual(following_count, 2)
        self.response_get_followers = self.client.get(self.url_followers)
        following_count = self.response_get_followers.context['followers'].all().count()
        self.assertEqual(following_count, 1)


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


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_profile = reverse('user:profile', kwargs={'pk': self.user1.pk})
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        self.url_post_detail = reverse('tweet:post_detail', kwargs={'pk': self.post.pk})

    def test_success_get(self):
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.response_get = self.client.get(self.url_post_detail)
        self.assertEquals(self.response_get.status_code, 200)
        self.assertTemplateUsed(self.response_get, 'tweet/post_detail.html')
        self.assertContains(self.response_get, self.post.text)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_home = reverse('tweet:top')
        self.url_profile = reverse('user:profile', kwargs={'pk': self.user1.pk})
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        self.assertTrue(Post.objects.exists())

    def test_success_post(self):
        self.url_post_delete = reverse('tweet:post_delete', kwargs={'pk': self.post.pk})
        self.response_delete = self.client.post(self.url_post_delete)
        self.assertRedirects(
            self.response_delete,
            self.url_profile,
            status_code=302,
            target_status_code=200
        )
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 0)

    def test_failure_post_with_not_exist_tweet(self):
        self.url_post_delete = reverse('tweet:post_delete', args=[99])
        self.response_delete = self.client.get(self.url_post_delete)
        self.assertEqual(self.response_delete.status_code, 404)
        self.assertTrue(Post.objects.exists())

    def test_failure_post_with_incorrect_user(self):
        self.client.logout()
        self.client.login(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_post_delete = reverse('tweet:post_delete', kwargs={'pk': self.post.pk})
        self.response_delete = self.client.post(self.url_post_delete)
        self.assertEqual(self.response_delete.status_code, 403)
        messages = list(get_messages(self.response_delete.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, 'This user is not login user')


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_profile2 = reverse('user:profile', kwargs={'pk': self.user2.pk})
        self.url_post_follow2 = reverse('tweet:follow',  kwargs={'pk': self.user2.pk})
        self.url_post_follow1 = reverse('tweet:follow',  kwargs={'pk': self.user1.pk})
        self.client.login(email='test@gmail.com', password='Hogehoge777')

    def test_success_post(self):
        self.response_follow = self.client.post(self.url_post_follow2)
        self.assertRedirects(
            self.response_follow,
            self.url_profile2,
            status_code=302,
            target_status_code=200
        )
        self.assertTrue(User.objects.filter(
            followees=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        self.url_post_follow99 = reverse('tweet:follow', args=[99])
        self.response_follow = self.client.post(self.url_post_follow99)
        self.assertEqual(self.response_follow.status_code, 404)

        following_count = self.user1.followees.all().count()
        self.assertEqual(following_count, 0)

    def test_failure_post_with_self(self):
        self.response_follow = self.client.post(self.url_post_follow1)
        self.assertEqual(self.response_follow.status_code, 403)
        self.assertFalse(User.objects.filter(
            followees=self.user1).exists())
        messages = list(get_messages(self.response_follow.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, 'you can not follow yourself')


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.user2 = User.objects.create_user(email='hogehoge@gmail.com', password='Hogehoge777')
        self.url_profile2 = reverse('user:profile', kwargs={'pk': self.user2.pk})
        self.url_post_follow2 = reverse('tweet:follow',  kwargs={'pk': self.user2.pk})
        self.url_post_follow1 = reverse('tweet:follow',  kwargs={'pk': self.user1.pk})
        self.url_post_unfollow2 = reverse('tweet:unfollow',  kwargs={'pk': self.user2.pk})
        self.url_post_unfollow1 = reverse('tweet:unfollow',  kwargs={'pk': self.user1.pk})
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        self.client.post(self.url_post_follow2)
        self.assertTrue(User.objects.filter(
            followees=self.user2).exists())

    def test_success_post(self):
        self.response_unfollow = self.client.post(self.url_post_unfollow2)
        self.assertRedirects(
            self.response_unfollow,
            self.url_profile2,
            status_code=302,
            target_status_code=200
        )
        self.assertFalse(User.objects.filter(
            followees=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        self.url_post_unfollow99 = reverse('tweet:unfollow', args=[99])
        self.response_unfollow = self.client.post(self.url_post_unfollow99)
        self.assertEqual(self.response_unfollow.status_code, 404)
        following_count = self.user1.followees.all().count()
        self.assertEqual(following_count, 1)
        self.assertTrue(User.objects.filter(
            followees=self.user2).exists())

    def test_failure_post_with_self(self):
        self.response_unfollow = self.client.post(self.url_post_unfollow1)
        self.assertEqual(self.response_unfollow.status_code, 403)
        self.assertFalse(User.objects.filter(
            followees=self.user1).exists())
        messages = list(get_messages(self.response_unfollow.wsgi_request))
        message = str(messages[0])
        self.assertEqual(message, 'you can not unfollow yourself')


class TestFavoriteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        self.url_like = reverse('tweet:like', kwargs={'pk': self.post.pk})
        self.url_like_none = reverse('tweet:like', args=[99])
        self.url_home = reverse('tweet:top')
        self.client.login(email='test@gmail.com', password='Hogehoge777')

    def test_success_post(self):
        response = self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['likes_count'], 1)
        self.assertEqual(json.loads(response.content)['liked'], True)

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(self.url_like_none, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        likes_count = self.post.like.all().count()
        self.assertEqual(likes_count, 0)

    def test_failure_post_with_favorited_tweet(self):
        self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        time.sleep(0.1)
        response = self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['likes_count'], 1)
        self.assertEqual(json.loads(response.content)['liked'], True)


class TestUnFavoriteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='test@gmail.com', password='Hogehoge777')
        self.post = Post.objects.create(text='テストを試しています。', user=self.user1)
        self.url_like = reverse('tweet:like', kwargs={'pk': self.post.pk})
        self.url_unlike = reverse('tweet:unlike', kwargs={'pk': self.post.pk})
        self.url_unlike_none = reverse('tweet:unlike', args=[99])
        self.client.login(email='test@gmail.com', password='Hogehoge777')
        response = self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(json.loads(response.content)['likes_count'], 1)
        self.assertEqual(json.loads(response.content)['liked'], True)

    def test_success_post(self):
        response = self.client.post(self.url_unlike, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['likes_count'], 0)
        self.assertEqual(json.loads(response.content)['liked'], False)

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(self.url_unlike_none, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
        likes_count = self.post.like.all().count()
        self.assertEqual(likes_count, 1)

    def test_failure_post_with_unfavorited_tweet(self):
        self.client.post(self.url_unlike, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        time.sleep(0.1)
        response = self.client.post(self.url_like, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
