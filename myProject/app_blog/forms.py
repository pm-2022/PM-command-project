from django import forms
from django.contrib.auth.forms import User, UserCreationForm
from .models import Article, ArticleImage


class ArticleImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={"multiple": True}))

    class Meta:
        model = ArticleImage
        fields = ["image", "title"]
        labels = {
            "title": "Image caption"
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "description", "main_page", "category"]
        labels = {
            "title": "Article title"
        }
