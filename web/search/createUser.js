import { $, createTable } from "./mian.js";
import data from "./data.js"
const form = $(".form-create")

form.addEventListener("submit", (ev) => {
    //prevenir el comportamiento por defecto 
    ev.preventDefault()
    const fields = Object.fromEntries(new FormData(ev.target))
    data.push(fields)
    createTable()
})