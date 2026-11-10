from django.contrib import admin
from django.urls import path
# Asegúrate de importar TODAS las funciones que tenés en tu views.py
from clientes.views import (
    index, 
    hola_mundo, 
    saludoNombre, 
    vistas, 
    guardar_cliente, 
    buscar_clientes
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta principal
    path('', index, name='index'),
    
    # Rutas de saludos
    path('saludo/', hola_mundo, name='hola_mundo'),
    # Dejamos la edad opcional en la URL usando <int:edad> pero sin la barra final para que coincida con el profe
    path('saludo/<str:nombre>/<int:edad>', saludoNombre, name='saludo_nombre_edad'),
    
    # Rutas de vistas y datos
    path('vistas/<str:form>/', vistas, name='vistas'),
    path('guardar_cliente/', guardar_cliente, name='guardar_cliente'),
    path('buscar_clientes/<str:buscar>', buscar_clientes, name='buscar_clientes'),
]


