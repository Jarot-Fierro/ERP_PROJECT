from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de Usaurio',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escribir nombre de usuario'

            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Escribir su contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = ['username', 'password']
