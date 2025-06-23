import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

ARCHIVO = "Empleados.csv"

# Crear archivo si no existe, con las nuevas columnas
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
            "Fecha Nacimiento", "Sexo", "Último Grado Estudio",
            "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso"
        ])

def empleado_existe(nombre, apellido):
    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            if fila["Nombre"].strip().lower() == nombre.strip().lower() and fila["Apellido"].strip().lower() == apellido.strip().lower():
                return True
    return False

def crear_entrada(frame, texto, fila):
    ttk.Label(frame, text=texto, background="#FFFFFF").grid(row=fila, column=0, pady=5, sticky="e")
    entrada = ttk.Entry(frame, width=30)
    entrada.grid(row=fila, column=1, pady=5)
    return entrada

def crear_combobox(frame, texto, fila, valores):
    ttk.Label(frame, text=texto, background="#FFFEFE").grid(row=fila, column=0, pady=5, sticky="e")
    combobox = ttk.Combobox(frame, values=valores, state="readonly", width=28)
    combobox.grid(row=fila, column=1, pady=5)
    combobox.current(0)
    return combobox

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("450x600")
    ventana.configure(bg="#e0f7fa")
    frame = ttk.Frame(ventana, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    entradas = {}
    entradas["Nombre"] = crear_entrada(frame, "Nombre:", 0)
    entradas["Apellido"] = crear_entrada(frame, "Apellido:", 1)

    puestos = ["Médico", "Enfermero", "Médico General", "Pediatra", "Otorrinolaringólogo", "Cirujano Plástico"]
    ttk.Label(frame, text="Puesto:", background="#FFFFFF").grid(row=2, column=0, pady=5, sticky="e")
    puesto_cb = ttk.Combobox(frame, values=puestos, state="readonly", width=28)
    puesto_cb.grid(row=2, column=1, pady=5)
    puesto_cb.current(0)

    departamento = crear_combobox(frame, "Departamento:", 3, ["1", "2", "3"])
    turno = crear_combobox(frame, "Turno:", 4, ["Matutino", "Vespertino", "Noche"])

    entradas["Fecha Nacimiento"] = crear_entrada(frame, "Fecha de Nacimiento (DD/MM/AAAA):", 5)

    sexo = crear_combobox(frame, "Sexo:", 6, ["Mujer", "Hombre", "Otro"])

    entradas["Último Grado Estudio"] = crear_entrada(frame, "Último Grado de Estudio:", 7)
    entradas["Cédula"] = crear_entrada(frame, "Cédula:", 8)
    entradas["Domicilio"] = crear_entrada(frame, "Domicilio:", 9)
    entradas["Teléfono"] = crear_entrada(frame, "Teléfono:", 10)
    entradas["Correo Electrónico"] = crear_entrada(frame, "Correo Electrónico:", 11)
    entradas["Fecha Ingreso"] = crear_entrada(frame, "Fecha de Ingreso (DD/MM/AAAA):", 12)

    def guardar():
        # Validar campos obligatorios
        campos_obligatorios = ["Nombre", "Apellido", "Fecha Nacimiento", "Último Grado Estudio", "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso"]
        if any(not entradas[c].get().strip() for c in campos_obligatorios) or not puesto_cb.get() or not departamento.get() or not turno.get() or not sexo.get():
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        # Validar formato fechas (opcional, se puede mejorar)
        try:
            datetime.strptime(entradas["Fecha Nacimiento"].get(), "%d/%m/%Y")
            datetime.strptime(entradas["Fecha Ingreso"].get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Use DD/MM/AAAA.")
            return

        if empleado_existe(entradas["Nombre"].get(), entradas["Apellido"].get()):
            messagebox.showerror("Error", "El empleado ya existe.")
            return

        with open(ARCHIVO, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                entradas["Nombre"].get(),
                entradas["Apellido"].get(),
                puesto_cb.get(),
                departamento.get(),
                turno.get(),
                entradas["Fecha Nacimiento"].get(),
                sexo.get(),
                entradas["Último Grado Estudio"].get(),
                entradas["Cédula"].get(),
                entradas["Domicilio"].get(),
                entradas["Teléfono"].get(),
                entradas["Correo Electrónico"].get(),
                entradas["Fecha Ingreso"].get()
            ])
        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=13, column=0, columnspan=2, pady=20)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Lista de Empleados")
    ventana.geometry("900x400")
    ventana.configure(bg="#e0f7fa")

    columnas = [
        "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
        "Fecha Nacimiento", "Sexo", "Último Grado Estudio",
        "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso"
    ]
    tree = ttk.Treeview(ventana, columns=columnas, show='headings')
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            tree.insert("", tk.END, values=[fila[col] for col in columnas])

