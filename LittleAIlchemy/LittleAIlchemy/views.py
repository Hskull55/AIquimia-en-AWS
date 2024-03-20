from django.shortcuts import render
import datetime

def alquimia(request):
    hora_actual = datetime.datetime.now()
    return render(request, 'alquimia.html', {'hora_actual': hora_actual})

def inicio(request):
    return render(request, 'inicio.html')
