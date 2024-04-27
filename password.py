import tkinter as tk
from tkinter import messagebox
import os
from cryptography.fernet import Fernet
import threading
from subprocess import Popen, PIPE
import sys
import subprocess

# Verificar y cargar la clave de cifrado
CLAVE_ARCHIVO = "clave.key" # clave de cifrado
CONFIG_FILE = "config.txt" # archivo en el que guardamos la clave de usuario

# Función para generar una clave de cifrado
def generar_clave():
    return Fernet.generate_key()

# Función para almacenar la clave en un archivo
def almacenar_clave(clave, nombre_archivo="clave.key"):
    with open(nombre_archivo, "wb") as archivo_clave:
        archivo_clave.write(clave)

# Función para cargar la clave desde el archivo
def cargar_clave(nombre_archivo="clave.key"):
    if not os.path.exists(nombre_archivo):
        # Generar una nueva clave y almacenarla en un archivo si no existe
        nueva_clave = generar_clave()
        almacenar_clave(nueva_clave, nombre_archivo)
        return nueva_clave
    else:
        with open(nombre_archivo, "rb") as archivo_clave:
            return archivo_clave.read()

# Función para cifrar la contraseña
def cifrar_contrasena(contrasena, clave):
    cipher_suite = Fernet(clave)
    return cipher_suite.encrypt(contrasena.encode())

# Función para descifrar la contraseña
def descifrar_contrasena(contra_cifrada, clave):
    cipher_suite = Fernet(clave)
    return cipher_suite.decrypt(contra_cifrada).decode()

def obtener_contrasena():
    contrasena_verificada = False

    while True:
        # Verificar si la contraseña está guardada en el archivo CONFIG_FILE
        if not contrasena_verificada and os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "rb") as file:
                contrasena_cifrada = file.read()
            contrasena = descifrar_contrasena(contrasena_cifrada, cargar_clave(CLAVE_ARCHIVO))
            if verificar_contrasena_sudo(contrasena):
                contrasena_verificada = True
                return contrasena

        # Solicitar la contraseña al usuario
        contrasena = tk.simpledialog.askstring("Contraseña", "Por favor, ingrese su contraseña:", show='*')
        if contrasena is None:
            limpiar_archivos_configuracion()
            sys.exit()
        elif contrasena.strip() == "":
            limpiar_archivos_configuracion()
            messagebox.showwarning("Contraseña requerida", "Debes ingresar una contraseña.")
        else:
            if verificar_contrasena_sudo(contrasena):
                contrasena_verificada = True
                almacenar_contrasena(contrasena)
                return contrasena
            else:
                limpiar_archivos_configuracion()
                messagebox.showerror("Contraseña Inválida", "Se necesita una contraseña válida para utilizar sudo.")

# Función para eliminar los archivos de configuración
def limpiar_archivos_configuracion():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

def almacenar_contrasena(contrasena):
    if contrasena is not None:  # Verificar si se ha ingresado una contraseña
        contrasena_cifrada = cifrar_contrasena(contrasena, cargar_clave(CLAVE_ARCHIVO))
        with open(CONFIG_FILE, "wb") as file:
            file.write(contrasena_cifrada)

def verificar_contrasena_sudo(contrasena):
    try:
        # Intentamos listar el directorio de root. Si la contraseña permite sudo devolverá 0
        proceso = subprocess.run(['sudo', '-k', '-S', 'ls', '/root'], input=contrasena, capture_output=True, text=True, timeout=5)
        if proceso.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al verificar la contraseña: {e}")
        return False


# Función para solicitar la contraseña al usuario y ejecutar una función con ella
def solicitar_contrasena_y_ejecutar(funcion, mostrar_output=True):
    contrasena = obtener_contrasena()
    if contrasena is None:
        messagebox.showwarning("Contraseña requerida", "Debes ingresar una contraseña.")
        return
    elif not verificar_contrasena_sudo(contrasena):
        messagebox.showerror("Contraseña Inválida", "Se necesita una contraseña válida para utilizar sudo.")
        return
    else:
        if mostrar_output:
            ventana_resultado = tk.Toplevel()
            ventana_resultado.title("Resultado de la Operación")

            etiqueta_progreso = tk.Label(ventana_resultado, text="Progreso:")
            etiqueta_progreso.pack(pady=5)

            texto_output = tk.Text(ventana_resultado, height=10, width=60)
            texto_output.pack(padx=10, pady=5)

            boton_cerrar = tk.Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy)
            boton_cerrar.pack(pady=5)

            # Deshabilitar el botón de cerrar mientras se está ejecutando el comando
            boton_cerrar.config(state=tk.DISABLED)

            def actualizar_output(line):
                texto_output.config(state=tk.NORMAL)
                texto_output.insert(tk.END, line + "\n")
                texto_output.config(state=tk.DISABLED)
                texto_output.see(tk.END)  # Desplazar hacia abajo para mostrar el último texto
                ventana_resultado.update()  # Actualizar la ventana para mostrar los cambios

            def ejecucion_contrasena():
                returncode = funcion(contrasena, actualizar_output)
                boton_cerrar.config(state=tk.NORMAL)  # Habilitar el botón de cerrar después de la ejecución
                if returncode == 0:
                    etiqueta_progreso.config(text="Operación completada exitosamente", fg="green")
                else:
                    etiqueta_progreso.config(text=f"Error al ejecutar la operación. Código de salida: {returncode}", fg="red")

            etiqueta_progreso = tk.Label(ventana_resultado, text="Ejecutando...", fg="blue")
            etiqueta_progreso.pack(pady=10)

            # Ejecutar el comando en un hilo separado para que la interfaz no se bloquee
            threading.Thread(target=ejecucion_contrasena).start()
        else:
            return funcion(contrasena)
