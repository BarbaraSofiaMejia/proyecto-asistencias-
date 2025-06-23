import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

ARCHIVO = "Empleados.csv"

if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Puesto", "Turno"])

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
    ventana.geometry("300x300")
    ventana.configure(bg="#f0f4f8")

    def entrada(etiqueta):
        tk.Label(ventana, text=etiqueta, bg="#f0f4f8").pack(pady=5)
        campo = tk.Entry(ventana)
        campo.pack()
        return campo

    nombre = entrada("Nombre")
    apellido = entrada("Apellido")

    tk.Label(ventana, text="Puesto", bg="#f0f4f8").pack(pady=5)
    puesto_cb = ttk.Combobox(ventana, values=["Doctor", "Enfermero", "Recepción"], state="readonly")
    puesto_cb.pack()
    puesto_cb.current(0)

    tk.Label(ventana, text="Turno", bg="#f0f4f8").pack(pady=5)
    turno_cb = ttk.Combobox(ventana, values=["Mañana", "Tarde", "Noche"], state="readonly")
    turno_cb.pack()
    turno_cb.current(0)

    def guardar():
        n = nombre.get().strip()
        a = apellido.get().strip()
        p = puesto_cb.get()
        t = turno_cb.get()

        if not n or not a:
            messagebox.showwarning("Campos vacíos", "Debes completar todos los campos.")
            return

        if empleado_existe(n, a):
            messagebox.showerror("Ya existe", "Ese empleado ya está registrado.")
            return

        with open(ARCHIVO, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([n, a, p, t])

        messagebox.showinfo("Registrado", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(ventana, text="Guardar", command=guardar).pack(pady=15)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Lista de Empleados")
    ventana.geometry("500x300")
    ventana.configure(bg="#f0f4f8")

    columnas = ["Nombre", "Apellido", "Puesto", "Turno"]
    tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=100, anchor="center")
    tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO, "r") as f:
        lector = csv.DictReader(f)
        for fila in lector:
            tabla.insert("", tk.END, values=[fila[col] for col in columnas])

def eliminar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Empleado")
    ventana.geometry("300x200")
    ventana.configure(bg="#f0f4f8")

    def entrada(etiqueta):
        tk.Label(ventana, text=etiqueta, bg="#f0f4f8").pack(pady=5)
        campo = tk.Entry(ventana)
        campo.pack()
        return campo

    nombre = entrada("Nombre")
    apellido = entrada("Apellido")

    def eliminar():
        n = nombre.get().strip().lower()
        a = apellido.get().strip().lower()

        if not n or not a:
            messagebox.showwarning("Vacío", "Escribe nombre y apellido.")
            return

        encontrado = False
        nuevos_datos = []

        with open(ARCHIVO, "r") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                if fila["Nombre"].strip().lower() == n and fila["Apellido"].strip().lower() == a:
                    encontrado = True
                else:
                    nuevos_datos.append(fila)

        if not encontrado:
            messagebox.showerror("No encontrado", "Ese empleado no existe.")
            return

        with open(ARCHIVO, "w", newline="") as f:
            escritor = csv.DictWriter(f, fieldnames=["Nombre", "Apellido", "Puesto", "Turno"])
            escritor.writeheader()
            escritor.writerows(nuevos_datos)

        messagebox.showinfo("Eliminado", "Empleado eliminado correctamente.")
        ventana.destroy()

    ttk.Button(ventana, text="Eliminar", command=eliminar).pack(pady=15)

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario")
    ventana.geometry("400x250")
    ventana.configure(bg="#a2d2ff")

    tk.Label(ventana, text="Control de Personal", font=("Helvetica", 16, "bold"), bg="#a2d2ff").pack(pady=20)
    ttk.Button(ventana, text="Registrar Empleado", command=registrar_empleado).pack(pady=5)
    ttk.Button(ventana, text="Ver Empleados", command=ver_empleados).pack(pady=5)
    ttk.Button(ventana, text="Eliminar Empleado", command=eliminar_empleado).pack(pady=5)

    ventana.mainloop()

crear_menu()
