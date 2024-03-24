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
