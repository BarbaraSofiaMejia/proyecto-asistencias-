import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

ARCHIVO = "Empleados.csv"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Puesto", "Departamento", "Turno"])

def empleado_existe(nombre, apellido):
    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["Nombre"].strip().lower() == nombre.lower() and fila["Apellido"].strip().lower() == apellido.lower():
                return True
    return False

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("350x400")
    ventana.configure(bg="#e6f2ff")

    def crear_entrada(etiqueta):
        tk.Label(ventana, text=etiqueta + ":", bg="#e6f2ff").pack(pady=5)
        entrada = tk.Entry(ventana)
        entrada.pack()
        return entrada

    nombre = crear_entrada("Nombre")
    apellido = crear_entrada("Apellido")

    tk.Label(ventana, text="Puesto:", bg="#e6f2ff").pack(pady=5)
    puesto_cb = ttk.Combobox(ventana, values=["Médico", "Enfermero", "Recepción", "Administrador"], state="readonly")
    puesto_cb.pack()
    puesto_cb.current(0)

    tk.Label(ventana, text="Departamento:", bg="#e6f2ff").pack(pady=5)
    dep_cb = ttk.Combobox(ventana, values=["Urgencias", "Pediatría", "Laboratorio", "Administración"], state="readonly")
    dep_cb.pack()
    dep_cb.current(0)

    tk.Label(ventana, text="Turno:", bg="#e6f2ff").pack(pady=5)
    turno_cb = ttk.Combobox(ventana, values=["Matutino", "Vespertino", "Noche"], state="readonly")
    turno_cb.pack()
    turno_cb.current(0)

    def guardar():
        nom = nombre.get().strip()
        ape = apellido.get().strip()
        puesto = puesto_cb.get()
        dep = dep_cb.get()
        turno = turno_cb.get()

        if not nom or not ape:
            messagebox.showwarning("Error", "Nombre y apellido son obligatorios.")
            return

        if empleado_existe(nom, ape):
            messagebox.showerror("Error", "Ese empleado ya existe.")
            return

        with open(ARCHIVO, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([nom, ape, puesto, dep, turno])

        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=20)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Ver Empleados")
    ventana.geometry("600x300")
    ventana.configure(bg="#e6f2ff")

    columnas = ["Nombre", "Apellido", "Puesto", "Departamento", "Turno"]
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            tree.insert("", tk.END, values=[fila[col] for col in columnas])

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario")
    ventana.geometry("400x250")
    ventana.configure(bg="#a8dadc")

    tk.Label(ventana, text="Menú del Sistema", font=("Helvetica", 16, "bold"), bg="#a8dadc").pack(pady=20)
    ttk.Button(ventana, text="Registrar Empleado", command=registrar_empleado).pack(pady=10)
    ttk.Button(ventana, text="Ver Empleados", command=ver_empleados).pack(pady=10)

    ventana.mainloop()

crear_menu()
