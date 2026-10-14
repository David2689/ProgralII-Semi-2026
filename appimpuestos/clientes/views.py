from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hola_mundo(resquest): 
    return HttpResponse("hola Mundo!!!")

def saludo_nombre(request, nombre, edad):
    return HttpResponse(f"Hola {nombre} de {edad} años, Bienvenido al mundo de la programacion!!")
def index(request):
    return render(request, 'index.html')
