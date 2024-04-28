## Mantenimiento básico de Ubuntu

------------------------------------------------------------------

Sistema de mantenimiento básico y otras cosas para Ubuntu. 
Creado con Python 3.
Versión actual del programa: 0.5

------------------------------------------------------------------
### Cosas que puede ir haciendo 
------------------------------------------------------------------

- Actualizar paquetes del sistema.
- Instalación desde gestor de software (tienda snap).
- Limpiar caché del sistema.
- Opción para trabajar con los repositorios instalados en el sistema (eliminar/editar/añadir). Todos los cambios se harán en el archivo source.list, pero se hará una copia de seguridad antes de realizar algún cambio en el archivo. La ubicación de la copia de seguridad será /etc/apt/sources.list.bak (esto todavía está en proceso por lo que puede fallar o no hacer lo que se espera)
- Reiniciar tarjetas de red.
- Incluye un menú Archivo y About con los que se puede interactuar a gole de clic.
- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez.
- Añadida la identificación del sistema (Ubuntu), Kernel, usuario, entorno gráfico, Ip pública, Ip Local, DNS local y DNS publicos, etc ...
- Añadida la monitorización del sistema con visualización en un gráfico con Tkinter y Matplotlib.
- Permite ver y ordenar los procesos del sistema, aun que el consumo de CPU se reduce al momento en el que se inicia este administrador de procesos. Se añade un buscador por nombre o PID para poder buscar el proceso que quieres cerrar con el botón creado para ello.
- Añadida la posibilidad de limpiar la caché de navegadores como Firefox, Chrome y Edge.
- Añadida la opción de diccionario en el menú Archivo. Este diccionario es obtenido de un archivo .md. El diccionario permite buscar entre todo su contenido. En la ventana del diccionario se ha añadido un menú desde el que el usuario podrá cargar archivos markdown para poder realizar consultas. El menú de esta ventana incluye también una opción para volver a cargar el diccionario por defecto, una opciń para cerrar el diccionario y la opción de abrir la terminal por defecto de Ubuntu (gnome-terminal).
- Se ha añadido la posibilidad de ver el hardware del equipo (procesador, grafica, tarjetas de red, etc ...)
- Para simplificar las cosas, al incio del programa se comprueba si la lista de dependencias que se muestra aquí debajo se cumple. Si no se cumple se procede a su instalación antes de intentar arrancar el programa.
- Se ha añadido la localización de equipos en la misma red. Dentro del listado de equipos obtenidos, tendremos la posibilidad de abrir con nautilus, si los permisos y el firewall lo permiten. Para esto se utiliza el protocolo samba, por lo que es necesario que esté instalado en el equipo con el que queremos conectarnos. En el equipo en el que se ejecute este script se instalará samba como dependencia.

## Dependencias Imprescindibles 

Dependencias necesarias para poder ejecutar el programa. Estas dependencias deben instalarse manualmente.

- Python3 -> sudo apt install python3.10 
- pip3 -> sudo apt install python3-pip

## Dependencias instalables

Estas dependencias las comprobará e instalará el programa una vez se ejecute si no las encuentra disponibles en el sistema.

- samba -> sudo apt install samba
- nmap -> sudo apt install python3-nmap
- Tkinter -> sudo apt install python3-tk
- Net-tools -> sudo apt install net-tools
- Pyqt5 -> sudo apt install python3-pyqt5
- Gnome-terminal -> sudo apt install gnome-terminal
- Matplotlib -> pip3 install matplotlib
- Pillow -> pip3 install --upgrade pillow
- Cryptography -> pip3 install cryptography
- psutil -> pip3 install psutil 
- markdown2 -> pip3 install markdown2
- PyQt5 -> pip3 install PyQt5
- ethtool -> sudo apt install ethtool
- speedtest-cli -> pip3 install speedtest-cli
- tabulate -> pip3 install tabulate
- opencv-python-headless -> pip3 install opencv-python-headless

## Instalación del paquete .DEB

- En una terminal (Ctrl+Alt+T):

  ``` sudo dpkg -i mantenimientobasico.deb ```

Tras la instalación deberías poder ver ya el lanzador del programa en el menú de Actividades.