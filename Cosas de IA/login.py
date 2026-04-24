import customtkinter as ctk
from tkinter import messagebox
from consultas import abrir_consultas

ARCHIVO_USUARIOS = "usuarios.txt"

def validar_usuario(usuario, password):
    try:
        with open(ARCHIVO_USUARIOS, "r") as f:
            for linea in f:
                user, pwd = linea.strip().split(",")
                if usuario == user and password == pwd:
                    return True
    except:
        messagebox.showerror("Error", "No se pudo leer el archivo")
    return False


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login IA")
        self.geometry("400x300")

        ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 20)).pack(pady=20)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pass.pack(pady=10)

        ctk.CTkButton(self, text="Ingresar", command=self.login).pack(pady=20)

    def login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if not user or not pwd:
            messagebox.showwarning("Campos vacíos", "Llena todos los campos")
            return

        if validar_usuario(user, pwd):
            messagebox.showinfo("Éxito", "Bienvenido")
            self.destroy()
            abrir_consultas()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")