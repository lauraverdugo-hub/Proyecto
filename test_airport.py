from airport import *
import matplotlib.pyplot as plt

# =========================================================
# CREACIÓN MANUAL DE AEROPUERTOS
# =========================================================

# Crear un aeropuerto manual y comprovar si pertenece a Schengen
airport1 = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport1)
PrintAirport(airport1)

print("   ")

airport2 = Airport ("LFPG", 49.0097, 2.5479)
SetSchengen(airport2)
PrintAirport(airport2)

print("   ")

airport3 = Airport ("KJFK", 40.6413, -73.7781)
SetSchengen(airport3)
PrintAirport(airport3)

print("-----")

# =========================================================
# CARGA DE AEROPUERTOS DESDE ARCHIVO
# =========================================================

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

# Mostrar gráfica y mapa de Google Earth
print("Generando gráfico de aeropuertos...")
fig, ax = plt.subplots(figsize=(7, 6))
PlotAirports(airports, ax)  # Muestra gráfico de barras
plt.tight_layout()
plt.show()

print("Generando archivo KML para Google Earth...")
MapAirports(airports)    # Genera archivo KML para Google Earth

print("\n--- Pruebas finalizadas ---")