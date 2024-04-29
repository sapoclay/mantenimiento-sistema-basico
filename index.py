import tkinter as tk
from tkinter import ttk
from comandos import ComandosSistema
from tkinter import messagebox
import sys
import dependencias


def instalar_dependencias_con_progreso():
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal
    progress_window = tk.Toplevel(root)
    progress_window.title("Instalando dependencias")
    progress_window.geometry("300x100")  # Establecer tamaño fijo
    progress_window.resizable(False, False)  # Hacer que la ventana no sea redimensionable
    progress_label = tk.Label(progress_window, text="Instalando dependencias...")
    progress_label.pack(pady=5)
    progress_bar = ttk.Progressbar(progress_window, length=200, mode="determinate")
    progress_bar.pack(pady=5)
    progress_bar["value"] = 0
    progress_bar["maximum"] = 100
    dependencias.instalar_dependencias(progress_bar)
    progress_window.destroy()  # Cerrar la ventana de progreso


# Comprobación de dependencias
if not dependencias.verificar_dependencias():
    # Si hay dependencias faltantes, mostrar ventana emergente para instalarlas
    if messagebox.askyesno("Instalación de dependencias", "Las dependencias son imprescindibles ¿Quieres instalarlas ahora?"):
        instalar_dependencias_con_progreso()
    else:
        # Si el usuario elige no instalar las dependencias, mostrar un mensaje y salir del programa
        messagebox.showinfo("Información", "El programa no puede iniciar sin todas las dependencias instaladas.")
        exit()
else:
    messagebox.showinfo("Información", "¡Todas las dependencias están instaladas! Haz clic en OK para iniciar el programa...")


from menu import mostrar_about  
from aplicacionesInicio import AplicacionesAutostart
from administrarProcesos import AdministrarProcesos
from navegadores import LimpiadorNavegadores
import multiprocessing
from diccionario import cargar_contenido_html, abrir_ventana_diccionario
import repositorios
from tkinter import scrolledtext
import hardware
import password
from password import solicitar_contrasena_y_ejecutar
from redlocal import mostrar_dispositivos_en_ventana


# Llamar a la función obtener_contrasena() para solicitar la contraseña al usuario al iniciar el programa
password.obtener_contrasena()


# Crear una instancia de la clase ComandosSistema
comandos_sistema = ComandosSistema()

# Funciones para actualizar, limpiar, abrir el gestor de software y el administrador de repositorios
def actualizar():
    password.solicitar_contrasena_y_ejecutar(comandos_sistema.actualizar_sistema, True)

def limpiar():
    password.solicitar_contrasena_y_ejecutar(comandos_sistema.limpiar_cache, True)

def abrir_snap_store():
    try:
        ComandosSistema.abrir_gestor_software()
    except Exception as e:
        # Mostrar el mensaje de error en una ventana emergente
        messagebox.showerror("Error al abrir Snap Store", f"Error: {e}")
    
def abrir_administrador_repositorios():
    ventana_admin_repos = tk.Toplevel(ventana_principal)
    # Ajustar el tamaño de la ventana de administración de repositorios
    ventana_admin_repos.geometry("600x400")  # Ancho x Alto
    ventana_admin_repos.title("Administrador de Repositorios")
    repositorios.Repositorios(ventana_admin_repos)

    
# Funciones para limpiar la caché de los navegadores web
def limpiar_cache_firefox(window):
    mensaje = LimpiadorNavegadores.limpiar_cache_firefox(window)
    etiqueta_limpiar_firefox_info.config(text=mensaje)

def limpiar_cache_chrome(window):
    mensaje = LimpiadorNavegadores.limpiar_cache_chrome(window)
    etiqueta_limpiar_chrome_info.config(text=mensaje)

def limpiar_cache_edge(window):
    mensaje = LimpiadorNavegadores.limpiar_cache_edge(window)
    etiqueta_limpiar_edge_info.config(text=mensaje)
    
# Obtener la lista de interfaces de red disponibles
interfaces = comandos_sistema.obtener_interfaces_red()

# Función para mostrar la ventana Generando informe mientras se crea el informe de  hardware
def mostrar_generando_informe():
    ventana_generando = tk.Toplevel()
    ventana_generando.title("Generando informe...")

    # Configurar el tamaño y posición de la ventana
    ventana_generando.geometry("400x150")  # Tamaño de 400x150 píxeles
    ventana_generando.resizable(False, False)  # No redimensionable

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_generando.winfo_screenwidth()
    alto_pantalla = ventana_generando.winfo_screenheight()

    # Calcular las coordenadas para centrar la ventana en la pantalla
    x = (ancho_pantalla - 400) // 2
    y = (alto_pantalla - 150) // 2

    # Establecer las coordenadas para centrar la ventana
    ventana_generando.geometry(f"+{x}+{y}")

    etiqueta_generando = tk.Label(ventana_generando, text="Generando informe sobre Hardware e Internet ...", font=("Arial", 12, "bold"))
    etiqueta_generando.pack(padx=20, pady=10)

    # Llamar a la función mostrar_info_hardware después de un breve tiempo
    ventana_generando.after(100, lambda: mostrar_info_hardware(ventana_generando))

