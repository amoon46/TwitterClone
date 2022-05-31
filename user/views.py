from django.views.generic import TemplateView, CreateView, UpdateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import User
from tweet.models import Post
from .forms import SignUpForm, LoginForm


class SignUpView(CreateView):

    # The form class to instantiate.
    form_class = SignUpForm

    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLを返す
    success_url = reverse_lazy('tweet:top')
    template_name = 'user/signup.html'

    def form_valid(self, form):  # 追記
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'


class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'user/logout_confirm.html'


class ProfileDisplay(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/profile.html'

    def get_context_data(self, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User, pk=pk)
        context = super().get_context_data(*args, **kwargs)
        context['post'] = Post.objects.filter(user=user).select_related('user').prefetch_related('like')
        context['followers'] = User.objects.filter(followees=user)

        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user/profile_update.html'
    fields = ('nickname', 'introduction')

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse_lazy('user:profile', kwargs={"pk": pk})

    def test_func(self):
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        return user == self.request.user
