from django import forms
from blog.models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class Postform(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author','title','text')

       
        
class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields= ('author','text')

class RegForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()

       