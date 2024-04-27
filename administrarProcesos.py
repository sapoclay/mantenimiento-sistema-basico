import tkinter as tk
from tkinter import ttk
import psutil
import threading
from tkinter import font
import tkinter.messagebox as messagebox

class AdministrarProcesos:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrar Procesos")
        self.column_sort_order = {}  # Diccionario para guardar el orden de clasificación de las columnas
        
        self.tree = ttk.Treeview(self.root, columns=("PID", "Nombre", "Uso de CPU"))
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("#1", text="PID", anchor=tk.W, command=lambda: self.sort_column("#1"))
        self.tree.heading("#2", text="Nombre", anchor=tk.W, command=lambda: self.sort_column("#2"))
        self.tree.heading("#3", text="Uso de CPU", anchor=tk.W, command=lambda: self.sort_column("#3"))
        self.tree.column("#0", stretch=tk.NO, width=0)
        self.tree.column("#1", stretch=tk.YES, width=100)
        self.tree.column("#2", stretch=tk.YES, width=200)
        self.tree.column("#3", stretch=tk.YES, width=100)
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        self.scrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)  # Mover el árbol a la izquierda
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Colocar la barra de desplazamiento a la derecha

        # Crear una fuente en negrita
        bold_font = font.Font(weight="bold")

        # Crear la etiqueta con el texto "Opciones" en negrita
        label = tk.Label(self.root, text="Opciones", font=bold_font)
        label.pack(side=tk.TOP, pady=(0, 5))  # Ajustar el relleno superior según sea necesario

        
        self.search_entry_var = tk.StringVar()
        self.search_entry_var.set("Buscar por nombre o PID")
        self.search_entry = tk.Entry(self.root, textvariable=self.search_entry_var, fg="grey")
        self.search_entry.pack(side=tk.TOP, fill=tk.X)
        self.search_entry.bind("<FocusIn>", self.on_entry_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.search_entry.bind("<KeyRelease>", self.filter_processes)
        
        self.close_button = tk.Button(self.root, text="Cerrar Proceso", command=self.close_process)
        self.close_button.pack(side=tk.TOP)
        
        self.load_processes()

    def on_entry_focus_in(self, event):
        if self.search_entry_var.get() == "Buscar por nombre o PID":
            self.search_entry_var.set("")
            self.search_entry.config(fg="black")

    def on_entry_focus_out(self, event):
        if not self.search_entry_var.get():
            self.search_entry_var.set("Buscar por nombre o PID")
            self.search_entry.config(fg="grey")
            
    def load_processes(self):
        self.tree.delete(*self.tree.get_children())
        for proc in psutil.process_iter(['pid', 'name']):
            proc_info = proc.info
            try:
                self.tree.insert("", "end", text="", values=(proc_info['pid'], proc_info['name'], "Calculando..."))
                threading.Thread(target=self.update_cpu_usage_single, args=(proc_info['pid'],)).start()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                self.tree.insert("", "end", text="", values=(proc_info['pid'], proc_info['name'], "N/A"))

    def close_process(self):
        selected_item = self.tree.selection()
        if selected_item:
            pid = self.tree.item(selected_item)["values"][0]
            name = self.tree.item(selected_item)["values"][1]
            confirm = messagebox.askyesno("Confirmar cierre", f"¿Estás seguro de que quieres cerrar el proceso {name} (PID: {pid})?")
            if confirm:
                try:
                    process = psutil.Process(pid)
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass
                self.load_processes()
            
    def filter_processes(self, event):
        query = self.search_entry_var.get().lower()
        for item in self.tree.get_children():
            pid = str(self.tree.item(item)["values"][0])  # Convertir el PID a cadena
            name = self.tree.item(item)["values"][1].lower()
            if query in pid or query in name:
                self.tree.selection_set(item)
                self.tree.see(item)
            else:
                self.tree.selection_remove(item)
                
    def sort_column(self, column):
        column_index = int(column[1:]) - 1
        current_sort_order = self.column_sort_order.get(column, "asc")  # Obtener el orden actual de clasificación de la columna
        items = [(self.tree.set(child, column_index), child) for child in self.tree.get_children('')]

        if column_index == 0:  # Verificar si la columna es PID
            items.sort(key=lambda x: int(x[0]), reverse=current_sort_order == "desc")  # Convertir a entero antes de ordenar
        elif column_index == 1:  # Verificar si la columna es Nombre
            items.sort(key=lambda x: x[0].lower(), reverse=current_sort_order == "desc")
        elif column_index == 2:  # Verificar si la columna es Uso de CPU
            items.sort(key=lambda x: float(x[0].rstrip("%")) if x[0] != "N/A" else float('inf'), reverse=current_sort_order == "desc")  # Convertir a float antes de ordenar

        for index, (value, child) in enumerate(items):
            self.tree.move(child, '', index)

        self.column_sort_order[column] = "desc" if current_sort_order == "asc" else "asc"
    
    def update_cpu_usage_single(self, pid):
        try:
            process = psutil.Process(pid)
            cpu_percent = process.cpu_percent(interval=0.5)
            self.root.after(0, self.update_tree, pid, f"{cpu_percent:.2f}%")
        except psutil.NoSuchProcess:
            print(f"No se pudo calcular el uso de CPU para el proceso {pid}: process PID not found")
        except Exception as e:
            print(f"No se pudo calcular el uso de CPU para el proceso {pid}: {e}")


    def update_tree(self, pid, cpu_percent):
        for child in self.tree.get_children():
            if self.tree.item(child)["values"][0] == pid:
                self.tree.item(child, values=(pid, self.tree.item(child)["values"][1], cpu_percent))
