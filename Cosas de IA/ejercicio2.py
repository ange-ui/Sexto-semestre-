import tkinter as tk

visitantes = []

def abrir():
    v = tk.Toplevel()

    e1 = tk.Entry(v); e1.grid(row=0, column=1)
    e2 = tk.Entry(v); e2.grid(row=1, column=1)
    e3 = tk.Entry(v); e3.grid(row=2, column=1)

    tk.Label(v, text="Nombre").grid(row=0, column=0)
    tk.Label(v, text="Edad").grid(row=1, column=0)
    tk.Label(v, text="Juegos").grid(row=2, column=0)

    lbl = tk.Label(v); lbl.grid(row=4, column=0, columnspan=2)

    def calc():
        try:
            edad = int(e2.get())
            juegos = int(e3.get())
            total = juegos * 50

            if edad < 10:
                total *= 0.75
            elif edad < 18:
                total *= 0.90

            visitantes.append(total)
            lbl.config(text=f"Pagar: {total}")
        except:
            lbl.config(text="Error")

    def total():
        lbl.config(text=f"Total: {sum(visitantes)}")

    tk.Button(v, text="Calcular", command=calc).grid(row=3, column=0)
    tk.Button(v, text="Total parque", command=total).grid(row=3, column=1)