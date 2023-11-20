from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class":"form-control"}))
    email = forms.CharField(max_length=30,required=True, widget=forms.EmailInput(attrs={"class":"form-control"}))

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={"class":"form-control"}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']
        