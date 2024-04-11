from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos, dbCombinaciones  # Importamos los modelos actualizados
import replicate

@csrf_protect
def alquimia(request):
    # Obtenemos los elementos de la base de datos
    listaElementos = dbElementos.objects.all()
    # Inicializamos nuevoElemento, error y descripcion sin valor para evitar errores al cargar la página
    nuevoElemento = None
    error = None
    descripcion = None

    if request.method == 'POST':
        # Asignamos los ids de los elementos a una variable
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

        # Ponemos el elemento 1 (Water) como predeterminado si se intentó combinar con uno o ambos elementos vacíos
        elementoId1 = elementoId1 if elementoId1 != '' else '1'
        elementoId2 = elementoId2 if elementoId2 != '' else '1'

        elemento1 = dbElementos.objects.filter(id=elementoId1).first()
        elemento2 = dbElementos.objects.filter(id=elementoId2).first()

        # Verificamos si la combinación ya existe en la base de datos
        combinacionExistenteA = dbCombinaciones.objects.filter(elemento1=elemento1, elemento2=elemento2).first()
        combinacionExistenteB = dbCombinaciones.objects.filter(elemento1=elemento2, elemento2=elemento1).first()

        # Si la combinación ya existe, sacamos la información de la base de datos
        if combinacionExistenteA:
            nuevoElemento = combinacionExistenteA.resultado
            descripcion = combinacionExistenteA.descripcion
        # Esto es por si están al revés
        elif combinacionExistenteB:
            nuevoElemento = combinacionExistenteB.resultado
            descripcion = combinacionExistenteB.descripcion
        # Si no está registrada la combinación, le pedimos a la IA que la genere
        else:
            nombre = f"{elemento1}{elemento2}"

            # Input de la API
            input_data = {
                "top_p": 1,
                "prompt": f"Tell me the result of combining {elemento1} and {elemento2}",
                "temperature": 0.75,
                "system_prompt": "You are an AI that combines elements as if we were playing the videogame Little Alchemy.You need to come up with the result of combining both an as output, write in a single word said result. Do not say anything else in the output. Just one single word. If both elements are the same, come up with a different one. You can create things that aren't actually elemnts, such as 'Car', 'House', 'Human', etc. as well as verbs and adjectives. The result can be a Copyrighted word such as 'Pokémon' or 'Ghostbusters'. Try to be creative with the combinations while generating results that make sense",
                "max_new_tokens": 800,
                "repetition_penalty": 1
            }

            # Output de la API
            output = replicate.run("meta/llama-2-70b-chat", input=input_data)

            # La API devuelve una lista de Python, así que hay que juntarlo todo
            resultadoCombinacion = ''.join(output).strip() if output else None

            # -----------------------------------------------------------------------

            # Input para la descripción del elemento resultante
            input_data = {
                "top_p": 1,
                "prompt": f"Give me a brief description for {resultadoCombinacion}",
                "system_prompt": "You are an AI specializing in generating descriptions for elements created by combining two inputs in a manner akin to the game Little Alchemy. Your task is to provide a detailed description of the resulting element without referencing its constituent parts. Simply begin describing the newly formed element without preamble. Don't start by saying 'Sure, heres the description' or anything like that and avoid giving your opinion on the result or simulating noises like *Ahhh*",
                "temperature": 0.75,
                "max_new_tokens": 600,
                "repetition_penalty": 1
            }

            # Output de la API. Usamos el modelo 7 porque si no tarda mucho
            output = replicate.run("meta/llama-2-7b-chat", input=input_data)

            # La API devuelve una lista de Python, así que hay que juntarlo todo
            descripcion = ''.join(output).strip() if output else None

            # Guardamos la combinación en la base de datos si se ha generado correctamente un resultado
            if resultadoCombinacion and len(resultadoCombinacion.split()) == 1:
                nuevoElemento = dbElementos(nombre=resultadoCombinacion)
                # Comprobamos si ya estaba registrado para que no se repita
                existeElemento = dbElementos.objects.filter(nombre=resultadoCombinacion)
                if not existeElemento:
                    nuevoElemento.save()

                # imagen = "TBD"
                nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=resultadoCombinacion,)
                nuevaCombinacion.save()
            # Este error se mostrará en un alert si la IA devuelve más de una palabra
            else:
                error = "Something went wrong. Try again later"

    return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error, 'descripcion':descripcion})

def inicio(request):
    return render(request, 'inicio.html')
