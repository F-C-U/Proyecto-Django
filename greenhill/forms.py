from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "imagen", "consola"]


class PersonaForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[], required=False)
    comuna = forms.ChoiceField(choices=[], required=False)

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].choices = [("0", "Seleccione una región")]
        self.fields["comuna"].choices = [("0", "Seleccione una comuna")]


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class EditarPerfilForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[], required=False)
    comuna = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = Persona
        fields = [
            "correo",
            "telefono",
            "region",
            "comuna",
            "direccion",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].choices = [("0", "Seleccione una región")]
        self.fields["comuna"].choices = [("0", "Seleccione una comuna")]