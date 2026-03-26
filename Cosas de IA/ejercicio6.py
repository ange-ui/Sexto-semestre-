import tkinter as tk

def abrir():
    v = tk.Toplevel()
    datos = []

    e = tk.Entry(v); e.grid(row=0, column=1)
    lbl = tk.Label(v); lbl.grid(row=2, column=0, columnspan=2)

    def proc():
        try:
            n = int(e.get())
            datos.append(n)
            if 0 < n < 20:
                lbl.config(text=f"Correcto: {n}")
            else:
                lbl.config(text="Incorrecto")
        except:
            lbl.config(text="Error")

    def hist():
        lbl.config(text=f"{datos}")

    tk.Button(v, text="Ingresar", command=proc).grid(row=1, column=0)
    tk.Button(v, text="Historial", command=hist).grid(row=1, column=1)