# Función para crear el informe de hardware detectado en el equipo
def mostrar_info_hardware(ventana_generando):
             
    # Obtener la información del hardware
    info_hardware = hardware.obtener_informacion_hardware()
    # Cerrar la ventana de "Generando informe..."
    ventana_generando.destroy()
    
    # Crear ventana principal
    ventana_info_hardware = tk.Toplevel()
    ventana_info_hardware.title("Información del Hardware")
    
    # Crear el notebook
    notebook = ttk.Notebook(ventana_info_hardware)
    notebook.pack(expand=True, fill="both")
    
    # Crear pestaña para la información general del sistema
    frame_general = ttk.Frame(notebook)
    notebook.add(frame_general, text="General")
    
    # Crear widget de texto con scroll para mostrar los datos generales
    texto_info_general = scrolledtext.ScrolledText(frame_general, wrap=tk.WORD, width=60, height=20)
    texto_info_general.pack(expand=True, fill="both")
    
    # Mostrar los datos generales en el widget de texto
    for key, value in info_hardware["Sistema"].items():
        texto_info_general.insert(tk.END, f"{key}: {value}\n")
    
    # Deshabilitar la edición del texto
    texto_info_general.configure(state="disabled")
    
    # Crear pestaña para la información del procesador
    frame_procesador = ttk.Frame(notebook)
    notebook.add(frame_procesador, text="Procesador")
    
    # Crear widget de texto con scroll para mostrar los datos del procesador
    texto_info_procesador = scrolledtext.ScrolledText(frame_procesador, wrap=tk.WORD, width=60, height=20)
    texto_info_procesador.pack(expand=True, fill="both")
    
    # Mostrar los datos del procesador en el widget de texto
    for key, value in info_hardware["Procesador"].items():
        texto_info_procesador.insert(tk.END, f"{key}: {value}\n")
    
    # Deshabilitar la edición del texto
    texto_info_procesador.configure(state="disabled")
    
    # Crear pestaña para la información de memoria RAM
    frame_memoria = ttk.Frame(notebook)
    notebook.add(frame_memoria, text="Memoria RAM")
    
    # Crear widget de texto con scroll para mostrar los datos de memoria RAM
    texto_info_memoria = scrolledtext.ScrolledText(frame_memoria, wrap=tk.WORD, width=60, height=20)
    texto_info_memoria.pack(expand=True, fill="both")
    
    # Mostrar los datos de memoria RAM en el widget de texto
    for key, value in info_hardware["Memoria"].items():
        texto_info_memoria.insert(tk.END, f"{key}: {value}\n")
    
    # Deshabilitar la edición del texto
    texto_info_memoria.configure(state="disabled")
    
    # Crear pestaña para la información de discos y puntos de montaje
    frame_discos = ttk.Frame(notebook)
    notebook.add(frame_discos, text="Espacio disponible")
    
    # Crear widget de texto con scroll para mostrar los datos de discos y puntos de montaje
    texto_info_discos = scrolledtext.ScrolledText(frame_discos, wrap=tk.WORD, width=60, height=20)
    texto_info_discos.pack(expand=True, fill="both")
    
    # Mostrar los datos de discos y puntos de montaje en el widget de texto
    for key, value in info_hardware["Discos y Puntos de Montaje"].items():
        texto_info_discos.insert(tk.END, f"{key}: {value}\n")
    
    # Deshabilitar la edición del texto
    texto_info_discos.configure(state="disabled")
    
    # Crear pestaña para la información de red
    frame_red = ttk.Frame(notebook)
    notebook.add(frame_red, text="Red")

    # Crear widget de texto con scroll para mostrar los datos de red
    texto_info_red = scrolledtext.ScrolledText(frame_red, wrap=tk.WORD, width=60, height=20)
    texto_info_red.pack(expand=True, fill="both")

    # Mostrar los datos de red en el widget de texto
    for key, value in info_hardware["Red"].items():
        texto_info_red.insert(tk.END, f"{key}: {value}\n")

    # Mostrar la velocidad de conexión a Internet
    texto_info_red.insert(tk.END, "\nVelocidad de conexión a Internet:\n")
    for key, value in info_hardware["Internet"].items():
        texto_info_red.insert(tk.END, f"{key}: {value}\n")

    # Deshabilitar la edición del texto
    texto_info_red.configure(state="disabled")

