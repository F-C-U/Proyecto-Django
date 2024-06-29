from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Persona(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rut = models.CharField(max_length=13)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField()
    region = models.CharField(max_length=200, default=None)
    comuna = models.CharField(max_length=200, default=None)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.apellido}"


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(blank=True, null=True, max_length=100)
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="productos", blank=True, null=True)
    consola = models.CharField(
        choices=[
            ("Xbox", "Xbox"),
            ("Playstation", "Playstation"),
            ("Nintendo Switch", "Nintendo Switch"),
        ],
        max_length=50,
    )

    def __str__(self):
        return f"{self.nombre}"


class Carrito(models.Model):
    crado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto}"


class Pedido(models.Model):
    carrito = models.OneToOneField(Carrito, on_delete=models.CASCADE, default=None)
    fecha = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    estado = models.CharField(
        choices=[
            ("Pendiente", "Pendiente"),
            ("En proceso", "En proceso"),
            ("Enviado", "Enviado"),
            ("Entregado", "Entregado"),
            ("Cancelado", "Cancelado"),
        ],
        max_length=50,
        default="Pendiente",
    )
    total = models.PositiveIntegerField()
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fecha} - {self.total} - {self.estado} - {self.persona}"
