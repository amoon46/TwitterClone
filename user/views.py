from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import SignUpForm


class SignUpView(CreateView):

    # The form class to instantiate.
    form_class = SignUpForm

    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLを返す
    success_url = reverse_lazy('home')
    template_name = 'user/signup.html'
