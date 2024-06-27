import re
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import * 
from .models import *

# Create your views here.
def index(request):
    return render(request,'greenhill/index.html')

def adminAgregar(request):
    form= ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('admin-agregar')
    else:
        form = ProductoForm()
    datos = {
        "form": form
    }
    return render(request, "greenhill/admin-agregar-producto.html", datos)

def catalogo(request):
    productos = Producto.objects.all()
    datos = {
        "productos": productos
    }
    return render(request, "greenhill/catalogo.html", datos)

def producto(request,id):
    producto = get_object_or_404(Producto, id=id)
    datos = {
        "producto": producto
    }
    return render(request,'greenhill/producto.html',datos)

def paginaProductos(request):
    productos = Producto.objects.all()
    datos = {
        "productos": productos
    }
    return render(request,'greenhill/admin-productos.html',datos)

def editarProductos(request,id):
    producto = get_object_or_404(Producto, id=id)
    data ={
        'form': ProductoForm(instance=producto)
    }
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to='admin-productos')
        data["form"] = formulario
    return render(request, 'greenhill/admin-modificar-producto.html', data)

def eliminarProductos(request, id):
    producto=get_object_or_404(Producto, id=id)
    producto.delete()
    return redirect(to='admin-productos')

def perfil(request):
    return render(request,'greenhill/perfil.html')

def pago(request):
    return render(request,'greenhill/pago.html')

def usuarios(request):
    usuarios = Persona.objects.all()
    datos = {
        "usuarios": usuarios
    }
    return render(request, "greenhill/admin-usuarios.html", datos)

def eliminarUsuario(request, id):
    usuario = get_object_or_404(Persona, id=id)
    usuario.delete()
    return redirect(to='usuarios')

def registro(request):
    form = PersonaForm()
    if request.method == "POST":
        form = PersonaForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('admin-agregar')
    else:
        form = PersonaForm()
    datos = {
        "form": form
    }
    
    return render(request,'greenhill/registrarse.html',datos)