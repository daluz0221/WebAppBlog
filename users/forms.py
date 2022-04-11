from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegister."""


    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    password2 = forms.CharField(label='Repetir Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


    class Meta:
        """Meta definition for UserRegisterform."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',   
        )

    def clean_password2(self):
        """confirmar que las dos contraseñas coincidan."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2



class LoginForm(forms.Form):
    """Formulario para el Login."""

    username = forms.CharField(label='Nombre de usuario', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))

    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))


    def clean(self):
        """Validar que el usuario exist"""
        cleaned_data = super(LoginForm, self).clean()
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Usuario o contraseña incorrectos")

        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña actual'}))

    password2 = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña nueva'}))

    # def clean_password2(self):
    #     """confirmar que las dos contraseñas coincidan."""
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Las contraseñas no coinciden")
    #     return password2

class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)


    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificamos si el codigo y el id de usuario son validos:
            activo = User.objects.code_validator(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('el codigo es incorrecto')
        else:
            raise forms.ValidationError('el codigo es incorrecto')


