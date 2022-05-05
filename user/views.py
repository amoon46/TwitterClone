from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import login

from .forms import SignUpForm, LoginForm


class SignUpView(CreateView):

    # The form class to instantiate.
    form_class = SignUpForm

    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLを返す
    success_url = reverse_lazy('twitter:home')
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


class ProfileDisplay(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = False     # set True if raise 403_Forbidden

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class ProfileUpdateView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/profile_update.html'
    fields = ('nickname', 'introduction')
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
