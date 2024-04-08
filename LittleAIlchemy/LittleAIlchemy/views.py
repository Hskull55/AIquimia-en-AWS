from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos
from .models import dbCombinaciones
import replicate

@csrf_protect
def alquimia(request):
    # Obtenemos los elementos de la base de datos
    listaElementos = dbElementos.objects.all
    # Inicializamos nuevoElemento sin valor para evitar errores al cargar la página
    nuevoElemento = None
    error = None

    if request.method == 'POST':
	# Asignamos los ids de los elementos a una variable
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

	# Ponemos el elemento 164 (Water) como predeterminado si se intentó combinar con uno o ambos elementos vacíos
        elementoId1 = elementoId1 if elementoId1 != '' else '164'
        elementoId2 = elementoId2 if elementoId2 != '' else '164'

        elemento1 = dbElementos.objects.filter(id=elementoId1).first()
        elemento2 = dbElementos.objects.filter(id=elementoId2).first()
        nombre = f"{elemento1}{elemento2}"

        # Input de la API
        input_data = {
            "top_p": 1,
            "prompt": f"Tell me the result of combining {elemento1} and {elemento2}",
            "temperature": 0.75,
            "system_prompt": "You are an AI that combines elements as if we were playing the videogame Little Alchemy.You need to come up with the result of combining both an as output, write in a single word said result. Do not say anything else in the output. Just one single word. If both elements are the same, come up with a different one. You can create things that aren't actually elemnts, such as 'Car', 'House', 'Human', etc. as well as verbs and adjectives. The result can be a Copyrighted word such as 'Pokémon' or 'Ghostbusters'",
            "max_new_tokens": 800,
            "repetition_penalty": 1
        }

        # Output de la API
        output = replicate.run("meta/llama-2-70b-chat", input=input_data)

        # La API devuelve una lista de Python, así que hay que juntarlo todo
        resultadoCombinacion = ''.join(output).strip() if output else None
        #print(resultadoCombinacion) --> Debugging
        if resultadoCombinacion and len(resultadoCombinacion.split()) == 1:
	    # Guardamos la combinación en la base de datos si se ha generado correctamente un resultado
            nuevoElemento = dbElementos(nombre=resultadoCombinacion)
            nuevoElemento.save()

            #descripcion = "TBD"
            #imagen = "TBD"
            nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=resultadoCombinacion)
            nuevaCombinacion.save()
        # Este error se mostrará en un alert si la IA devuelve más de una palabra
        else:
            error = "Ha ocurrido algo inesperado. Inténtalo otra vez"

    return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error})

def inicio(request):
    return render(request, 'inicio.html')
