from django.shortcuts import render
from .models import Prueba
import datetime

def alquimia(request):
    nombres = Prueba.objects.all
    return render(request, 'alquimia.html', {'nombres': nombres})

def inicio(request):
    return render(request, 'inicio.html')
