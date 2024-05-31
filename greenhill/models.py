from django.db import models

# Create your models here.

class Persona(models.Model):
    rut = models.CharField(max_length=13)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField(max_length=9)
    region = models.IntegerChoices()
    comuna = models.IntegerChoices()
    direccion = models.CharField(max_length=100)
    pass1 = models.CharField(max_length=16)
    pass2 = models.CharField(max_length=16)
