from django.contrib import admin
from django.urls import path
from clientes.views import (
    index, 
    hola_mundo, 
    saludoNombre, 
    vistas, 
    guardar_cliente, 
    buscar_clientes,      
    guardar_producto,
    buscar_productos,      # <-- IMPORTANTE: Agregamos buscar_productos
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('saludo/', hola_mundo, name='hola_mundo'),
    path('saludo/<str:nombre>/<int:edad>', saludoNombre, name='saludo_nombre_edad'),
    path('vistas/<str:form>/', vistas, name='vistas'),
    path('guardar_cliente/', guardar_cliente, name='guardar_cliente'),
    path('buscar_clientes/<str:buscar>', buscar_clientes, name='buscar_clientes'),
    path('buscar_clientes/', buscar_clientes, {'buscar': ''}, name='buscar_todos_clientes'),
    path('guardar_producto/', guardar_producto, name='guardar_producto'),
    path('buscar_productos/<str:buscar>', buscar_productos, name='buscar_productos'),
    path('buscar_productos/', buscar_productos, {'buscar': ''}, name='buscar_todos_productos'),
]