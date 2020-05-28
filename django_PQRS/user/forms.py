from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control bg-light'

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control bg-light'