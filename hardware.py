import platform
import psutil
import subprocess
import re
import speedtest
from tkinter import messagebox
import password
import getpass
from comandos import ComandosSistema
from tabulate import tabulate

comandos_sistema = ComandosSistema()

def obtener_velocidad_internet_speedtest():
    try:
        # Crear un objeto Speedtest
        st = speedtest.Speedtest()

        # Realizar la prueba de velocidad
        st.get_best_server()
        velocidad_descarga = st.download() / 10**6  # Convertir a Mbps
        velocidad_subida = st.upload() / 10**6  # Convertir a Mbps

        return {
            "Velocidad de Subida (Mbps)": velocidad_subida,
            "Velocidad de Descarga (Mbps)": velocidad_descarga
        }
    except Exception as e:
        print(f"Error al obtener la velocidad de internet con Speedtest: {e}")
        return {"Velocidad de Subida (Mbps)": "No disponible", "Velocidad de Descarga (Mbps)": "No disponible"}


def obtener_informacion_hardware():
    
    info = {}

    # Información del sistema
    info["Sistema"] = {
        "Sistema Operativo": platform.system(),
        "Nombre del Nodo": platform.node(),
        "Release": platform.release(),
        "Versión": platform.version(),
        "Arquitectura": platform.machine(),
        "Plataforma": platform.platform(),  # Tipo de plataforma (32 o 64 bits)
        "Tiempo de Actividad": comandos_sistema.get_tiempo_actividad(),  # Tiempo de actividad del sistema
        "Kernel": platform.uname().version,  # Versión del kernel
        "Fabricante del Equipo": comandos_sistema.get_fabricante_equipo(),  # Fabricante del equipo
        "Nombre de Usuario": getpass.getuser(),  # Nombre del usuario actual
        "Zona Horaria": comandos_sistema.get_zona_horaria()  # Configuración de la zona horaria
    }

    # Información del procesador
    # Obtener la información del procesador utilizando el método estático
    info_procesador = ComandosSistema.obtener_informacion_procesador()

    # Convertir la información en una tabla utilizando tabulate
    tabla_procesador = tabulate(info_procesador, headers=["Atributo", "Valor"])

    info["Procesador"] = {
        "Info": tabla_procesador
    }

    # Información de la memoria RAM
    info_memoria = ComandosSistema().obtener_informacion_memoria()
    info["Memoria"] = {
        "Memoria": info_memoria
    }
    
    # Información de la tarjeta gráfica y resolución de pantalla
    try:
        info["Sistema"]["Tarjeta Gráfica"] = subprocess.check_output("lspci | grep VGA", shell=True).decode().strip()
        info["Sistema"]["Resolución de Pantalla"] = subprocess.check_output("xrandr | grep \* | cut -d' ' -f4", shell=True).decode().strip()
    except Exception as e:
        info["Sistema"]["Tarjeta Gráfica"] = "No se pudo obtener la información"
        info["Sistema"]["Resolución de Pantalla"] = "No se pudo obtener la información"
    
    # Espacio en disco
    espacio_disco = {"Espacio disponible (GB)": 0, "Espacio usado (GB)": 0}
    particiones = psutil.disk_partitions()
    for particion in particiones:
        punto_de_montaje = particion.mountpoint
        try:
            espacio = psutil.disk_usage(punto_de_montaje)
            espacio_disco["Espacio disponible (GB)"] += espacio.free / (1024 ** 3)
            espacio_disco["Espacio usado (GB)"] += espacio.used / (1024 ** 3)
        except PermissionError:
            messagebox.showerror("Error", f"No se puede acceder a la partición {punto_de_montaje}")

    info["Discos y Puntos de Montaje"] = espacio_disco

    # Interfaces de red encontradas
    interfaces = subprocess.check_output(["ip", "link", "show"]).decode()
    interfaces = re.findall(r'\d+: (\S+):', interfaces)
    info["Red"] = {"Interfaces de red": interfaces}

    velocidad_conexion = {}
    contrasena = password.obtener_contrasena()
    for interface in interfaces:
        try:
            comando = f"echo '{contrasena}' | sudo -S /sbin/ethtool {interface}"
            salida = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT).decode()
            velocidad_matches = re.search(r"Speed:\s+(\d+)Mb/s", salida)
            if velocidad_matches:
                velocidad = velocidad_matches.group(1)
                velocidad_conexion[interface] = f"{velocidad} MB/s"
        except subprocess.CalledProcessError as e:
            if "orden no encontrada" in e.output.decode():
                messagebox.showerror("Error", "ethtool no está instalado. Instale ethtool para obtener información de velocidad de conexión.")
            else:
                messagebox.showerror("Error", f"No se pudo obtener la velocidad de conexión para {interface}: {e.output}")
    
    # Añadir la velocidad de conexión al diccionario de información
    info["Red"].update({"Velocidad de conexión": velocidad_conexion})

    # Obtener la velocidad de internet
    velocidad_internet = obtener_velocidad_internet_speedtest()
    info["Internet"] = velocidad_internet
    
    return info