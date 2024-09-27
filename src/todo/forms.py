from django.contrib.auth.forms import UserCreationForm
from django import forms

from todo.models import CustomUser, Todo


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'details')