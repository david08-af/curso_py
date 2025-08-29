import tkinter as tk

# funciones
def calcular_distancia():
    velocidad = entry_velocidad.get()
    tiempo= entry_tiempo.get()
    distancia= float(velocidad) * float(tiempo)
    label_distancia.configure(text=f"distancia: {distancia}") 

#crear la ventana
root = tk.Tk() 

#configurar ventana 
root.title("calcular distancia")
root.minsize(350,150)

#elementos 
#label
label_title = tk.Label(root,text="calcular distancia")
label_velocidad = tk.Label(root,text="velocidad")
label_tiempo = tk.Label(root,text="tiempo")
label_distancia = tk.Label(root,text="distancia:" )
#caja de texto
text_velocidad= tk.StringVar()
text_tiempo= tk.StringVar()
#entrada de texto
entry_velocidad= tk.Entry(root,width=20,textvariable=text_velocidad)
entry_tiempo= tk.Entry(root,width=20,textvariable=text_tiempo)

#boton
bt = tk.Button(root, text="evaluar", command=calcular_distancia)

#posicion de los elementos 
label_title.grid(column=0,row=0)
label_velocidad.grid(column=0,row=1)
label_tiempo.grid(column=0,row=2)

entry_velocidad.grid(column=1,row=1)
entry_tiempo.grid(column=1,row=2)

bt.grid(column=0,row=4)

# #iniciaslizar la ventana

root.mainloop()