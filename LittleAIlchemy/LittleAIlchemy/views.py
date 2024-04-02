from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos
from .models import dbCombinaciones
import datetime

@csrf_protect
def alquimia(request):
    listaElementos = dbElementos.objects.all
    nuevoElemento = None

    if request.method == 'POST':
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

        elementoId1 = elementoId1 if elementoId1 != '' else '1'
        elementoId2 = elementoId2 if elementoId2 != '' else '1'

        elemento1 = dbElementos.objects.filter(id=elementoId1).first()
        elemento2 = dbElementos.objects.filter(id=elementoId2).first()
        nombre = f"{elemento1}{elemento2}"
        nuevoElemento = dbElementos(nombre=nombre)
        nuevoElemento.save()

        #descripcion = "TBD"
        #imagen = "TBD"
        nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=nombre)
        nuevaCombinacion.save()
    return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento})

def inicio(request):
    return render(request, 'inicio.html')
