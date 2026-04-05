from django import forms
from .models import Post, Comment, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'cover', 'status', 'categories', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'body':  forms.Textarea(attrs={'class':'form-control','rows':12}),
            'status': forms.Select(attrs={'class':'form-controls'}),
            'categories': forms.CheckboxSelectMultiple(),
            'tags': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ['body']
        widgets = {'body': forms.Textarea(attrs={'class':'form-control','rows':3})}
        labels  = {'body': ''}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model  = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['username','email','first_name','last_name']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = ['avatar','bio','website']