# Función para mostrar el mensaje cuando reiniciamos la tarjeta de red
def mostrar_mensaje(mensaje):
    messagebox.showinfo("Mensaje", mensaje)
    
# Función para abrir la ventana en la que se muestra el diccionario
def abrir_diccionario():
    contenido_html = cargar_contenido_html()
    proc = multiprocessing.Process(target=abrir_ventana_diccionario, args=(contenido_html,))
    proc.start()

# Función para cerrar el programa y limpiar los archivos de configuración
def salir():
    password.limpiar_archivos_configuracion()
    sys.exit()
    
# Función para abrir la ventana de actualizaciones
def abrir_ventana_actualizaciones():
    # Importar el módulo actualizaciones.py
    import actualizaciones
    # Llamar a la función para mostrar la ventana de actualizaciones
    actualizaciones.mostrar_ventana_actualizaciones()

# --------------------------------------------------------- #
# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Mantenimiento de Sistema")

# Configurar la ventana para que no sea redimensionable
ventana_principal.resizable(False, False)

# Crear el menú
menubar = tk.Menu(ventana_principal)

# Crear el menú Archivo
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_separator()
archivo_menu.add_command(label="Abrir Diccionario", command=abrir_diccionario)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Archivo", menu=archivo_menu)

# Crear el menú Papelera
papelera_menu = tk.Menu(menubar, tearoff=0)
papelera_menu.add_command(label="Eliminar Archivo", command=ComandosSistema.eliminar_archivo)
papelera_menu.add_command(label="Vaciar Papelera", command=ComandosSistema.vaciar_papelera)

# Agregar el menú Papelera como una cascada en el menú principal
menubar.add_cascade(label="Papelera", menu=papelera_menu)

# Crear el menú Preferencias
preferencias_menu = tk.Menu(menubar, tearoff=0)
preferencias_menu.add_command(label="Buscar Actualizaciones", command=abrir_ventana_actualizaciones)

# Agregar el menú Preferencias como una cascada en el menú principal
menubar.add_cascade(label="Preferencias", menu=preferencias_menu)

# Opción "About" fuera del menú "Archivo"
menubar.add_command(label="About", command=mostrar_about)  # Llama a mostrar_about cuando se haga clic
# Configurar el menú en la ventana principal
ventana_principal.config(menu=menubar)

#----------------------------------------------------#
# Botones y etiquetas para la interfaz principal

# COLUMNAS 0 y 1
# Crear etiquetas y botones para actualizar, limpiar y abrir el gestor de software
etiqueta_actualizar = tk.Label(ventana_principal, text="Actualizar Sistema:")
etiqueta_actualizar.grid(row=0, column=0, padx=10, pady=5, sticky="e")
boton_actualizar = tk.Button(ventana_principal, text="Actualizar", command=lambda: solicitar_contrasena_y_ejecutar(comandos_sistema.actualizar_sistema, True))
boton_actualizar.grid(row=0, column=1, padx=10, pady=5)

etiqueta_limpiar = tk.Label(ventana_principal, text="Limpiar Cache Sistema:")
etiqueta_limpiar.grid(row=1, column=0, padx=10, pady=5, sticky="e")
boton_limpiar = tk.Button(ventana_principal, text="Limpiar", command=lambda: solicitar_contrasena_y_ejecutar(comandos_sistema.limpiar_cache, True))
boton_limpiar.grid(row=1, column=1, padx=10, pady=5)

# Crear una etiqueta para indicar la acción
etiqueta_abrir_software = tk.Label(ventana_principal, text="Abrir Gestor de Software:")
etiqueta_abrir_software.grid(row=2, column=0, padx=10, pady=5, sticky="e")
# Crear un botón para abrir Snap Store
boton_abrir_software = tk.Button(ventana_principal, text="Abrir Snap Store", command=abrir_snap_store)
boton_abrir_software.grid(row=2, column=1, padx=10, pady=5)

etiqueta_abrir_boton_repositorios = tk.Label(ventana_principal, text="Administrar Repositorios:")
etiqueta_abrir_boton_repositorios.grid(row=3, column=0, padx=10, pady=5, sticky="e")
# Crear el botón para abrir la ventana de administrar repositorios
boton_admin_repositorios = tk.Button(ventana_principal, text="Administrar", command=abrir_administrador_repositorios)
boton_admin_repositorios.grid(row=3, column=1, padx=10, pady=5)

