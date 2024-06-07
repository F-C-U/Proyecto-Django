from django.db import models

# Create your models here.

class Persona(models.Model):
    rut = models.CharField(max_length=13)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=100)
    pass1 = models.CharField(max_length=16)
    pass2 = models.CharField(max_length=16)

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos', null=True)

class Pedido(models.Model):
    fecha = models.DateField()
    total = models.IntegerField()
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

