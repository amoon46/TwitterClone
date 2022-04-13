from django import forms
from user.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # widget=forms.PasswordInput パスワードを隠す****
    password1 = forms.CharField(required=False)
    password2 = password1
    # デフォルトのパスワードを1つ削除

    class Meta:
        model = User
        fields = ('email', 'password')
