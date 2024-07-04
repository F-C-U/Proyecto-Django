import re
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, "greenhill/index.html")


def adminAgregar(request):
    if request.user.is_authenticated and request.user.is_superuser:
        form = ProductoForm()
        if request.method == "POST":
            form = ProductoForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("admin-agregar")
        else:
            form = ProductoForm()
        datos = {"form": form}
        return render(request, "greenhill/admin-agregar-producto.html", datos)
    else:
        return redirect(to="index")


def catalogo(request):
    productos = Producto.objects.all()
    datos = {"productos": productos}
    return render(request, "greenhill/catalogo.html", datos)


def producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    datos = {"producto": producto}
    return render(request, "greenhill/producto.html", datos)


def paginaProductos(request):
    productos = Producto.objects.all()
    datos = {"productos": productos}
    return render(request, "greenhill/admin-productos.html", datos)


def editarProductos(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        producto = get_object_or_404(Producto, id=id)
        data = {"form": ProductoForm(instance=producto)}
        if request.method == "POST":
            formulario = ProductoForm(
                data=request.POST, instance=producto, files=request.FILES
            )
            if formulario.is_valid():
                formulario.save()
                return redirect(to="admin-productos")
            data["form"] = formulario
        return render(request, "greenhill/admin-modificar-producto.html", data)
    else:
        return redirect(to="index")


def eliminarProductos(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        return redirect(to="admin-productos")
    else:
        return redirect(to="index")


def perfil(request):
    if request.user.is_authenticated:
        persona = get_object_or_404(Persona, usuario=request.user)
        datos = {"persona": persona}
        return render(request, "greenhill/perfil.html",datos)


def pago(request):
    return render(request, "greenhill/pago.html")


def usuarios(request):
    if request.user.is_authenticated and request.user.is_superuser:
        usuarios = Persona.objects.all()
        datos = {"usuarios": usuarios}
        return render(request, "greenhill/admin-usuarios.html", datos)
    else:
        return redirect(to="index")


def eliminarUsuario(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        usuario = get_object_or_404(Persona, id=id)
        usuario.delete()
        return redirect(to="usuarios")
    else:
        return redirect(to="index")


def registroUser(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect(to="registrarse")
    else:
        form = RegistroForm()
    datos = {"form": form}
    return render(request, "greenhill/usr-registro.html", datos)


def registro(request):
    if request.method == "POST":
        form = PersonaForm(request.POST)
        form.instance = form.instance.region
        if form.is_valid():
            form.instance.usuario = request.user
            form.save()
            return redirect(to="index")
    else:
        form = PersonaForm()
    datos = {"form": form}
    return render(request, "greenhill/registrarse.html", datos)


def carrito(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(
            id=request.session.get("carrito_id")
        )
        items = CarritoItem.objects.filter(carrito=carrito)
        precio_total = sum(item.producto.precio * item.cantidad for item in items)
        return render(
            request,
            "greenhill/carrito.html",
            {"carrito": carrito, "items": items, "precio_total": precio_total},
        )
    else:
        return redirect(to="login")


def agregarCarrito(request, id):
    producto = get_object_or_404(Producto, id=id)
    carrito, creado = Carrito.objects.get_or_create(
        id=request.session.get("carrito_id")
    )
    carrito_item, creado = CarritoItem.objects.get_or_create(
        carrito=carrito, producto=producto
    )
    if not creado:
        carrito_item.cantidad += 1
    carrito_item.save()
    request.session["carrito_id"] = carrito.id
    return redirect(to="carrito")


def quitarCarrito(request, id):
    carrito_item = get_object_or_404(CarritoItem, id=id)
    carrito_item.delete()
    return redirect(to="carrito")


def adminPedidos(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pedidos = Pedido.objects.all()
        datos = {"pedidos": pedidos}
        return render(request, "greenhill/admin-pedidos.html", datos)
    else:
        return redirect(to="index")


def pedidos(request):
    if request.user.is_authenticated:
        persona = get_object_or_404(Persona, usuario=request.user)
        pedidos = Pedido.objects.filter(persona=persona)
        datos = {"pedidos": pedidos}
        print(datos)
        return render(request, "greenhill/pedidos.html", datos)
    else:
        return redirect(to="login")


def pedido(request, id):
    if request.user.is_authenticated:
        pedido = get_object_or_404(Pedido, id=id)
        datos = {"pedido": pedido}
        return render(request, "greenhill/detalle-pedido.html", datos)
    else:
        return redirect(to="login")


def crearPedido(request):
    carrito = get_object_or_404(Carrito, id=request.session.get("carrito_id"))
    persona = get_object_or_404(Persona, usuario=request.user)
    if not CarritoItem.objects.filter(carrito=carrito).exists():
        return HttpResponse("No hay productos en el carrito", 400)
    total = sum(
        item.producto.precio * item.cantidad
        for item in CarritoItem.objects.filter(carrito=carrito)
    )
    pedido = Pedido.objects.create(carrito=carrito, persona=persona, total=total)
    del request.session["carrito_id"]
    return redirect(to="pedidos")
