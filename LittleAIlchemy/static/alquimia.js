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
    contenedor.appendChild(elemento)
  })
})
