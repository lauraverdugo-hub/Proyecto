# =====================================================================
# AIRPORT OPERATIONS SUITE — MÓDULO AIRCRAFT (V4 EVOLUCIONADO)
# =====================================================================
from airport import IsSchengenAirport
from LEBL import AssignGate, Terminal,SetGates, BoardingArea, BarcelonaAP
import matplotlib.pyplot as plt








class Aircraft:
  def __init__(self, aircraft_id, airline_company, origin_airport, landing_time, destination, departure_time):
      self.aircraft_id = aircraft_id
      self.airline_company = airline_company
      self.origin_airport = origin_airport
      self.landing_time = landing_time
      self.destination = destination
      self.departure_time = departure_time








# =====================================================================
# -------- FUNCIONES AUXILIARES DE TIEMPO -------- #
# =====================================================================




def TimeToMinutes(time_str):
  """ Convierte formato hh:mm a minutos totales desde el inicio del día. """
  if not time_str or ":" not in time_str:
      return -1
  try:
      h, m = time_str.split(":")
      return int(h) * 60 + int(m)
  except ValueError:
      return -1








# =====================================================================
# -------- FUNCIONES V2 (MANTENIDAS PARA COMPATIBILIDAD) -------- #
# =====================================================================




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
                          Aircraft(aircraft_id, airline, origin, arrival_time, "", "")
                      )
  except FileNotFoundError:
      return [], -1
  return aircrafts, None








def PlotArrivals(aircrafts, ax):
  if not aircrafts:
      print("Error: The aircraft list is empty.")
      return
  hours_count = [0] * 24
  for ac in aircrafts:
      time_str = ac.landing_time
      try:
          hour = int(time_str.split(':')[0])
          if 0 <= hour < 24:
              hours_count[hour] += 1
      except (ValueError, IndexError):
          pass
  hours_labels = [f"{h}h" for h in range(24)]
  ax.clear()
  ax.set_facecolor("#ffffff")
  ax.bar(hours_labels, hours_count, color='#9dc3e6', edgecolor='#2f5597', label='Flights per hour')
  ax.set_xlabel('Hour of the Day')
  ax.set_ylabel('Number of Landings')
  ax.set_title('Landing Frequency at Barcelona El Prat (LEBL)')
  ax.grid(axis='y', linestyle='--', alpha=0.5)
  ax.legend()








def SaveFlights(aircrafts, filename):
  if not aircrafts:
      return "Error: Empty list"
  try:
      with open(filename, "w") as F:
          F.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
          for a in aircrafts:
              id_val = a.aircraft_id if a.aircraft_id else "-"
              orig_val = a.origin_airport if a.origin_airport else "-"
              time_val = a.landing_time if a.landing_time else "0"
              airl_val = a.airline_company if a.airline_company else "-"
              F.write(f"{id_val} {orig_val} {time_val} {airl_val}\n")
  except Exception:
      return "Error during file writing"
  return None








def PlotAirlines(aircrafts, ax):
  if not aircrafts:
      print("Error: The aircraft list is empty.")
      return
  airline_counts = {}
  for ac in aircrafts:
      code = ac.airline_company
      airline_counts[code] = airline_counts.get(code, 0) + 1
  labels = list(airline_counts.keys())
  values = list(airline_counts.values())
  ax.clear()
  ax.set_facecolor("#ffffff")
  ax.bar(labels, values, color='#f4b183', edgecolor='#c55a11', label='Flights per airline')
  ax.set_xlabel('Airline (ICAO Code)')
  ax.set_ylabel('Number of Flights')
  ax.set_title('Flights per Airline arriving at LEBL')
  ax.tick_params(axis='x', rotation=90, labelsize=8)
  ax.grid(axis='y', linestyle='--', alpha=0.5)
  ax.legend()








def PlotFlightsType(aircrafts, ax):
  if not aircrafts:
      print("Error: The aircraft list is empty.")
      return
  schengen_count = sum(1 for ac in aircrafts if IsSchengenAirport(ac.origin_airport))
  non_schengen_count = len(aircrafts) - schengen_count
  labels = ['Flights Type']
  ax.clear()
  ax.set_facecolor("#ffffff")
  ax.bar(labels, [schengen_count], label='Schengen', color='#87CEFA')
  ax.bar(labels, [non_schengen_count], bottom=[schengen_count], label='No Schengen', color='#FF7F7F')
  ax.set_ylabel('Count')
  ax.set_title('Schengen vs No-Schengen Arrivals')
  ax.grid(axis='y', linestyle='--', alpha=0.3)
  ax.legend()








