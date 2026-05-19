from airport import IsSchengenAirport
import matplotlib.pyplot as plt

"""
   Módulo de gestión de vuelos y llegadas de aeronaves.
   Funciones principales:
    1. Cargar vuelos desde un archivo.
    2. Mostrar estadísticas de llegadas.
    3. Guardar vuelos en archivos.
    4. Generar gráficas con matplotlib.
    5. Crear mapas KML para Google Earth.
    6. Calcular distancias mediante la fórmula de Haversine.
    7. Filtrar vuelos de larga distancia.
"""

"""
    Clase que representa una aeronave.
    Atributos:
        aircraft_id : str
             Identificador o matrícula de la aeronave.
        airline_company : str
             Código ICAO de la aerolínea.
        origin_airport : str
             Código ICAO del aeropuerto de origen.
        landing_time : str
             Hora de llegada en formato hh:mm.
    Resultado:
        Crea un objeto Aircraft con todos sus atributos.
"""
class Aircraft:
    def __init__(self, aircraft_id, airline_company, origin_airport, landing_time):
        self.aircraft_id = aircraft_id
        self.origin_airport = origin_airport
        self.landing_time = landing_time
        self.airline_company = airline_company

"""
    Carga vuelos desde un archivo de texto.
    Parámetros:
         filename (str): Nombre del archivo de entrada.
    Formato del archivo:
         AIRCRAFT ORIGIN ARRIVAL AIRLINE
         AEA123 LEBL 10:30 IBE
    Resultado:
         list: Lista de objetos Aircraft. Devuelve [] si el archivo no existe.
"""
def LoadArrivals(filename):
    aircrafts = [] # Abre el archivo y devuelve una lista de Aircraft
    try:
        with open(filename, "r") as F: # Abre archivo y se cierra automáticamente
            next(F) # Saltar encabezado: AIRCRAFT ORIGIN ARRIVAL AIRLINE
            for line in F:
                parts = line.strip().split()
                if len(parts) == 4:
                    aircraft_id = parts[0]
                    origin = parts[1]
                    arrival_time = parts[2]
                    airline = parts[3]

                    # Validación del formato de tiempo (hh:mm)
                    if len(parts) == 4:
                        if ":" in arrival_time:
                            # Intentamos dividir el tiempo para asegurar que son números reales
                            h_m = arrival_time.split(":") # Separamos la hora en dos partes
                            if h_m[0].isdigit() and h_m[1].isdigit(): # .isdigit() comprueba que sean números reales
                                new_aircraft = Aircraft(aircraft_id, airline, origin, arrival_time)
                                aircrafts.append(new_aircraft)
    except FileNotFoundError:
        return []
    return aircrafts

<<<<<<< HEAD
def PlotArrivals(aircrafts, ax):
=======
import matplotlib.pyplot as plt

"""
    Genera una gráfica de llegadas por hora.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra un gráfico de barras con el número de aterrizajes por hora.
"""
def PlotArrivals(aircrafts):
>>>>>>> ffaaecd455fc3543e55a48b559ac0012e4773e8a
    if not aircrafts:
        print("Error: The aircraft list is empty.")
        return

    # Inicializamos contador para las 24 horas del día
    hours_count = [0] * 24
    i = 0
    while i < len(aircrafts):
        time_str = aircrafts[i].landing_time # Guardamos la hora de cada avión en la variable time_str
        try:
            # Extraemos la hora antes de los dos puntos para operar con ella
            hour = int(time_str.split(':')[0])
            if hour >= 0 and hour < 24:
                hours_count[hour] += 1 # Sumamos al contador
        except (ValueError, IndexError):
            pass  # Ignorar formatos de tiempo inválidos y pasar al siguiente
        i += 1

    # Configuración de la gráfica
    hours_labels = [f"{h}h" for h in range(24)] # Coge el número (entre 0 y 23) que hay en h y le pone la letra "h" al final

    # Limpiar eje
    ax.clear()

    # Fondo minimalista
    ax.set_facecolor("#ffffff")

    # Barras
    ax.bar(hours_labels,hours_count,color='#9dc3e6',edgecolor='#2f5597',label='Flights per hour')

    # Configuración
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Landings')
    ax.set_title('Landing Frequency at Barcelona El Prat (LEBL)')

    ax.grid(axis='y',linestyle='--',alpha=0.5)
    ax.legend()

"""
    Guarda vuelos en un archivo de texto.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
        filename (str): Nombre del archivo de salida.
    Formato:
        Campos vacíos se sustituyen por "-" o "0".
    Resultado:
        Genera un archivo con los vuelos. Devuelve un mensaje de error si ocurre un problema.
"""
def SaveFlights(aircrafts, filename):
    if not aircrafts:
        return "Error: Empty list" # Código de error

    try:
        F = open(filename, "w") # Abrimos el archivo en modo escritura
        F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n") # Escribimos el encabezado
        j = 0
        while j < len(aircrafts):
            a = aircrafts[j] # Guardamos el avión en la variable a
            # Gestión de campos vacíos según requerimiento
            # Si el campo tiene información la pone, pero si está vacío, pone un 0 o un guion
            if a.aircraft_id:
                id_val = a.aircraft_id
            else:
                id_val = "-"
            if a.origin_airport:
                orig_val = a.origin_airport
            else:
                orig_val = "-"
            if a.landing_time:
                time_val = a.landing_time
            else:
                time_val = "0"
            if a.airline_company:
                airl_val = a.airline_company
            else:
                airl_val = "-"
            line = f"{id_val} {orig_val} {time_val} {airl_val}\n"
            F.write(line)
            j += 1 # El bucle avanza
        F.close()
    except Exception:
        return "Error during file writing"

    return None  # En caso de no haver error devuelve None (operación completada con éxito)

