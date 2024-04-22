import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos, dbCombinaciones
from .forms import FormRegistro
import replicate

@login_required
@csrf_protect
def alquimia(request):
    # Obtenemos los elementos de la base de datos
    listaElementos = dbElementos.objects.all()
    # Inicializamos varias varibales sin valor para evitar errores al cargar la página
    nuevoElemento = None
    error = None
    descripcion = None
    imagen = None

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
            descripcion = dbElementos.objects.get(nombre=nuevoElemento).descripcion
        # Esto es por si están al revés
        elif combinacionExistenteB:
            nuevoElemento = combinacionExistenteB.resultado
            descripcion = dbElementos.objects.get(nombre=nuevoElemento).descripcion
        # Si no está registrada la combinación, le pedimos a la IA que la genere
        else:

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
                "system_prompt": "You are an AI that describes words. You will receive an input and you need to describe it. The output must be just the description of said word, so don't say anything like 'Here's the description for X' just start writing the description itself.",
#                "system_prompt": "You are an AI that combines elements as if we were playing Little Alchemy. As input you will recieve a word. I need you to come up with a description for said word. Just give me the description, no need to tell me anything else; so don't say Sure, Of course or anything like that, just start describing whatever was created. Do not mention the elements you think it came from. Don't start by saying 'Sure, heres the description for (WORD)' or anything like that and try to give a serious, easy to undertand description. If for whatever reason you can't create a serious, objective description or the input is a word that doesn't exist, then simply try to come up with a description that seems logical given the context of the game",
                "temperature": 0.75,
                "max_new_tokens": 600,
                "repetition_penalty": 1
            }

            # Output de la API. Usamos el modelo 7 porque si no tarda mucho
            output = replicate.run("meta/llama-2-7b-chat", input=input_data)

            # La API devuelve una lista de Python, así que hay que juntarlo todo
            descripcion = ''.join(output).strip() if output else None

            # -----------------------------------------------------------------------

            # Input para la imagen
            input_data = {
                "top_p": 1,
                "prompt": f"Given the element {resultadoCombinacion}, tell me which of these file names sounds more closely related to it: (Fire.png, Water.png, Earth.png, Air.png, Explosion.png, Heart.png, Shiny.png, Evil.png, Skull.png, Hand.png, Dance.png, Clothes.png, Crown.png, Eyes.png, Tree.png, Flower.png, Snow.png, Lightning.png, Cloud.png, Internet.png, Moon.png, Sun.png, Soup.png, Dragon.png, Volcano.png, Rain.png, Rainbow.png, Weapon.png, Music.png, Wood.png, Game.png, Toxin.png, Blood.png, Person.png, Magic.png, Sport.png, Mountain.png, Sound.png, Wave.png, Biohazard.png, Building.png, Virus.png, Desert.png)",
                "system_prompt":"You choose a file name from a list. Always output your answer with just the file name. No pre-amble. Only choose from the given list. If not present on the list, choose the closest one but don't create a new one that is not on the list",
#                "system_prompt":"You are an ai that chooses the most suitable file name for a given word. If there isn't a direct match, you need to choose the file name that's more closely associated with the word given as input. Answer with just the name of the file. Don't write anything else. The output must be just the name of the file. It must be one of the file names given as input. The output will never be a file name that is not on the provided list",
                "temperature": 0.75,
                "max_new_tokens": 60,
                "repetition_penalty": 1
            }

            # Output de la API. Usamos el 70 porque el 7 es medio tonto
            output = replicate.run("meta/llama-2-70b-chat", input=input_data)

            # La API devuelve una lista de Python, así que hay que juntarlo todo
            imagen = ''.join(output).strip() if output else None
            palabras = imagen.split()
            print(palabras)
            # Control de errores por si la IA devuelve una cadena larga, o el nombre del fichero está entre comillas
            for palabra in palabras:
                if palabra.endswith(".png"):
                       imagen = palabra
                       break
                elif palabra.startswith('"') and palabra.endswith('"'):
                    corte = palabra[1:-1]
                    if corte.endswith(".png"):
                         imagen = corte
                         break
                elif palabra.startswith('"') and palabra.endswith('.'):
                    corte = palabra[1:-2]
                    if corte.endswith(".png"):
                         imagen = corte
                         break
                elif palabra.endswith('.'):
                    corte = palabra[:-1]
                    if corte.endswith(".png"):
                         imagen = corte
                         break


            print(imagen)

            # Si la API devuleve algo raro / un nombre que no existe, le asignamos al elemento la imagen de uno de los dos a partir de los cuales se creó
            rutaImagen = os.path.join("static/imagenes/elementos/", imagen)
            if not os.path.exists(rutaImagen):
                imagen = elemento1.imagen

            # Guardamos la combinación en la base de datos si se ha generado correctamente un resultado
            if resultadoCombinacion and len(resultadoCombinacion.split()) == 1:
                # Si la IA devuelve el resultado entre comillas o con un punto, lo quitamos
                resultadoCombinacion = resultadoCombinacion.strip('"').replace(".", "")
                nuevoElemento = dbElementos(nombre=resultadoCombinacion, descripcion=descripcion, imagen=imagen)
                # Comprobamos si ya estaba registrado para que no se repita
                existeElemento = dbElementos.objects.filter(nombre=resultadoCombinacion)
                if not existeElemento:
                    nuevoElemento.save()

                # Como "resultado" es una clave foránea que hace referencia a dbElementos.nombre, tenemos que hacer esto
                resultadoCombinacion = dbElementos.objects.get(nombre=nuevoElemento)
                nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=resultadoCombinacion,)
                nuevaCombinacion.save()

            # Este error se mostrará en un alert si la IA devuelve más de una palabra
            else:
                error = "Something went wrong. Try again later"

    return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error, 'descripcion':descripcion, 'imagen':imagen})

# Renderizamos la página de inicio
@login_required
def inicio(request):
    return render(request, 'inicio.html')

# Utilizando el formulario predeterminado de Django para inicio de sesión "LoginView", implantamos el sistema de autenticación de usarios
class MiLoginView(LoginView):
    # El login se hará mediante la plantilla "login.html"
    template_name = 'login.html'
    # Si el login tiene éxito, nos redirigirá a la raíz del proyecto (Página de inicio)
    def get_success_url(self):
        return '/'

# Página de registro
def registro(request):
    # Esto es `para cuando envías el formulario de registro, validarlo y llevarte a login
    if request.method == 'POST':
        formulario = FormRegistro(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('/login/')
    else:
    # Y esto para que cuando entres normalmente, te aparezca el formulario y ya
        formulario = FormRegistro()
    return render(request, 'registro.html', {'form': formulario})
