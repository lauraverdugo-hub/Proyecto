# GRUPO 3
Miembros del equipo: Alex Martinez Valverde, Luca Romero Marcia, Laura Verdugo Muñoz

<img src=https://github.com/lauraverdugo-hub/Proyecto/blob/1a846f964df05c4af2f351f8f136ba739f68fa24/1000033472.webp width="100" height="150">                                                   <img src=https://github.com/lauraverdugo-hub/Proyecto/blob/1a846f964df05c4af2f351f8f136ba739f68fa24/IMG_8128.jpeg width="100" height="150">                                                 <img src=https://github.com/lauraverdugo-hub/Proyecto/blob/4d12c4d082931b3d6bd5952f3fa75f1e748cf8c5/Captura%20de%20pantalla%202026-06-01%20214619.png width="100" height="150">

# Versión 1
En esta primera versión, el desarrollo se centra en el almacenamiento y manipulación de información sobre aeropuertos. Cada aeropuerto cuenta con atributos clave como su código ICAO, coordenadas geográficas y su pertenencia o no al espacio Schengen. A partir de estos datos, se han implementado funciones básicas para cargar la lista de aeropuertos desde un archivo de texto (airports.txt), añadir o eliminar registros de aeropuertos de una lista, generar gráficos estadísticos y proyectar la localización exacta de cada aeropuerto en Google Earth mediante la generación de archivos KML.  

Todas estas funciones estan implementadas en el fichero airport.py. Para verificar su correcto funcionamiento se ha desarrollado otro fichero de pruebas (test_airport.py). Finalmente, se ha creado el archivo interface.py, el cual despliega una interfaz gráfica desarrollada en Tkinter que unifica todas las herramientas de control. A través de esta interfaz, el usuario puede:

- Cargar un archivo de texto con el listado global de aeropuertos (airports.txt).  
- Añadir nuevos aeropuertos o eliminar existentes de la lista activa.  
- Visualizar un gráfico de barras apiladas que muestre la proporción de aeropuertos pertenecientes y no pertenecientes a la zona Schengen.  
- Filtrar y exportar de forma exclusiva la lista de aeropuertos pertenecientes al espacio Schengen a un nuevo archivo.  
- Exportar y mostrar la posición geográfica de los aeropuertos en Google Earth, diferenciándolos por colores según su estado Schengen.

Link a la demo de la V1: https://youtu.be/dKBVPXncndo

# Versión 2
La segunda versión amplía el alcance de la aplicación al integrar información detallada sobre los vuelos que llegan al aeropuerto de Barcelona-El Prat (LEBL). Para cada aeronave, el sistema procesa su identificador de vuelo, el código ICAO de su compañía aérea, el aeropuerto de origen y la hora estimada de aterrizaje. Con estos datos, se han diseñado funciones específicas para la lectura de datos desde un fichero de texto (arrivals.txt), la representación de gráficas y el mapeo de las rutas aéreas en Google Earth.

Estas funciones se han implemnetado en el fichero aircraft.py. A diferencia de la versión anterior, la sección de pruebas se integra directamente al final de este archivo. Toda esto se acopla posteriormente a interface.py. De este modo, la interfaz gráfica permite realizar las siguientes acciones:

- Cargar el archivo de vuelos diarios (arrivals.txt).  
- Almacenar y exportar la información procesada de las aeronaves a un fichero externo.  
- Generar un gráfico representativo de la frecuencia de aterrizajes desglosada por franjas horarias.  
- Desplegar un gráfico de barras con la cantidad de vuelos operados por cada aerolínea.  
- Mostrar un gráfico de barras apiladas comparando el número de vuelos procedentes de orígenes Schengen frente a los que no pertenecen a esa zona.  
- Calcular distancias geográficas y proyectar en Google Earth las trayectorias de aquellos vuelos de larga distancia que superen los 2000 km.

Link a la demo de la V2: https://youtu.be/EJtJWdHMbDo

# Versión 3
Esta tercera versión introduce la infraestructura física y el modelado logístico para la gestión de las puertas de embarque del aeropuerto de Barcelona-El Prat (LEBL). Para ello, se crea el fichero LEBL.py, el cual se definen las clases BarcelonaAP, Terminal, BoardingArea y Gate. El sistema permite configurar de forma automatizada las puertas de embarque mediante rangos numéricos y la concatenación de prefijos específicos por cada zona, garantizando un estado inicial libre de ocupación. Asimismo, procesa los archivos de aerolíneas (T1_Airlines.txt y T2_Airlines.txt) para vincular qué compañías operan en cada terminal.  

Las funciones determinan el estado de ocupación de las instalaciones, ofrecen búsquedas rápidas de terminal por aerolínea y resuelven la asignación de puertas en función de la compañía aérea del vuelo y el carácter Schengen/no Schengen de su procedencia. Al igual que en la versión 2, la sección de pruebas se ejecuta al final del propio fichero antes de exportar sus controles a interface.py. Desde la interfaz gráfica, el usuario puede:  

- Construir e inicializar dinámicamente toda la estructura de datos del aeropuerto LEBL a partir de su archivo de configuración (LEBL.txt).  
- Asignar de manera estática una puerta de embarque idónea y libre a cada uno de los vuelos que llegan al aeropuerto.  
- Monitorear e inspeccionar el estado de ocupación de las puertas en tiempo real (pudiendo integrar de forma adicional un gráfico representativo de la planta del aeropuerto con el estado de cada puerta).

Link a la demo de la V3: https://youtu.be/BdrKllftA4Y

# Versión 4
Esta cuarta y última versión amplía el sistema hacia un entorno operativo dinámico y realista al incorporar el flujo de salidas del aeropuerto. Para ello, se expande la clase Aircraft en aircraft.py para procesar la hora de salida y el aeropuerto de destino final de los vuelos. Las funciones diseñadas permiten leer un archivo de salidas (departures.txt), fusionar los movimientos de llegada y salida de una misma aeronave comprobando la compatibilidad de sus horarios e identificar aquellos aviones que pasaron la noche estacionados en el aeropuerto y realizan su primer despegue a primera hora de la mañana.

El núcleo del programa (LEBL.py) se rediseña por completo para pasar de un modelo estático a uno dinámico, organizado por franjas horarias. A medida que avanza el tiempo en la simulación, el sistema libera automáticamente las puertas de embarque de los aviones que ya han despegado, dejándolas disponibles para los nuevos vuelos que van a aterrizar. Al igual que en las versiones anteriores, se incluye la sección de pruebas al final del código y se actualiza la interfaz gráfica. Desde este panel de control, el usuario puede:

- Utilizar todas las funciones desarrolladas en las versiones anteriores.
- Cargar el archivo de salidas (departures.txt) y vincular los despegues con las llegadas de un mismo avión.
- Simular el paso del tiempo, asignando puertas de embarque de manera dinámica hora por hora.
- Generar gráficos de ocupación por terminal para ver cuántas puertas se usan cada hora y cuántos vuelos se han quedado sin puerta debido a la ocupación del aeropuerto.

Link a la demo de la V4:
