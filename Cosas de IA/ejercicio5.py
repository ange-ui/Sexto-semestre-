import tkinter as tk

def validar(n):
    return 0 < n < 20

def abrir():
    v = tk.Toplevel()
    e = tk.Entry(v); e.grid(row=0, column=1)

    lbl = tk.Label(v); lbl.grid(row=2, column=0, columnspan=2)

    def proc():
        try:
            n = int(e.get())
            if validar(n):
                lbl.config(text=f"Correcto: {n}")
            else:
                lbl.config(text="Fuera de rango")
        except:
            lbl.config(text="Error")

    tk.Button(v, text="Validar", command=proc).grid(row=1, column=0, columnspan=2)