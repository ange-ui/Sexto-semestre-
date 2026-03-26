import tkinter as tk

ventas = []

def abrir():
    v = tk.Toplevel()

    e1 = tk.Entry(v); e1.grid(row=0, column=1)
    e2 = tk.Entry(v); e2.grid(row=1, column=1)
    e3 = tk.Entry(v); e3.grid(row=2, column=1)

    tk.Label(v, text="Nombre").grid(row=0, column=0)
    tk.Label(v, text="Mes").grid(row=1, column=0)
    tk.Label(v, text="Importe").grid(row=2, column=0)

    lbl = tk.Label(v); lbl.grid(row=4, column=0, columnspan=2)

    def calc():
        mes = e2.get().lower()
        try:
            imp = float(e3.get())
            desc = 0

            if mes == "octubre":
                desc = 0.15
            elif mes == "diciembre":
                desc = 0.20
            elif mes == "julio":
                desc = 0.10

            total = imp * (1 - desc)
            ventas.append(total)
            lbl.config(text=f"Total: {total}")
        except:
            lbl.config(text="Error")

    def total():
        lbl.config(text=f"Ventas: {sum(ventas)}")

    tk.Button(v, text="Calcular", command=calc).grid(row=3, column=0)
    tk.Button(v, text="Total día", command=total).grid(row=3, column=1)