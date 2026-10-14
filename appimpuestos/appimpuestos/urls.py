"""
URL configuration for appimpuestos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from clientes.views import index, hola_mundo, saludo_nombre

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),  # Ruta raíz que ahora sí funcionará
    path('saludo/', hola_mundo, name='hola_mundo'),
    path('saludo/<str:nombre>/', saludo_nombre, name='saludo_nombre'),
    # Nota: Si vas a usar la ruta con edad, recuerda actualizar también tu vista en views.py 
    # para que reciba el parámetro edad, por ejemplo: def saludo_nombre(request, nombre, edad=None):
    path('saludo/<str:nombre>/<int:edad>/', saludo_nombre, name='saludo_nombre_edad'),
]


