from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'consola']

class PersonaForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[])
    comuna = forms.ChoiceField(choices=[])
    class Meta:

        model = Persona
        fields = ['rut', 'nombre', 'apellido', 'correo', 'telefono', 'region','comuna', 'direccion', 'pass1', 'pass2']