def eliminar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Eliminar Empleado")
    ventana.geometry("300x150")
    ventana.configure(bg="#e0f7fa")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)

    def eliminar():
        if not nombre.get() or not apellido.get():
            messagebox.showwarning("Error", "Completa ambos campos.")
            return

        if not empleado_existe(nombre.get(), apellido.get()):
            messagebox.showerror("Error", "Dato no existente.")
            return

        empleados_actualizados = []
        with open(ARCHIVO, "r") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                if not (fila["Nombre"].strip().lower() == nombre.get().strip().lower() and
                        fila["Apellido"].strip().lower() == apellido.get().strip().lower()):
                    empleados_actualizados.append(fila)

        with open(ARCHIVO, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=empleados_actualizados[0].keys() if empleados_actualizados else [
                "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
                "Fecha Nacimiento", "Sexo", "Último Grado Estudio",
                "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso"
            ])
            writer.writeheader()
            writer.writerows(empleados_actualizados)

        messagebox.showinfo("Éxito", "Empleado eliminado.")
        ventana.destroy()

    ttk.Button(frame, text="Eliminar", command=eliminar).grid(row=2, column=0, columnspan=2, pady=10)

def registrar_asistencia():
    ventana = tk.Toplevel()
    ventana.title("Registrar Asistencia")
    ventana.geometry("300x150")
    ventana.configure(bg="#e0f7fa")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)

    def registrar():
        if empleado_existe(nombre.get(), apellido.get()):
            messagebox.showinfo("Éxito", "Asistencia registrada.")
        else:
            messagebox.showerror("Error", "Dato no existente.")
        ventana.destroy()

    ttk.Button(frame, text="Registrar", command=registrar).grid(row=2, column=0, columnspan=2, pady=10)

def retardos_permisos():
    ventana = tk.Toplevel()
    ventana.title("Retardos y Permisos")
    ventana.geometry("300x200")
    ventana.configure(bg="#e0f7fa")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    tipo = crear_entrada(frame, "Tipo (Retardo/Permiso):", 2)

    def guardar():
        if empleado_existe(nombre.get(), apellido.get()):
            messagebox.showinfo("Éxito", f"{tipo.get()} registrado.")
        else:
            messagebox.showerror("Error", "Dato no existente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

def registrar_incapacidad():
    ventana = tk.Toplevel()
    ventana.title("Registrar Incapacidad")
    ventana.geometry("300x200")
    ventana.configure(bg="#5dafb9")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    dias = crear_entrada(frame, "Días de incapacidad:", 2)

    def guardar():
        if not dias.get().isdigit():
            messagebox.showerror("Error", "Ingrese un número válido de días.")
            return
        if empleado_existe(nombre.get(), apellido.get()):
            messagebox.showinfo("Éxito", f"Incapacidad registrada por {dias.get()} días.")
        else:
            messagebox.showerror("Error", "Dato no existente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

def registrar_vacaciones():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vacaciones")
    ventana.geometry("300x220")
    ventana.configure(bg="#e0f7fa")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    inicio = crear_entrada(frame, "Fecha de inicio:", 2)
    fin = crear_entrada(frame, "Fecha de fin:", 3)

    def guardar():
        if empleado_existe(nombre.get(), apellido.get()):
            messagebox.showinfo("Éxito", f"Vacaciones registradas del {inicio.get()} al {fin.get()}.")
        else:
            messagebox.showerror("Error", "Dato no existente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=10)

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario - Control de Personal")
    ventana.geometry("700x400")
    ventana.configure(bg="#4498a3")

    tk.Label(ventana, text="Sistema de Control de Personal Hospitalario", font=("Helvetica", 16, "bold"), bg="#b2ebf2").pack(pady=30)

    def activar_menu():
        ventana.config(menu=menu_principal)
        boton_menu.pack_forget()
        tk.Label(ventana, text="Menú activado.", fg="green", bg="#b2ebf2", font=("Arial", 10)).pack()

    global boton_menu
    boton_menu = ttk.Button(ventana, text="Ir al menú de opciones", command=activar_menu)
    boton_menu.pack(pady=10)

    global menu_principal
    menu_principal = tk.Menu(ventana)
    opciones = tk.Menu(menu_principal, tearoff=0)
    opciones.add_command(label="Registrar Empleado", command=registrar_empleado)
    opciones.add_command(label="Ver Empleados", command=ver_empleados)
    opciones.add_command(label="Eliminar Empleado", command=eliminar_empleado)
    opciones.add_command(label="Registrar Asistencia", command=registrar_asistencia)
    opciones.add_command(label="Retardos y Permisos", command=retardos_permisos)
    opciones.add_command(label="Registrar Incapacidad", command=registrar_incapacidad)
    opciones.add_command(label="Registrar Vacaciones", command=registrar_vacaciones)

    menu_principal.add_cascade(label="Opciones", menu=opciones)
    ventana.mainloop()

crear_menu()
