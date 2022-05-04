from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate

from .forms import SignUpForm, LoginForm


class SignUpView(CreateView):

    # The form class to instantiate.
    form_class = SignUpForm

    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLを返す
    success_url = reverse_lazy('twitter:home')
    template_name = 'user/signup.html'

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):  # 追記
        response = super().form_valid(form)
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return response


class Login(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'

    def form_valid(self, form):
        print("ログインしました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("ログインに失敗しました。")
        return super().form_invalid(form)


class LogoutConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'user/logout_confirm.html'


class ProfileDisplay(TemplateView):
    template_name = 'user/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user/profile_update.html'
    fields = ('nickname', 'introduction')
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        self.kwargs['pk'] = self.request.user.pk
        return super().get_object()
