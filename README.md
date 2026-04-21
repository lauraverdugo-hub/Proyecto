# GRUPO 3
Miembros del equipo: Alex Martinez Valverde, Luca Romero Marcia, Laura Verdugo Muñoz

# Versión 1
En esta primera versión nos centraremos en la manipulación de información sobre aeropuertos. Cada aeropuerto presenta información relevante (código ICAO, coordenadas y pertenencia al áera Schengen o no), que nos permitirá desarrollar funciones básicas. Entre estas seran cargar los aeropuertos desde un fichero, añadir y eliminar aeropuertos de esa lista, mostrar unos gráficos y mostrar la localización de cada aeropuerto en el Google Earth. Todas estas funciones se han designado en un fichero llamado airport.py. Seguidamente, se ha creado otro fichero llamado test_airport.py, el cual nos permite verificar que las funciones funcionan correctamente. Finalmente, se ha creado otro fichero llamado interface.py, donde se muestra una interfaz gráfica, desde la cual podemos probar todas las funciones implementadas en airport.py. De esta manera, en la interfaz gráfica podremos hacer:
- Cargar un fichero llamado airports.txt con todos los aeropuertos
- Añadir y eliminar aeropuertos
- Gráfico que muestra cuantos aeropuertos son de la zona Schengen y cuantos no
- Guardar una lista de aeropuertos exclusivos de la zona Schengen
- Mostrar la posición de cada aeropuerto en el Google Earth

Link a la demo de la V1: https://upcbcntech-my.sharepoint.com/personal/laura_verdugo_office365_estudiantat_upc_edu/_layouts/15/stream.aspx?id=%2Fpersonal%2Flaura%5Fverdugo%5Foffice365%5Festudiantat%5Fupc%5Fedu%2FDocuments%2FV%C3%ADdeos%2FClipchamp%2FProyecto%20de%20v%C3%ADdeo%201%2FExports%2FV1%2Emp4&referrer=StreamWebApp%2EWeb&referrerScenario=AddressBarCopied%2Eview%2Efe47689b%2D3d18%2D4180%2Da28e%2D568709e786fe&isDarkMode=false

# Versión 2
En esta segunda versión se incluirá información sobre los vuelos que llegan al aeropuerto del Prat de Barcelona (LEBL). Para cada uno de estos vuelos, sabemos el código del avión, su compañía de vuelo, su origen y el tiempo estimado para aterrizar. Con esta información, designaremos funciones para descragar información de cada vuelo desde un fichero, mostrar diferentes gráficos y mostrar las trayectorias de cada uno en el Google Earth en un fichero llamado aircraft.py. A diferencia de la versión anterior, en está incluiremos la sección de test al final de aircraft.py. Finalmente, incluiremos estas funciones a interface.py. De esta manera, en la interfaz gráfica podremos hacer:
- Cargar un fichero llamado arrivals.txt con todos los vuelos
- Guardar información de cada vuelo
- Gráfico que muestra la frecuencia de aterrizaje por cada hora
- Gráfico que muestra el número de vuelos por aerolínia
- Gráfico que muestra el número de vuelos que llegan desde la zona Schengen y de los que no
- Mostrar las trayectorias de los vuelos de más de 2000km en Google Earth

Link a la demo de la V2:
