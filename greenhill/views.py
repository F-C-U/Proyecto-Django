from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import * 

# Create your views here.
def index(request):
    return render(request,'greenhill/index.html')

def adminAgregar(request):
    form= ProductoForm()
    if request.method == "POST":
        form = ProductoForm(request.POST,files=request.FILES)
        if form.is_valid():
            return HttpResponseRedirect("greenhill/index.html")
    else:
        form = ProductoForm()
    datos = {
        "form": form
    }
    return render(request, "greenhill/admin-agregar-producto.html", datos)