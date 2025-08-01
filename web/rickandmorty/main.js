const d = document
const $ = s => d.querySelector(s) 

const sect = $(".main-section")

async function charateres () {
    const res = await fetch("https://rickandmortyapi.com/api/character")
    if (!res.ok) {
        console.error("error al solicitar los datos del servidor");
        
    }
    const data = await res.json()

    data.results.forEach(character => {
        const card = d.createRange().createContextualFragment(`
            <article class="card">
                <img class="image" src="${character.image} />
                <p class="title"> ${character.name}    
            </article>
        `)
        sect.append(card)
    });
}
charateres()