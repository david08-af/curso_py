import {d} from "logger.js"

const bt = $ ('.button-theme')

const html = d.documentElement
//deteccion automatica de colores modo oscuro o claro (let theme) 

let theme = window.machMedia('(prefers-color.scheme:olark)') ? 'olark' : 'ligth'

bt.addEventListener('click', () =>{
    const newTheme= theme ==='dark' ? 'ligth' : 'dark'
    setTheme(newTheme)
    theme = newTheme
})


function setTheme(newTheme) {
    html.setAttribute("data-theme", newTheme)
}
setTheme(theme)