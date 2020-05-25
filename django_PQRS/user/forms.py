from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ('email', 'password')
