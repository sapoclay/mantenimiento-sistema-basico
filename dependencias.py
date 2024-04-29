import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import sys
from password import obtener_contrasena  # Importa la función obtener_contrasena del archivo password.py

# Lista de dependencias junto con sus métodos de instalación
DEPENDENCIAS = {
    "samba": ["sudo", "apt", "install", "-y", "samba"],
    "nmap": ["sudo", "apt", "install", "-y", "python3-nmap"],
    "python3-tk": ["sudo", "apt", "install", "-y", "python3-tk"],
    "net-tools": ["sudo", "apt", "install", "-y", "net-tools"],
    "ethtool": ["sudo", "apt", "install", "-y", "ethtool"],
    "python3-pyqt5": ["sudo", "apt", "install", "-y", "python3-pyqt5"],
    "gnome-terminal": ["sudo", "apt", "install", "-y", "gnome-terminal"],
    "matplotlib": ["pip3", "install", "matplotlib"],
    "pillow": ["pip3", "install", "--upgrade", "pillow"],
    "cryptography": ["pip3", "install", "cryptography"],
    "psutil": ["pip3", "install", "psutil"],
    "markdown2": ["pip3", "install", "markdown2"],
    "pyqt5": ["pip3", "install", "PyQt5"],
    "speedtest-cli": ["pip3", "install", "speedtest-cli"],
    "tabulate": ["pip3", "install", "tabulate"],
    "opencv-python-headless": ["pip3", "install", "opencv-python-headless"],
    "wget": ["pip3", "install", "wget"]
}


def verificar_dependencias():
    dependencias_faltantes = []
    for dependencia, instalacion in DEPENDENCIAS.items():
        # Verificar si la dependencia está instalada utilizando apt
        if instalacion[0] == 'sudo' and dependencia != 'pip3':
            # Verificar si la dependencia está instalada utilizando apt
            proceso = subprocess.run(['apt', 'list', '--installed', dependencia], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Si el proceso devuelve un código de retorno distinto de 0, la dependencia no está instalada
            if proceso.returncode != 0 or dependencia not in proceso.stdout:
                dependencias_faltantes.append(dependencia)

        # Verificar si la dependencia está instalada utilizando pip3
        elif instalacion[0] == 'pip3':
            proceso = subprocess.run(['pip3', 'show', dependencia], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Si el proceso devuelve un código de retorno distinto de 0, la dependencia no está instalada    
            if proceso.returncode != 0:
                dependencias_faltantes.append(dependencia)

    # Retornar True si todas las dependencias están instaladas, False de lo contrario
    if dependencias_faltantes:
        mensaje = "Las siguientes dependencias necesarias no están instaladas o no tienen la versión correcta:\n\n"
        mensaje += "\n".join(dependencias_faltantes)
        messagebox.showinfo("Dependencias faltantes", mensaje)
        return False
    else:
        return True



def instalar_dependencias(progress_bar=None):
    total_dependencias = len(DEPENDENCIAS)
    progreso_actual = 0

    # Obtener la contraseña del usuario
    contrasena = obtener_contrasena()

    for dependencia, metodo_instalacion in DEPENDENCIAS.items():
        print(f"Instalando {dependencia}...")
        try:
            # Ejecutar el proceso de instalación con sudo y la contraseña obtenida
            proceso_instalacion = subprocess.Popen(["sudo", "-S"] + metodo_instalacion, stdin=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            salida, error = proceso_instalacion.communicate(input=contrasena + "\n")

            # Verificar si ocurrieron errores durante la instalación
            if proceso_instalacion.returncode != 0:
                if progress_bar:
                    messagebox.showerror("Error de instalación", f"No se pudo instalar {dependencia}: {error}")
                    sys.exit(1)  # Salir del programa con código de error 1
                else:
                    print(f"No se pudo instalar {dependencia}: {error}")
                return False
            
            
            progreso_actual += 1
            if progress_bar:
                progreso = int((progreso_actual / total_dependencias) * 100)
                progress_bar["value"] = progreso
                progress_bar.update()
        except subprocess.CalledProcessError as e:
            if progress_bar:
                messagebox.showerror("Error de instalación", f"No se pudo instalar {dependencia}: {e}")
            else:
                print(f"No se pudo instalar {dependencia}: {e}")
            return False
    
    if progress_bar:
        messagebox.showinfo("Instalación completada", "Todas las dependencias se han instalado correctamente.")
    else:
        print("Todas las dependencias se han instalado correctamente.")
    
    return True


def iniciar_programa():
    messagebox.showinfo("¡Todas las dependencias están instaladas! Iniciando el programa...")

def main():
    if not verificar_dependencias():
        if messagebox.askyesno("Instalación de dependencias", "Algunas dependencias necesarias no están instaladas. ¿Desea instalarlas ahora?"):
            root = tk.Tk()
            root.withdraw()
            progress_window = tk.Toplevel()
            progress_window.title("Instalando dependencias")
            progress_window.geometry("300x100")
            progress_label = tk.Label(progress_window, text="Instalando dependencias...")
            progress_label.pack(pady=5)
            progress_bar = ttk.Progressbar(progress_window, length=200, mode="determinate")
            progress_bar.pack(pady=5)
            progress_bar["value"] = 0
            progress_bar["maximum"] = 100
            if instalar_dependencias(progress_bar):
                progress_window.destroy()
                iniciar_programa()
            else:
                progress_window.destroy()
                messagebox.showerror("Error", "No se pudieron instalar todas las dependencias. El programa no puede iniciar.")
        else:
            messagebox.showinfo("Información", "El programa no puede iniciar sin todas las dependencias instaladas.")
    else:
        iniciar_programa()
