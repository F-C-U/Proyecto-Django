from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',index,name='index'),
    path('admin-agregar',adminAgregar,name='admin-agregar'),
    path('catalogo',catalogo,name='catalogo'),
    path('producto/<id>',producto,name='producto'),
    path('eliminar-producto/<int:id>/', eliminarProductos, name='eliminar-producto'),
    path('editar-producto/<int:id>/', editarProductos, name='editar-producto'),
    path('admin-productos/', paginaProductos, name='admin-productos'),
    path('perfil',perfil,name='perfil'),
    path('pago',pago,name='pago'),
    path('usuarios',usuarios,name='usuarios'),
    path('registrarse',registro,name='registrarse'),
    path('carrito',carrito,name='carrito'),
    path('pedidos',pedidos,name='pedidos'),
    path('agregar-carrito/<int:id>/', agregarCarrito, name='agregar-carrito'),
    path('eliminar-carrito/<int:id>/', quitarCarrito, name='eliminar-carrito'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)