import tkinter as tk

trabajadores = []

def calcular(s):
    if s < 4000:
        return s * 1.15
    elif s <= 7000:
        return s * 1.10
    else:
        return s * 1.08

def abrir():
    v = tk.Toplevel()

    tk.Label(v, text="Nombre").grid(row=0, column=0)
    e1 = tk.Entry(v); e1.grid(row=0, column=1)

    tk.Label(v, text="Sueldo").grid(row=1, column=0)
    e2 = tk.Entry(v); e2.grid(row=1, column=1)

    lbl = tk.Label(v); lbl.grid(row=3, column=0, columnspan=2)

    def proc():
        try:
            s = float(e2.get())
            n = e1.get()
            nuevo = calcular(s)
            trabajadores.append((n, nuevo))
            lbl.config(text=f"{n}: {nuevo}")
        except:
            lbl.config(text="Error")

    def ver():
        texto = "\n".join([f"{n}: {s}" for n, s in trabajadores])
        lbl.config(text=texto)

    tk.Button(v, text="Calcular", command=proc).grid(row=2, column=0)
    tk.Button(v, text="Historial", command=ver).grid(row=2, column=1)