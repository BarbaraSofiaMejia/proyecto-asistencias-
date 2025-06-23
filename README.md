# Sistema Hospitalario - Control de Personal

Este sistema permite llevar un control completo del personal de un hospital a través de una interfaz gráfica hecha en Python con Tkinter. A continuación se detallan todas las funciones que realiza la aplicación:

## ¿Qué hace este sistema?

- **Registrar empleados:**  
  Permite ingresar los datos personales y profesionales de un nuevo empleado, como nombre, apellido, puesto, departamento, turno, fecha de nacimiento, grado de estudios, cédula, domicilio, teléfono, correo y fecha de ingreso.  
  También valida si el empleado ya está registrado para evitar duplicados.

- **Ver empleados registrados:**  
  Muestra en una tabla todos los empleados registrados con sus respectivos datos. La información se toma directamente del archivo donde se guarda todo automáticamente.

- **Registrar días festivos:**  
  Se pueden registrar fechas especiales como días festivos, indicando el nombre del festivo, la fecha y si es obligatorio o no.

- **Ver días festivos registrados:**  
  Muestra en una tabla todos los días festivos que se han guardado, con su respectiva información.

- **Registrar vacaciones:**  
  Permite asignar vacaciones a un empleado en uno de los dos bloques disponibles (enero-junio o julio-diciembre), indicando la fecha de inicio y de fin.

- **Registrar permisos:**  
  Permite registrar un permiso para un empleado, eligiendo si es con sueldo o sin sueldo, e ingresando las fechas de inicio y fin del permiso.

- **Registrar turnos personalizados:**  
  Si un empleado necesita un horario distinto al turno normal, se puede crear un turno personalizado indicando los días que trabajará y su horario específico (hora de entrada y salida).

- **Registrar asistencias:**  
  Permite llevar un control diario de las asistencias de los empleados, registrando su nombre, la fecha, hora de entrada y el turno que le corresponde.

Todas las funciones están integradas en un menú donde el usuario puede acceder a cada sección fácilmente.
