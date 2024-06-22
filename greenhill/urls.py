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
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)