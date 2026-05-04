import customtkinter as ctk
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import messagebox
import warnings
warnings.filterwarnings("ignore")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATASET_PATH = "/mnt/user-data/uploads/heart_disease_uci.csv"

COLORS = {
    "bg":        "#0f0f1a",
    "panel":     "#1a1a2e",
    "card":      "#16213e",
    "accent":    "#0f3460",
    "blue":      "#4361ee",
    "cyan":      "#4cc9f0",
    "purple":    "#7209b7",
    "pink":      "#f72585",
    "green":     "#06d6a0",
    "yellow":    "#ffd60a",
    "red":       "#ef233c",
    "text":      "#e2e8f0",
    "subtext":   "#94a3b8",
    "border":    "#334155",
}


def validar_numero(valor: str, nombre: str) -> tuple[bool, float, str]:
    """Valida que el valor sea un número real válido."""
    if valor.strip() == "":
        return False, 0.0, f"⚠ El campo '{nombre}' está vacío."
    try:
        num = float(valor.replace(",", "."))
        if np.isnan(num) or np.isinf(num):
            return False, 0.0, f"⚠ '{nombre}' no puede ser NaN o infinito."
        return True, num, ""
    except ValueError:
        return False, 0.0, f"⚠ '{nombre}' debe ser un número válido. Recibido: '{valor}'"

def validar_rango(x_min: str, x_max: str) -> tuple[bool, float, float, str]:
    ok1, xmin, err1 = validar_numero(x_min, "X mín")
    ok2, xmax, err2 = validar_numero(x_max, "X máx")
    if not ok1:
        return False, 0, 0, err1
    if not ok2:
        return False, 0, 0, err2
    if xmin >= xmax:
        return False, 0, 0, "⚠ X mín debe ser menor que X máx."
    if abs(xmax - xmin) < 1e-10:
        return False, 0, 0, "⚠ El rango es demasiado pequeño para graficar."
    return True, xmin, xmax, ""


#  Aplicación principal 

class LinearApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Generador de Funciones Lineales  |  f(x) = mx + b")
        self.geometry("1280x820")
        self.minsize(1000, 700)
        self.configure(fg_color=COLORS["bg"])

        # Estado
        self.df = self._cargar_dataset()
        self.funciones: list[dict] = []          # historial de funciones
        self.mostrar_dataset = ctk.BooleanVar(value=False)
        self.col_x = ctk.StringVar()
        self.col_y = ctk.StringVar()
        self.mostrar_cuadricula = ctk.BooleanVar(value=True)
        self.mostrar_ecuacion   = ctk.BooleanVar(value=True)

        self._construir_ui()
        self._actualizar_columnas()

    # ─ Dataset 
    def _cargar_dataset(self) -> pd.DataFrame:
        try:
            df = pd.read_csv(DATASET_PATH)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el dataset:\n{e}")
            return pd.DataFrame()

    def _columnas_numericas(self) -> list[str]:
        if self.df.empty:
            return []
        return list(self.df.select_dtypes(include=[np.number]).columns)

    #  UI 
    def _construir_ui(self):
        #  Encabezado 
        header = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=0, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="  📈  Generador de Funciones Lineales",
            font=ctk.CTkFont("Courier New", 22, "bold"),
            text_color=COLORS["cyan"],
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkLabel(
            header,
            text="f(x) = mx + b",
            font=ctk.CTkFont("Courier New", 18, "italic"),
            text_color=COLORS["yellow"],
        ).pack(side="right", padx=20)

        #  Cuerpo principal 
        body = ctk.CTkFrame(self, fg_color=COLORS["bg"])
        body.pack(fill="both", expand=True, padx=12, pady=8)

        # Panel izquierdo (controles)
        self.panel_izq = ctk.CTkFrame(body, fg_color=COLORS["panel"], width=320, corner_radius=12)
        self.panel_izq.pack(side="left", fill="y", padx=(0, 8))
        self.panel_izq.pack_propagate(False)

        # Panel derecho (gráfica)
        self.panel_der = ctk.CTkFrame(body, fg_color=COLORS["panel"], corner_radius=12)
        self.panel_der.pack(side="left", fill="both", expand=True)

        self._construir_controles()
        self._construir_grafica()

    #  Panel de controles 
    def _construir_controles(self):
        p = self.panel_izq

        scroll = ctk.CTkScrollableFrame(p, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        def seccion(titulo, color=COLORS["cyan"]):
            ctk.CTkLabel(
                scroll, text=titulo,
                font=ctk.CTkFont("Courier New", 13, "bold"),
                text_color=color,
            ).pack(anchor="w", pady=(14, 2))
            sep = ctk.CTkFrame(scroll, fg_color=color, height=2)
            sep.pack(fill="x", pady=(0, 6))

        def campo(parent, label, placeholder, textvariable=None):
            ctk.CTkLabel(parent, text=label,
                         font=ctk.CTkFont(size=12),
                         text_color=COLORS["subtext"]).pack(anchor="w")
            e = ctk.CTkEntry(
                parent, placeholder_text=placeholder,
                font=ctk.CTkFont("Courier New", 13),
                fg_color=COLORS["card"], border_color=COLORS["border"],
                text_color=COLORS["text"], height=36,
                textvariable=textvariable,
            )
            e.pack(fill="x", pady=(2, 6))
            return e

        #  Parámetros de la función 
        seccion("PARÁMETROS DE f(x)")

        self.entry_m = campo(scroll, "Pendiente  m", "ej: 2.5")
        self.entry_b = campo(scroll, "Término independiente  b", "ej: -1")

        #  Rango X 
        seccion("RANGO DEL EJE X")

        fila_rango = ctk.CTkFrame(scroll, fg_color="transparent")
        fila_rango.pack(fill="x")
        fila_rango.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(fila_rango, text="X mín", font=ctk.CTkFont(size=12),
                     text_color=COLORS["subtext"]).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(fila_rango, text="X máx", font=ctk.CTkFont(size=12),
                     text_color=COLORS["subtext"]).grid(row=0, column=1, sticky="w", padx=(8, 0))

        self.entry_xmin = ctk.CTkEntry(fila_rango, placeholder_text="-10",
                                       font=ctk.CTkFont("Courier New", 13),
                                       fg_color=COLORS["card"], border_color=COLORS["border"],
                                       text_color=COLORS["text"], height=36)
        self.entry_xmin.grid(row=1, column=0, sticky="ew", pady=(2, 6))

        self.entry_xmax = ctk.CTkEntry(fila_rango, placeholder_text="10",
                                       font=ctk.CTkFont("Courier New", 13),
                                       fg_color=COLORS["card"], border_color=COLORS["border"],
                                       text_color=COLORS["text"], height=36)
        self.entry_xmax.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(2, 6))

        # Valores por defecto
        self.entry_xmin.insert(0, "-10")
        self.entry_xmax.insert(0, "10")

        #  Opciones visuales 
        seccion(" OPCIONES VISUALES")

        ctk.CTkSwitch(scroll, text="Mostrar cuadrícula",
                      variable=self.mostrar_cuadricula,
                      font=ctk.CTkFont(size=12),
                      button_color=COLORS["blue"],
                      progress_color=COLORS["cyan"]).pack(anchor="w", pady=2)

        ctk.CTkSwitch(scroll, text="Mostrar ecuación en gráfica",
                      variable=self.mostrar_ecuacion,
                      font=ctk.CTkFont(size=12),
                      button_color=COLORS["blue"],
                      progress_color=COLORS["cyan"]).pack(anchor="w", pady=2)

        #  Dataset UCI 
        seccion("DATASET HEART DISEASE UCI", color=COLORS["pink"])

        ctk.CTkSwitch(scroll, text="Superponer puntos del dataset",
                      variable=self.mostrar_dataset,
                      font=ctk.CTkFont(size=12),
                      button_color=COLORS["purple"],
                      progress_color=COLORS["pink"],
                      command=self._toggle_dataset).pack(anchor="w", pady=2)

        self.frame_cols = ctk.CTkFrame(scroll, fg_color="transparent")
        self.frame_cols.pack(fill="x")

        ctk.CTkLabel(self.frame_cols, text="Columna X  (eje horizontal)",
                     font=ctk.CTkFont(size=12),
                     text_color=COLORS["subtext"]).pack(anchor="w", pady=(6, 0))
        self.combo_x = ctk.CTkOptionMenu(
            self.frame_cols, variable=self.col_x,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["card"], button_color=COLORS["purple"],
            dropdown_fg_color=COLORS["card"],
        )
        self.combo_x.pack(fill="x", pady=(2, 6))

        ctk.CTkLabel(self.frame_cols, text="Columna Y  (eje vertical)",
                     font=ctk.CTkFont(size=12),
                     text_color=COLORS["subtext"]).pack(anchor="w")
        self.combo_y = ctk.CTkOptionMenu(
            self.frame_cols, variable=self.col_y,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["card"], button_color=COLORS["purple"],
            dropdown_fg_color=COLORS["card"],
        )
        self.combo_y.pack(fill="x", pady=(2, 6))
        self.frame_cols.pack_forget()   # oculto por defecto

        #  Botones 
        seccion("ACCIONES")

        ctk.CTkButton(
            scroll, text="▶  Graficar  f(x)", height=42,
            font=ctk.CTkFont("Courier New", 14, "bold"),
            fg_color=COLORS["blue"], hover_color=COLORS["accent"],
            command=self._graficar,
        ).pack(fill="x", pady=4)

        ctk.CTkButton(
            scroll, text="➕  Agregar al historial", height=36,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["purple"], hover_color="#5a189a",
            command=self._agregar_historial,
        ).pack(fill="x", pady=2)

        ctk.CTkButton(
            scroll, text="🗑  Limpiar todo", height=36,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["red"], hover_color="#b5172d",
            command=self._limpiar,
        ).pack(fill="x", pady=2)

        #  Resultado f(x) 
        seccion("EVALUAR UN PUNTO")

        self.entry_px = campo(scroll, "Valor de x₀", "ej: 3")
        self.label_fx = ctk.CTkLabel(
            scroll, text="f(x₀) = —",
            font=ctk.CTkFont("Courier New", 15, "bold"),
            text_color=COLORS["green"],
        )
        self.label_fx.pack(anchor="w", pady=4)
        ctk.CTkButton(
            scroll, text="Calcular f(x₀)", height=34,
            font=ctk.CTkFont(size=12),
            fg_color=COLORS["green"], hover_color="#04a07a", text_color="#000",
            command=self._evaluar_punto,
        ).pack(fill="x", pady=2)

        #  Mensaje de estado 
        self.label_status = ctk.CTkLabel(
            p, text="", wraplength=290,
            font=ctk.CTkFont(size=11),
            text_color=COLORS["yellow"],
        )
        self.label_status.pack(pady=6, padx=8)

    #  Panel de gráfica 
    def _construir_grafica(self):
        p = self.panel_der

        # Info superior
        top = ctk.CTkFrame(p, fg_color=COLORS["card"], corner_radius=8, height=48)
        top.pack(fill="x", padx=10, pady=(10, 4))
        top.pack_propagate(False)

        self.label_ecuacion = ctk.CTkLabel(
            top, text="f(x) = mx + b",
            font=ctk.CTkFont("Courier New", 17, "bold"),
            text_color=COLORS["yellow"],
        )
        self.label_ecuacion.pack(side="left", padx=16)

        self.label_info = ctk.CTkLabel(
            top, text="Dataset: Heart Disease UCI  |  921 registros",
            font=ctk.CTkFont(size=11),
            text_color=COLORS["subtext"],
        )
        self.label_info.pack(side="right", padx=16)

        # Historial de funciones
        hist_frame = ctk.CTkFrame(p, fg_color=COLORS["card"], corner_radius=8, height=44)
        hist_frame.pack(fill="x", padx=10, pady=(0, 4))
        hist_frame.pack_propagate(False)

        ctk.CTkLabel(hist_frame, text="Historial:",
                     font=ctk.CTkFont(size=11), text_color=COLORS["subtext"]).pack(side="left", padx=8)

        self.label_historial = ctk.CTkLabel(
            hist_frame, text="—",
            font=ctk.CTkFont("Courier New", 11),
            text_color=COLORS["cyan"], wraplength=700,
        )
        self.label_historial.pack(side="left", padx=4)

        # Figura matplotlib
        fig_frame = ctk.CTkFrame(p, fg_color=COLORS["bg"], corner_radius=8)
        fig_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.fig = Figure(figsize=(9, 6), dpi=100, facecolor=COLORS["bg"])
        self.ax  = self.fig.add_subplot(111)
        self._estilizar_axes()

        self.canvas = FigureCanvasTkAgg(self.fig, master=fig_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        toolbar_frame = ctk.CTkFrame(fig_frame, fg_color=COLORS["panel"], height=30)
        toolbar_frame.pack(fill="x")
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.config(background=COLORS["panel"])
        toolbar.update()

        self._dibujar_placeholder()

    def _estilizar_axes(self):
        ax = self.ax
        ax.set_facecolor(COLORS["card"])
        ax.tick_params(colors=COLORS["subtext"], labelsize=9)
        ax.xaxis.label.set_color(COLORS["text"])
        ax.yaxis.label.set_color(COLORS["text"])
        ax.title.set_color(COLORS["cyan"])
        for spine in ax.spines.values():
            spine.set_edgecolor(COLORS["border"])

    def _dibujar_placeholder(self):
        self.ax.clear()
        self._estilizar_axes()
        self.ax.set_title("Ingresa los parámetros y presiona  ▶ Graficar",
                          fontsize=13, color=COLORS["subtext"], style="italic")
        self.ax.set_xlabel("x", fontsize=11)
        self.ax.set_ylabel("f(x)", fontsize=11)
        self.ax.axhline(0, color=COLORS["border"], linewidth=0.8)
        self.ax.axvline(0, color=COLORS["border"], linewidth=0.8)
        self.canvas.draw()

    #  Lógica de graficación 
    def _graficar(self):
        # Validaciones
        ok_m, m, err_m = validar_numero(self.entry_m.get(), "Pendiente m")
        if not ok_m:
            self._set_status(err_m, error=True)
            return

        ok_b, b, err_b = validar_numero(self.entry_b.get(), "Término b")
        if not ok_b:
            self._set_status(err_b, error=True)
            return

        ok_r, xmin, xmax, err_r = validar_rango(self.entry_xmin.get(), self.entry_xmax.get())
        if not ok_r:
            self._set_status(err_r, error=True)
            return

        # Todo válido → graficar
        self._dibujar(m, b, xmin, xmax)

    def _dibujar(self, m: float, b: float, xmin: float, xmax: float):
        self.ax.clear()
        self._estilizar_axes()

        x = np.linspace(xmin, xmax, 600)
        y = m * x + b

        # Función principal
        line_color = COLORS["cyan"]
        self.ax.plot(x, y, color=line_color, linewidth=2.5, zorder=4,
                     label=f"f(x) = {m:g}x + {b:g}")

        # Líneas de referencia
        self.ax.axhline(0, color=COLORS["border"], linewidth=0.8, zorder=1)
        self.ax.axvline(0, color=COLORS["border"], linewidth=0.8, zorder=1)

        # Punto de intersección con eje Y
        self.ax.scatter([0], [b], color=COLORS["yellow"], zorder=6, s=60,
                        label=f"(0, {b:g})  intersección Y")

        # Intersección con eje X (si existe)
        if m != 0:
            x0 = -b / m
            if xmin <= x0 <= xmax:
                self.ax.scatter([x0], [0], color=COLORS["pink"], zorder=6, s=60,
                                label=f"({x0:.3g}, 0)  raíz")

        # Dataset superpuesto
        if self.mostrar_dataset.get() and not self.df.empty:
            cx, cy = self.col_x.get(), self.col_y.get()
            if cx and cy and cx in self.df.columns and cy in self.df.columns:
                sub = self.df[[cx, cy]].dropna()
                self.ax.scatter(sub[cx], sub[cy],
                                color=COLORS["purple"], alpha=0.35, s=18,
                                zorder=2, label=f"Dataset: {cx} vs {cy}")

        # Historial de funciones (líneas fantasma)
        colores_hist = [COLORS["green"], COLORS["pink"], COLORS["yellow"], "#ff9f1c", "#e040fb"]
        for i, fn in enumerate(self.funciones[-5:]):
            xh = np.linspace(fn["xmin"], fn["xmax"], 400)
            yh = fn["m"] * xh + fn["b"]
            self.ax.plot(xh, yh, color=colores_hist[i % len(colores_hist)],
                         linewidth=1.2, linestyle="--", alpha=0.6,
                         label=f"f(x) = {fn['m']:g}x + {fn['b']:g}  (hist.)")

        # Cuadrícula
        if self.mostrar_cuadricula.get():
            self.ax.grid(True, color=COLORS["border"], linewidth=0.5, alpha=0.6)

        # Ecuación en la gráfica
        if self.mostrar_ecuacion.get():
            signo = "+" if b >= 0 else "−"
            eq_txt = f"f(x) = {m:g}x  {signo}  {abs(b):g}"
            self.ax.text(
                0.02, 0.97, eq_txt,
                transform=self.ax.transAxes,
                fontsize=13, color=COLORS["yellow"],
                verticalalignment="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor=COLORS["accent"],
                          edgecolor=COLORS["border"], alpha=0.85),
            )

        self.ax.set_xlabel("x", fontsize=11, color=COLORS["text"])
        self.ax.set_ylabel("f(x)", fontsize=11, color=COLORS["text"])
        self.ax.set_title(f"Función Lineal   f(x) = {m:g}x + {b:g}",
                          fontsize=13, color=COLORS["cyan"], pad=10)

        legend = self.ax.legend(
            loc="lower right", fontsize=9,
            facecolor=COLORS["card"], edgecolor=COLORS["border"],
            labelcolor=COLORS["text"],
        )

        self.canvas.draw()

        # Actualizar etiquetas
        signo = "+" if b >= 0 else "−"
        self.label_ecuacion.configure(text=f"f(x) = {m:g}x  {signo}  {abs(b):g}")
        self._set_status(f"✔ Graficado: f(x) = {m:g}x + {b:g}  |  x ∈ [{xmin:g}, {xmax:g}]",
                         error=False)

    #  Historial 
    def _agregar_historial(self):
        ok_m, m, err_m = validar_numero(self.entry_m.get(), "Pendiente m")
        ok_b, b, err_b = validar_numero(self.entry_b.get(), "Término b")
        ok_r, xmin, xmax, err_r = validar_rango(self.entry_xmin.get(), self.entry_xmax.get())

        if not ok_m:
            self._set_status(err_m, error=True); return
        if not ok_b:
            self._set_status(err_b, error=True); return
        if not ok_r:
            self._set_status(err_r, error=True); return

        entry = {"m": m, "b": b, "xmin": xmin, "xmax": xmax}
        if entry not in self.funciones:
            self.funciones.append(entry)
            textos = [f"f(x)={fn['m']:g}x+{fn['b']:g}" for fn in self.funciones[-5:]]
            self.label_historial.configure(text="  |  ".join(textos))
            self._set_status(f"✔ Función agregada al historial ({len(self.funciones)} total).", error=False)
        else:
            self._set_status("ℹ Esta función ya está en el historial.", error=False)

    #  Evaluar punto 
    def _evaluar_punto(self):
        ok_m, m, _ = validar_numero(self.entry_m.get(), "m")
        ok_b, b, _ = validar_numero(self.entry_b.get(), "b")
        ok_x, px, err = validar_numero(self.entry_px.get(), "x₀")

        if not ok_m or not ok_b:
            self._set_status("⚠ Primero define m y b válidos.", error=True); return
        if not ok_x:
            self._set_status(err, error=True); return

        resultado = m * px + b
        self.label_fx.configure(text=f"f({px:g}) = {resultado:.6g}")
        self._set_status(f"✔ f({px:g}) = {resultado:.6g}", error=False)

    #  Limpiar 
    def _limpiar(self):
        self.funciones.clear()
        self.label_historial.configure(text="—")
        self.label_ecuacion.configure(text="f(x) = mx + b")
        self.label_fx.configure(text="f(x₀) = —")
        for e in (self.entry_m, self.entry_b, self.entry_px):
            e.delete(0, "end")
        self.entry_xmin.delete(0, "end"); self.entry_xmin.insert(0, "-10")
        self.entry_xmax.delete(0, "end"); self.entry_xmax.insert(0, "10")
        self._set_status("", error=False)
        self._dibujar_placeholder()

    #  Dataset toggle 
    def _toggle_dataset(self):
        if self.mostrar_dataset.get():
            self.frame_cols.pack(fill="x")
        else:
            self.frame_cols.pack_forget()

    def _actualizar_columnas(self):
        cols = self._columnas_numericas()
        if cols:
            self.combo_x.configure(values=cols)
            self.combo_y.configure(values=cols)
            self.col_x.set(cols[0] if len(cols) > 0 else "")
            self.col_y.set(cols[1] if len(cols) > 1 else cols[0])

    #  Utilidad 
    def _set_status(self, msg: str, error: bool = False):
        color = COLORS["red"] if error else COLORS["green"]
        self.label_status.configure(text=msg, text_color=color)


#  Punto de entrada 
if __name__ == "__main__":
    app = LinearApp()
    app.mainloop()