# Botón para reiniciar la tarjeta de red seleccionada
boton_reiniciar_red = tk.Button(ventana_principal, text="Reiniciar Tarjeta de Red", command=lambda: ComandosSistema.reiniciar_tarjeta_red(combo_interfaz.get(), etiqueta_ip_local_info, etiqueta_ip_publica_info, mostrar_mensaje))
boton_reiniciar_red.grid(row=4, column=0, padx=10, pady=10)
combo_interfaz = ttk.Combobox(ventana_principal, values=interfaces)
combo_interfaz.grid(row=4, column=1, padx=10, pady=10)

# Línea separadora
separador = ttk.Separator(ventana_principal, orient='horizontal')
separador.grid(row=5, column=0, columnspan=2, sticky='ew', pady=5)

# Botón monitorizar sistema
etiqueta_monitorizar = tk.Label(ventana_principal, text="Monitorizar Sistema:")
etiqueta_monitorizar.grid(row=6, column=0, padx=10, pady=5, sticky="e")
boton_monitorizar = tk.Button(ventana_principal, text="Monitorizar", command=comandos_sistema.monitorizar_sistema)
boton_monitorizar.grid(row=6, column=1, padx=10, pady=10)

# Botón aplicaciones al inicio
etiqueta_monitorizar = tk.Label(ventana_principal, text="Aplicaciones al Inicio:")
etiqueta_monitorizar.grid(row=7, column=0, padx=10, pady=5, sticky="e")
boton_monitorizar = tk.Button(ventana_principal, text="Modificar", command=lambda: AplicacionesAutostart(tk.Toplevel(ventana_principal)))
boton_monitorizar.grid(row=7, column=1, padx=10, pady=10)

# Administrar procesos
etiqueta_monitorizar = tk.Label(ventana_principal, text="Administrar Procesos:")
etiqueta_monitorizar.grid(row=8, column=0, padx=10, pady=5, sticky="e")
boton_administrar_procesos = tk.Button(ventana_principal, text="Administrar", command=lambda: AdministrarProcesos(tk.Toplevel(ventana_principal)))
boton_administrar_procesos.grid(row=8, column=1, padx=10, pady=10)
# Línea separadora
separador = ttk.Separator(ventana_principal, orient='horizontal')
separador.grid(row=10, column=0, columnspan=2, sticky='ew', pady=5)

# Botones para limpiar la caché
boton_limpiar_firefox = tk.Button(ventana_principal, text="Limpiar Caché Firefox", command=lambda: limpiar_cache_firefox(ventana_principal))
boton_limpiar_firefox.grid(row=11, column=0, padx=10, pady=5)

boton_limpiar_chrome = tk.Button(ventana_principal, text="Limpiar Caché Chrome", command=lambda: limpiar_cache_chrome(ventana_principal))
boton_limpiar_chrome.grid(row=12, column=0, padx=10, pady=5)

boton_limpiar_edge = tk.Button(ventana_principal, text="Limpiar Caché Edge", command=lambda: limpiar_cache_edge(ventana_principal))
boton_limpiar_edge.grid(row=13, column=0, padx=10, pady=5)


# COLUMNAS 2 y 3
# # Crear etiquetas para mostrar el usuario, la versión del sistema operativo, la versión del kernel y el entorno gráfico
etiqueta_sistema_usuario = tk.Label(ventana_principal, text="Usuario:")
etiqueta_sistema_usuario.grid(row=0, column=2, padx=10, pady=5, sticky="e")
etiqueta_sistema_operativo = tk.Label(ventana_principal, text="Sistema Operativo:")
etiqueta_sistema_operativo.grid(row=1, column=2, padx=10, pady=5, sticky="e")
etiqueta_version = tk.Label(ventana_principal, text="Versión de Ubuntu:")
etiqueta_version.grid(row=2, column=2, padx=10, pady=5, sticky="e")
etiqueta_version_kernel = tk.Label(ventana_principal, text="Kernel:")
etiqueta_version_kernel.grid(row=3, column=2, padx=10, pady=5, sticky="e")

etiqueta_tipo_escritorio = tk.Label(ventana_principal, text="Escritorio:")
etiqueta_tipo_escritorio.grid(row=4, column=2, padx=10, pady=5, sticky="e")
# Línea separadora
separador = ttk.Separator(ventana_principal, orient='horizontal')
separador.grid(row=5, column=2, columnspan=2, sticky='ew', pady=5)

