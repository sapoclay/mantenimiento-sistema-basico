#import shutil
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog, Scrollbar
from password import obtener_contrasena

class Repositorios:
    def __init__(self, master):
        self.master = master
        master.title("Gestor de Repositorios")

        # Crear un marco para los botones de acción
        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(padx=10, pady=10)

        # Botones para agregar y restaurar repositorios
        tk.Button(self.frame_botones, text="Agregar Repositorio", command=self.agregar_repositorio).pack(side=tk.LEFT, padx=10)
        tk.Button(self.frame_botones, text="Restaurar sources.list", command=self.restaurar_backup).pack(side=tk.LEFT, padx=10)

        # Crear un marco para mostrar la lista de repositorios
        self.frame_repositorios = tk.Frame(master)
        self.frame_repositorios.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Inicializar la contraseña como None
        self.contrasena = None

        # Mostrar la lista de repositorios
        self.mostrar_repositorios()

        # Mostrar una advertencia sobre la copia de seguridad
        self.mostrar_advertencia_copia_seguridad()

    def hacer_backup_sources_list(self):
        contrasena = obtener_contrasena()
        if contrasena is None:
            messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para ejecutar esta acción.")
            return

        try:
            # Ejecutar el comando sudo cp para hacer una copia de seguridad del archivo sources.list
            comando = ['sudo', '-S', 'cp', '/etc/apt/sources.list', '/etc/apt/sources.list.bak']
            proceso = subprocess.run(comando, input=contrasena.encode(), text=True, capture_output=True, check=True)
            messagebox.showinfo("Éxito", "Copia de seguridad de sources.list creada correctamente.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo hacer una copia de seguridad de sources.list: {e}")

    def restaurar_backup(self):
        try:
            contrasena = obtener_contrasena()
            if contrasena is None:
                messagebox.showwarning("Contraseña requerida", "Debes ingresar la contraseña para ejecutar esta acción.")
                return

            # Ejecutar el comando sudo cp para restaurar la copia de seguridad del archivo sources.list
            comando = ['sudo', '-S', 'cp', '/etc/apt/sources.list.bak', '/etc/apt/sources.list']
            proceso = subprocess.run(comando, input=contrasena.encode(), text=True, capture_output=True, check=True)
            
            # Verificar si la copia de seguridad se restauró correctamente
            if proceso.returncode == 0:
                messagebox.showinfo("Éxito", "Copia de seguridad restaurada correctamente.")
                # Actualizar la lista de repositorios después de restaurar la copia de seguridad
                self.actualizar_repositorios()
            else:
                messagebox.showerror("Error", "No se pudo restaurar la copia de seguridad.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo restaurar la copia de seguridad: {e}")

    def agregar_repositorio(self):
        # Función interna para manejar el botón de "Guardar" en la ventana de agregar repositorio
        def guardar_repositorio():
            url = entry_url.get()
            if not url:
                messagebox.showerror("Error", "Por favor, ingrese la URL del repositorio.")
                return

            contrasena = obtener_contrasena()
            if not contrasena:
                return
            
            self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
            
            try:
                subprocess.run(['sudo', '-S', 'add-apt-repository', url], input=contrasena.encode(), check=True)
                messagebox.showinfo("Éxito", f"Repositorio {url} agregado correctamente.")
                ventana_agregar.destroy()
                # Actualizar la lista de repositorios después de agregar uno nuevo
                self.actualizar_repositorios()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"No se pudo agregar el repositorio: {e}")

        # Crear una nueva ventana para agregar el repositorio
        ventana_agregar = tk.Toplevel(self.master)
        ventana_agregar.title("Agregar Repositorio")

        # Etiqueta y campo de entrada para la URL del repositorio
        tk.Label(ventana_agregar, text="URL del Repositorio:").pack()
        entry_url = tk.Entry(ventana_agregar, width=50)
        entry_url.pack()

        # Botón para guardar el repositorio
        boton_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar_repositorio)
        boton_guardar.pack(pady=5)

    def mostrar_repositorios(self):
        # Limpiar el contenido del marco antes de mostrar la lista de repositorios
        for widget in self.frame_repositorios.winfo_children():
            widget.destroy()

        # Obtener la lista de repositorios instalados
        lista_repositorios = self.obtener_repositorios_instalados()

        # Crear una barra de desplazamiento vertical
        scrollbar = tk.Scrollbar(self.frame_repositorios, orient=tk.VERTICAL)

        # Crear un Listbox para mostrar los repositorios
        repos_listbox = tk.Listbox(self.frame_repositorios, yscrollcommand=scrollbar.set)

        # Agregar cada repositorio a la Listbox
        for repo in lista_repositorios:
            repos_listbox.insert(tk.END, repo)

        # Configurar la relación entre el Listbox y la barra de desplazamiento
        scrollbar.config(command=repos_listbox.yview)

        # Empacar la barra de desplazamiento y el Listbox en el marco de repositorios
        repos_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Asociar un evento de selección al Listbox para realizar acciones
        repos_listbox.bind('<<ListboxSelect>>', lambda event: self.seleccionar_repositorio(repos_listbox))

        # Configurar el tamaño de la ventana secundaria
        self.master.geometry("600x400")

        # Centrar la ventana secundaria
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x_offset = (self.master.winfo_screenwidth() - width) // 2
        y_offset = (self.master.winfo_screenheight() - height) // 2
        self.master.geometry(f"+{x_offset}+{y_offset}")

        
    def seleccionar_repositorio(self, listbox):
        # Obtener el índice del elemento seleccionado
        seleccion = listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            # Obtener el valor del repositorio seleccionado
            repo_seleccionado = listbox.get(indice)
            # Mostrar una ventana de diálogo para editar o eliminar el repositorio
            self.mostrar_ventana_accion_repo(repo_seleccionado)
    
    def mostrar_ventana_accion_repo(self, repo_seleccionado):
        # Crear una nueva ventana de diálogo
        ventana_dialogo = tk.Toplevel(self.master)
        ventana_dialogo.title("Editar o Eliminar Repositorio")

        # Etiqueta y campo de entrada para mostrar la URL del repositorio seleccionado
        tk.Label(ventana_dialogo, text="URL del Repositorio:").pack()
        entry_url = tk.Entry(ventana_dialogo, width=50)
        entry_url.insert(tk.END, repo_seleccionado)
        entry_url.pack()

        # Agregar menú contextual para el campo de entrada
        menu_contextual = tk.Menu(ventana_dialogo, tearoff=0)
        menu_contextual.add_command(label="Pegar", command=lambda: entry_url.event_generate("<<Paste>>"))
        entry_url.bind("<Button-3>", lambda event: menu_contextual.post(event.x_root, event.y_root))

        # Botones para aplicar cambios, eliminar o cancelar la operación
        boton_editar = tk.Button(ventana_dialogo, text="Editar Repositorio", command=lambda: self.editar_repositorio(repo_seleccionado, entry_url.get(), ventana_dialogo))
        boton_editar.pack(pady=5)
        boton_eliminar = tk.Button(ventana_dialogo, text="Eliminar Repositorio", command=lambda: self.eliminar_repo(repo_seleccionado, ventana_dialogo))
        boton_eliminar.pack(pady=5)
        boton_cancelar = tk.Button(ventana_dialogo, text="Cancelar", command=ventana_dialogo.destroy)
        boton_cancelar.pack(pady=5)

    def eliminar_repo(self, repo_a_eliminar, ventana_dialogo):
        # Solicitar confirmación al usuario antes de eliminar el repositorio
        confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de que deseas eliminar el repositorio '{repo_a_eliminar}'?")
        if confirmacion:
            contrasena = obtener_contrasena()
            if not contrasena:
                return

            try:
                self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
                # Ejecutar el comando para eliminar el repositorio
                subprocess.run(['sudo', '-S', 'add-apt-repository', '--remove', repo_a_eliminar], input=contrasena.encode(), check=True)
                messagebox.showinfo("Éxito", "Repositorio eliminado correctamente.")
                ventana_dialogo.destroy()
                # Actualizar la lista de repositorios después de eliminar uno
                self.actualizar_repositorios()
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"No se pudo eliminar el repositorio: {e}")

    def editar_repositorio(self, repo_original, repo_nuevo, ventana_dialogo):
        try:
            contrasena = obtener_contrasena()
            if not contrasena:
                return
            
            self.hacer_backup_sources_list()  # Hacer una copia de seguridad del archivo sources.list
            # Ejecutar el comando para editar el repositorio
            subprocess.run(['sudo', '-S', 'add-apt-repository', '--remove', repo_original], input=contrasena.encode(), check=True)
            subprocess.run(['sudo', '-S', 'add-apt-repository', repo_nuevo], input=contrasena.encode(), check=True)
            messagebox.showinfo("Éxito", "Repositorio editado correctamente.")
            ventana_dialogo.destroy()
            # Actualizar la lista de repositorios después de editar uno
            self.actualizar_repositorios()
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudo editar el repositorio: {e}")

    def obtener_repositorios_instalados(self):
        # Comando para obtener la lista de repositorios
        comando = "apt-cache policy | grep http | awk '{print $2 $3}'"

        # Ejecutar el comando y recuperar la salida
        try:
            resultado = subprocess.run(comando, shell=True, text=True, capture_output=True, check=True)
            repositorios = resultado.stdout.strip().split('\n')
            return repositorios
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"No se pudieron obtener los repositorios: {e}")
            return []

    def mostrar_advertencia_copia_seguridad(self):
        messagebox.showwarning("Advertencia", "Se realizará una copia de seguridad del archivo sources.list antes de hacer cualquier modificación. La ubicación de la copia de seguridad será: /etc/apt/sources.list.bak")

    def actualizar_repositorios(self):
        self.mostrar_repositorios()

def abrir_administrador_repositorios():
    ventana_admin_repos = tk.Toplevel(ventana_principal)
    ventana_admin_repos.title("Administrador de Repositorios")
    Repositorios(ventana_admin_repos)

# Ejecutar la ventana principal solo si este archivo se ejecuta directamente
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    boton_admin_repos = tk.Button(ventana_principal, text="Administrar Repositorios", command=abrir_administrador_repositorios)
    boton_admin_repos.pack()
    ventana_principal.mainloop()