import tkinter as tk
from tkinter import messagebox
#from tkinter import simpledialog
import subprocess
import repositorios
import netifaces
import urllib.request
import time
import platform
import os
import getpass
import platform
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
#from datetime import datetime
import tkinter as tk
import subprocess
import re
from password import obtener_contrasena
import shutil


class ComandosSistema:
    @staticmethod
    def ejecutar_comando_con_sudo(comando, contrasena, callback=None):
        comando_sudo = f"echo {contrasena} | sudo -S {comando}"
        proceso = subprocess.Popen(comando_sudo, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)

        while proceso.poll() is None:
            linea = proceso.stdout.readline().rstrip("\n")
            if linea:
                callback(linea)

            linea_error = proceso.stderr.readline().rstrip("\n")
            if linea_error:
                callback(linea_error)

        output, _ = proceso.communicate()  # Recoger cualquier salida restante
        if output:
            callback(output)

        return proceso.returncode

    @staticmethod
    def actualizar_sistema(contrasena, callback=None):
        comando = "sudo apt update && sudo apt upgrade -y"
        return ComandosSistema.ejecutar_comando_con_sudo(comando, contrasena, callback)

    @staticmethod
    def limpiar_cache(contrasena, callback=None):
        comando = "sudo apt clean && sudo apt autoremove"
        return ComandosSistema.ejecutar_comando_con_sudo(comando, contrasena, callback)

    @staticmethod
    def abrir_gestor_software():
        try:
            # Verificar si Snap Store está instalado
            snap_store_instalado = subprocess.run(["which", "snap-store"], stdout=subprocess.PIPE).returncode == 0

            # Si Snap Store no está instalado, mostrar un mensaje de advertencia en una ventana emergente
            if not snap_store_instalado:
                messagebox.showwarning("Snap Store no está instalado", "Snap Store no está instalado en el sistema.")
                return

            # Abrir Snap Store
            subprocess.Popen("snap-store", shell=True)
        except Exception as e:
            # Mostrar el mensaje de error en una ventana emergente
            messagebox.showerror("Error al abrir Snap Store", f"Error: {e}")


    @staticmethod
    def abrir_interfaz_repositorios():
        # Solicitar los permisos de root
        password = tk.simpledialog.askstring("Contraseña", "Por favor, ingrese su contraseña de root:", show='*')
        if not password:
            messagebox.showwarning("Advertencia", "Se requieren permisos de root para continuar.")
            return

        try:
            # Verificar que la contraseña es válida
            subprocess.run(['sudo', '-S', 'ls'], input=password.encode(), stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo verificar la contraseña: {e}")
            return

        # Abrir la interfaz de repositorios
        repositorios.abrir_interfaz_repositorios(password)
        
    @staticmethod
    def reiniciar_servicio_red():
        # Ejecutar el comando para obtener los servicios de red
        try:
            resultado = subprocess.run(['systemctl', 'list-units', '--type=service'], capture_output=True, text=True)
            servicios_red = resultado.stdout

            # Comprobar qué servicio de red está en uso
            if 'NetworkManager.service' in servicios_red:
                ComandosSistema.reiniciar_networkmanager()
            elif 'systemd-networkd.service' in servicios_red:
                ComandosSistema.reiniciar_systemd_networkd()
            else:
                print("No se encontró ningún servicio de red conocido en uso.")
        except Exception as e:
            print(f"Error al obtener los servicios de red: {e}")

    def reiniciar_networkmanager():
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
            print("Se reinició el servicio NetworkManager.")
        except subprocess.CalledProcessError as e:
            print(f"Error al reiniciar NetworkManager: {e}")

    def reiniciar_systemd_networkd():
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'systemd-networkd'], check=True)
            print("Se reinició el servicio systemd-networkd.")
        except subprocess.CalledProcessError as e:
            print(f"Error al reiniciar systemd-networkd: {e}")

    @staticmethod
    def reiniciar_tarjeta_red(interfaz, etiqueta_ip_local_info, etiqueta_ip_publica_info, ventana, callback=None):
        try:
            # Verificar si se ha seleccionado una interfaz
            if not interfaz:
                messagebox.showwarning("Tarjeta de red no seleccionada", "Por favor, seleccione una tarjeta de red.")
                return

            # Obtener la contraseña
            contrasena = obtener_contrasena()
            if contrasena is None:
                messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para reiniciar la tarjeta de red.")
                return

            # Convertir la contraseña a cadena si es de tipo bytes
            if isinstance(contrasena, bytes):
                contrasena = contrasena.decode('utf-8')

            # Instalar ifconfig con sudo si no está instalado
            if not shutil.which("ifconfig"):
                messagebox.showinfo("Instalación de ifconfig", "ifconfig no está instalado en el sistema. Se procederá a su instalación.")

                comando_instalacion = ['sudo', '-S', 'apt', 'install', 'net-tools']
                proceso_instalacion = subprocess.run(comando_instalacion, input=contrasena, universal_newlines=True, check=True)
                if proceso_instalacion.returncode == 0:
                    messagebox.showinfo("Instalación exitosa", "'ifconfig' se ha instalado correctamente. Continuamos con el reinicio de la tarjeta de red...")
                else:
                    messagebox.showerror("Error de instalación", "Ha ocurrido un error durante la instalación de 'ifconfig'.")
                    return

            # Desactivar y luego activar la interfaz de red específica
            subprocess.run(['sudo', '-S', 'ifconfig', interfaz, 'down'], input=contrasena, universal_newlines=True, check=True)
            time.sleep(7)
            messagebox.showinfo("Reinicio de red", "Tarjeta de red apagada correctamente")

            subprocess.run(['sudo', '-S', 'ifconfig', interfaz, 'up'], input=contrasena, universal_newlines=True, check=True)
            time.sleep(7)
            messagebox.showinfo("Reinicio de red", "Tarjeta de red iniciada correctamente")

            # Esperar unos segundos antes de obtener las nuevas direcciones IP
            time.sleep(7)

            # Obtener las nuevas direcciones IP después de reiniciar la tarjeta de red
            nueva_ip_local = ComandosSistema.obtener_direccion_ip_local()
            nueva_ip_publica = ComandosSistema.obtener_direccion_ip_publica()

            # Actualizar las etiquetas con las nuevas direcciones IP
            etiqueta_ip_local_info.config(text=nueva_ip_local)
            etiqueta_ip_publica_info.config(text=nueva_ip_publica)

            if callback:
                callback("La tarjeta de red se reinició correctamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Error al reiniciar la tarjeta de red: {e}")




        
    @staticmethod
    def obtener_interfaces_red():
        interfaces = []
        try:
            resultado = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
            lineas = resultado.stdout.split('\n')
            for linea in lineas:
                if 'state UP' in linea:
                    partes = linea.split(': ')
                    if len(partes) > 1:
                        interfaz = partes[1].split(':')[0]
                        interfaces.append(interfaz)
        except Exception as e:
            print(f"Error al obtener interfaces de red: {e}")
        return interfaces
    
    @staticmethod
    def obtener_direccion_ip_local():
        # Obtener la dirección IP local
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            try:
                address = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                if not address.startswith('127.'):
                    return address
            except (KeyError, IndexError):
                pass
        return 'No disponible'

    @staticmethod
    def obtener_direccion_ip_publica():
        try:
            ip = urllib.request.urlopen('https://ifconfig.me/ip').read().decode('utf8')
            return ip.strip()  # Eliminar espacios en blanco alrededor de la dirección IP
        except Exception as e:
            print(f"No se pudo obtener la dirección IP pública: {e}")
            return 'No disponible'
        
    @staticmethod
    def obtener_info_sistema():
        # Obtener el nombre y la versión del sistema operativo
        nombre_sistema = platform.system()
        version_sistema = platform.release()

        # Mapear el nombre del sistema operativo a un formato más legible
        if nombre_sistema == 'Linux':
            nombre_sistema = 'Ubuntu'  # Cambiar 'Linux' por el nombre específico del sistema
            # Obtener la versión específica de Ubuntu
            version_ubuntu = ComandosSistema.obtener_version_ubuntu()
        else:
            version_ubuntu = 'No disponible'  # Otra plataforma que no sea Linux

        # Obtener el nombre del usuario logueado
        usuario = getpass.getuser()

        return usuario, nombre_sistema, version_sistema, version_ubuntu

    @staticmethod
    def obtener_version_ubuntu():
        try:
            with open('/etc/os-release', 'r') as f:
                for line in f:
                    if line.startswith('VERSION_ID='):
                        return line.strip().split('=')[1].strip('"')
        except Exception as e:
            print(f"Error al obtener la versión de Ubuntu: {e}")
        return 'No disponible'
    
    @staticmethod
    def obtener_tipo_escritorio():
        # Archivos de configuración comunes para diferentes entornos de escritorio
        archivos_configuracion = {
            "GNOME": "/usr/share/glib-2.0/schemas/org.gnome.desktop.interface.gschema.xml",
            "KDE": "/usr/share/plasma/plasmoids/org.kde.plasma.desktop/contents/config/main.xml",
            "LXDE": "/etc/xdg/openbox/rc.xml",
            "MATE": "/usr/share/mate-control-center/ui/",
            "Cinnamon": "/usr/share/cinnamon/cinnamon-settings/cinnamon-settings.py",
            "XFCE": "/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml"
            # Agrega aquí más entradas para otros entornos de escritorio
        }

        gestor_ventanas = os.environ.get('XDG_SESSION_TYPE', 'Desconocido')
        
        # Buscar cada archivo de configuración en la lista
        for escritorio, archivo in archivos_configuracion.items():
            if os.path.isfile(archivo):
                return f"{escritorio} - gestor de ventanas {gestor_ventanas}"

        return "Desconocido"

    @staticmethod
    def monitorizar_sistema():
        # Obtener los datos del sistema
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        # Obtener los datos de red
        red_info = psutil.net_io_counters(pernic=False)
        red_envio = red_info.bytes_sent
        red_recepcion = red_info.bytes_recv
        temperatura_cpu = psutil.sensors_temperatures().get('cpu_thermal', [None])[0].current if 'cpu_thermal' in psutil.sensors_temperatures() else None
        carga_sistema = psutil.getloadavg()[0]

        # Crear listas de nombres, valores y colores para los datos
        nombres = ['CPU', 'Memoria', 'Disco', 'Red (enviado)', 'Red (recibido)', 'Temperatura CPU', 'Carga del sistema']
        valores = [cpu_percent, mem_percent, disk_percent, red_envio / 1024 / 1024, red_recepcion / 1024 / 1024, temperatura_cpu, carga_sistema]
        colores = ['blue', 'green', 'red', 'orange', 'purple', 'cyan', 'magenta']

        # Filtrar los datos que no están disponibles y actualizar las listas
        nombres = [n for n, v in zip(nombres, valores) if v is not None]
        valores = [v for v in valores if v is not None]
        colores = colores[:len(valores)]

        # Crear una nueva ventana de Tkinter
        ventana_grafico = tk.Toplevel()
        ventana_grafico.title("Estadísticas")

        # Crear una figura de Matplotlib
        fig, ax = plt.subplots(figsize=(12, 8))

        # Visualizar los datos en un gráfico de barras
        ax.bar(nombres, valores, color=colores)
        ax.set_xlabel('Recursos del Sistema')
        ax.set_ylabel('Porcentaje de Uso / Valor')
        ax.set_title('Monitorización del Sistema')
        ax.grid(True)

        # Crear un lienzo de Matplotlib para integrarlo en la ventana de Tkinter
        canvas = FigureCanvasTkAgg(fig, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Ejecutar el bucle principal de la ventana de Tkinter
        ventana_grafico.mainloop()
    
    @staticmethod
    def obtener_servidores_dns():
        dns_local = ""
        dns_publico = ""

        try:
            # Obtener los servidores DNS configurados en /etc/resolv.conf (locales)
            with open('/etc/resolv.conf', 'r') as file:
                for line in file:
                    if line.startswith('nameserver'):
                        if not dns_local:
                            dns_local = line.split()[1]
                        else:
                            break  # Solo necesitamos el primer servidor DNS local

            # Ejecutar resolvectl para obtener los servidores DNS públicos
            resultado = subprocess.run(['resolvectl', 'status'], capture_output=True, text=True)
            if resultado.returncode == 0:
                output_lines = resultado.stdout.split('\n')

                for line in output_lines:
                    if line.strip().startswith("DNS Servers"):
                        dns_publico = line.split(":")[1].strip()
                        break  # Solo necesitamos el primer servidor DNS público

            return dns_local, dns_publico

        except Exception as e:
            print(f"Error al obtener los servidores DNS: {e}")

        return dns_local, dns_publico
    
    @staticmethod
    def get_tiempo_actividad():
        # Ejecutar el comando 'uptime' para obtener el tiempo de actividad del sistema
        try:
            tiempo_actividad_raw = subprocess.check_output(['uptime'], universal_newlines=True)
            # Extraer el tiempo de actividad del resultado
            tiempo_actividad_match = re.search(r'up\s+(.*?),', tiempo_actividad_raw)
            if tiempo_actividad_match:
                tiempo_actividad = tiempo_actividad_match.group(1)
                # Separar el tiempo de actividad en horas y minutos
                tiempo_parts = tiempo_actividad.split(':')
                if len(tiempo_parts) == 2:
                    horas = tiempo_parts[0]
                    minutos = tiempo_parts[1]
                    if int(horas) == 0:
                        return f"{minutos} minutos"
                    else:
                        return f"{horas} horas, {minutos} minutos"
                else:
                    return tiempo_actividad.strip()
            else:
                return "No disponible"
        except Exception as e:
            print(f"Error al obtener el tiempo de actividad: {e}")
            return "No disponible"
    
    @staticmethod
    def get_fabricante_equipo():
        # Ejecutar el comando 'dmidecode' para obtener información sobre el fabricante del equipo
        try:
            contrasena = obtener_contrasena()  # Sin decodificar
            fabricante_raw = subprocess.check_output(['sudo', '-S', '-k', 'dmidecode', '-s', 'system-manufacturer'], input=contrasena, universal_newlines=True)
            return fabricante_raw.strip()
        except Exception as e:
            print(f"Error al obtener el fabricante del equipo: {e}")
            return "No disponible"

    @staticmethod
    def get_zona_horaria():
        # Ejecutar el comando 'timedatectl' para obtener la zona horaria del sistema
        try:
            contrasena = obtener_contrasena()  # Sin decodificar
            zona_horaria_raw = subprocess.check_output(['sudo', '-S', '-k', 'timedatectl', 'show', '-p', 'Timezone'], input=contrasena, universal_newlines=True)
            zona_horaria_match = re.search(r'Timezone=(.*)', zona_horaria_raw)
            if zona_horaria_match:
                zona_horaria = zona_horaria_match.group(1)
                return zona_horaria.strip()
            else:
                return "No disponible"
        except Exception as e:
            print(f"Error al obtener la zona horaria: {e}")
            return "No disponible"
    
    @staticmethod    
    def obtener_informacion_procesador():
        # Obtener información básica del procesador
        info_procesador = {
            "Procesador": platform.processor(),
            "Frecuencia del Procesador (MHz)": psutil.cpu_freq().current
        }

        # Obtener número de núcleos y hilos del procesador
        info_procesador["Número de núcleos y hilos"] = psutil.cpu_count(logical=True)

        # Obtener arquitectura del procesador
        info_procesador["Arquitectura del procesador"] = platform.architecture()[0]

        # Obtener utilización actual de la CPU
        info_procesador["Utilización actual de la CPU"] = psutil.cpu_percent()

        # Obtener información detallada sobre la CPU
        info_cpu = {}
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if ':' in line:
                        parts = line.split(':')
                        key = parts[0].strip()
                        value = parts[1].strip()
                        info_cpu[key] = value
        except FileNotFoundError:
            info_cpu["Error"] = "No se pudo acceder a la información detallada de la CPU"

        info_procesador["Información detallada sobre la CPU"] = info_cpu

        table_data = []
        for key, value in info_procesador.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    table_data.append([sub_key, sub_value])
            else:
                table_data.append([key, value])
        return table_data

    @staticmethod    
    def obtener_informacion_memoria():
        # Obtener información de la memoria RAM
        mem = psutil.virtual_memory()

        # Obtener información sobre la memoria swap
        swap = psutil.swap_memory()

        # Crear un diccionario con la información
        info_memoria = {
            "Memoria RAM Total (MB)": mem.total,
            "Memoria RAM Disponible (MB)": mem.available,
            "Uso de Memoria RAM (%)": mem.percent,
            "Memoria Swap Total (MB)": swap.total,
            "Memoria Swap Disponible (MB)": swap.free,
            "Uso de Memoria Swap (%)": swap.percent
        }

        return info_memoria
    