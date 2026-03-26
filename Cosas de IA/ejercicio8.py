import tkinter as tk

def abrir():
    v = tk.Toplevel()
    datos = []

    e = tk.Entry(v); e.grid(row=0, column=1)
    lbl = tk.Label(v); lbl.grid(row=3, column=0, columnspan=2)

    def add():
        try:
            n = int(e.get())
            if n == 0:
                lbl.config(text=f"{datos} Total: {sum(datos)}")
            else:
                datos.append(n)
                lbl.config(text=f"Suma: {sum(datos)}")
        except:
            lbl.config(text="Error")

    tk.Button(v, text="Agregar", command=add).grid(row=1, column=0, columnspan=2)