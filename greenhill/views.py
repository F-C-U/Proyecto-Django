from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'greenhill/index.html')

def adminAgregar(request):
    return render(request,'greenhill/admin-agregar-producto.html')