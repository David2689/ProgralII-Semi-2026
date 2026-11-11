from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponse,JsonResponse 
import json
from django.views.decorators.csrf import csrf_exempt
from .models import clientes

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
    return render(request, 'index.html')

def vistas(request, form):
    return render(request, f"{form}.html")

from django.db.models import Q # Poné esto arriba de todo si no lo tenés

def buscar_clientes(request, buscar):
    # Busca en el código O en el nombre que contenga el texto
    datos = clientes.objects.filter(
        Q(codigo__icontains=buscar) | Q(nombre__icontains=buscar)
    ).values()
    return JsonResponse({'datos': list(datos)})

@csrf_exempt
def guardar_cliente(request):
    if request.method=="POST":
        datos = json.loads(request.body)  
        if( datos.get("accion")=="nuevo" ):
                
            editCliente = clientes.objects.create(
                codigo=datos.get("codigo"),
                nombre=datos.get("nombre"),
                direccion=datos.get("direccion"),
                telefono=datos.get("telefono"),
                email=datos.get("email"),
                tipo=datos.get("tipo")
            )
        elif( datos.get("accion")=="modificar" ):
            editCliente = clientes.objects.get(id=datos.get("idCliente"))
            editCliente.codigo=datos.get("codigo")
            editCliente.nombre=datos.get("nombre")
            editCliente.direccion=datos.get("direccion")
            editCliente.telefono=datos.get("telefono")
            editCliente.email=datos.get("email")
            editCliente.tipo=datos.get("tipo")
            editCliente.save()
        elif( datos.get("accion")=="eliminar" ):
            editCliente = clientes.objects.get(id=datos.get("idCliente"))
            editCliente.delete()
        return JsonResponse({'msg':'ok', 'id': editCliente.id})
    else:
        return JsonResponse({'msg':'Metodo no permitido'})