from airport import *

# Crear un aeropuerto manual y comprovar si pertenece a Schengen
airport1 = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport1)
PrintAirport (airport1)

print("   ")

airport2 = Airport ("LFPG", 49.0097, 2.5479)
SetSchengen(airport2)
PrintAirport (airport2)

print("   ")

airport3 = Airport ("KJFK", 40.6413, -73.7781)
SetSchengen(airport3)
PrintAirport (airport3)

print("-----")

# Cargar aeropuertos desde archivo
airports = LoadAirports("airports.py")  # asegúrate de tener este archivo con datos DMS
print(f"Cargados {len(airports)} aeropuertos")
for a in airports:
    SetSchengen(a)  # marcar si es Schengen
    PrintAirport(a)

print("-----")

# Agregar un aeropuerto
new_airport = Airport("LIS", 38.774, -9.134)  # Lisboa
SetSchengen(new_airport)
AddAirport(airports, new_airport)
for a in airports:
    if a.icao_code == "LIS":
        PrintAirport(a)

print("-----")

# Eliminar un aeropuerto
RemoveAirport(airports, "CYUL")  # Montreal, si existía en lista
print("Antes de eliminar CYUL:")
for a in airports:
    PrintAirport(a)
print("Después de eliminar CYUL:")
for a in airports:
    if a.icao_code == "CYUL":
        PrintAirport(a)

print("-----")

# Guardar aeropuertos Schengen en archivo
ret_code = SaveSchengenAirports(airports, "schengen_airports.py")
if ret_code == -1:
    print("No hay aeropuertos Schengen para guardar")
else:
    print("Archivo schengen_airports.py creado con aeropuertos Schengen")

print("-----")

# Mostrar gráfica y mapa de Google Earth
PlotAirports(airports)   # Muestra gráfico de barras

MapAirports(airports)    # Genera archivo KML para Google Earth