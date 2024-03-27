from django.shortcuts import render
from .models import Prueba
import datetime

def alquimia(request):
    objeto_prueba = Prueba.objects.get(id=1)
    nombre_prueba = objeto_prueba.nombre
    return render(request, 'alquimia.html', {'nombre_prueba': nombre_prueba})

def inicio(request):
    return render(request, 'inicio.html')
