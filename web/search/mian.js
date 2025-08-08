import data from "./data.js"

const d = document
const $ = s => d.querySelector(s)
const $$ = s => d.querySelectorAll(s)

// seleccionar los elementos de nuestro html
// seleccionar el formulario de busqueda
const formSearch = $(".form-search")
const contentTable = $(".content-tablet")

//funcion que creara la tabla con contenido dinamico 
function createTable() {
    let tr = ""
    //agregando los datos de formas dinamicas y externas 
    data.forEach(el =>{
        tr += `
        
        <tr class="table-content">
            <td>${el.name}</td>
            <td>${el.age}</td>
        </tr>
        `
    })
    //creando la tabla dinamicamente con js y agregando contenido dinamico 
    let table = `
    <table> 
        <thead>
            <tr> 
                <th>nombre</th>
                <th>edad</th>
            </tr> 
        </thead> 
        <tbody>
            ${tr}
        </tbody>
    </table>       
    `
    contentTable.innerHTML = table
}
createTable()

// funcion encargada de agregar y eliminar una clase de un elemento de html
formSearch.addEventListener("submit", (ev) => {
  ev.preventDefault()
  const field = new FormData(ev.targe)
  const search = field.get("search")
  const rows = $$(".table-content")

  rows.forEach(row => {
    
    if (row.textContent.includes(search)) {
      row.classList.add("filter")
    } else {
      row.classList.remove("filter")
    }
  })
})
