# Formulario para registro de usuarios
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormRegistro(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
