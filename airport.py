class Airport:
    def __init__(self, icao_code, latitude, longitude):
        self.icao_code = icao_code
        self.latitude = latitude
        self.longitude = longitude
        self.schengen = False

def IsSchengenAirport(code):
# Recibe el código ICAO de un aeropuerto y comprueba si pertenece a Schengen
    if code == "" or len(code) < 2:
        return False

    schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
            'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE',
            'ES', 'LS']
    return code[:2] in schengen_codes

def SetSchengen(airport):
# Establece el atributo schengen de un aeropuerto utilizando su código ICAO
    airport.schengen = IsSchengenAirport(airport.icao_code)

def PrintAirport(airport):
# Escribe en pantalla los datos del aeropuerto
    print("ICAO: ", airport.icao_code)
    print("Latitude: ", airport.latitude)
    print("Longitude: ", airport.longitude)
    print("Schengen: ", airport.schengen)

# Convierte DMS (N635906 o W0734429) a grados decimales (float)
def ConvertCoord(coord):
  if not coord:
      return 0.0

  direction = coord[0]           # N/S/E/W

  if direction in ['N', 'S']:
      deg = int(coord[1:3])      # latitud: 2 dígitos de grados
      min_ = int(coord[3:5])
      sec = int(coord[5:7])
  else:
      deg = int(coord[1:4])      # longitud: 3 dígitos de grados
      min_ = int(coord[4:6])
      sec = int(coord[6:8])

  decimal = deg + min_/60 + sec/3600

  if direction in ['S', 'W']:
      decimal = -decimal

  return decimal

# Convierte grados decimales (float) a DMS con N/S/E/W
def CoordToString(decimal, is_lat):
    if is_lat:
        if decimal >= 0:
            direction = 'N'
        else:
            direction = 'S'
    else:  # longitud
        if decimal >= 0:
            direction = 'E'
        else:
            direction = 'W'
    decimal = abs(decimal)
    deg = int(decimal)
    min_ = int((decimal - deg) * 60)
    sec = int(((decimal - deg) * 60 - min_) * 60)

    if is_lat:
        return "{}{:02d}{:02d}{:02d}".format(direction, deg, min_, sec)
    else:
        return "{}{:03d}{:02d}{:02d}".format(direction, deg, min_, sec)


def LoadAirports(filename):
    airports = []
    try:
        with open(filename, "r") as F: # abre archivo y se cierra automáticamente
            next(F)  # saltar encabezado
            for line in F:
                parts = line.strip().split()
                if len(parts) == 3:
                    code = parts[0]
                    lat_str = parts[1]
                    lon_str = parts[2]
                    latitude = ConvertCoord(lat_str)
                    longitude = ConvertCoord(lon_str)
                    airports.append(Airport(code, latitude, longitude))
    except FileNotFoundError:
        return []
    return airports

def SaveSchengenAirports(airports, filename):
    schengen_airports = []
    i = 0
    while i < len(airports):
        if airports[i].schengen:
            schengen_airports.append(airports[i])
        i += 1

    if len(schengen_airports) == 0:
        return "Error in the code" # código dd error

    F = open(filename, "w")
    F.write("CODE LAT LON\n")
    j = 0
    while j < len(schengen_airports):
        a = schengen_airports[j]
        lat_str = CoordToString(a.latitude, True)
        lon_str = CoordToString(a.longitude, False)
        F.write(a.icao_code)
        F.write(" ")
        F.write(lat_str)
        F.write(" ")
        F.write(lon_str)
        F.write("\n")
        j += 1
    F.close()

def AddAirport(airports, airport):
    found = False
    i = 0
    while i < len(airports):
        if airports[i].icao_code == airport.icao_code:
            found = True
        i += 1
    if not found:
        airports.append(airport)

def RemoveAirport(airports, code):
    i = 0
    while i < len(airports):
        if airports[i].icao_code == code:
            airports.remove(airports[i])
            return
        i += 1
    return "Error in the code" # código de error

import matplotlib.pyplot as plt

def PlotAirports(airports):
# Muestra un gráfico de barras apiladas con aeropuertos Schengen y no Schengen.
    schengen_count = 0
    non_schengen_count = 0
    for a in airports:
        if a.schengen:
            schengen_count += 1
        else:
            non_schengen_count += 1

    # Datos para la gráfica
    labels = ['Airports'] # etiqueta de la barra en el eje X
    # listas con los valores que se van a graficar
    schengen = [schengen_count]
    non_schengen = [non_schengen_count]

    # Crear gráfica de barras apiladas
    plt.bar(labels, schengen, label='Schengen', color='#87CEFA')
    plt.bar(labels, non_schengen, bottom=schengen, label='No Schengen', color='#FF7F7F')

    plt.ylabel('Count') # etiqueta vertical (eje Y)
    plt.title('Schengen vs No Schengen Airports')
    plt.legend() # muestra la leyenda con colores y etiquetas
    plt.show()

def MapAirports(airports, filename = "airports.kml"):
# Genera un archivo KML para ver los aeropuertos en Google Earth.
    F = open(filename, "w")
    # Encabezado KML
    F.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
""")
    for a in airports:
        color = "#ffff0000" if a.schengen else "ff0000ff"  # KML: ABGR (azul/rojo)
        F.write(f"""
    <Placemark>
        <name>{a.icao_code}</name>
        <Style>
            <IconStyle>
                <color>{color}</color>
                <scale>1.1</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Point>
            <coordinates>{a.longitude},{a.latitude},0</coordinates>
        </Point>
    </Placemark>
""")
    # Cierre KML
    F.write("""
</Document>
</kml>
""")
    F.close()
    print(f"Archivo {filename} creado. Ábrelo con Google Earth.")