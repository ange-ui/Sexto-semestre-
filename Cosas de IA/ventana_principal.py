import tkinter as tk
import ejercicio1, ejercicio2, ejercicio3, ejercicio4, ejercicio5
import ejercicio6, ejercicio7, ejercicio8, ejercicio9, ejercicio10

def abrir():
    ventana = tk.Tk()
    ventana.title("Menú Principal")

    tk.Label(ventana, text="Menú Principal").grid(row=0, column=0, columnspan=2)

    botones = [
        ("1. Sueldos", ejercicio1.abrir),
        ("2. Parque", ejercicio2.abrir),
        ("3. Tienda", ejercicio3.abrir),
        ("4. < 10", ejercicio4.abrir),
        ("5. Rango", ejercicio5.abrir),
        ("6. Historial", ejercicio6.abrir),
        ("7. Suma n", ejercicio7.abrir),
        ("8. Acumulativa", ejercicio8.abrir),
        ("9. >100", ejercicio9.abrir),
        ("10. Pagos", ejercicio10.abrir),
    ]

    fila = 1
    for texto, comando in botones:
        tk.Button(ventana, text=texto, command=comando).grid(row=fila, column=0, columnspan=2, pady=2)
        fila += 1

    tk.Button(ventana, text="Salir", command=ventana.destroy).grid(row=fila, column=0, columnspan=2)

    ventana.mainloop()

    