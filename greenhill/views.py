import re
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, "greenhill/index.html")


def adminAgregar(request):
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


def eliminarProductos(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect(to="admin-productos")


def perfil(request):
    return render(request, "greenhill/perfil.html")


def pago(request):
    return render(request, "greenhill/pago.html")


def usuarios(request):
    usuarios = Persona.objects.all()
    datos = {"usuarios": usuarios}
    return render(request, "greenhill/admin-usuarios.html", datos)


def eliminarUsuario(request, id):
    usuario = get_object_or_404(Persona, id=id)
    usuario.delete()
    return redirect(to="usuarios")


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

    try:
        form = PersonaForm()
        datos = {"form": form}

        if request.method == "POST":
            print(request.POST)
            # form = PersonaForm(request.POST)

            for valor in request.POST.values():
                print(valor)

            if len(request.POST) == 9:

                persona = Persona()
                persona.rut = request.POST.get("rut")
                persona.nombre = request.POST.get("nombre")
                persona.apellido = request.POST.get("apellido")
                persona.correo = request.POST.get("correo")
                persona.telefono = request.POST.get("telefono")
                persona.region = request.POST.get("region")
                persona.comuna = request.POST.get("comuna")
                persona.direccion = request.POST.get("direccion")
                persona.usuario = request.user
                persona.save()
                return redirect(to="index")
            else:
                raise Exception("Error en la cantidad de datos")
    except Exception as e:
        print(e)
    finally:
        form = PersonaForm()
        datos = {"form": form}
        """ if form.is_valid():

            form.instance.usuario = request.user
            region=form.cleaned_data['region']
            print(region)
            comuna=form.cleaned_data['comuna'] 
            print(comuna)
            print(form)
            form.save()
            return redirect(to="index") """

    return render(request, "greenhill/registrarse.html", datos)


def carrito(request):
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
    return render(request, "greenhill/admin-pedidos.html")


def pedidos(request):
    pedidos = pedidos.objects.all()
    return render(request, "greenhill/pedidos.html", {"pedidos": pedidos})


def crearPedido(request):
    carrito = get_object_or_404(Carrito, id=request.session.get("carrito_id"))
    if not CarritoItem.objects.filter(carrito=carrito).exists():
        return HttpResponse("No hay productos en el carrito",400)
    total = sum(item.producto.precio * item.cantidad for item in CarritoItem.objects.filter(carrito=carrito))
    pedido = Pedido(carrito=carrito, total=total)
    del request.session["carrito_id"]
    return redirect(to="pedidos")