# Crear etiquetas para mostrar las direcciones IP
etiqueta_ip_local = tk.Label(ventana_principal, text="Dirección IP Local:")
etiqueta_ip_local.grid(row=6, column=2, padx=10, pady=5, sticky="e")
etiqueta_ip_publica = tk.Label(ventana_principal, text="Dirección IP Pública:")
etiqueta_ip_publica.grid(row=7, column=2, padx=10, pady=5, sticky="e")

# Obtener la información del sistema
usuario, nombre_sistema, version_sistema, entorno_grafico = comandos_sistema.obtener_info_sistema()
tipo_escritorio = comandos_sistema.obtener_tipo_escritorio()
ip_local = comandos_sistema.obtener_direccion_ip_local()
ip_publica = comandos_sistema.obtener_direccion_ip_publica()

# Mostrar la información del sistema en las etiquetas
etiqueta_sistema_usuario_info = tk.Label(ventana_principal, text=usuario)
etiqueta_sistema_usuario_info.grid(row=0, column=3, padx=10, pady=5, sticky="w")
etiqueta_sistema_operativo_info = tk.Label(ventana_principal, text=nombre_sistema)
etiqueta_sistema_operativo_info.grid(row=1, column=3, padx=10, pady=5, sticky="w")
etiqueta_version_kernel_info = tk.Label(ventana_principal, text=entorno_grafico)
etiqueta_version_kernel_info.grid(row=2, column=3, padx=10, pady=5, sticky="w")
etiqueta_version_info = tk.Label(ventana_principal, text=version_sistema)
etiqueta_version_info.grid(row=3, column=3, padx=10, pady=5, sticky="w")
etiqueta_tipo_escritorio_info = tk.Label(ventana_principal, text=tipo_escritorio)
etiqueta_tipo_escritorio_info.grid(row=4, column=3, padx=10, pady=5, sticky="w")
# Mostrar las direcciones IP en etiquetas
etiqueta_ip_local_info = tk.Label(ventana_principal, text=ip_local)
etiqueta_ip_local_info.grid(row=6, column=3, padx=10, pady=5, sticky="w")
etiqueta_ip_publica_info = tk.Label(ventana_principal, text=ip_publica)
etiqueta_ip_publica_info.grid(row=7, column=3, padx=10, pady=5, sticky="w")


# Crear las etiquetas para los DNS
dns_local, dns_publico = ComandosSistema.obtener_servidores_dns()

etiqueta_dns_local = tk.Label(ventana_principal, text="DNS Local:")
etiqueta_dns_local.grid(row=8, column=2, padx=10, pady=5, sticky="e")

etiqueta_dns_local_info = tk.Label(ventana_principal, text=dns_local)
etiqueta_dns_local_info.grid(row=8, column=3, padx=10, pady=5, sticky="w")

etiqueta_dns_publico = tk.Label(ventana_principal, text="DNS Público:")
etiqueta_dns_publico.grid(row=9, column=2, padx=10, pady=5, sticky="e")

etiqueta_dns_publico_info = tk.Label(ventana_principal, text=dns_publico)
etiqueta_dns_publico_info.grid(row=9, column=3, padx=10, pady=5, sticky="w")

# Línea separadora
separador = ttk.Separator(ventana_principal, orient='horizontal')
separador.grid(row=10, column=2, columnspan=2, sticky='ew', pady=5)

# Crear etiquetas para mostrar mensajes de estado
etiqueta_limpiar_firefox_info = tk.Label(ventana_principal, text="")
etiqueta_limpiar_firefox_info.grid(row=11, column=1, padx=10, pady=5, sticky="w")

etiqueta_limpiar_chrome_info = tk.Label(ventana_principal, text="")
etiqueta_limpiar_chrome_info.grid(row=12, column=1, padx=10, pady=5, sticky="w")

etiqueta_limpiar_edge_info = tk.Label(ventana_principal, text="")
etiqueta_limpiar_edge_info.grid(row=13, column=1, padx=10, pady=5, sticky="w")

# Botón para mostrar el hardware del equipo
boton_info_hardware = tk.Button(ventana_principal, text="Mostrar Hardware", command=mostrar_generando_informe)
boton_info_hardware.grid(row=11, column=3, columnspan=2, padx=10, pady=10)

# Botón para escanear dispositivos y mostrarlos en una ventana nueva
boton_escanear = tk.Button(ventana_principal, text="Buscar equipos en red local", command=mostrar_dispositivos_en_ventana)
boton_escanear.grid(row=12, column=3, columnspan=2, padx=10, pady=10)


# Llamamos a la función salir para eliminar los archivos de configuración
ventana_principal.protocol("WM_DELETE_WINDOW", salir)
# Ejecutar la ventana principal
ventana_principal.mainloop()