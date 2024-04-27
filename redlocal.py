import tkinter as tk
from tkinter import ttk
import nmap
import subprocess
import threading

# Función para encontrar dispositivos en la red local
def encontrar_dispositivos_en_red():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.0/24', arguments='-sn')
    dispositivos = [host for host in nm.all_hosts()]
    return dispositivos

def abrir_administrador_de_archivos(ip):
    try:
        subprocess.Popen(['nautilus', f'smb://{ip}'])  # Cambiar 'nautilus' al administrador de archivos correspondiente en el sistema
    except FileNotFoundError:
        print("Administrador de archivos no encontrado.")
    except Exception as e:
        print(f"Error al abrir el administrador de archivos: {e}")

# Función para manejar el evento de doble clic
def doble_clic(event, lista_dispositivos):
    ip_seleccionada = lista_dispositivos.get(tk.ACTIVE)
    threading.Thread(target=abrir_administrador_de_archivos, args=(ip_seleccionada,)).start()

# Función para mostrar los dispositivos encontrados en una ventana nueva
def mostrar_dispositivos_en_ventana():
    dispositivos = encontrar_dispositivos_en_red()

    ventana = tk.Toplevel()
    ventana.title("Dispositivos en la red local")
    ventana.geometry("400x300")  # Tamaño fijo

    lista_dispositivos = tk.Listbox(ventana, width=50, height=20)

    for dispositivo in dispositivos:
        lista_dispositivos.insert(tk.END, dispositivo)

    lista_dispositivos.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(ventana, orient="vertical", command=lista_dispositivos.yview)
    scrollbar.pack(side="right", fill="y")
    lista_dispositivos.config(yscrollcommand=scrollbar.set)

    # Vincular función de doble clic
    lista_dispositivos.bind("<Double-1>", lambda event: doble_clic(event, lista_dispositivos))
