## Mantenimiento básico de Ubuntu

------------------------------------------------------------------

![about-mantenimiento-basico](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/effd83b6-50c1-4d46-8b93-c52fe66deeb5)

Sistema de mantenimiento básico para Ubuntu. Creado con Python 3.
Versión actual del programa: 0.5
Por el momento se adapta solo a necesidades específicas del usuario
que me lo ha pedido.

------------------------------------------------------------------

### Acciones disponibles por el momento

![actualizar-sistema](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/f4e551ae-7dd7-44bf-8c2b-76c69938c745)
- Actualizar paquetes.
- Instalación desde gestor de software.
- Limpiar caché del sistema.
![administrar-repos](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/1f6d0a02-cbec-4985-81e3-3a4e4b5319f2)
- Añadida una opción para trabajar con los repositorios instalados en el sistema (eliminar/editar). Además de darnos la posibilidad de añadir repositorios. Todos los cambios se harán en el archivo source.list, pero se hará una copia de seguridad antes de realizar algún cambio en el archivo. La ubicación de la copia de seguridad será /etc/apt/sources.list.bak (en proceso de mejora. ¡Utilizar con cuidado por lo que pueda pasar!)
![reiniciar-tarjeta-de-red](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/58147f74-1cb3-4b0e-bc27-32969ccee1c9)
- Añadida la posibilidad de reiniciar la tarjeta de red que se seleccione en el desplegable.
- Menú Archivo y about.
![password-usuario](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/e20f6bec-01cc-4ee0-883e-3d0bd2caf1a8)
- Añadida la capacidad de almacenar de forma cifrada la contraseña del usuario, para solo tener que escribirla una única vez.
- Se ha creado una clase para los comandos que se lancen. Y un módulo para los elementos de menú que se vayan creando.
- Añadida la identificación del sistema (Ubuntu), tipo de escritorio y gestor de ventanas, Kernel, usuario, entorno gráfico, Ip pública, Ip Local, DNS local y DNS publicos.
![monitorizar-sistema](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/2bdd8fac-9a3b-49c1-81d7-21418584f7b2)
- Añadida la monitorización del sistema con visualización en un gráfico con Tkinter y Matplotlib.
![administrar-procesos](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/36fd22b4-d8a9-4029-b326-535e9c434641)
- Administrar procesos. Permite ordenar los procesos, aun que el consumo de CPU se reduce al momento en el que se inicia este administrador de procesos. Se añade un buscador por nombre o PID para poder cerrar dichos procesos.
![aplicaciones-al-inicio](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/f501105b-5ebd-4828-8dac-3e696a7f4fe0)
- Disponible la capacidad de añadir o eliminar aplicaciones que se ejecutan al inicio del sistema operativo.
![pantalla-principal](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/eeb07b97-6337-4761-bbd6-17c551b2aec2)
- Añadida la posibilidad de limpiar la caché de navegadores como Firefox, Chrome y Edge.
![diccionario](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/23e7eb11-1e92-4602-bf18-345ef78465db)
- Añadida la opción de diccionario en el menú Archivo. Este diccionario es obtenido de un archivo .md y permite buscar entre todo su contenido. Además en la ventana del diccionario he añadido un menú desde el que el usuario podrá cargar archivos markdown para poder realizar consultas. Además, también he puesto una opción para volver a cargar el diccionario por defecto. También se incluye en el menú la opción de Salir del diccionario y la opción de abrir la terminal por defecto de Ubuntu (gnome-terminal). Por el momento esto solo lo he probado en X11.
![informe-hardware](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/248383c7-8f9b-4a87-8ef7-fd9ce4d51aeb)
- Se ha añadido la posibilidad de ver el hardware del equipo (procesador, grafica, tarjetas de red, etc ...)
![comprobacion-dependencias](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/f83250c5-2bbf-4ff8-bc3e-75f6e42f9c66)
- Para simplificar las cosas, al incio del programa se comprueba si la lista de dependencias que se muestra aquí debajo se cumple. Si no se cumple se procede a su instalación antes de intentar arrancar el programa.
![equipos-red-local](https://github.com/sapoclay/mantenimiento-sistema-basico/assets/6242827/acfa6f8b-5f9e-4fa3-b4ba-6351a8139c52)
- Se ha añadido la localización de equipos en la misma red. Dentro del listado de equipos obtenidos, tendremos la posibilidad de abrir con nautilus, si los permisos y el firewall nos lo permiten. Para esto se utiliza el protocolo samba, por lo que es necesario que esté instalado en el equipo con el que queremos conectarnos. En el equipo en el que se ejecute este script se instalará samba como dependencia.

------------------------------------------------------------------

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

