import tkinter as tk

def abrir():
    v = tk.Toplevel()
    datos = []

    e = tk.Entry(v); e.grid(row=0, column=1)
    lbl = tk.Label(v); lbl.grid(row=3, column=0, columnspan=2)

    def add():
        try:
            n = int(e.get())
            datos.append(n)
            s = sum(datos)

            if s > 100:
                lbl.config(text=f"Fin: {datos} = {s}")
            else:
                lbl.config(text=f"Suma: {s}")
        except:
            lbl.config(text="Error")

    tk.Button(v, text="Agregar", command=add).grid(row=1, column=0, columnspan=2)