def MapFlights(aircrafts, airports_dict, filename="flights.kml"):
  lebl_lat, lebl_lon = 41.297, 2.083
  try:
      with open(filename, "w", encoding="utf-8") as F:
          F.write(
              '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n\t<name>Trayectorias de Vuelo a LEBL</name>\n')
          for a in aircrafts:
              if a.origin_airport in airports_dict:
                  apt = airports_dict[a.origin_airport]
                  lat = apt.get("latitude", 0) if isinstance(apt, dict) else getattr(apt, 'latitude', 0)
                  lon = apt.get("longitude", 0) if isinstance(apt, dict) else getattr(apt, 'longitude', 0)
                  color = "ffff0000" if IsSchengenAirport(a.origin_airport) else "ff0000ff"
                  F.write(f"""\t<Placemark>
\t\t<name>{a.aircraft_id} desde {a.origin_airport}</name>
\t\t<Style><LineStyle><color>{color}</color><width>2</width></LineStyle></Style>
\t\t<LineString><tessellate>1</tessellate><coordinates>{lon},{lat},0 {lebl_lon},{lebl_lat},0</coordinates></LineString>
\t</Placemark>\n""")
          F.write("</Document>\n</kml>")
      print(f"Mapa generado: {filename}")
      return None
  except Exception:
      return "Error: Could not write KML file"








# =====================================================================
# -------- FUNCIONES OPERATIVAS V4 (CORREGIDAS Y ROBUSTAS) -------- #
# =====================================================================




def LoadDepartures(filename):
  """ Carga los datos de despegue y gestiona errores de lectura de fichero. """
  aircrafts = []
  try:
      with open(filename, "r") as F:
          next(F)  # Saltar encabezado
          for line in F:
              parts = line.strip().split()
              if len(parts) != 4:
                  continue
              aircraft_id, destination, departure_time, airline = parts
              if ":" in departure_time:
                  h_m = departure_time.split(":")
                  if h_m[0].isdigit() and h_m[1].isdigit():
                      aircrafts.append(
                          Aircraft(aircraft_id, airline, "", "", destination, departure_time)
                      )
  except FileNotFoundError:
      return [], -1
  return aircrafts, None








def MergeMovements(arrivals, departures):
  """ Combina arribos y partidas validando compatibilidad horaria y aviones repetidos. """
  if not arrivals or not departures:
      return [], -1




  aircraft_dict = {}




  # Procesar arribos
  for ac in arrivals:
      aircraft_dict[ac.aircraft_id] = ac




  # Fusionar partidas con lógica robusta de tiempos compatibles
  for dep in departures:
      if dep.aircraft_id in aircraft_dict:
          arr = aircraft_dict[dep.aircraft_id]
          # Si el tiempo de aterrizaje es previo al despegue, se fusiona
          if TimeToMinutes(arr.landing_time) < TimeToMinutes(dep.departure_time):
              arr.destination = dep.destination
              arr.departure_time = dep.departure_time
          else:
              # Es el mismo avión pero en otra rotación diaria posterior
              # Para evitar colisión de ID en el diccionario, mutamos la clave del avión nocturno/siguiente
              new_key = f"{dep.aircraft_id}_DEP"
              aircraft_dict[new_key] = dep
      else:
          aircraft_dict[dep.aircraft_id] = dep




  return list(aircraft_dict.values()), None








def NightAircraft(aircrafts):
  """ Detecta aviones que pasaron la noche en el aeropuerto (solo tienen despegue). """
  if not aircrafts:
      return [], -1
  night_list = [ac for ac in aircrafts if ac.landing_time == "" and ac.departure_time != ""]
  return night_list, None








def FreeGate(bcn, aircraft_id):
  """ Libera la puerta asignada a una matrícula específica. """
  for terminal in bcn.terminals:
      for area in terminal.boarding_areas:
          for gate in area.gates:
              if gate.aircraft_id == aircraft_id:
                  gate.occupied = False
                  gate.aircraft_id = ""
                  return None
  return -1








def AssignNightGates(bcn, aircrafts):
  """ Asigna pasarela a los aviones estacionados desde la noche anterior. """
  if not aircrafts:
      return -1
  for ac in aircrafts:
      if ac.landing_time == "" and ac.departure_time != "":
          AssignGate(bcn, ac)
  return None








