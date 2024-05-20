// JavaScript para el juego
const elementos = document.querySelectorAll('.elemento');
const contenedores = document.querySelectorAll('.vacio');

// Control de arrastre para los elementos
elementos.forEach(elemento => {
    elemento.addEventListener('dragstart', (e) => {
        // Creamos un div temporal fuera de la vista del usuario
        // (Necesitaba hacer esto para arreglar un bug. Sé que es cutre, pero funciona)
        const contenedorTemp = document.createElement('div');
        contenedorTemp.style.position = 'absolute';
        contenedorTemp.style.left = '-9999px';

        // Clonamos el elemento y lo metemos en el div temporal
        const elementoClonado = elemento.cloneNode(true);
        elementoClonado.classList.add('arrastrando');
        elementoClonado.classList.add('clon');
        contenedorTemp.appendChild(elementoClonado);

        document.body.appendChild(contenedorTemp);

        // Centramos la imagen para que el cursor salga en medio
        e.dataTransfer.setDragImage(elementoClonado, 50, 50);

        // Eliminamos el contenedor temporal al dejar de arrastrar porque aunque no se vea, al inspeccionar elementos me salen si no 347248327549 divs vacíos
        elemento.addEventListener('dragend', () => {
            contenedorTemp.remove();
        });
    });

    // Al dejar de arrastrar le quita al clon la clase "arrastrando" porque si no, conserva sus propiedades
    elemento.addEventListener('dragend', () => {
        const clon = document.querySelector('.arrastrando');
        if (clon) {
            clon.classList.remove('arrastrando');
            const contenedores = document.querySelectorAll('.vacio');
            let soltadoEnContenedor = false;

            // Miramos a ver si e ha soltado el elemento en algún contenedor
            contenedores.forEach((contenedor) => {
                if (contenedor.contains(clon)) {
                    soltadoEnContenedor = true;
                }
            });

            // Si no es el caso, eliminamos el clon porque si no, se añade por debajo del body
            if (!soltadoEnContenedor) {
                clon.remove();
            }
        }
    });
    // Este event listener es para mover automáticamente los elementos al hacer click sobre ellos
    elemento.addEventListener('click', () => {
        // Clonamos el elemento
        const elementoClonado = elemento.cloneNode(true);
        // Miramos en qué contenedor se encuentra actualmente el elemento
        const contenedorOrigen = elemento.parentElement;
        const contenedoresVacios = document.querySelectorAll('.vacio.contenedor');

        // Recorremos los contenedores "vacíos"...
        for (const contenedor of contenedoresVacios) {
            // Si no tienen nada dentro, metemos el elemento dentro
            if (contenedor.querySelectorAll('.elemento').length === 0) {
                contenedor.appendChild(elementoClonado);
                // Nos salimos del bucle una vez esté hecho para que no lo mueva al segundo contenedor vacío
                return;
            }
        }
    });
});

contenedores.forEach(contenedor => {
    // Esto es para que se puedan añadir elementos arrastrando a los contenedores "vacíos"
    contenedor.addEventListener('dragover', e => {
        e.preventDefault();
        const elemento = document.querySelector('.arrastrando');
        const elementosEnContenedor = contenedor.querySelectorAll('.elemento');
        // Solo deja si el contenedor está vacío
        if (contenedor.classList.contains('vacio') && elementosEnContenedor.length === 0) {
            contenedor.appendChild(elemento);
        }
    });

    // Aquí añadimos un event listener que permite descartar los elementos colocados haciendo click
    if (contenedor.classList.contains('vacio')) {
        contenedor.addEventListener('click', (event) => {
            const elementoSeleccionado = event.target;
            if (elementoSeleccionado.classList.contains('elemento')) {
                elementoSeleccionado.remove();
            }
        });
    }
});

// Función que obtiene los ids y los nombres de los elementos para combinarlos
function combinar() {
    var contenedoresVacios = document.querySelectorAll('.izquierda .vacio.contenedor');
    var ids = [];
    var textos = [];

    // Esto es una función anónima. La he usado porque no necesito tener esta función fuera de "combinar".
    // Es la forma de decirle al forEach lo que tiene que hacer en cada iteración.
    // https://www.javascripttutorial.net/javascript-anonymous-functions/
    contenedoresVacios.forEach(function (contenedor) {
        var elemento = contenedor.querySelector('.elemento');
        if (elemento) {
            var elementoID = elemento.id;
            var elementoTexto = elemento.innerText;
            ids.push(elementoID);
            textos.push(elementoTexto);
        }
    });

    // Si en el array ids hay más de 0 elementos, el value del hidden1 será el id del primer elemento. Lo mismo para el segundo.
    document.getElementById('hidden1').value = ids.length > 0 ? ids[0] : '';
    document.getElementById('hidden2').value = ids.length > 1 ? ids[1] : '';

    document.getElementById('formCombinar').submit();
}

