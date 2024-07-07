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
    if (
        request.user.is_authenticated
        and Persona.objects.filter(usuario=request.user).exists()
    ):
        persona = get_object_or_404(Persona, usuario=request.user)
        datos = {"persona": persona}
        return render(request, "greenhill/perfil.html", datos)
    else:
        return redirect(to="registrarse")


def editarPerfil(request, id):
    if (
        request.user.is_authenticated
        and Persona.objects.filter(usuario=request.user).exists()
    ):
        persona = get_object_or_404(Persona, id=id)
        data = {"form": PersonaForm(instance=persona)}
        if request.method == "POST":
            formulario = PersonaForm(data=request.POST, instance=persona)
            if formulario.is_valid():
                formulario.save()
                return redirect(to="perfil")
            data["form"] = formulario
        return render(request, "greenhill/editar-perfil.html", data)
    else:
        return redirect(to="index")


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
        region = request.POST.get("region")
        comuna = request.POST.get("comuna")
        request.session["region"] = region
        request.session["comuna"] = comuna
        request.POST._mutable = True
        request.POST["region"] = ""
        request.POST["comuna"] = ""
        if form.is_valid():
            form.instance.usuario = request.user
            form.instance.region = request.session.get("region")
            form.instance.comuna = request.session.get("comuna")
            form.save()
            if "region" in request.session:
                del request.session["region"]
            if "comuna" in request.session:
                del request.session["comuna"]
            return redirect(to="index")
    else:
        form = PersonaForm()
    datos = {"form": form}
    return render(request, "greenhill/registrarse.html", datos)


def carrito(request):
    if (
        request.user.is_authenticated
        and Persona.objects.filter(usuario=request.user).exists()
    ):
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
    elif (
        request.user.is_authenticated
        and not Persona.objects.filter(usuario=request.user).exists()
    ):
        return redirect(to="registrarse")

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
    if (
        request.user.is_authenticated
        and Persona.objects.filter(usuario=request.user).exists()
    ):
        persona = get_object_or_404(Persona, usuario=request.user)
        pedidos = Pedido.objects.filter(persona=persona)
        datos = {"pedidos": pedidos}
        print(datos)
        return render(request, "greenhill/pedidos.html", datos)
    elif (
        request.user.is_authenticated
        and not Persona.objects.filter(usuario=request.user).exists()
    ):
        return redirect(to="registrarse")
    else:
        return redirect(to="login")


def pedido(request, id):
    if (
        request.user.is_authenticated
        and Persona.objects.filter(usuario=request.user).exists()
    ):
        pedido = get_object_or_404(Pedido, id=id)
        datos = {"pedido": pedido}
        return render(request, "greenhill/detalle-pedido.html", datos)
    elif (
        request.user.is_authenticated
        and not Persona.objects.filter(usuario=request.user).exists()
    ):
        return redirect(to="registrarse")


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


def cambiar_estado_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado")
        pedido.estado = nuevo_estado
        pedido.save()
        return redirect("pedidos")

    return redirect("pedidos")


def bloquear_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = False
    usuario.save()
    return redirect("usuarios")


def desbloquear_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    usuario.is_active = True
    usuario.save()
    return redirect("usuarios")
