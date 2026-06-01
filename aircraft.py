from airport import IsSchengenAirport
from LEBL import (AssignGate, SetGates, BoardingArea, Terminal, BarcelonaAP)
import matplotlib.pyplot as plt

class Aircraft:
    def __init__(self, aircraft_id, airline_company, origin_airport, landing_time, destination, departure_time):
        self.aircraft_id = aircraft_id
        self.origin_airport = origin_airport
        self.landing_time = landing_time
        self.airline_company = airline_company
        self.destination = destination
        self.departure_time = departure_time

# -------- FUNCIONES V2 -------- #

def LoadArrivals(filename):
    aircrafts = []
    try:
        with open(filename, "r") as F:
            next(F)
            for line in F:
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                aircraft_id, origin, arrival_time, airline = parts
                if ":" in arrival_time:
                    h_m = arrival_time.split(":")
                    if h_m[0].isdigit() and h_m[1].isdigit():
                        aircrafts.append(
                            Aircraft(
                                aircraft_id,
                                airline,
                                origin,
                                arrival_time,
                                "",
                                ""
                            )
                        )
    except FileNotFoundError:
        return [], -1

    return aircrafts, None

<<<<<<< HEAD
=======
"""
    Genera una gráfica de llegadas por hora.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra un gráfico de barras con el número de aterrizajes por hora.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
def PlotArrivals(aircrafts, ax):
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
=======
"""
    Genera una gráfica de vuelos por aerolínea.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra un gráfico de barras con la cantidad de vuelos por aerolínea.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
def PlotAirlines(aircrafts, ax):
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

<<<<<<< HEAD

=======
"""
    Genera una gráfica comparando vuelos Schengen y no Schengen.
    Parámetros:
        aircrafts (list): Lista de objetos Aircraft.
    Resultado:
        Muestra una gráfica de barras apiladas.
    """
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
def PlotFlightsType(aircrafts, ax):
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

def MapFlights(aircrafts, airports_dict, filename="flights.kml"):
    lebl_lat, lebl_lon = 41.297, 2.083  # Barcelona (LEBL)

    try:
        with open(filename, "w", encoding="utf-8") as F:
            F.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>Trayectorias de Vuelo a LEBL</name>
""")
            j = 0
            while j < len(aircrafts):
                a = aircrafts[j]
                if a.origin_airport in airports_dict:
                    apt = airports_dict[a.origin_airport]
                    # ✔ adaptado a diccionario (NO objeto)
                    lat = apt["latitude"]
                    lon = apt["longitude"]
                    # Color KML: Schengen / No-Schengen
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
                {lon},{lat},0
                {lebl_lon},{lebl_lat},0
            </coordinates>
        </LineString>
    </Placemark>
""")
                j += 1
            F.write("</Document>\n</kml>")
        print(f"Mapa generado: {filename}")
        return None
    except Exception:
        return "Error: Could not write KML file"

import math

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

# -------- FUNCIONES V4 -------- #

def LoadDepartures(filename):
    aircrafts = []
    try:
        with open(filename, "r") as F:
            next(F)
            for line in F:
                parts = line.strip().split()
                if len(parts) != 4:
                    continue
                aircraft_id, destination, departure_time, airline = parts
                if ":" in departure_time:
                    h_m = departure_time.split(":")
                    if h_m[0].isdigit() and h_m[1].isdigit():
                        aircrafts.append(
                            Aircraft(
                                aircraft_id,
                                airline,
                                "",
                                "",
                                destination,
                                departure_time
                            )
                        )
    except FileNotFoundError:
        return [], -1

    return aircrafts, None

def TimeToMinutes(time_str): # Función auxiliar para comprovar que el formato de las horas este bien
    if not time_str:
        return -1

    h, m = time_str.split(":")
    return int(h) * 60 + int(m)

def MergeMovements(arrivals, departures):
    if arrivals is None or departures is None:
        return [], -1

    aircraft_dict = {}
    for ac in arrivals:
        aircraft_dict[ac.aircraft_id] = ac
    for dep in departures:
        if dep.aircraft_id in aircraft_dict:
            arr = aircraft_dict[dep.aircraft_id]
            arr.destination = dep.destination
            arr.departure_time = dep.departure_time
        else:
            aircraft_dict[dep.aircraft_id] = dep

    return list(aircraft_dict.values()), None

