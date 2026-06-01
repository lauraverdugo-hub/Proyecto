from airport import *
import matplotlib.pyplot as plt

# =========================================================
# CREACIÓN MANUAL DE AEROPUERTOS
# =========================================================

<<<<<<< HEAD
=======
"""
   Programa principal para gestionar aeropuertos.
   Funciones realizadas:
    1. Crear aeropuertos manualmente.
    2. Comprobar si pertenecen al espacio Schengen.
    3. Mostrar información por pantalla.
    4. Cargar aeropuertos desde un archivo.
    5. Añadir y eliminar aeropuertos.
    6. Guardar aeropuertos Schengen en un archivo.
    7. Mostrar estadísticas gráficas.
    8. Generar un archivo KML para Google Earth.
"""

"""
   Crea manualmente un aeropuerto y comprueba si pertenece al espacio Schengen.
   Formato:
         Airport(codigo_ICAO, latitud, longitud)
   Resultado:
         Se crea un objeto Airport, se actualiza el atributo Schengen y se muestra por pantalla.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
# Crear un aeropuerto manual y comprovar si pertenece a Schengen
airport1 = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport1)
PrintAirport(airport1)

print("   ")

<<<<<<< HEAD
=======
"""
   Creación del aeropuerto Charles de Gaulle (París).
   Resultado:
          Se muestra la información completa del aeropuerto.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
airport2 = Airport ("LFPG", 49.0097, 2.5479)
SetSchengen(airport2)
PrintAirport(airport2)

print("   ")

<<<<<<< HEAD
=======
"""
   Creación del aeropuerto JFK (Nueva York).
   Resultado:
          Se muestra la información del aeropuerto indicando que no pertenece al espacio Schengen.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
airport3 = Airport ("KJFK", 40.6413, -73.7781)
SetSchengen(airport3)
PrintAirport(airport3)

print("-----")

# =========================================================
# CARGA DE AEROPUERTOS DESDE ARCHIVO
# =========================================================

<<<<<<< HEAD
=======
"""
   Carga aeropuertos desde un archivo de texto.
   Formato del archivo:
          CODE LAT LON
          LEBL N412300 E0020500
   Resultado:
          Se crea una lista de objetos Airport.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
# Cargar aeropuertos desde archivo
airports = LoadAirports("airports.py")  # asegúrate de tener este archivo con datos DMS
print(f"Cargados {len(airports)} aeropuertos")
for a in airports:
    SetSchengen(a)
    PrintAirport(a)

print("-----")

# =========================================================
# AGREGAR AEROPUERTO
# =========================================================

<<<<<<< HEAD
=======
"""
   Añade un nuevo aeropuerto a la lista.
   Formato:
         Airport("LIS", latitud, longitud)
   Resultado:
         Si el aeropuerto no existe previamente se añade a la lista.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
# Agregar un aeropuerto
new_airport = Airport("LIS", 38.774, -9.134)  # Lisboa
SetSchengen(new_airport)
AddAirport(airports, new_airport)
for a in airports:
    if a.icao_code == "LIS":
        PrintAirport(a)

print("-----")

# =========================================================
# ELIMINAR AEROPUERTO
# =========================================================

<<<<<<< HEAD
=======
"""
   Elimina un aeropuerto de la lista utilizando su código ICAO.
   Parámetros:
           Lista de aeropuertos y código ICAO.
   Resultado:
           El aeropuerto se elimina si existe.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
# Eliminar un aeropuerto
RemoveAirport(airports, "CYUL")  # Montreal, si existía en lista
print("Antes de eliminar CYUL:")
for a in airports:
    PrintAirport(a)
RemoveAirport(airports, "CYUL")
print("Después de eliminar CYUL:")
found = False
for a in airports:
    if a.icao_code == "CYUL":
        PrintAirport(a)
        found = True
if not found:
    print("CYUL eliminado correctamente.")

print("-----")

# =========================================================
# GUARDAR AEROPUERTOS SCHENGEN
# =========================================================

<<<<<<< HEAD
=======
"""
   Guarda únicamente los aeropuertos Schengen en un archivo de texto.
   Formato del archivo generado:
          CODE LAT LON
   Resultado:
          Se genera el archivo 'schengen_airports.py'.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
# Guardar aeropuertos Schengen en archivo
ret_code = SaveSchengenAirports(airports, "schengen_airports.py")
if ret_code == -1:
    print("No hay aeropuertos Schengen para guardar")
else:
    print("Archivo schengen_airports.txt creado con aeropuertos Schengen")

print("-----")

# =========================================================
# MAPA KML Y GRÁFICO DE AEROPUERTOS
# =========================================================

<<<<<<< HEAD
# Mostrar gráfica y mapa de Google Earth
print("Generando gráfico de aeropuertos...")
fig, ax = plt.subplots(figsize=(7, 6))
PlotAirports(airports, ax)  # Muestra gráfico de barras
=======
"""
   Muestra una gráfica de barras con la cantidad de aeropuertos Schengen y no Schengen. También genera un archivo KML para visualizar los aeropuertos en Google Earth.
   Resultado:
          Se abre una ventana con la gráfica generada mediante matplotlib. También se crea el archivo 'airports.kml'.
"""
# Mostrar gráfica y mapa de Google Earth
print("Generando gráfico de aeropuertos...")
fig, ax = plt.subplots(figsize=(7, 6))
PlotAirports(airports, ax) # Muestra gráfico de barras
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
plt.tight_layout()
plt.show()

print("Generando archivo KML para Google Earth...")
MapAirports(airports)    # Genera archivo KML para Google Earth

<<<<<<< HEAD
print("\n--- Pruebas finalizadas ---")
=======
print("\n--- Pruebas finalizadas ---")
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
