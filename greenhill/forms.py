from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "imagen", "consola"]


class PersonaForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[])
    comuna = forms.ChoiceField(choices=[])

    class Meta:
        model = Persona
        fields = [
            "rut",
            "nombre",
            "apellido",
            "correo",
            "telefono",
            "region",
            "comuna",
            "direccion",
        ]


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