def NightAircraft(aircrafts):
    if not aircrafts:
        return [], -1

    night_list = []
    for ac in aircrafts:
        # Avión nocturno: no tiene llegada pero sí salida
        if ac.landing_time == "" and ac.departure_time != "":
            night_list.append(ac)

    return night_list, None

def FreeGate(bcn, aircraft_id):
    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                if gate.aircraft_id == aircraft_id:
                    gate.occupied = False
                    gate.aircraft_id = ""
                    return None
    return -1

def AssignNightGates(bcn, aircrafts):
    if not aircrafts:
        return -1

    for aircraft in aircrafts:
        if (aircraft.landing_time == "" and aircraft.departure_time != ""):
            AssignGate(bcn, aircraft)

    return None

def TimeToMinutes(time_str): # Función auxiliar
    if not time_str:
        return -1

    h, m = time_str.split(":")
    return int(h) * 60 + int(m)

def AssignGatesAtTime(bcn, aircrafts, time):
    if not aircrafts:
        return -1

    hour = int(time.split(":")[0])
    not_assigned = 0
    for ac in aircrafts:
        if ac.departure_time:
            if int(ac.departure_time.split(":")[0]) == hour:
                FreeGate(bcn, ac.aircraft_id)
    for ac in aircrafts:
        if ac.landing_time:
            if int(ac.landing_time.split(":")[0]) == hour:
                if AssignGate(bcn, ac) == -1:
                    not_assigned += 1

    return not_assigned

def PlotDayOccupancy(bcn, aircrafts):
    if not aircrafts:
        return -1

    # ----------------------------------
    # Reiniciar estado del aeropuerto
    # ----------------------------------

    for terminal in bcn.terminals:
        for area in terminal.boarding_areas:
            for gate in area.gates:
                gate.occupied = False
                gate.aircraft_id = ""

    # ----------------------------------
    # Asignar night aircraft
    # ----------------------------------

    night_aircraft, error = NightAircraft(aircrafts)
    if error != -1:
        AssignNightGates(bcn,night_aircraft)

    # ----------------------------------
    # Preparar estructuras de datos
    # ----------------------------------

    terminal_data = {}
    for terminal in bcn.terminals:
        terminal_data[terminal.name] = []
    hours = []
    unassigned = []

    # ----------------------------------
    # Simulación hora a hora
    # ----------------------------------

    for hour in range(24):
        current_time = f"{hour:02d}:00"
        failed = AssignGatesAtTime(bcn,aircrafts,current_time)
        hours.append(hour)
        unassigned.append(failed)

        # Contar puertas ocupadas
        for terminal in bcn.terminals:
            occupied = 0
            for area in terminal.boarding_areas:
                for gate in area.gates:
                    if gate.occupied:
                        occupied += 1
            terminal_data[terminal.name].append(occupied)

    # ----------------------------------
    # Crear gráfica
    # ----------------------------------

    plt.figure(figsize=(12, 6))
    for terminal_name in terminal_data:
        plt.plot(
            hours,
            terminal_data[terminal_name],
            marker="o",
            linewidth=2,
            label=f"Terminal {terminal_name}"
        )
    plt.plot(
        hours,
        unassigned,
        color="red",
        marker="s",
        linewidth=3,
        label="Aircraft not assigned"
    )
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Aircraft")
    plt.title("LEBL Gate Occupancy Throughout the Day")
    plt.xticks(range(24))
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return None

# ---------------- CREACIÓN DE AEROPUERTO (bcn) ---------------- #

# =========================================================
# CREAR AEROPUERTO BCN (LEBL)
# =========================================================

bcn = BarcelonaAP("LEBL")

# =========================================================
# TERMINAL 1
# =========================================================

t1 = Terminal("T1")
# Aerolíneas (ejemplo típico V3/V4)
t1.airlines = ["VLG", "IBE", "RYR", "EZY"]
# Boarding Areas
t1_schengen = BoardingArea("T1-S", "Schengen")
t1_non_schengen = BoardingArea("T1-NS", "non-Schengen")
# Puertas Schengen
SetGates(t1_schengen, 1, 10, "T1S")
# Puertas No-Schengen
SetGates(t1_non_schengen, 1, 5, "T1NS")
t1.boarding_areas.append(t1_schengen)
t1.boarding_areas.append(t1_non_schengen)
bcn.terminals.append(t1)