//Función que muestra el tutorial
function mostrarTutorial() {
    // En este array guardamos los mensajes del tutorial para que tengan un índice
    const textoTutorial = [
        "On your right you can find your element collection. Elements are your main and only resource in this game, and your goal is to create as many different ones as possible.",
        "On the right side you will find your alchemy table. You will need to place two elements here if you wish to combine them.",
        "To add an element to your alchemy table, you can either drag it or click on it. The choice is yours, sorcerer.",
        "Once you have added two elements to the alchemy table, you will need to click on the combine button and wait a few seconds.",
        "If you made a mistake or came up with a better combination, you can delete individual elements from the alchemy table by clicking on them. You can also clear both elements at once by clicking on the red button.",
        "The navigation bar at the bottom will allow you to return to the main screen, check the sorcerer leaderboard, log out of your account or repeat this tutorial (?).",
        "At some point, your collection will be too powerful to handle. When that happens, you can use the search bar on top of your elements to search for them by name."
    ];

    // Necesitamos un contador para mostrar las páginas del tutorial
    var tutorialActual = 0;

    // Mostramos el tutorial
    function mostrarPaginas() {
        swal({
            text: textoTutorial[tutorialActual],
            buttons: {
                //Exit: true,
                Back: {
                    text: "Back",
                    value: "Back",
                },
                Next: {
                    text: "Next",
                    value: "Next",
                },
            },
            closeOnClickOutside: false,
            icon: `../static/imagenes/tutorial/Tutorial${tutorialActual + 1}.png`
        })
        .then((value) => {
            switch (value) {
                //case "Exit":
                    //break;
                case "Next":
                    tutorialActual++;
                    if (tutorialActual < textoTutorial.length) {
                        mostrarPaginas();
                    } else {
                        swal("Tutorial completed", "That is all you need to know about Aiquimia. Start creating new elements and prove your worth, young sorcerer", "../static/imagenes/Thalasor.png");
                    }
                    break;
                case "Back":
                    if (tutorialActual > 0) {
                        tutorialActual--;
                        mostrarPaginas();
                    }
                    break;
            }
        });
    }

    swal({
        title: "Tutorial",
        text: "Greetings, young sorcerer. My name is Thalasor. I am the Arch-Mage of Arstotzka. Do you want me to teach you how to play Aiquimia?",
        buttons: {
            No: {
                text: "No",
                value: false,
            },
            Yes: {
                text: "Yes",
                value: true,
            }
        },
        closeOnClickOutside: false,
        icon: "../static/imagenes/Thalasor.png"
    })
    .then((value) => {
        if (value) {
            mostrarPaginas();
        } else {
            swal("Tutorial skipped", "Very well then. I will leave you alone, young sorcerer. If you ever need my help, click on the (?) button. Farewell.", "../static/imagenes/Thalasor.png");
        }
    });
}

// Alert para informar de la creación de un nuevo elemento / Error + tutorial
window.onload = function () {
    var tutorial = document.getElementById('tutorial').innerText;
    if (tutorial == "True") {
        mostrarTutorial();
    }
    var nuevoElemento = document.getElementById('nuevoElemento').innerText;
    var descripcion = document.getElementById('descripcion').innerText;
    var descubiertoPor = document.getElementById('descubiertoPor').innerText;
    var imagen = document.getElementById('imagenSwal').innerText;
    var usuario = document.getElementById('usuario').innerText;
    var victoria = document.getElementById('victoria').innerText;

    // Si el usuario actual descubió el elemento, cambiamos el color del destello
    var tipoDestello = usuario == descubiertoPor ? "destelloShiny" : "destello"; 

    // Aquí miramos si el usuario ha ganado (modo desafío) para mostrar ese mensaje en vez del normal
    if (victoria) {
        swal("You did it!", "His majesty is pleased", {
            button: "Glory to Arstotzka",
            icon: "../static/imagenes/elementos/" + imagen,
            className: tipoDestello
        });
    } else if (nuevoElemento !== "None") {
        swal("You have created " + nuevoElemento, descripcion, {
            button: "That's rad.",
            icon: "../static/imagenes/elementos/" + imagen,
            className: tipoDestello
        });
    }

    var error = document.getElementById('error').innerText;
    if (error !== "None") {
        swal(error, "Our most sincere apologies", {
            button: "D'oh!",
        });
    }
};

// Función para mostrar el marcador
function puntuacion() {
    var marcador = document.getElementById('puntuacion').innerText;
//    alert(puntuacion);
    swal("TOP 10", marcador, {
        button: "Nice",
    });
}

// Función que limpia la mesa de alquimia

function despejar() {
    var contenedoresVacios = document.querySelectorAll('.vacio');
    contenedoresVacios.forEach(function(contenedor) {
        while (contenedor.firstChild) {
            contenedor.removeChild(contenedor.firstChild);
        }
    });
}

// Event listener para la barra de búsqueda

// El evento se activa cuando el DOM se ha cargado completamente porque sin esto no me funcionaba
document.addEventListener('DOMContentLoaded', function() {
    // Guardamos en una variable el texto que se está buscando y los elementos
    var busqueda = document.getElementById('busqueda');
    var elementos = document.querySelectorAll('.elemento');

    // Añadimos al campo de texto de la barra de búsqueda un evento que se activa al soltar una tecla
    busqueda.addEventListener('keyup', function() {
        // Convertimos el texto en minúsculas para que sea más manejable
        var busquedaControl = this.value.trim().toLowerCase();

        elementos.forEach(function(elemento) {
            var texto = elemento.textContent.trim().toLowerCase();
            // Si el nombre de un elemento coincide con lo que tenemos en la barra de búsqueda, mostramos el elemento
            if (texto.includes(busquedaControl)) {
                elemento.style.display = 'block';
            // En caso contrario lo ocultamos
            } else {
                elemento.style.display = 'none';
            }
        });
    });
});
