import tkinter as tk
import ventana_principal 

USUARIO_VALIDO = "admin"
CONTRASENA_VALIDA = "1234"

def login():
    user = entry_user.get()
    pwd = entry_pass.get()

    if user == USUARIO_VALIDO and pwd == CONTRASENA_VALIDA:
        root.destroy()
        ventana_principal.abrir()
    else:
        lbl_msg.config(text="Usuario o contraseña incorrectos")

root = tk.Tk()
root.title("Login")

tk.Label(root, text="Usuario").grid(row=0, column=0)
entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1)

tk.Label(root, text="Contraseña").grid(row=1, column=0)
entry_pass = tk.Entry(root, show="*")
entry_pass.grid(row=1, column=1)

tk.Button(root, text="Ingresar", command=login).grid(row=2, column=0, columnspan=2)

lbl_msg = tk.Label(root, text="", fg="red")
lbl_msg.grid(row=3, column=0, columnspan=2)

root.bind("<Return>", lambda e: login())

root.mainloop()

