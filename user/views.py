from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from .forms import SignUpForm


class HomeView(TemplateView):
    template_name = "user/home.html"


class SignUpView(CreateView):

    # The form class to instantiate.
    form_class = SignUpForm

    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLを返す
    success_url = reverse_lazy('user:home')
    template_name = 'user/signup.html'
