const d=document
const $= s => d.querySelector(s)
//funcionalidad de dark mode
const bt = document.querySelector(".button-theme")
const html = document.documentElement
const dis = $(".form-par")

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
    ev.preventDefault()
    const formData= new FormData(ev.target)
    const David = formData.get("David")
    const dilan = formData.get("dilan")
    const leo = formData.get("leo")
    evaluar(David)
    evaluar(dilan)
    evaluar(leo)
}

function evaluar(evalue) {
    //if significa si 
    //else significa sino
    //else if significa sino si
    if (evalue >= 1){
        console.log("positivo");
    } else if (evalue <= -1){
        console.log("negativo")
    } else {
        console.log("neutro")
    }
}