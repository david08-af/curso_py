name = "lucas"
name1 = "andres"
#condicional que conprueba una variable
if name =="lucas":
    print("admin: ",name)
elif name == "andres":
    print("user", name)
#para conprobar la segunda variable name1 tendriamos que duplicar el condicional anterior
#la funcion ev(name)va a recibir un parametro entre los parentesis, este parametro sera las variables que creamos o queremos comprobar su condicion
def ev (name):
    if name =="lucas":
        print("admin: ",name)
    elif name == "andres":
        print("user", name)
    else:
        print("no se reconoce este usuario")

#llamar a la funcion y pasarle el parametro 
ev(name)
ev(name1)
ev("lautaro")