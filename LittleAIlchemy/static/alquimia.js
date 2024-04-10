
//JavaScript para el juego

const elementos = document.querySelectorAll('.elemento')
const contenedores = document.querySelectorAll('.contenedor')

// Control de arrastre para los elementos
elementos.forEach(elemento => {
    elemento.addEventListener('dragstart', () => {
        elemento.classList.add('arrastrando');
    });

    elemento.addEventListener('dragend', () => {
        elemento.classList.remove('arrastrando');
    });

    // Este event listener es para mover automáticamente los elementos al hacer click sobre ellos
    elemento.addEventListener('click', () => {
        // Mira si el contenedor en el que está el elemento es el contenedor de elementos principal o uno de los "Vacíos"
        const contenedorOrigen = elemento.parentElement;

        // Si está en uno "vacío" lo mueve al principal
        if (contenedorOrigen.classList.contains('vacio')) {
            const contenedorElementos = document.querySelector('.contenedorElementos');
            contenedorElementos.appendChild(elemento);
        // Si no, busca los contenedores "vacíos"
        } else {
            const contenedoresVacios = document.querySelectorAll('.vacio.contenedor');

            // Y comprueba si están vacíos o no
            for (const contenedor of contenedoresVacios) {
                // Si lo están, mete el elemento dentro
                if (contenedor.querySelectorAll('.elemento').length === 0) { 
                    contenedor.appendChild(elemento); 
                    // Nos salimos del bucle una vez esté hecho para que no lo mueva al segundo contenedor vacío
                    return;
                }
            }
        }
    });
});

contenedores.forEach(contenedor => {
    contenedor.addEventListener('dragover', e => {
        e.preventDefault()
        const elemento = document.querySelector('.arrastrando')
        const elementosEnContenedor = contenedor.querySelectorAll('.elemento');

        //Esto es para que se pueda arrastrar solo un elemento por casilla vacía
        if (contenedor.classList.contains('vacio') && elementosEnContenedor.length === 0) {
            contenedor.appendChild(elemento);
        } else if (!contenedor.classList.contains('vacio')) {
            contenedor.appendChild(elemento);
        }

    })
})

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
    // alert("Elemento 1: ID - " + ids[0] + ", Texto - " + textos[0] + "\nElemento 2: ID - " + ids[1] + ", Texto - " + textos[1]);

    // Si en el array ids hay más de 0 elementos, el value del hidden1 será el id del primer elemento. Lo mismo para el segundo.
    document.getElementById('hidden1').value = ids.length > 0 ? ids[0] : '';
    document.getElementById('hidden2').value = ids.length > 1 ? ids[1] : '';

    document.getElementById('formCombinar').submit();
}

// Alert para informar de la creación de un nuevo elemento / Error
window.onload = function () {
    var nuevoElemento = document.getElementById('nuevoElemento').innerText;
    var descripcion = document.getElementById('descripcion').innerText;

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
