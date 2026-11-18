from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import clientes, productos  # <-- IMPORTANTE: Agregamos productos

# Create your views here.
def hola_mundo(request):
    return HttpResponse("Hola Mundo, Bienvenidos a Progra III")

def saludoNombre(request, nombre, edad=None):
    if edad:
        return HttpResponse(f"Hola {nombre}, tu edad es {edad}, Bienvenidos a Progra III")
    else:
        return HttpResponse(f"Hola {nombre}, Bienvenidos a Progra III")

def index(request):
    return render(request, 'index.html')

def vistas(request, form):
    return render(request, f"{form}.html")

def buscar_clientes(request, buscar):
    datos = clientes.objects.filter(
        Q(codigo__icontains=buscar) | Q(nombre__icontains=buscar)
    ).values()
    return JsonResponse({'datos': list(datos)})

@csrf_exempt
def guardar_cliente(request):
    if request.method == "POST":
        datos = json.loads(request.body)  
        if datos.get("accion") == "nuevo":
            editCliente = clientes.objects.create(
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                telefono=datos.get("telefono"),
                email=datos.get("email"),
                tipo=datos.get("tipo")
            )
        elif datos.get("accion") == "modificar":
            editCliente = clientes.objects.get(id=datos.get("idCliente"))
            editCliente.codigo = datos.get("codigo")
            editCliente.nombre = datos.get("nombre")
            editCliente.direccion = datos.get("direccion")
            editCliente.telefono = datos.get("telefono")
            editCliente.email = datos.get("email")
            editCliente.tipo = datos.get("tipo")
            editCliente.save()
        elif datos.get("accion") == "eliminar":
            editCliente = clientes.objects.get(id=datos.get("idCliente"))
            editCliente.delete()
            return JsonResponse({'msg': 'ok'})
            
        return JsonResponse({'msg': 'ok', 'id': editCliente.id if 'editCliente' in locals() else None})
    return JsonResponse({'msg': 'Metodo no permitido'})

@csrf_exempt
def guardar_producto(request):
    if request.method == "POST":
        datos = json.loads(request.body)
        if datos.get("accion") == "nuevo":
            editProducto = productos.objects.create(
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                marca=datos.get("marca"),
                precio=datos.get("precio")
            )
        elif datos.get("accion") == "modificar":
            editProducto = productos.objects.get(id=datos.get("idProducto"))
            editProducto.codigo = datos.get("codigo")
            editProducto.nombre = datos.get("nombre")
            editProducto.marca = datos.get("marca")
            editProducto.precio = datos.get("precio")
            editProducto.save()
        elif datos.get("accion") == "eliminar":
            editProducto = productos.objects.get(id=datos.get("idProducto"))
            editProducto.delete()
            return JsonResponse({'msg': 'ok'})
            
        return JsonResponse({'msg': 'ok', 'id': editProducto.id if 'editProducto' in locals() else None})
    return JsonResponse({'msg': 'Metodo no permitido'})

def buscar_productos(request, buscar):
    datos = productos.objects.filter(
        Q(codigo__icontains=buscar) | Q(nombre__icontains=buscar) | Q(marca__icontains=buscar)
    ).values()
    return JsonResponse({'datos': list(datos)})