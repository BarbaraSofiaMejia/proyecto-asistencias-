import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

ARCHIVO = "Empleados.csv"
ARCHIVO_VACACIONES = "Vacaciones.csv"
ARCHIVO_PERMISOS = "Permisos.csv"
ARCHIVO_FESTIVOS = "DiasFestivos.csv"
ARCHIVO_TURNOS = "TurnosPersonalizados.csv"
ARCHIVO_ASISTENCIAS = "Asistencias.csv"

# Crear archivos si no existen con encabezados correspondientes
if not os.path.exists(ARCHIVO):
    with open(ARCHIVO, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
            "Fecha Nacimiento", "Sexo", "Último Grado Estudio",
            "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso",
            "Ocupacion"
        ])

if not os.path.exists(ARCHIVO_VACACIONES):
    with open(ARCHIVO_VACACIONES, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Bloque", "Fecha Inicio", "Fecha Fin"])

if not os.path.exists(ARCHIVO_PERMISOS):
    with open(ARCHIVO_PERMISOS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Tipo", "Fecha Inicio", "Fecha Fin", "Días"])

if not os.path.exists(ARCHIVO_FESTIVOS):
    with open(ARCHIVO_FESTIVOS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre Festivo", "Fecha", "Obligatorio"])

if not os.path.exists(ARCHIVO_TURNOS):
    with open(ARCHIVO_TURNOS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Dias", "Hora Inicio", "Hora Fin"])

if not os.path.exists(ARCHIVO_ASISTENCIAS):
    with open(ARCHIVO_ASISTENCIAS, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Apellido", "Fecha", "Hora Entrada", "Turno"])

# Funciones de utilidad

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
    ttk.Label(frame, text=texto, background="#FFFFFF").grid(row=fila, column=0, pady=5, sticky="e")
    combobox = ttk.Combobox(frame, values=valores, state="readonly", width=28)
    combobox.grid(row=fila, column=1, pady=5)
    combobox.current(0)
    return combobox

def registrar_empleado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Empleado")
    ventana.geometry("480x650")
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
    turno = crear_combobox(frame, "Turno:", 4, ["Matutino", "Vespertino", "Noche", "Mixto", "Personalizado"])

    entradas["Fecha Nacimiento"] = crear_entrada(frame, "Fecha de Nacimiento (DD/MM/AAAA):", 5)

    sexo = crear_combobox(frame, "Sexo:", 6, ["Mujer", "Hombre", "Otro"])

    entradas["Último Grado Estudio"] = crear_entrada(frame, "Último Grado de Estudio:", 7)
    entradas["Cédula"] = crear_entrada(frame, "Cédula:", 8)
    entradas["Domicilio"] = crear_entrada(frame, "Domicilio:", 9)
    entradas["Teléfono"] = crear_entrada(frame, "Teléfono:", 10)
    entradas["Correo Electrónico"] = crear_entrada(frame, "Correo Electrónico:", 11)
    entradas["Fecha Ingreso"] = crear_entrada(frame, "Fecha de Ingreso (DD/MM/AAAA):", 12)

    ocupaciones = ["Doctor", "Enfermero", "Limpieza", "Seguridad", "Administrativo", "Otro"]
    ocupacion_cb = crear_combobox(frame, "Ocupación:", 13, ocupaciones)

    def guardar():
        campos_obligatorios = ["Nombre", "Apellido", "Fecha Nacimiento", "Último Grado Estudio", "Cédula", "Domicilio",
                               "Teléfono", "Correo Electrónico", "Fecha Ingreso"]
        if any(not entradas[c].get().strip() for c in campos_obligatorios) or not puesto_cb.get() or not departamento.get() or not turno.get() or not sexo.get() or not ocupacion_cb.get():
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

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
                entradas["Fecha Ingreso"].get(),
                ocupacion_cb.get()
            ])
        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=14, column=0, columnspan=2, pady=20)

def ver_empleados():
    ventana = tk.Toplevel()
    ventana.title("Lista de Empleados")
    ventana.geometry("1000x400")
    ventana.configure(bg="#e0f7fa")

    columnas = [
        "Nombre", "Apellido", "Puesto", "Departamento", "Turno",
        "Fecha Nacimiento", "Sexo", "Último Grado Estudio",
        "Cédula", "Domicilio", "Teléfono", "Correo Electrónico", "Fecha Ingreso", "Ocupacion"
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

def registrar_festivo():
    ventana = tk.Toplevel()
    ventana.title("Registrar Día Festivo")
    ventana.geometry("350x200")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre Festivo:", 0)
    fecha = crear_entrada(frame, "Fecha (DD/MM/AAAA):", 1)
    obligatorio = crear_combobox(frame, "¿Obligatorio?:", 2, ["Sí", "No"])

    def guardar():
        try:
            datetime.strptime(fecha.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "Fecha inválida. Usa DD/MM/AAAA")
            return
        with open(ARCHIVO_FESTIVOS, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([nombre.get(), fecha.get(), obligatorio.get()])
        messagebox.showinfo("Éxito", "Festivo registrado")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=10)

def ver_festivos():
    ventana = tk.Toplevel()
    ventana.title("Días Festivos")
    ventana.geometry("400x300")
    ventana.configure(bg="#e0f7fa")

    columnas = ["Nombre Festivo", "Fecha", "Obligatorio"]
    tree = ttk.Treeview(ventana, columns=columnas, show='headings')
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor='center')
    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    with open(ARCHIVO_FESTIVOS, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            tree.insert("", tk.END, values=[fila[col] for col in columnas])

def registrar_turno_personalizado():
    ventana = tk.Toplevel()
    ventana.title("Registrar Turno Personalizado")
    ventana.geometry("400x300")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    dias = crear_entrada(frame, "Días del turno (Ej: Lunes,Martes):", 2)
    hora_inicio = crear_entrada(frame, "Hora de inicio (HH:MM):", 3)
    hora_fin = crear_entrada(frame, "Hora de fin (HH:MM):", 4)

    def guardar():
        if empleado_existe(nombre.get(), apellido.get()):
            with open(ARCHIVO_TURNOS, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([nombre.get(), apellido.get(), dias.get(), hora_inicio.get(), hora_fin.get()])
            messagebox.showinfo("Éxito", "Turno personalizado registrado")
        else:
            messagebox.showerror("Error", "Empleado no encontrado")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

def registrar_permiso():
    ventana = tk.Toplevel()
    ventana.title("Registrar Permiso")
    ventana.geometry("400x300")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    tipo = crear_combobox(frame, "Tipo de Permiso:", 2, ["Con Sueldo", "Sin Sueldo"])
    inicio = crear_entrada(frame, "Fecha Inicio (DD/MM/AAAA):", 3)
    fin = crear_entrada(frame, "Fecha Fin (DD/MM/AAAA):", 4)

    def guardar():
        try:
            f_inicio = datetime.strptime(inicio.get(), "%d/%m/%Y")
            f_fin = datetime.strptime(fin.get(), "%d/%m/%Y")
            dias = (f_fin - f_inicio).days + 1
            if dias > 31:
                messagebox.showerror("Error", "El permiso no puede ser mayor a 1 mes")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto")
            return

        if empleado_existe(nombre.get(), apellido.get()):
            with open(ARCHIVO_PERMISOS, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([nombre.get(), apellido.get(), tipo.get(), inicio.get(), fin.get(), dias])
            messagebox.showinfo("Éxito", "Permiso registrado")
        else:
            messagebox.showerror("Error", "Empleado no encontrado")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

def registrar_vacaciones():
    ventana = tk.Toplevel()
    ventana.title("Registrar Vacaciones")
    ventana.geometry("400x300")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)

    bloque = crear_combobox(frame, "Bloque:", 2, ["Enero - Junio", "Julio - Diciembre"])
    inicio = crear_entrada(frame, "Fecha de inicio (DD/MM/AAAA):", 3)
    fin = crear_entrada(frame, "Fecha de fin (DD/MM/AAAA):", 4)

    def guardar():
        try:
            f_inicio = datetime.strptime(inicio.get(), "%d/%m/%Y")
            f_fin = datetime.strptime(fin.get(), "%d/%m/%Y")
            if f_fin < f_inicio:
                messagebox.showerror("Error", "La fecha de fin debe ser después de la fecha de inicio")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto")
            return

        if empleado_existe(nombre.get(), apellido.get()):
            with open(ARCHIVO_VACACIONES, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([nombre.get(), apellido.get(), bloque.get(), inicio.get(), fin.get()])
            messagebox.showinfo("Éxito", "Vacaciones registradas")
        else:
            messagebox.showerror("Error", "Empleado no encontrado")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

def registrar_asistencia():
    ventana = tk.Toplevel()
    ventana.title("Registrar Asistencia")
    ventana.geometry("350x200")
    frame = ttk.Frame(ventana, padding="10")
    frame.pack()

    nombre = crear_entrada(frame, "Nombre:", 0)
    apellido = crear_entrada(frame, "Apellido:", 1)
    fecha = crear_entrada(frame, "Fecha (DD/MM/AAAA):", 2)
    hora_entrada = crear_entrada(frame, "Hora de entrada (HH:MM):", 3)
    turno = crear_combobox(frame, "Turno:", 4, ["Matutino", "Vespertino", "Noche", "Mixto", "Personalizado"])

    def guardar():
        try:
            datetime.strptime(fecha.get(), "%d/%m/%Y")
            datetime.strptime(hora_entrada.get(), "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha o hora incorrecto")
            return

        if empleado_existe(nombre.get(), apellido.get()):
            with open(ARCHIVO_ASISTENCIAS, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([nombre.get(), apellido.get(), fecha.get(), hora_entrada.get(), turno.get()])
            messagebox.showinfo("Éxito", "Asistencia registrada")
        else:
            messagebox.showerror("Error", "Empleado no encontrado")
        ventana.destroy()

    ttk.Button(frame, text="Guardar", command=guardar).grid(row=5, column=0, columnspan=2, pady=10)

def crear_menu():
    ventana = tk.Tk()
    ventana.title("Sistema Hospitalario - Control de Personal")
    ventana.geometry("750x450")
    ventana.configure(bg="#4498a3")

    tk.Label(ventana, text="Sistema de Control de Personal Hospitalario", font=("Helvetica", 16, "bold"), bg="#b2ebf2").pack(pady=30)

    menu_principal = tk.Menu(ventana)
    opciones = tk.Menu(menu_principal, tearoff=0)

    opciones.add_command(label="Registrar Empleado", command=registrar_empleado)
    opciones.add_command(label="Ver Empleados", command=ver_empleados)
    opciones.add_separator()
    opciones.add_command(label="Registrar Día Festivo", command=registrar_festivo)
    opciones.add_command(label="Ver Días Festivos", command=ver_festivos)
    opciones.add_separator()
    opciones.add_command(label="Registrar Vacaciones", command=registrar_vacaciones)
    opciones.add_command(label="Registrar Permiso", command=registrar_permiso)
    opciones.add_command(label="Registrar Turno Personalizado", command=registrar_turno_personalizado)
    opciones.add_command(label="Registrar Asistencia", command=registrar_asistencia)
    opciones.add_separator()
    opciones.add_command(label="Salir", command=ventana.quit)

    menu_principal.add_cascade(label="Opciones", menu=opciones)
    ventana.config(menu=menu_principal)

    ventana.mainloop()

crear_menu()