<<<<<<< HEAD
def PlotAirlines(aircrafts, ax):
=======
"""
    Genera una gráfica de vuelos por aerolínea.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra un gráfico de barras con la cantidad de vuelos por aerolínea.
"""
def PlotAirlines(aircrafts):
>>>>>>> ffaaecd455fc3543e55a48b559ac0012e4773e8a
    if not aircrafts:
        print("Error: The aircraft list is empty.")
        return

    # 1. Contar vuelos por aerolínea usando un diccionario
    airline_counts = {} # Crea un diccionario vacío donde guardaremos CÓDIGO: CANTIDAD
    i = 0
    while i < len(aircrafts):
        code = aircrafts[i].airline_company
        if code in airline_counts:
            airline_counts[code] += 1
        else:
            airline_counts[code] = 1
        i += 1

    # 2. Preparar datos para el gráfico
    # Convertimos el diccionario en dos listas independientes
    labels = list(airline_counts.keys())
    values = list(airline_counts.values())

    # Limpiar eje
    ax.clear()

<<<<<<< HEAD
    # Estilo visual
    ax.set_facecolor("#ffffff")

    # Barras
    ax.bar(labels,values,color='#f4b183',edgecolor='#c55a11',label='Flights per airline')

    # Configuración
    ax.set_xlabel('Airline (ICAO Code)')
    ax.set_ylabel('Number of Flights')
    ax.set_title('Flights per Airline arriving at LEBL')

    ax.tick_params(axis='x', rotation=90, labelsize=8)
    ax.grid(axis='y',linestyle='--',alpha=0.5)
    ax.legend()

def PlotFlightsType(aircrafts, ax):
=======
"""
    Genera una gráfica comparando vuelos Schengen y no Schengen.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra una gráfica de barras apiladas.
    """
def PlotFlightsType(aircrafts):
>>>>>>> ffaaecd455fc3543e55a48b559ac0012e4773e8a
    if not aircrafts:
        print("Error: The aircraft list is empty.")
        return

    schengen_count = 0
    non_schengen_count = 0
    j = 0
    # Recorremos la lista y clasificamos según el origen
    while j < len(aircrafts):
        # Usamos la función IsSchengenAirport que definimos en airport.py
        if IsSchengenAirport(aircrafts[j].origin_airport):
            schengen_count += 1
        else:
            non_schengen_count += 1
        j += 1

    # Configuración de la gráfica de barras apiladas
    labels = ['Flights Type']
    s_data = [schengen_count]
    ns_data = [non_schengen_count]

    # Limpiar eje
    ax.clear()

    # Fondo limpio
    ax.set_facecolor("#ffffff")

    # Barras apiladas
    ax.bar(labels,s_data,label='Schengen',color='#87CEFA')

    ax.bar(labels,ns_data,bottom=s_data,label='No Schengen',color='#FF7F7F')

    # Configuración
    ax.set_ylabel('Count')
    ax.set_title('Schengen vs No-Schengen Arrivals')

    ax.grid(axis='y',linestyle='--',alpha=0.3)
    ax.legend()

"""
    Genera un archivo KML con trayectorias de vuelo.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
        airports_dict (dict): Diccionario con aeropuertos y coordenadas.
        filename (str): Nombre del archivo KML de salida.
    Resultado:
        Crea un archivo KML compatible con Google Earth.
    """
def MapFlights(aircrafts, airports_dict, filename="flights.kml"):
    lebl_lat, lebl_lon = 41.297, 2.083 # Definimos las coordenadas del aeropuerto LEBL
    # Genera un archivo KML para ver las rutas aéreas en Google Earth
    try:
        F = open(filename, "w")
        F.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Trayectorias de Vuelo a LEBL</name>
""")
        j = 0
        while j < len(aircrafts):
            a = aircrafts[j]
            if a.origin_airport in airports_dict: # Verifica si su aeropuerto de origen existe en el diccionario de aeropuertos proporcionado
                apt = airports_dict[a.origin_airport] # Si existe, extrae el objeto del aeropuerto para obtener su latitud y longitud
                # Color KML:(Schengen=Azul, No-Schengen=Rojo)
                color = "ffff0000" if IsSchengenAirport(a.origin_airport) else "ff0000ff"
                F.write(f"""
    <Placemark>
        <name>{a.aircraft_id} desde {a.origin_airport}</name>
        <Style>
            <LineStyle>
                <color>{color}</color>
                <width>2</width>
            </LineStyle>
        </Style>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
                {apt.longitude},{apt.latitude},0
                {lebl_lon},{lebl_lat},0
            </coordinates>
        </LineString>
    </Placemark>
