#tres chicos quieren comprar una consola, pero hay un problema, los precios no estan al lado del estante, ellos quieren comprar la consola mas cara.
#tenemos que solicitar elo dinero que tiene cada uno, si hay dos consolas con el mismo precio mostrar las dos consolas.
david_cash = 21000
lautaro_cash =  31000
valentino_cash = 17000

console = {
    #"console": "precio",
    "play 5": "25000",
    "xbox360": "15000"
} 

if david_cash == console['play 5']:
    print(f"david te podes comprar la consola {console  ['play 5']}")