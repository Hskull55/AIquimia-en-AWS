import os, datetime, replicate, logging
from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import dbElementos, dbCombinaciones
from .forms import FormRegistro

logger = logging.getLogger()

@login_required
@csrf_protect
def alquimia(request):
    # Obtenemos los elementos creados por el usuario actual
    elementosCreados = request.user.elementosCreados.all()
    # Obtenemos los elementos con IDs 1, 2, 3 y 4; que son Agua, Aire, Tierra y Fuego
    elementosBasicos = dbElementos.objects.filter(id__in=[1, 2, 3, 4])
    # Mostramos los elementos del jugador
    listaElementos = (elementosCreados | elementosBasicos).order_by('nombre')
    # Inicializamos varias varibales sin valor para evitar errores al cargar la página
    nuevoElemento = None
    error = None
    descripcion = None
    imagen = None
    descubiertoPor= None
    usuario = request.user

    if request.method == 'POST':
        logger.error("TEST - {}".format(usuario))
        # Asignamos los ids de los elementos a una variable
        elementoId1 = request.POST.getlist('elementoId[]')[0]
        elementoId2 = request.POST.getlist('elementoId[]')[1]

        # Ponemos el elemento 1 (Water) como predeterminado si se intentó combinar con uno o ambos elementos vacíos
        elementoId1 = elementoId1 if elementoId1 != '' else '1'
        elementoId2 = elementoId2 if elementoId2 != '' else '1'

        elemento1 = dbElementos.objects.filter(id=elementoId1).first()
        elemento2 = dbElementos.objects.filter(id=elementoId2).first()
        logger.info("{} ha combinado {} y {}".format(usuario, elemento1, elemento2))

        # Verificamos si la combinación ya existe en la base de datos
        combinacionExistenteA = dbCombinaciones.objects.filter(elemento1=elemento1, elemento2=elemento2).first()
        combinacionExistenteB = dbCombinaciones.objects.filter(elemento1=elemento2, elemento2=elemento1).first()
        # Si la combinación ya existe, sacamos la información de la base de datos
        if combinacionExistenteA:
            nuevoElemento = combinacionExistenteA.resultado
            descripcion = dbElementos.objects.get(nombre=nuevoElemento).descripcion
            descubiertoPor = dbElementos.objects.get(nombre=nuevoElemento).descubiertoPor
            # Añadimos al usuario como creador para que le aparezca el elemento
            añadir = combinacionExistenteA.resultado
            añadir.creadores.add(request.user)
            # Añadimos al usuario actual a la lista de usuarios que han realizado esta combinación
            combinacionExistenteA.creadoresC.add(request.user)
        # Esto es por si están al revés
        elif combinacionExistenteB:
            nuevoElemento = combinacionExistenteB.resultado
            descripcion = dbElementos.objects.get(nombre=nuevoElemento).descripcion
            descubiertoPor = dbElementos.objects.get(nombre=nuevoElemento).descubiertoPor
            # Añadimos al usuario como creador para que le aparezca el elemento
            añadir = combinacionExistenteB.resultado
            añadir.creadores.add(request.user)
            # Añadimos al usuario actual a la lista de usuarios que han realizado esta combinación
            combinacionExistenteB.creadoresC.add(request.user)
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
                "prompt": f"Given the element {resultadoCombinacion}, tell me which of these file names sounds more closely related to it: (Fire.png, Water.png, Earth.png, Air.png, Explosion.png, Heart.png, Shiny.png, Evil.png, Skull.png, Hand.png, Dance.png, Clothes.png, Crown.png, Eyes.png, Tree.png, Flower.png, Snow.png, Lightning.png, Cloud.png, Internet.png, Moon.png, Sun.png, Soup.png, Dragon.png, Volcano.png, Rain.png, Rainbow.png, Weapon.png, Music.png, Wood.png, Game.png, Toxin.png, Blood.png, Person.png, Magic.png, Sport.png, Mountain.png, Sound.png, Wave.png, Biohazard.png, Building.png, Virus.png, Desert.png, Brick.png, Island.png, Car.png, Train.png, Plane.png, Boat.png, Tornado.png, Money.png, Robot.png, Luck.png, Logic.png, Art.png, Danger.png, Celebration.png, Bubbles.png, Prohibition.png, Spiral.png)",
                "system_prompt":"You choose a file name from a list. Always output your answer with just the file name. No pre-amble. Only choose from the given list. If not present on the list, choose the closest one but don't create a new one that is not on the list",
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

            # Si la API devuleve algo raro / un nombre que no existe, le asignamos al elemento la imagen de uno de los dos a partir de los cuales se creó
            rutaImagen = os.path.join("static/imagenes/elementos/", imagen)
            if not os.path.exists(rutaImagen):
                imagen = elemento1.imagen
                logger.error("La imagen {} no existe".format(rutaImagen))

            # Guardamos la combinación en la base de datos si se ha generado correctamente un resultado
            if resultadoCombinacion and len(resultadoCombinacion.split()) == 1:
                # Si la IA devuelve el resultado entre comillas o con un punto, lo quitamos
                resultadoCombinacion = resultadoCombinacion.strip('"').replace(".", "")
                # Comprobamos si ya estaba registrado para que no se repita
                elementoExistente = dbElementos.objects.filter(nombre=resultadoCombinacion).first()
                if not elementoExistente:
                    descubiertoPor = request.user
                    nuevoElemento = dbElementos(nombre=resultadoCombinacion, descripcion=descripcion, imagen=imagen, descubiertoPor=descubiertoPor)
                    nuevoElemento.save()
                else:
                    descubiertoPor = dbElementos.objects.get(nombre=elementoExistente).descubiertoPor
                    nuevoElemento = dbElementos(nombre=resultadoCombinacion, descripcion=descripcion, imagen=imagen, descubiertoPor=descubiertoPor)
            # Esto debería añadir al usuario actual como creador si ya he arreglado el bug
                añadir = dbElementos.objects.get(nombre=resultadoCombinacion)
                añadir.creadores.add(request.user)
                # Como "resultado" es una clave foránea que hace referencia a dbElementos.nombre, tenemos que hacer esto
                resultadoCombinacion = dbElementos.objects.get(nombre=nuevoElemento)
                nuevaCombinacion = dbCombinaciones(elemento1=elemento1, elemento2=elemento2, resultado=resultadoCombinacion)
                nuevaCombinacion.save()
                # Añadimos al usuario actual a la lista de usuarios que han realizado esta combinación
                nuevaCombinacion.creadoresC.add(request.user)
            # Este error se mostrará en un alert si la IA devuelve más de una palabra
            else:
                error = "Something went wrong. Try again later"
                logger.error("No se generó un elemento")
    # Sin flat=True los nombres no salen bien
    contadorDescubrimientos = Counter(dbElementos.objects.values_list('descubiertoPor', flat=True))
    # Solo pillamos a los 10 primeros
    top = contadorDescubrimientos.most_common(10)
    # Contamos cuantos elementos y combinaciones ha creado el usuario (Total, no descubierto)
    contadorElementos = dbElementos.objects.filter(creadores=request.user).count()
    contadorCombinaciones = dbCombinaciones.objects.filter(creadoresC=request.user).count()
    if nuevoElemento:
        imagen = nuevoElemento.imagen
    #return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error, 'descripcion':descripcion, 'imagen':imagen, 'descubiertoPor':descubiertoPor, 'top':top, 'contadorElementos':contadorElementos, 'contadorCombinaciones':contadorCombinaciones, 'usuario':usuario})
    # Aquí usamos una cookie para ver si es la primera vez que un usuario entra al juego
    tutorialHecho = request.COOKIES.get('tutorialHecho')
    if tutorialHecho != 'true':
        # Si la cookie está en "false" o no existe, cargamos la página y la creamos
        response = HttpResponse(render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error, 'descripcion':descripcion, 'imagen':imagen, 'descubiertoPor':descubiertoPor, 'top':top, 'contadorElementos':contadorElementos, 'contadorCombinaciones':contadorCombinaciones, 'usuario':usuario, 'tutorial': True}))
        expiracion = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie('tutorialHecho', 'true', expires=expiracion)
        return response
    else:
        # Si la cookie ya existe, solamente cargamos la página
        return render(request, 'alquimia.html', {'listaElementos': listaElementos, 'nuevoElemento': nuevoElemento, 'error': error, 'descripcion':descripcion, 'imagen':imagen, 'descubiertoPor':descubiertoPor, 'top':top, 'contadorElementos':contadorElementos, 'contadorCombinaciones':contadorCombinaciones, 'usuario':usuario, 'tutorial': False})

# Renderizamos la página de inicio
@login_required
def inicio(request):
    # Miramos si el usuario es administrador para mostrar o no el botón de la consola
    soyAdmin = request.user.groups.filter(name='Administradores').exists()
    # Aquí usamos una cookie para ver si es la primera vez que un usuario visita la página principal
    clienteHabitual = request.COOKIES.get('clienteHabitual')
    if clienteHabitual != 'true':
        # Si la cookie está en "false" o no existe, cargamos la página y la creamos
        response = HttpResponse(render(request, 'inicio.html', {'soyAdmin': soyAdmin, 'bienvenida': True}))
        expiracion = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie('clienteHabitual', 'true', expires=expiracion)
        return response
    else:
        # Si la cookie ya existe, solamente cargamos la página
        return render(request, 'inicio.html', {'soyAdmin': soyAdmin, 'bienvenida': False})

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


# Vista para cerrar sesión
def vistaLogout(request):
    logout(request)
    return redirect('/login/')


# 404 Personalizado
def custom404(request, exception):
    return render(request, '404.html', status=404)
