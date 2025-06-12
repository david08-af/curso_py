const d=document
const $= s => d.querySelector(s)
//funcionalidad de dark mode
const bt = document.querySelector(".button-theme")
const html = document.documentElement
//selecionar el formulario
const form = document.querySelector("form")
const dis = $(".form-parc")

let theme = window.matchMedia("(prefers-color-scheme: dark)")?"dark": "ligth"
bt.addEventListener("click", () => { 
    let newTheme = theme === "ligth"? "dark":"ligth"
    setTheme(newTheme)
    theme=newTheme
    console.log(theme);
})
function setTheme(newTheme){
    html.setAttribute("data-theme",theme)
}
setTheme(theme)
//method onsubmit obtener los datos del formulario
form.onsubmit = (ev)=>{
    const formData= new formData(ev.target)
    const vel = formData.get("vel")
    const time = formData.get("time")

}