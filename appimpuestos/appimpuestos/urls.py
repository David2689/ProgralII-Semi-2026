from django.contrib import admin
from django.urls import path
# Asegurate de importar todas las funciones desde tu views
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
    
    # Ruta principal (donde se carga el menú y las ventanas)
    path('', index, name='index'),
    
    # Rutas de prueba / saludos (por si las usás)
    path('saludo/', hola_mundo, name='hola_mundo'),
    path('saludo/<str:nombre>/<int:edad>', saludoNombre, name='saludo_nombre_edad'),
    
    # Ruta para cargar los formularios HTML (clientes, buscador, etc.)
    path('vistas/<str:form>/', vistas, name='vistas'),
    
    # Ruta para guardar, modificar o eliminar clientes
    path('guardar_cliente/', guardar_cliente, name='guardar_cliente'),
    
    # RUTAS DEL BUSCADOR (Acá está la clave)
    # 1. Cuando buscan con un texto (ej: /buscar_clientes/David)
    path('buscar_clientes/<str:buscar>', buscar_clientes, name='buscar_clientes'),
    
    # 2. Cuando abren el buscador y la caja está vacía (ej: /buscar_clientes/)
    path('buscar_clientes/', buscar_clientes, {'buscar': ''}, name='buscar_todos_clientes'),
]