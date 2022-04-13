from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import User
from .forms import SignUpForm


class HomeView(TemplateView):
    template_name = "user/home.html"


# Create your views here.
class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    # The form class to instantiate.
    success_url = reverse_lazy('user:home')
    # プロジェクトのURLConf(url.py)が読み込まれる前に、URLの返す
    template_name = 'user/signup.html'
