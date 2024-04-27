import subprocess
import os

class LimpiadorNavegadores:
    @staticmethod
    def limpiar_cache_chrome(window):
        chrome_path = '/usr/bin/google-chrome'
        if not os.path.exists(chrome_path):
            return "Google Chrome no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            # Primero mostrar el mensaje
            mensaje = "Caché de Google Chrome limpiada correctamente."
            subprocess.run([chrome_path, '--clear-browser-data'], check=True)
            return mensaje
        except subprocess.CalledProcessError as e:
            return f"Error al limpiar la caché de Google Chrome: {e}"

    @staticmethod
    def limpiar_cache_firefox(window):
        firefox_path = '/usr/bin/firefox'
        if not os.path.exists(firefox_path):
            return "Mozilla Firefox no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            # Primero mostrar el mensaje
            mensaje = "Caché de Mozilla Firefox limpiada correctamente."
            subprocess.run([firefox_path, '--clear-cache'], check=True)
            return mensaje
        except subprocess.CalledProcessError as e:
            return f"Error al limpiar la caché de Mozilla Firefox: {e}"

    @staticmethod
    def limpiar_cache_edge(window):
        edge_path = '/usr/bin/microsoft-edge'
        if not os.path.exists(edge_path):
            return "Microsoft Edge no está instalado o no se encuentra en la ruta por defecto."
        
        try:
            # Primero mostrar el mensaje
            mensaje = "Caché de Edge limpiada correctamente."
            subprocess.run([edge_path, '--clear-browser-data'], check=True)
            return mensaje
        except subprocess.CalledProcessError as e:
            return f"Error al limpiar la caché de Edge: {e}"
