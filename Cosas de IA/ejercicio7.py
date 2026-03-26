import tkinter as tk

def abrir():
    v = tk.Toplevel()

    e = tk.Entry(v); e.grid(row=0, column=1)
    lbl = tk.Label(v); lbl.grid(row=2, column=0, columnspan=2)

    def calc():
        try:
            n = int(e.get())
            if n > 0:
                nums = list(range(1, n+1))
                lbl.config(text=f"{nums} = {sum(nums)}")
            else:
                lbl.config(text="Error")
        except:
            lbl.config(text="Error")

    tk.Button(v, text="Calcular", command=calc).grid(row=1, column=0, columnspan=2)