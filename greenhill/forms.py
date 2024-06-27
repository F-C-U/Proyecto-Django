from django import forms
from .models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'consola']

class PersonaForm(forms.ModelForm):
    region = forms.ChoiceField(choices=[(0,'--Region--')])
    comuna = forms.ChoiceField(choices=[(0,'--Comuna--')])
    pass1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder':'Contraseña'}))
    pass2 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'placeholder':'Repetir Contraseña'}))
    class Meta:
        model = Persona
        fields = ['rut', 'nombre', 'apellido', 'correo', 'telefono', 'region','comuna', 'direccion', 'pass1', 'pass2']