# =========================================================
# TERMINAL 2
# =========================================================

t2 = Terminal("T2")
t2.airlines = ["AEE", "DLH", "AFR", "BAW"]
# Boarding Areas
t2_schengen = BoardingArea("T2-S", "Schengen")
t2_non_schengen = BoardingArea("T2-NS", "non-Schengen")
# Puertas Schengen
SetGates(t2_schengen, 11, 18, "T2S")
# Puertas No-Schengen
SetGates(t2_non_schengen, 6, 10, "T2NS")
t2.boarding_areas.append(t2_schengen)
t2.boarding_areas.append(t2_non_schengen)
bcn.terminals.append(t2)

# ---------------- TEST SECTION ---------------- #

if __name__ == "__main__":

    print("=== CARGA DE DATOS ===")

    # =========================================================
    # 1. CARGA DE ARRIVALS Y DEPARTURES
    # =========================================================

    arrivals, err1 = LoadArrivals("arrivals.txt")
    departures, err2 = LoadDepartures("departures.txt")
    if err1 == -1 or err2 == -1:
        print("Error cargando archivos")
        exit()
    else:
        print(f"Arrivals: {len(arrivals)} | Departures: {len(departures)}")

    # =========================================================
    # 2. GRÁFICOS V2
    # =========================================================

    print("\n=== GRÁFICOS V2 ===")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    PlotArrivals(arrivals, ax1)
    plt.show()
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    PlotAirlines(arrivals, ax2)
    plt.show()
    fig3, ax3 = plt.subplots(figsize=(9, 6))
    PlotFlightsType(arrivals, ax3)
    plt.show()
    airports_dict = {
        "MAD": {"latitude": 40.49, "longitude": -3.56},
        "LHR": {"latitude": 51.47, "longitude": -0.45},
        "JFK": {"latitude": 40.64, "longitude": -73.77},
        "CDG": {"latitude": 49.01, "longitude": 2.55},
        "FRA": {"latitude": 50.03, "longitude": 8.56},
        "AMS": {"latitude": 52.31, "longitude": 4.76},
        "BCN": {"latitude": 41.297, "longitude": 2.083},  # Barcelona
        "FCO": {"latitude": 41.80, "longitude": 12.25},
        "IST": {"latitude": 41.27, "longitude": 28.73},
        "DXB": {"latitude": 25.25, "longitude": 55.36}
    }
    MapFlights(arrivals, airports_dict)

    # =========================================================
    # 3. MERGE MOVIMIENTOS (V4 CORE)
    # =========================================================

    print("\n=== MERGE MOVEMENTS ===")
    movements, err3 = MergeMovements(arrivals, departures)
    if err3 == -1:
        print("Error en MergeMovements")
        exit()
    print(f"Movimientos totales: {len(movements)}")

    # =========================================================
    # 4. CREAR AEROPUERTO BCN
    # =========================================================

    print("\n=== CONFIGURANDO AEROPUERTO BCN ===")

    # =========================================================
    # 5. NIGHT AIRCRAFT
    # =========================================================

    night, err4 = NightAircraft(movements)
    if err4 == -1:
        print("Error NightAircraft")
        exit()
    for ac in night:
        AssignGate(bcn, ac)

    # =========================================================
    # 6. SIMULACIÓN HORARIA V4
    # =========================================================

    print("\n=== SIMULACIÓN V4 ===")
    for h in range(24):
        time = f"{h:02d}:00"
        not_assigned = AssignGatesAtTime(bcn, movements, time)
        print(f"{time} → No asignados: {not_assigned}")

    # =========================================================
    # 7. GRÁFICO FINAL V4
    # =========================================================

    print("Cargando gráfico de PlotDayOccupancy")
    PlotDayOccupancy(bcn, movements)

    # =========================================================
    # 8. FIN
    # =========================================================

<<<<<<< HEAD
    print("\n=== SIMULACIÓN FINALIZADA ===")
=======
        # =========================================================
        # GENERACIÓN KML
        # =========================================================

        print("Generando archivo KML para Google Earth...")
        MapFlights(lista_vuelos,test_airports,"vuelos_barcelona.kml")

    print("\n--- Pruebas finalizadas ---")
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
