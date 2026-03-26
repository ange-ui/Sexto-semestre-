import tkinter as tk

trabajadores = []

def abrir():
    v = tk.Toplevel()

    e1 = tk.Entry(v); e1.grid(row=0, column=1)
    e2 = tk.Entry(v); e2.grid(row=1, column=1)
    e3 = tk.Entry(v); e3.grid(row=2, column=1)
    e4 = tk.Entry(v); e4.grid(row=3, column=1)
    e5 = tk.Entry(v); e5.grid(row=4, column=1)

    tk.Label(v, text="Nombre").grid(row=0, column=0)
    tk.Label(v, text="Horas normales").grid(row=1, column=0)
    tk.Label(v, text="Pago hora").grid(row=2, column=0)
    tk.Label(v, text="Horas extra").grid(row=3, column=0)
    tk.Label(v, text="Hijos").grid(row=4, column=0)

    lbl = tk.Label(v); lbl.grid(row=6, column=0, columnspan=2)

    def calc():
        try:
            hn = float(e2.get())
            ph = float(e3.get())
            he = float(e4.get())
            h = int(e5.get())

            pago = hn * ph
            extra = he * ph * 1.5
            bono = h * 0.5

            total = pago + extra + bono
            trabajadores.append(total)

            lbl.config(text=f"Total: {total}")
        except:
            lbl.config(text="Error")

    def rep():
        lbl.config(text=f"Pagos: {trabajadores}")

    tk.Button(v, text="Calcular", command=calc).grid(row=5, column=0)
    tk.Button(v, text="Reporte", command=rep).grid(row=5, column=1)
    