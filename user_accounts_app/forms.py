from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='First Name', max_length=10, label_suffix='', required=True)
    last_name = forms.CharField(label='Last Name', max_length=10, label_suffix='', required=True)
    email = forms.CharField(label='Email', max_length=50, label_suffix='', required=False)
    username = forms.CharField(label_suffix='')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label_suffix='')

    class Meta:
        fields = ['username', 'password']
