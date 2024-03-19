from django.shortcuts import render
import datetime

def pagina_prueba(request):
    return render(request, 'prueba.html')

def alquimia(request):
    hora_actual = datetime.datetime.now()
    return render(request, 'alquimia.html', {'hora_actual': hora_actual})
