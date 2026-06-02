"""
   Clase que representa un aeropuerto.
   Atributos:
       icao_code : str
            Código ICAO del aeropuerto (ejemplo: 'LEBL').
       latitude : float
            Latitud del aeropuerto en grados decimales.
       longitude : float
            Longitud del aeropuerto en grados decimales.
       schengen : bool
            Indica si el aeropuerto pertenece a un país Schengen.
"""
class Airport:
   def __init__(self, icao_code, latitude, longitude):
       self.icao_code = icao_code
       self.latitude = latitude
       self.longitude = longitude
       self.schengen = False


"""
   Comprueba si un código ICAO pertenece a un país del espacio Schengen.
   Parámetros:
       code (str): Código ICAO del aeropuerto (ej. 'LEMD').
   Resultado:
       bool: True si el prefijo está en la lista Schengen, False en caso contrario.
"""
def IsSchengenAirport(code):
# Recibe el código ICAO de un aeropuerto y comprueba si pertenece a Schengen
   if code == "" or len(code) < 2:
       return False


   schengen_codes = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
           'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE',
           'ES', 'LS']
   return code[:2] in schengen_codes


"""
   Actualiza el atributo schengen de un aeropuerto.
   Parámetros:
       airport : Airport. Objeto aeropuerto.
   Resultado:
       Modifica el atributo schengen del aeropuerto según su código ICAO.
"""
def SetSchengen(airport):
# Establece el atributo schengen de un aeropuerto utilizando su código ICAO
   airport.schengen = IsSchengenAirport(airport.icao_code)


"""
   Imprime por consola los detalles de cada aeropuerto.
   Parámetros:
       airport : Airport. Objeto aeropuerto a mostrar.
   Resultado:
       Imprime el código ICAO, latitud, longitud y estado Schengen.
"""
def PrintAirport(airport):
# Escribe en pantalla los datos del aeropuerto
   print("ICAO: ", airport.icao_code)
   print("Latitude: ", airport.latitude)
   print("Longitude: ", airport.longitude)
   print("Schengen: ", airport.schengen)


"""
   Convierte coordenadas en formato DMS a grados decimales.
   Parámetros:
       coord (str): Coordenada en formato 'N635906' o 'W0734429'.
   Resultado:
       float: Valor decimal (positivo para N/E, negativo para S/W).
"""
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


"""
   Convierte coordenadas decimales a formato DMS.
   Parámetros:
       decimal (float): Coordenada en grados decimales.
       is_lat (bool): True si es latitud, False si es longitud.
   Resultado:
       str: Coordenada en formato DMS con N/S/E/W.
"""
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


"""
   Crea una lista de objetos Airport a partir de un archivo de texto.
   Parámetros:
       filename (str): Ruta del archivo (formato: ICAO LAT LON).
   Resultado:
       list: Lista de objetos Airport. Si hay error, devuelve la lista vacía.
"""
def LoadAirports(filename):
   airports = []
   try:
       with open(filename, "r") as F:
           next(F)  # saltar encabezado: CODE LAT LON
           for line in F:
               parts = line.strip().split()
               # El archivo tiene 3 columnas: ICAO, LAT, LON
               if len(parts) == 3:
                   code = parts[0]
                   lat_str = parts[1]
                   lon_str = parts[2]


                   try:
                       latitude = ConvertCoord(lat_str)
                       longitude = ConvertCoord(lon_str)


                       nuevo_ap = Airport(code, latitude, longitude)
                       airports.append(nuevo_ap)
                   except Exception as e:
                       print(f"Error procesando línea {code}: {e}")
               else:
                   # Esto te avisará en consola si una línea no tiene 3 columnas
                   print(f"Línea ignorada (formato incorrecto): {line.strip()}")
   except FileNotFoundError:
       print("Error: Archivo no encontrado")
       return []
   except Exception as e:
       print(f"Error general: {e}")
       return []


   return airports


"""
   Guarda solo los aeropuertos que pertenecen a la zona Schengen en un archivo de texto.
   Parámetros:
       airports (list): Lista de objetos Airport.
       filename (str): Nombre del archivo de salida.
   Resultado:
       Genera un archivo de texto con los aeropuertos Schengen. Devuelve un mensaje de error si no existen aeropuertos Schengen.
"""
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


"""
   Añade un nuevo aeropuerto a la lista si su código ICAO no existe ya.
   Parámetros:
       airports (list): Lista actual de aeropuertos.
       airport (Airport): El nuevo aeropuerto a añadir.
   Resultado:
       Inserta el aeropuerto en la lista si el código ICAO no está repetido.
"""
def AddAirport(airports, airport):
   found = False
   i = 0
   while i < len(airports):
       if airports[i].icao_code == airport.icao_code:
           found = True
       i += 1
   if not found:
       airports.append(airport)


"""
   Elimina un aeropuerto de la lista mediante su código ICAO.
   Parámetros:
       airports (list): Lista actual de aeropuertos.
       code (str): Código ICAO del aeropuerto a eliminar.
   Resultado:
       Elimina el aeropuerto encontrado. Devuelve un mensaje de error si no existe.
"""
def RemoveAirport(airports, code):
   i = 0
   while i < len(airports):
       if airports[i].icao_code == code:
           airports.remove(airports[i])
           return
       i += 1
   return "Error in the code" # código de error


"""
   Genera y muestra un gráfico de barras comparando aeropuertos Schengen vs No Schengen.
   Parámetros:
       airports (list): Lista de objetos Airport.
   Resultado:
       Genera una gráfica de barras apiladas utilizando matplotlib.
"""
def PlotAirports(airports, ax):
# Muestra un gráfico de barras apiladas con aeropuertos Schengen y no Schengen.
   schengen_count = 0
   non_schengen_count = 0
   for a in airports:
       if a.schengen:
           schengen_count += 1
       else:
           non_schengen_count += 1


   # Datos para la gráfica
   labels = ['Airports']
   schengen = [schengen_count]
   non_schengen = [non_schengen_count]


   # Limpiar eje por si había un gráfico anterior
   ax.clear()


   # Fondo minimalista
   ax.set_facecolor("#ffffff")


   # Barras apiladas
   ax.bar(labels,schengen,label='Schengen',color='#87CEFA')
   ax.bar(labels,non_schengen,bottom=schengen,label='No Schengen',color='#FF7F7F')


   # Estilo
   ax.set_ylabel('Count')
   ax.set_title('Schengen vs No Schengen Airports')
   ax.legend()


   # Grid suave opcional
   ax.grid(axis='y',linestyle='--',alpha=0.3)


"""
   Genera un archivo KML para visualizar aeropuertos en Google Earth.
   Parámetros:
       airports (list): Lista de objetos Airport.
       filename (str): Nombre del archivo .kml resultante (por defecto "airports.kml").
   Formato:
       Exporta latitud, longitud y color (Azul=No Schengen, Rojo=Schengen) al archivo.
   Resultado:
       Crea un archivo KML con marcadores de aeropuertos. Los aeropuertos Schengen aparecen en un color diferente.
"""
def MapAirports(airports, filename = "airports.kml"):
# Genera un archivo KML para ver los aeropuertos en Google Earth.
# Schengen -> azul, No Schengen -> rojo
  F = open(filename, "w")
  # Encabezado KML
  F.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
""")
  for a in airports:
      color = "#ffff0000" if a.schengen else "ff0000ff"  # KML: ABGR (verde/rojo)
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
