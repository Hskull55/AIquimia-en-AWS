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

// Alert para informar de la creación de un nuevo elemento / Error
window.onload = function () {
    var nuevoElemento = document.getElementById('nuevoElemento').innerText;
    var descripcion = document.getElementById('descripcion').innerText;
    var descubiertoPor = document.getElementById('descubiertoPor').innerText;

    if (nuevoElemento !== "None") {
        swal("You have created " + nuevoElemento, descripcion, {
            button: "That's rad.",
        });
    }

    var error = document.getElementById('error').innerText;
    if (error !== "None") {
        swal(error, "Our most sincere apologies", {
            button: "D'oh!",
        });
    }
};

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
