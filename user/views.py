from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import User
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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/profile_update.html'
    fields = ('nickname', 'introduction')
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user