""")
            j += 1
        # Cierre KML
        F.write("</Document>\n</kml>")
        F.close()
        print(f"Mapa generado: {filename}")
    except Exception:
        return "Error: Could not write KML file"

    return None

import math

"""
    Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine.
    Parámetros:
        lat1, lon1: Coordenadas del punto 1 (grados).
        lat2, lon2: Coordenadas del punto 2 (grados).
    Resultado:
        float: Distancia en kilómetros entre ambos puntos.
    """
def CalculateHaversine(lat1, lon1, lat2, lon2):
    # Calcula la distancia de círculo máximo entre dos puntos
    # Basado en el Anexo 2: Haversine Formula
    r = 6371.0  # Radio medio de la Tierra en km

    # Convertir grados a radianes
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    lam1, lam2 = math.radians(lon1), math.radians(lon2)

    # Diferencias de lat y lon
    d_phi = phi1 - phi2
    d_lam = lam1 - lam2

    # Fórmula de Haversine
    a = (math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c

"""
    Filtra vuelos de larga distancia.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
        airports_dict (dict): Diccionario con información de aeropuertos.
    Resultado:
        list: Lista de vuelos cuya distancia a Barcelona supera los 2000 km.
"""
def LongDistanceArrivals(aircrafts, airports_dict):
    # Coordenadas de destino: Barcelona (LEBL)
    lebl_lat, lebl_lon = 41.297, 2.083
    long_distance_list = []
    j = 0
    while j < len(aircrafts):
        a = aircrafts[j]
        # Verificamos si tenemos las coordenadas del aeropuerto de origen
        if a.origin_airport in airports_dict:
            apt = airports_dict[a.origin_airport] # Obtenemos las coordenadas
            dist = CalculateHaversine(apt.latitude, apt.longitude, lebl_lat, lebl_lon)
            if dist > 2000:
                long_distance_list.append(a)
        j += 1
    return long_distance_list

# ---------------- TEST SECTION ---------------- #

"""
   Bloque principal de pruebas.
   Funciones comprobadas:
    1. Carga de vuelos.
    2. Generación de gráficas.
    3. Guardado de archivos.
    4. Clasificación Schengen.
    5. Filtrado de larga distancia.
    6. Generación de mapas KML.
"""

if __name__ == "__main__":

    # 1. Cargamos los datos del archivo
    archivo_entrada = "arrivals.txt"
    lista_vuelos = LoadArrivals(archivo_entrada)
    if not lista_vuelos:
        print(f"Error: No se pudo cargar el archivo {archivo_entrada} o está vacío.")
    else:
        print(f"Se han cargado {len(lista_vuelos)} vuelos con éxito.")

        # =========================================================
        # PRUEBA 1 - GRÁFICO DE LLEGADAS POR HORA
        # =========================================================

        print("Generando gráfico de llegadas por hora...")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        PlotArrivals(lista_vuelos, ax1)
        plt.show()

        # =========================================================
        # PRUEBA 2 - GRÁFICO POR AEROLÍNEA
        # =========================================================

        print("Generando gráfico de vuelos por aerolínea...")
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        PlotAirlines(lista_vuelos, ax2)
        plt.show()

        # =========================================================
        # GUARDADO DE VUELOS
        # =========================================================

        archivo_salida = "arrivals_saved.txt"
        error_save = SaveFlights(lista_vuelos, archivo_salida)
        if error_save:
            print(error_save)
        else:
            print(f"Archivo guardado correctamente como: {archivo_salida}")

        # =========================================================
        # DATOS DE PRUEBA PARA AEROPUERTOS
        # =========================================================

        class MockAirport:
            def __init__(self, lat, lon):
                self.latitude = lat
                self.longitude = lon

        test_airports = {
            "MAD": MockAirport(40.49, -3.56),
            "JFK": MockAirport(40.64, -73.77),
            "LHR": MockAirport(51.47, -0.45)
        }

        # =========================================================
        # FILTRADO DE VUELOS LARGOS
        # =========================================================

        print("Filtrando vuelos de larga distancia (>2000km)...")
        vuelos_largos = LongDistanceArrivals(lista_vuelos,test_airports)
        print(f"Vuelos de larga distancia encontrados: {len(vuelos_largos)}")

        # =========================================================
        # PRUEBA 3 - SCHENGEN VS NO SCHENGEN
        # =========================================================

        print("Generando gráfico Schengen vs No-Schengen...")
        fig3, ax3 = plt.subplots(figsize=(9, 6))
        PlotFlightsType(lista_vuelos, ax3)
        plt.show()

        # =========================================================
        # GENERACIÓN KML
        # =========================================================

        print("Generando archivo KML para Google Earth...")

        MapFlights(lista_vuelos,test_airports,"vuelos_barcelona.kml")

    print("\n--- Pruebas finalizadas ---")
