# GRUPO 3
Miembros del equipo: Alex Martinez Valverde, Luca Romero Marcia, Laura Verdugo Muñoz

# Versión 1
En esta primera versión nos centraremos en la manipulación de información sobre aeropuertos. Cada aeropuerto presenta información relevante (código ICAO, coordenadas y pertenencia al áera Schengen o no), que nos permitirá desarrollar funciones básicas. Entre estas seran cargar los aeropuertos desde un fichero, añadir y eliminar aeropuertos de esa lista, mostrar unos gráficos y mostrar la localización de cada aeropuerto en el Google Earth. Todas estas funciones se han designado en un fichero llamado airport.py. Seguidamente, se ha creado otro fichero llamado test_airport.py, el cual nos permite verificar que las funciones funcionan correctamente. Finalmente, se ha creado otro fichero llamado interface.py, donde se muestra una interfaz gráfica, desde la cual podemos probar todas las funciones implementadas en airport.py. De esta manera, en la interfaz gráfica podremos hacer:
- Cargar un fichero llamado airports.txt con todos los aeropuertos
- Añadir y eliminar aeropuertos
- Gráfico que muestra cuantos aeropuertos son de la zona Schengen y cuantos no
- Guardar una lista de aeropuertos exclusivos de la zona Schengen
- Mostrar la posición de cada aeropuerto en el Google Earth

Link a la demo de la V1: https://youtu.be/dKBVPXncndo

# Versión 2
En esta segunda versión se incluirá información sobre los vuelos que llegan al aeropuerto del Prat de Barcelona (LEBL). Para cada uno de estos vuelos, sabemos el código del avión, su compañía de vuelo, su origen y el tiempo estimado para aterrizar. Con esta información, designaremos funciones para descragar información de cada vuelo desde un fichero, mostrar diferentes gráficos y mostrar las trayectorias de cada uno en el Google Earth en un fichero llamado aircraft.py. A diferencia de la versión anterior, en está incluiremos la sección de test al final de aircraft.py. Finalmente, incluiremos estas funciones a interface.py. De esta manera, en la interfaz gráfica podremos hacer:
- Cargar un fichero llamado arrivals.txt con todos los vuelos
- Guardar información de cada vuelo
- Gráfico que muestra la frecuencia de aterrizaje por cada hora
- Gráfico que muestra el número de vuelos por aerolínia
- Gráfico que muestra el número de vuelos que llegan desde la zona Schengen y de los que no
- Mostrar las trayectorias de los vuelos de más de 2000km en Google Earth

Link a la demo de la V2: https://youtu.be/EJtJWdHMbDo

# Versión 3
En esta tercera versión se incluirá nuevas funcionalidades para la gestión de puertas de embarque en el aeropuerto del Prat de Barcelona (LEBL). Para ello, se creará un fichero llamado LEBL.py, en el que se incluiran diferentes funciones. Entre ellas estan la configuración de puertas de embarque, que nos permite crear puertas de mediante rangos numéricos, asignarles una nomenclatura con prefijos y asegura un estado inicial limpio (todas las puertas libres), además de cargar datos desde archivos para actualizar la lista de aerolíneas de la terminal y completar la estructura de las puertas de embarque en el aeropuerto. También se mostrará el estado de ocupación de cada puerta, un sistema de búsqueda rápida para identificar en qué terminal opera cada compañía y una asignación de puertas según la ocupación.
Además, al igual que en la versión anterior, al final se incluirá una sección de test, con la que se comprobará que todo funcione correctamente. Finalmente, se incluiran estas funciones a interface.py. De esta manera, en la interfaz gráfica podremos ver:
- Crear la estructura de datos del aeropuerto LEBL
- Asignar puertas de embarque a los vuelos de llegada
- Visualizar la ocupación de las puertas de embarque (idealmente en forma de gráfico con la estructura del aeropuerto)

Link a la demo de la V3:
