from django.shortcuts import render
from .models import Prueba
import datetime

def alquimia(request):
    listaElementos = Prueba.objects.all
    return render(request, 'alquimia.html', {'listaElementos': listaElementos})

def inicio(request):
    return render(request, 'inicio.html')
