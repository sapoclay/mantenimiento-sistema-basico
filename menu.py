import tkinter as tk
from tkinter import messagebox
import os

def salir(ventana):
    if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
        ventana.destroy()

def mostrar_about():
    about_window = tk.Toplevel()
    about_window.title("Acerca de")
    about_window.geometry("400x200")
    about_window.resizable(False, False)

    # Obtener la ruta absoluta del directorio del script
    dir_actual = os.path.dirname(os.path.realpath(__file__))
    ruta_imagen = os.path.join(dir_actual, "logo.png")

    # Cargar la imagen
    img = tk.PhotoImage(file=ruta_imagen)

    # Mostrar la imagen en un Label
    img_label = tk.Label(about_window, image=img)
    img_label.image = img  # Mantener una referencia para evitar que la imagen sea eliminada por el recolector de basura
    img_label.pack(pady=10)

    about_label = tk.Label(about_window, text="Mantenimiento de Sistema Ubuntu\nVersión: 0.5.1\nEste programa realiza tareas de mantenimiento básico\nen sistemas Ubuntu.\nNo se dan garantías de ningún tipo.\n")
    about_label.pack(padx=20, pady=20)
