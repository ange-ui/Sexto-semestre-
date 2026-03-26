import tkinter as tk

def abrir():
    v = tk.Toplevel()
    intentos = [0]

    e = tk.Entry(v); e.grid(row=0, column=1)
    tk.Label(v, text="Número").grid(row=0, column=0)

    lbl = tk.Label(v); lbl.grid(row=2, column=0, columnspan=2)

    def validar():
        try:
            n = int(e.get())
            intentos[0] += 1
            if n < 10:
                lbl.config(text=f"Correcto: {n} Intentos: {intentos[0]}")
            else:
                lbl.config(text="Error")
        except:
            lbl.config(text="Error")

    tk.Button(v, text="Validar", command=validar).grid(row=1, column=0, columnspan=2)