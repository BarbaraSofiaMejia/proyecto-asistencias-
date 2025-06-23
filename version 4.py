import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

ARCHIVO = "Empleados.csv"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
            "Sexo", "Teléfono", "Correo"
        ])

def empleado_existe(nombre, apellido):
    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["Nombre"].strip().lower() == nombre.lower() and fila["Apellido"].strip().lower() == apellido.lower():
                return True
    return False

def crear_entrada(frame, texto, fila):
    ttk.Label(frame, text=texto).grid(row=fila, column=0, sticky="e", pady=4)
    entrada = ttk.Entry(frame)
    entrada.grid(row=fila, column=1, pady=4)
    return entrada

def crear_combobox(frame, texto, fila, opciones):
    ttk.Label(frame, text=texto).grid(row=fila, column=0, sticky="e", pady=4)
    cb = ttk.Combobox(frame, values=opciones, state="readonly")
    cb.grid(row=fila, column=1, pady=4)
    cb.current(0)
    return cb

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("420x400")
    ventana.configure(bg="#f0f4f8")
    frame = ttk.Frame(ventana, padding=20)
    frame.pack()

    entradas = {}
    entradas["Nombre"] = crear_entrada(frame, "Nombre:", 0)
    entradas["Apellido"] = crear_entrada(frame, "Apellido:", 1)

    puesto_cb = crear_combobox(frame, "Puesto:", 2, ["Médico", "Enfermero", "Recepción"])
    dep_cb = crear_combobox(frame, "Departamento:", 3, ["Urgencias", "Pediatría", "Admin"])
    turno_cb = crear_combobox(frame, "Turno:", 4, ["Matutino", "Vespertino", "Noche"])
    sexo_cb = crear_combobox(frame, "Sexo:", 5, ["Mujer", "Hombre", "Otro"])

    entradas["Teléfono"] = crear_entrada(frame, "Teléfono:", 6)
    entradas["Correo"] = crear_entrada(frame, "Correo:", 7)

    def guardar():
        datos = {k: v.get().strip() for k, v in entradas.items()}
        if not all(datos.values()):
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        if empleado_existe(datos["Nombre"], datos["Apellido"]):
            messagebox.showerror("Duplicado", "Ese empleado ya está registrado.")
            return

        with open(ARCHIVO, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datos["Nombre"], datos["Apellido"], puesto_cb.get(), dep_cb.get(),
                turno_cb.get(), sexo_cb.get(), datos["Teléfono"], datos["Correo"]
            ])
        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=8, column=0, columnspan=2, pady=20)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Lista de Empleados")
    ventana.geometry("800x300")
    ventana.configure(bg="#e0f7fa")

    columnas = ["Nombre", "Apellido", "Puesto", "Departamento", "Turno", "Sexo", "Teléfono", "Correo"]
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=90, anchor="center")
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            tree.insert("", tk.END, values=[fila[col] for col in columnas])

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario - Personal")
    ventana.geometry("400x250")
    ventana.configure(bg="#a8dadc")

    tk.Label(ventana, text="Menú Principal", font=("Helvetica", 16), bg="#a8dadc").pack(pady=20)
    ttk.Button(ventana, text="Registrar Empleado", command=registrar_empleado).pack(pady=10)
    ttk.Button(ventana, text="Ver Empleados", command=ver_empleados).pack(pady=10)

    ventana.mainloop()

crear_menu()
