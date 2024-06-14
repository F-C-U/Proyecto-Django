from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
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
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.nombre = request.POST.get('nombre')
        producto.precio = request.POST.get('precio')
        producto.description = request.POST.get('descripcion')
        producto.stock = request.POST.get('stock')
        producto.imagen = request.FILES.get('imagen')
        producto.save()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def eliminarProductos(request, id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=id)
        producto.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)