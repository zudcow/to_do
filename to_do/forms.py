from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields= ('username', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    class Meta:
        model = User
        fields = ('username', 'password')
