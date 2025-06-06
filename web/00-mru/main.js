//funcionalidad de dark mode
const bt = document.querySelector(".button-theme")
const html = document.documentElement

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
//selecionar el formulario
const form = document.querySelector("form")
//method onsubmit obtener los datos del formulario
form.onsubmit = (ev)=>{
    const formData= new formData(ev.target)
    
}