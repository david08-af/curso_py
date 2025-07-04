import { $ } from "./logger.js"

const form = $("form")
//method onsubmit obtener los datos del formulario
form.onsubmit = (ev)=>{
    const formData= new formData(ev.target)
    const vel = formData.get("vel")
    const time = formData.get("time")

}