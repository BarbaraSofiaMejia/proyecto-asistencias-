import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

ARCHIVO = "Empleados.csv"

# Crear archivo si no existe
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Puesto"])

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("300x250")
    ventana.configure(bg="#e0f7fa")

    tk.Label(ventana, text="Nombre:", bg="#e0f7fa").pack(pady=5)
    nombre_entry = tk.Entry(ventana)
    nombre_entry.pack()

    tk.Label(ventana, text="Apellido:", bg="#e0f7fa").pack(pady=5)
    apellido_entry = tk.Entry(ventana)
    apellido_entry.pack()

    tk.Label(ventana, text="Puesto:", bg="#e0f7fa").pack(pady=5)
    puesto_cb = ttk.Combobox(ventana, values=["Médico", "Enfermero", "Administrativo"], state="readonly")
    puesto_cb.pack()
    puesto_cb.current(0)

    def guardar():
        nombre = nombre_entry.get().strip()
        apellido = apellido_entry.get().strip()
        puesto = puesto_cb.get().strip()

        if not nombre or not apellido or not puesto:
            messagebox.showwarning("Campos vacíos", "Por favor, llena todos los campos.")
            return

        with open(ARCHIVO, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([nombre, apellido, puesto])

        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=15)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Lista de Empleados")
    ventana.geometry("400x300")
    ventana.configure(bg="#e0f7fa")

    columnas = ["Nombre", "Apellido", "Puesto"]
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            tree.insert("", tk.END, values=[fila["Nombre"], fila["Apellido"], fila["Puesto"]])

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario - Inicio")
    ventana.geometry("400x200")
    ventana.configure(bg="#4498a3")

    tk.Label(ventana, text="Sistema Hospitalario", font=("Helvetica", 16, "bold"), bg="#b2ebf2").pack(pady=20)

    ttk.Button(ventana, text="Registrar Empleado", command=registrar_empleado).pack(pady=10)
    ttk.Button(ventana, text="Ver Empleados", command=ver_empleados).pack(pady=10)

    ventana.mainloop()

crear_menu()
