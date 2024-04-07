from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos
from .models import dbCombinaciones
from .testLlama import combinarAPI
import datetime

@csrf_protect
def alquimia(request):
    # Obtenemos los elementos de la base de datos
    listaElementos = dbElementos.objects.all
    # Inicializamos nuevoElemento sin valor para evitar errores al cargar la página
    nuevoElemento = None

    if request.method == 'POST':
	# Asignamos los ids de los elementos a una variable
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

	# Ponemos el elemento 1 (Agua) como predeterminado si se intentó combinar con uno o ambos elementos vacíos
        elementoId1 = elementoId1 if elementoId1 != '' else '1'
        elementoId2 = elementoId2 if elementoId2 != '' else '1'

	# Guardamos la combinación en la base de datos como un nuevo elemento
        elemento1 = dbElementos.objects.filter(id=elementoId1).first()
        elemento2 = dbElementos.objects.filter(id=elementoId2).first()
        nombre = f"{elemento1}{elemento2}"
        nuevoElemento = dbElementos(nombre=nombre)
        #nombre1 = elemento1.nombre
        #nombre2 = elemento2.nombre
        #nombre = combinarAPI(nombre1, nombre2)
        nuevoElemento = dbElementos(nombre=nombre)
        nuevoElemento.save()

	# Guardamos los datos de la combinación en sí
        #descripcion = "TBD"
        #imagen = "TBD"
        nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=nombre)
        nuevaCombinacion.save()
    return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento})

def inicio(request):
    return render(request, 'inicio.html')
