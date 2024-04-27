## Mantenimiento básico de Ubuntu

------------------------------------------------------------------

Sistema de mantenimiento básico para Ubuntu. Creado con Python 3.
Versión actual del programa: 0.5
Por el momento se adapta solo a necesidades específicas del usuario
que me lo ha pedido.

------------------------------------------------------------------

- Actualizar paquetes
- Instalación desde gestor de software
- Limpiar caché del sistema
- Añadida una opción para trabajar con los repositorios instalados en el sistema (eliminar/editar). Además de darnos la posibilidad de añadir repositorios. Todos los cambios se harán en el archivo source.list, pero se hará una copia de seguridad antes de realizar algún cambio en el archivo. La ubicación de la copia de seguridad será /etc/apt/sources.list.bak (en proceso)
- Reiniciar tarjetas de red
- Menú Archivo y about
- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez.
- Se ha creado una clase para los comandos que se lancen. Y un módulo para los elementos de menú que se vayan creando.
- Añadida la identificación del sistema (Ubuntu), Kernel, usuario, entorno gráfico, Ip pública, Ip Local, DNS local y DNS publicos.
- Añadida la posibilidad de reiniciar la tarjeta de red que se seleccione en el desplegable.
- Añadida la monitorización del sistema con visualización en un gráfico con Tkinter y Matplotlib.
- Administrar procesos. Permite ordenar correctamente los procesos, aun que el consumo de CPU se reduce al momento en el que se inicia este administrador de procesos. Se añade un buscador por nombre o PID.
- Añadida la posibilidad de limpiar la caché de navegadores como Firefox, Chrome y Edge.
- Añadida la opción de diccionario en el menú Archivo. Este diccionario es obtenido de un archivo .md y permite buscar entre todo su contenido. Además en la ventana del diccionario he añadido un menú desde el que el usuario podrá cargar archivos markdown para poder realizar consultas. Además, también he puesto una opción para volver a cargar el diccionario por defecto. También se incluye en el menú la opción de Salir del diccionario y la opción de abrir la terminal por defecto de Ubuntu (gnome-terminal).
- Se ha añadido la posibilidad de ver el hardware del equipo (procesador, grafica, tarjetas de red, etc ...)
- Para simplificar las cosas, al incio del programa se comprueba si la lista de dependencias que se muestra aquí debajo se cumple. Si no se cumple se procede a su instalación antes de intentar arrancar el programa.
- Se ha añadido la localización de equipos en la misma red. Dentro del listado de equipos obtenidos, tendremos la posibilidad de abrir con nautilus, si los permisos y el firewall nos lo permiten. Para esto se utiliza el protocolo samba, por lo que es necesario que esté instalado en el equipo con el que queremos conectarnos. En el equipo en el que se ejecute este script se instalará samba como dependencia.

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