def AssignGatesAtTime(bcn, aircrafts, time):
  """
  Asigna y libera puertas dentro de un rango de una hora.
  Cumple con la orden estricta: PRIMERO liberar, SEGUNDO asignar.
  """
  if not aircrafts:
      return -1




  hour = int(time.split(":")[0])
  not_assigned = 0




  # 1. Liberar puertas de aviones que despegan exactamente en este bloque horario
  for ac in aircrafts:
      if ac.departure_time:
          # Control robusto para claves mutadas (_DEP)
          clean_id = ac.aircraft_id.split("_")[0]
          if int(ac.departure_time.split(":")[0]) == hour:
              FreeGate(bcn, clean_id)




  # 2. Asignar puertas a aviones que aterrizan en este bloque horario
  for ac in aircrafts:
      if ac.landing_time:
          if int(ac.landing_time.split(":")[0]) == hour:
              # Si la asignación devuelve -1 (puertas llenas), sumamos al overbooking
              if AssignGate(bcn, ac) == -1:
                  not_assigned += 1




  return not_assigned








def PlotDayOccupancy(bcn, aircrafts):
  """ Simula la jornada de 24h y grafica la ocupación y aviones denegados. """
  if not aircrafts:
      return -1




  # Reiniciar estado operativo completo de LEBL
  for terminal in bcn.terminals:
      for area in terminal.boarding_areas:
          for gate in area.gates:
              gate.occupied = False
              gate.aircraft_id = ""




  # Ubicar aviones nocturnos en sus compuertas iniciales
  night_aircraft, error = NightAircraft(aircrafts)
  if error is None and night_aircraft:
      AssignNightGates(bcn, night_aircraft)




  # Estructuras de rastreo horario
  terminal_data = {t.name: [] for t in bcn.terminals}
  hours = list(range(24))
  unassigned = []




  # Ejecutar simulación cronológica horaria
  for hour in hours:
      current_time = f"{hour:02d}:00"
      failed = AssignGatesAtTime(bcn, aircrafts, current_time)
      unassigned.append(failed)




      # Contabilizar ocupación resultante por terminal
      for terminal in bcn.terminals:
          occupied = sum(1 for area in terminal.boarding_areas for gate in area.gates if gate.occupied)
          terminal_data[terminal.name].append(occupied)




  # Renderizado gráfico unificado
  plt.figure(figsize=(10, 5))
  for t_name, tracking_list in terminal_data.items():
      plt.plot(hours, tracking_list, marker="o", linewidth=2, label=f"Terminal {t_name}")




  plt.plot(hours, unassigned, color="red", marker="s", linewidth=2.5, linestyle="--", label="Aircraft Unassigned")




  plt.xlabel("Hour of Day")
  plt.ylabel("Number of Aircraft / Gates")
  plt.title("LEBL Dynamic Gate Occupancy Throughout the Day (V4)")
  plt.xticks(hours)
  plt.grid(True, linestyle="--", alpha=0.5)
  plt.legend()
  plt.tight_layout()
  plt.show()




  return None


# ---------------- CREACIÓN DE AEROPUERTO (bcn) ---------------- #

# Se crea la estructura principal del aeropuerto que será utilizada para la simulación de asignación de puertas.
# El aeropuerto contiene terminales, áreas de embarque y puertas de embarque para vuelos Schengen y No Schengen.

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

# Se crea la Terminal 2 con sus aerolíneas asociadas.
# Se definen áreas de embarque para vuelos Schengen y No Schengen y se generan las puertas disponibles para cada tipo de operación.

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

"""
    Programa principal de simulación aeroportuaria.
    Funcionalidades:
        1. Cargar vuelos de llegada y salida.
        2. Generar estadísticas y gráficos.
        3. Combinar movimientos de aeronaves.
        4. Configurar el aeropuerto de Barcelona (LEBL).
        5. Asignar puertas a aeronaves nocturnas.
        6. Simular la ocupación horaria de puertas.
        7. Mostrar gráficos de ocupación.
        8. Generar archivos KML para Google Earth.
    Resultado:
        Ejecuta una simulación completa de gestión de aeronaves y puertas de embarque en LEBL.
"""
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
    # 8. GENERACIÓN KML
    # =========================================================

    print("Generando archivo KML para Google Earth...")
    MapFlights(airports_dict, "vuelos_barcelona.kml")

    print("\n=== SIMULACIÓN FINALIZADA ===")
