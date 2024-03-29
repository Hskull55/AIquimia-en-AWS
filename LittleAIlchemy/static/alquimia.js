//JavaScript para el juego

const elementos = document.querySelectorAll('.elemento')
const contenedores = document.querySelectorAll('.contenedor')

elementos.forEach(elemento => {
    elemento.addEventListener('dragstart', () => {
      elemento.classList.add('arrastrando')
    })

    elemento.addEventListener('dragend', () => {
      elemento.classList.remove('arrastrando')
    })
})

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

function combinar() {
    var contenedoresVacios = document.querySelectorAll('.izquierda .vacio.contenedor');
    var ids = [];
    var textos = [];

    // Esto es una función anónima. La he usado porque no necesito tener esta función fuera de "combinar".
    // Es la forma de decirle al forEach lo que tiene que hacer en cada iteración.
    // https://www.javascripttutorial.net/javascript-anonymous-functions/
    contenedoresVacios.forEach(function(contenedor) {
        var elemento = contenedor.querySelector('.elemento');
        if (elemento) {
            var elementoID = elemento.id;
            var elementoTexto = elemento.innerText;
            ids.push(elementoID);
            textos.push(elementoTexto);
        }
    });
    alert("Elemento 1: ID - " + ids[0] + ", Texto - " + textos[0] + "\nElemento 2: ID - " + ids[1] + ", Texto - " + textos[1]);
}
