from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


from .forms import PostForm
from .models import Post
from user.models import User


class TopView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'tweet/top.html'
    paginate_by = 25

    def get_queryset(self):
        return Post.objects.all().select_related('user').prefetch_related('like')


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'tweet/post_create.html'
    success_url = reverse_lazy('tweet:top')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'tweet/post_detail.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk)
        if (post.user != self.request.user):
            messages.warning(self.request, 'This user is not login user')
        return post.user == self.request.user


class UpdatePost(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    model = Post
    template_name = 'tweet/post_update.html'
    fields = ['text']

    def get_success_url(self):
        pk_post = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk_post)
        pk_user = post.user.pk
        return reverse_lazy('user:profile', kwargs={"pk": pk_user})


class DeletePost(LoginRequiredMixin, OnlyYouMixin, DeleteView):
    model = Post
    template_name = 'tweet/post_delete.html'

    def get_success_url(self):
        pk_post = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=pk_post)
        pk_user = post.user.pk
        return reverse_lazy('user:profile', kwargs={"pk": pk_user})


###############################################################
# like


class Like(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if self.request.user in post.like.all():
            pass
        else:
            post.like.add(self.request.user)
        likes_count = post.like.count()
        liked = True
        context = {
            'post_pk': post.pk,
            'likes_count': likes_count,
            'liked': liked,
        }
        return JsonResponse(context)


class UnLike(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=pk)
        if self.request.user in post.like.all():
            post.like.remove(self.request.user)
        likes_count = post.like.count()
        liked = False
        context = {
            'post_pk': post.pk,
            'likes_count': likes_count,
            'liked': liked,
        }
        return JsonResponse(context)


###############################################################
# follow


class UserFollow(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        login_user = self.request.user
        user = get_object_or_404(User, pk=pk)
        followees = login_user.followees.all()

        if ((user != login_user) and (user != 404)):
            if user in followees:
                pass
            else:
                login_user.followees.add(user)
        elif (user == 404):
            messages.warning(request, 'This user do not exist')
        else:
            messages.warning(request, 'you can not follow yourself')
            raise PermissionDenied()
        return redirect('user:profile', pk)


class UserUnFollow(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        pk = self.kwargs['pk']
        login_user = self.request.user
        user = get_object_or_404(User, pk=pk)
        followees = login_user.followees.all()

        if (user != login_user):
            if user in followees:
                login_user.followees.remove(user)
            else:
                pass
        else:
            messages.warning(request, 'you can not unfollow yourself')
            raise PermissionDenied()
        return redirect('user:profile', pk)


class UserFollowingList(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'tweet/following_list.html'

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        context = super().get_context_data(*args, **kwargs)
        context['following'] = user.followees.all()
        return context


class UserFollowersList(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'tweet/followers_list.html'

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        context = super().get_context_data(*args, **kwargs)
        context['followers'] = User.objects.filter(followees=user)
        return context
