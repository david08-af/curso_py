import data from "./data.js"
import { $ } from "./mian.js"
const form = $(".form-delete")

form.addEventListener("submit", (ev) => {
    ev.preventDefault()
    const fields = Object.fromEntries(new FormData(ev.target))

    if (fields.name !== "" || fields.age) {
        data.forEach((element, index) => {
            let name = element.name.toLowerCase()
            let formName = fields.name.toLowerCase()
            if (name === formName && element.age === fields.age) {
                //el metodo splice funciona como una nabaja suiza, puede insertar, remover, remplazar un elemento de un array
                data.splice(index, 1)
            }
        })
        createTable()

    }
})