from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Prueba
import datetime

@csrf_protect
def alquimia(request):
    listaElementos = Prueba.objects.all
    if request.method == 'POST':
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

        elementoId1 = elementoId1 if elementoId1 != '' else '1'
        elementoId2 = elementoId2 if elementoId2 != '' else '1'

        elemento1 = Prueba.objects.filter(id=elementoId1).first()
        elemento2 = Prueba.objects.filter(id=elementoId2).first()
        nombre = f"{elemento1}{elemento2}"
        #nombre = f"{elementoId1} + {elementoId2} = {int(elementoId1) + int(elementoId2)}"
        nuevoElemento = Prueba(nombre=nombre)
        nuevoElemento.save()

    return render(request, 'alquimia.html', {'listaElementos': listaElementos})

def inicio(request):
    return render(request, 'inicio.html')
