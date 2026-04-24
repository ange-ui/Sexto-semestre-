import customtkinter as ctk
import pandas as pd

def abrir_consultas():
    app = ctk.CTk()
    app.title("Consultas IA")
    app.geometry("800x500")

    # Datos de ejemplo (puedes cambiarlo por Titanic u otro dataset)
    data = {
        "Nombre": ["Ana", "Luis", "Carlos", "Sofia", "Pedro"],
        "Edad": [23, 35, 29, 40, 22],
        "Salario": [8000, 12000, 9500, 15000, 7000]
    }

    df = pd.DataFrame(data)

    frame_botones = ctk.CTkFrame(app)
    frame_botones.pack(side="left", fill="y", padx=10, pady=10)

    frame_resultado = ctk.CTkFrame(app)
    frame_resultado.pack(side="right", expand=True, fill="both", padx=10, pady=10)

    textbox = ctk.CTkTextbox(frame_resultado)
    textbox.pack(expand=True, fill="both")

    def mostrar(resultado):
        textbox.delete("1.0", "end")
        textbox.insert("end", str(resultado))

    # 🔟 CONSULTAS COMPLEJAS

    ctk.CTkButton(frame_botones, text="1. Promedio edad",
                  command=lambda: mostrar(df["Edad"].mean())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="2. Mayor salario",
                  command=lambda: mostrar(df["Salario"].max())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="3. Menor edad",
                  command=lambda: mostrar(df["Edad"].min())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="4. Filtrar edad > 25",
                  command=lambda: mostrar(df[df["Edad"] > 25])).pack(pady=5)

    ctk.CTkButton(frame_botones, text="5. Ordenar salario",
                  command=lambda: mostrar(df.sort_values(by="Salario"))).pack(pady=5)

    ctk.CTkButton(frame_botones, text="6. Suma salarios",
                  command=lambda: mostrar(df["Salario"].sum())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="7. Conteo registros",
                  command=lambda: mostrar(df.shape[0])).pack(pady=5)

    ctk.CTkButton(frame_botones, text="8. Desviación estándar",
                  command=lambda: mostrar(df["Salario"].std())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="9. Mediana edad",
                  command=lambda: mostrar(df["Edad"].median())).pack(pady=5)

    ctk.CTkButton(frame_botones, text="10. Edad + salario alto",
                  command=lambda: mostrar(df[(df["Edad"] > 25) & (df["Salario"] > 9000)])).pack(pady=5)

    app.mainloop()