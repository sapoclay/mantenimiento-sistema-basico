import os
import tkinter as tk
from tkinter import ttk

class AplicacionesAutostart:

    def __init__(self, master):
        self.master = master
        self.master.title("Configuración de Aplicaciones de Autostart")

        # Crear un Treeview para mostrar las aplicaciones de autostart
        self.treeview = ttk.Treeview(master, columns=("Aplicación"))
        self.treeview.heading("#0", text="ID")
        self.treeview.heading("#1", text="Aplicación")
        self.treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Obtener la lista de aplicaciones de autostart
        self.actualizar_lista_aplicaciones()

        # Botones para agregar y eliminar aplicaciones
        self.btn_agregar = tk.Button(master, text="Agregar", command=self.agregar_aplicacion)
        self.btn_agregar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_eliminar = tk.Button(master, text="Eliminar", command=self.eliminar_aplicacion)
        self.btn_eliminar.grid(row=1, column=1, padx=5, pady=5)

    def actualizar_lista_aplicaciones(self):
        # Limpiar el Treeview antes de actualizar
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        # Obtener la lista de aplicaciones de autostart
        aplicaciones_autostart = self.obtener_aplicaciones_autostart()

        # Agregar las aplicaciones al Treeview
        for i, app in enumerate(aplicaciones_autostart, start=1):
            self.treeview.insert("", "end", text=str(i), values=(app,))

    def obtener_aplicaciones_autostart(self):
        aplicaciones_autostart = []

        # Leer el contenido del directorio autostart
        autostart_dir = os.path.expanduser("~/.config/autostart/")
        if os.path.exists(autostart_dir):
            for filename in os.listdir(autostart_dir):
                if filename.endswith(".desktop"):
                    aplicaciones_autostart.append(filename[:-8])  # Eliminar la extensión .desktop

        return aplicaciones_autostart

    def agregar_aplicacion(self):
        # Permitir al usuario seleccionar un archivo .desktop para agregarlo al autostart
        archivo_desktop = tk.filedialog.askopenfilename(title="Seleccionar Aplicación",
                                                        filetypes=[("Archivos Desktop", "*.desktop")])
        if archivo_desktop:
            nombre_aplicacion = os.path.basename(archivo_desktop)
            destino = os.path.expanduser("~/.config/autostart/") + nombre_aplicacion
            os.system(f"cp {archivo_desktop} {destino}")
            self.actualizar_lista_aplicaciones()

    def eliminar_aplicacion(self):
        # Obtener el ID de la fila seleccionada en el Treeview
        seleccion = self.treeview.selection()
        if seleccion:
            id_fila = self.treeview.index(seleccion)
            aplicacion = self.treeview.item(seleccion)["values"][0]

            # Eliminar la aplicación del autostart
            ruta_aplicacion = os.path.expanduser(f"~/.config/autostart/{aplicacion}.desktop")
            os.remove(ruta_aplicacion)
            self.actualizar_lista_aplicaciones()
