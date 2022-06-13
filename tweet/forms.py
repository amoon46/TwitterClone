from django.forms import ModelForm
from django.forms.widgets import Textarea
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={'rows': '10', 'placeholder': '130文字であなたの思いの丈を綴ってください'}),
        }
