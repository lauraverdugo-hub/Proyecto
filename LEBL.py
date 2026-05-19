import matplotlib.pyplot as plt

class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = ""

class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.type = area_type  # "Schengen" o "non-Schengen"
        self.gates = []

class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []  # Lista de códigos ICAO

class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []

class Aircraft:
    def __init__(self, aircraft_id, airline_company, origin_airport, scheduled_time, is_schengen=True):
        self.aircraft_id = aircraft_id
        self.airline_company = airline_company
        self.origin_airport = origin_airport
        self.scheduled_time = scheduled_time
        self.is_schengen = is_schengen

def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []  # Limpiamos lista previa
    i = init_gate
    while i <= end_gate:
        gate_name = f"{prefix}{i}"
        new_gate = Gate(gate_name)
        area.gates.append(new_gate)
        i += 1
    return None

def LoadAirlines(terminal, t_name):
    filename = f"{t_name}_Airlines.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            terminal.airlines = []  # Reset list
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    icao_code = parts[1].strip().upper()
                    terminal.airlines.append(icao_code)
    except FileNotFoundError:
        return -1
    return None

def LoadAirportStructure(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return None

            header = lines[0].strip().split()
            bcn = BarcelonaAP(header[0])
            num_terminals = int(header[1])

            current_line = 1
            t_idx = 0
            while t_idx < num_terminals:
                t_info = lines[current_line].strip().split()
                t_name = t_info[1]
                num_areas = int(t_info[2])

                new_terminal = Terminal(t_name)
                LoadAirlines(new_terminal, t_name)

                current_line += 1
                a_idx = 0
                while a_idx < num_areas:
                    a_info = lines[current_line].strip().split()

                    # Formato: Area X Schengen Gates 1 - 11
                    area_name = a_info[0] + " " + a_info[1]
                    area_type = a_info[2]
                    init_g = int(a_info[4])
                    end_g = int(a_info[6])

                    b_area = BoardingArea(area_name, area_type)
                    prefix = f"{t_name}{a_info[1]}G"
                    SetGates(b_area, init_g, end_g, prefix)

                    new_terminal.boarding_areas.append(b_area)
                    current_line += 1
                    a_idx += 1

                bcn.terminals.append(new_terminal)
                t_idx += 1
            return bcn
    except (FileNotFoundError, IndexError, ValueError):
        return None

def GateOccupancy(bcn):
    occupancy_list = []
    for term in bcn.terminals:
        for area in term.boarding_areas:
            for gate in area.gates:
                status = "Occupied" if gate.occupied else "Free"
                occupancy_list.append([gate.name, status, gate.aircraft_id])
    return occupancy_list

def IsAirlineInTerminal(terminal, name):
    if name == "" or name is None:
        return False, -1  # Retorna booleano y código de error según enunciado
    if not terminal.airlines:
        return False, 0
    if name in terminal.airlines:
        return True, 0
    return False, 0

def SearchTerminal(bcn, airline_name):
    for term in bcn.terminals:
        found, code = IsAirlineInTerminal(term, airline_name)
        if found:
            return term.name
    return ""

def AssignGate(bcn, aircraft):
    t_name = SearchTerminal(bcn, aircraft.airline_company)
    if not t_name:
        return -1

    # Determinar tipo de vuelo según el atributo o el origen
    if hasattr(aircraft, 'is_schengen'):
        flight_type = "Schengen" if aircraft.is_schengen else "non-Schengen"
    else:
        try:
            from airport import IsSchengenAirport
            flight_type = "Schengen" if IsSchengenAirport(aircraft.origin_airport) else "non-Schengen"
        except ImportError:
            flight_type = "Schengen"

    for term in bcn.terminals:
        if term.name == t_name:
            for area in term.boarding_areas:
                if area.type == flight_type:
                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.aircraft_id = aircraft.aircraft_id
                            return None  # Éxito
    return -1  # No hay puertas disponibles

# --- GRÁFICO APILADO REQUERIDO PARA LA INTERFAZ ---

def PlotOccupancyChart(bcn, target_frame=None, airline_filter=None):
    areas_names = []
    occupied_counts = []
    free_counts = []

    for t in bcn.terminals:
        for a in t.boarding_areas:
            areas_names.append(f"{t.name}\n{a.name[-1]}")

            if airline_filter:
                # Si hay filtro, contamos como "ocupado" solo si coincide con la aerolínea buscada
                occ = sum(1 for g in a.gates if g.occupied and g.aircraft_id.startswith(airline_filter.upper()))
                # El resto de puertas de esa área se muestran como "disponibles" para esa aerolínea
                free = len(a.gates) - occ
            else:
                # Lógica normal sin filtro
                occ = sum(1 for g in a.gates if g.occupied)
                free = sum(1 for g in a.gates if not g.occupied)

            occupied_counts.append(occ)
            free_counts.append(free)

    fig, ax = plt.subplots(figsize=(6, 3.2))

    title_text = f'Ocupación de Puertas en {bcn.code}'
    if airline_filter:
        title_text += f" (Filtrado por: {airline_filter.upper()})"
        ax.bar(areas_names, free_counts, label='Otras / Libres', color='#bdc3c7')
        ax.bar(areas_names, occupied_counts, bottom=free_counts, label=f'Ocupadas por {airline_filter.upper()}',
               color='#e74c3c')
    else:
        ax.bar(areas_names, free_counts, label='Libres', color='#2ecc71')
        ax.bar(areas_names, occupied_counts, bottom=free_counts, label='Ocupadas', color='#e74c3c')

    ax.set_ylabel('Número de Puertas')
    ax.set_title(title_text, fontsize=10, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    plt.tight_layout()

    if target_frame is None:
        plt.show()
    return fig

def ExportFlightsToKMLWithTerminal(aircrafts, bcn, airports_list, filename="vuelos_terminales.kml"):
    # Mapeo rápido de coordenadas de aeropuertos para calcular las rutas
    apt_coords = {a.icao_code: (a.latitude, a.longitude) for a in airports_list}

    lebl_lat, lebl_lon = 41.2974, 2.0833

    kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
 <Document>
   <name>Vuelos por Terminales - LEBL V3</name>
   <Style id="style_T1">
     <LineStyle><color>ff990000</color><width>3</width></LineStyle>
     <IconStyle><color>ff990000</color></IconStyle>
   </Style>
   <Style id="style_T2">
     <LineStyle><color>ff009900</color><width>3</width></LineStyle>
     <IconStyle><color>ff009900</color></IconStyle>
   </Style>
   <Style id="style_default">
     <LineStyle><color>ff888888</color><width>2</width></LineStyle>
   </Style>
"""

    for ac in aircrafts:
        # Determinamos la terminal usando la lógica de la V3
        t_name = SearchTerminal(bcn, ac.airline_company)
        style = "#style_default"
        if t_name == "T1":
            style = "#style_T1"
        elif t_name == "T2":
            style = "#style_T2"

        orig = ac.origin_airport
        if orig in apt_coords:
            orig_lat, orig_lon = apt_coords[orig]

            kml_content += f"""    <Placemark>
     <name>{ac.aircraft_id} ({ac.airline_company}) -> Terminal: {t_name if t_name else 'Desconocida'}</name>
     <styleUrl>{style}</styleUrl>
     <LineString>
       <altitudeMode>relativeToGround</altitudeMode>
       <coordinates>
         {orig_lon},{orig_lat},5000
         {lebl_lon},{lebl_lat},0
       </coordinates>
     </LineString>
   </Placemark>
"""

    kml_content += """  </Document>
</kml>"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(kml_content)
    return filename

# ------------------- TEST SECTION ---------------- #

if __name__ == "__main__":
    print("--- INICIANDO TEST DE SISTEMA LEBL ---")

    # 1. Probar carga de estructura
    # Cambia "Terminals.txt" por "LEBL.txt" si ese es el nombre de tu archivo
    mi_aeropuerto = LoadAirportStructure("Terminals.txt")

    if mi_aeropuerto is None:
        print("Error Crítico: No se pudo cargar la estructura. Revisa el archivo Terminals.txt")
    else:
        print(f"Aeropuerto {mi_aeropuerto.code} cargado con {len(mi_aeropuerto.terminals)} terminales.")

        # 2. Probar IsAirlineInTerminal y SearchTerminal
        # Asumimos que "AEE" está en el archivo T1_Airlines.txt
        airline_test = "AEE"
        terminal_asignada = SearchTerminal(mi_aeropuerto, airline_test)

        if terminal_asignada:
            print(f"Aerolínea {airline_test} encontrada en: {terminal_asignada}")
        else:
            print(f"Aerolínea {airline_test} no encontrada en ninguna terminal.")

        # 3. Probar asignación de puerta
        # Creamos el avión con el atributo is_schengen incluido
        test_plane = Aircraft("DALEN", "AEE", "ATH", "18:45", is_schengen=True)

        # Llamamos a la función con 2 argumentos (bcn, aircraft)
        resultado = AssignGate(mi_aeropuerto, test_plane)

        if resultado is None:  # Según tu código, devuelve None si tiene éxito
            print(f"Avión {test_plane.aircraft_id} asignado con éxito.")
        else:
            print("Error: No se pudo asignar puerta (lleno o aerolínea no válida).")

        # 4. Probar GateOccupancy (La función que devuelve la lista de listas)
        print("\n--- REPORTE DE OCUPACIÓN (GateOccupancy) ---")
        lista_ocupacion = GateOccupancy(mi_aeropuerto)

        puertas_ocupadas = 0
        for gate_info in lista_ocupacion:
            # gate_info es [nombre, estado, id_avion]
            if gate_info[1] == "Occupied":
                print(f"Puerta: {gate_info[0]} | Estado: {gate_info[1]} | Avión: {gate_info[2]}")
                puertas_ocupadas += 1

        if puertas_ocupadas == 0:
            print("No hay puertas ocupadas actualmente.")

        # 5. Extra: Verificar que una aerolínea vacía da error (según enunciado)
        print("\n--- PRUEBA DE SEGURIDAD ---")
        resultado_vacio, codigo_error = IsAirlineInTerminal(mi_aeropuerto.terminals[0], "")
        if codigo_error == -1:
            print("Verificación de nombre vacío: Correcta (detectó error -1)")

        # 6. Extra: Probar visualización del plot con las terminales y el Google Earth
        print("Generando gráfico con las terminales del aeropuerto...")
        PlotOccupancyChart(mi_aeropuerto)