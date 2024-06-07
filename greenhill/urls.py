from django.urls import path
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('admin-agregar',adminAgregar,name='admin-agregar'),
]