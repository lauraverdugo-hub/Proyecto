import tkinter as tk # interfaz gráfica
from tkinter import messagebox, filedialog, scrolledtext # ventanas de error y guardar/abrir archivos
import os # manejar rutas de archivo
import webbrowser # abrir Google Earth automáticamente
from airport import * # funciones de airport.py
from aircraft import * # nueva importación para la Versión 2

# --- NUEVAS IMPORTACIONES PARA LOS GRÁFICOS ---
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Fuerza a Matplotlib a no usar ventanas interactivas propias

aircrafts = [] # nueva lista global para los vuelos cargados
airports = [] # lista de todos los aeropuertos guardados/creados

# ---------------- FUNCIONES V1 ---------------- #

def add_airport():
   code = entry_code.get().upper() # get() extra el texto y upper() lo escribe en mayúsculas
   lat = entry_lat.get()
   lon = entry_lon.get()

   if code == "" or lat == "" or lon == "":
       messagebox.showerror("Error", "Todos los campos son obligatorios")
       return

   try:
       # los convierte a números
       lat = float(lat)
       lon = float(lon)
   except:
       messagebox.showerror("Error", "Lat/Lon deben ser números")
       return

   a = Airport(code, lat, lon) # crea un aeropuerto
   SetSchengen(a) # dtermina si es Schengen
   AddAirport(airports, a)

   update_list() # actualiza la lista
   clear_entries() # limpia los campos

def remove_airport():
   selected = listbox.curselection() # mira los elementos de la lista seleccionados
   if not selected:
       messagebox.showerror("Error", "Selecciona un aeropuerto")
       return

   index = selected[0]
   code = airports[index].icao_code  # obtenemos el código ICAO

   result = RemoveAirport(airports, code)

   if result == -1:
       messagebox.showerror("Error", "Aeropuerto no encontrado")
   else:
       update_list()

def select_airport(event): # permite interactuar con la lista
   # Se ejecuta al hacer click en la lista
   # Detecta el aeropuerto seleccionado
   # Rellena los campos automáticamente
   selected = listbox.curselection()
   if not selected:
       return

   a = airports[selected[0]]

   entry_code.delete(0, tk.END) # borra_todo lo que se haya escrito anteriormente
   entry_code.insert(0, a.icao_code) # escribe el dato del aeropuerto seleccionado empezando desde la posición inicial

   entry_lat.delete(0, tk.END)
   entry_lat.insert(0, a.latitude)

   entry_lon.delete(0, tk.END)
   entry_lon.insert(0, a.longitude)

def load_airports():
   # Abre un explorador de archivos
   # Carga los aeropuertos desde archivo
   filename = filedialog.askopenfilename()
   if filename:
       global airports # Indica que la función va a modificar una lista llamada airports que vive fuera de la función
                       # (en el ámbito global del programa), para que los datos persistan después de terminar la carga
       airports = LoadAirports(filename)

       for a in airports:
           SetSchengen(a)

       update_list()

def save_schengen():
   # Guarda solo aeropuertos Schengen en un archivo
   filename = filedialog.asksaveasfilename(defaultextension=".txt")
   if filename:
       SaveSchengenAirports(airports, filename)

def plot_airports():
   if len(airports) == 0:
       messagebox.showerror("Error", "No hay aeropuertos")
       return
   PlotAirports(airports) # muestra el gráfico

def map_airports():
   if len(airports) == 0:
       messagebox.showerror("Error", "No hay aeropuertos")
       return

   filename = "airports.kml"
   MapAirports(airports, filename) # Genera archivo KML

   path = os.path.abspath(filename) # Obtiene ruta completa
   webbrowser.open(path) # Lo abre automáticamente

# ---------------- FUNCIONES V2 ---------------- #

def load_arrivals():
   filename = filedialog.askopenfilename()
   if filename:
       global aircrafts
       aircrafts = LoadArrivals(filename)
       if not aircrafts:
           messagebox.showerror("Error", "No se pudieron cargar los vuelos o el archivo está vacío.")
       else:
           messagebox.showinfo("Éxito", f"Se han cargado {len(aircrafts)} vuelos.")

def plot_flight_stats():
   if not aircrafts:
       messagebox.showerror("Error", "Primero debes cargar un archivo de vuelos.")
       return
   # Puedes llamar a las tres funciones de gráficos una tras otra
   PlotArrivals(aircrafts)
   PlotAirlines(aircrafts)
   PlotFlightsType(aircrafts)

def long_distance_filter():
   if not aircrafts:
       messagebox.showerror("Error", "No hay vuelos cargados.")
       return

   # Creamos el diccionario de aeropuertos necesario para el cálculo
   # Convertimos la lista 'airports' en un diccionario {ICAO: objeto}
   airports_dict = {a.icao_code: a for a in airports}
   long_dist = LongDistanceArrivals(aircrafts, airports_dict)

   if not long_dist:
       messagebox.showinfo("Resultado", "No se encontraron vuelos de más de 2000km.")
   else:
       # Mostramos cuántos hay y preguntamos si quiere guardarlos
       if messagebox.askyesno("Larga Distancia",f"Se han encontrado {len(long_dist)} vuelos. ¿Deseas guardarlos en un archivo?"):
           save_filename = filedialog.asksaveasfilename(defaultextension=".txt")
           if save_filename:
               SaveFlights(long_dist, save_filename)

def map_flight_trajectories():
   if not aircrafts or not airports: # Aseguramos de tener tanto los vuelos como la base de datos de aeropuertos
       messagebox.showerror("Error", "Se necesitan vuelos y aeropuertos cargados.")
       return

   airports_dict = {a.icao_code: a for a in airports}
   filename = "flight_trajectories.kml"

   MapFlights(aircrafts, airports_dict, filename)

   path = os.path.abspath(filename)
   webbrowser.open(path)

# --- FUNCIONES DE APOYO PARA LA INTERFAZ ---

def update_list(): # para actualizar la lista cada vez que se carga o se elimina algo
   listbox.delete(0, tk.END) # borra_todo lo que haya en la lista actualmente
   for a in airports:
       listbox.insert(tk.END,f"{a.icao_code} | {round(a.latitude,4)}, {round(a.longitude,4)} | {'Schengen' if a.schengen else 'No Schengen'}")
       # inserta la información necesaria de cada aeropuerto

def clear_entries(): # sirve para vaciar/limpiar los campos de texto
   entry_code.delete(0, tk.END) # se borra_todo el contenido desde el primer carácter hasta el último
   entry_lat.delete(0, tk.END)
   entry_lon.delete(0, tk.END)

def log_info(message):
   info_text.config(state='normal') # por defecto, el cuadro de texto suele estar en modo "solo lectura"
   info_text.insert(tk.END, f"> {message}\n") # añadimos el mensaje
   info_text.config(state='disabled')
   info_text.see(tk.END) # scroll automático hacia abajo para ver el último mensaje

def update_flights_list(): # para actualizar la lista cada vez que se carga o se elimina algo
   listbox_vuelos.delete(0, tk.END)
   for f in aircrafts:
       try:
           info = f"{f.aircraft_id} | {f.origin_airport} | {f.landing_time} | {f.airline_company}"
           listbox_vuelos.insert(tk.END, info)
       except AttributeError:
           listbox_vuelos.insert(tk.END, "Error: Los atributos no coinciden en Aircraft")

def load_arrivals_wrapper():
   filename = filedialog.askopenfilename()
   if filename:
       global aircrafts
       aircrafts = LoadArrivals(filename)
       if aircrafts:
           log_info(f"Cargados {len(aircrafts)} vuelos.")
           update_flights_list()

def mostrar_en_interfaz(funcion_plot, datos):
    if not datos:
        messagebox.showerror("Error", "No hay datos cargados.")
        return

    # Evitar que el frame crezca para ajustarse al contenido
    plot_frame.pack_propagate(False)

    for widget in plot_frame.winfo_children():
        widget.destroy()

    try:
        plt.clf()

        # Ejecutamos tu función original
        funcion_plot(datos)

        fig = plt.gcf()

        # AJUSTE DE TAMAÑO: Forzamos un tamaño pequeño inicial y ajuste de márgenes
        # Esto evita que el gráfico "empuje" a los botones hacia abajo
        fig.set_size_inches(5, 3)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()

        # Usamos expand=True pero dentro de un contenedor con tamaño bloqueado
        widget_canvas = canvas.get_tk_widget()
        widget_canvas.pack(fill="both", expand=True)

        log_info("Gráfico ajustado al panel.")

    except Exception as e:
        log_info(f"Error: {e}")

# ---------------- INTERFAZ GRÁFICA ---------------- #

root = tk.Tk()
root.title("Airport Manager")
root.geometry("1100x850")
root.resizable(False, False) # Evita que la ventana se deforme
root.configure(bg="#f0f0f0")

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# --- PANEL IZQUIERDO ---
left_panel = tk.Frame(main_frame, bg="#f0f0f0")
left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

tk.Label(left_panel, text="Aeropuertos", font=("Arial", 10, "bold")).pack(anchor="w")
listbox = tk.Listbox(left_panel, height=10); listbox.pack(fill="both", expand=True, pady=(0, 5))
listbox.bind("<<ListboxSelect>>", select_airport)

tk.Label(left_panel, text="Vuelos (Arrivals)", font=("Arial", 10, "bold")).pack(anchor="w")
listbox_vuelos = tk.Listbox(left_panel, height=10); listbox_vuelos.pack(fill="both", expand=True, pady=(0, 5))

input_frame = tk.LabelFrame(left_panel, text="Datos del Aeropuerto", padx=10, pady=10)
input_frame.pack(fill="x")
tk.Label(input_frame, text="ICAO:").grid(row=0, column=0)
entry_code = tk.Entry(input_frame, width=7); entry_code.grid(row=0, column=1, padx=2)
tk.Label(input_frame, text="Lat:").grid(row=0, column=2)
entry_lat = tk.Entry(input_frame, width=7); entry_lat.grid(row=0, column=3, padx=2)
tk.Label(input_frame, text="Lon:").grid(row=0, column=4)
entry_lon = tk.Entry(input_frame, width=7); entry_lon.grid(row=0, column=5, padx=2)

# --- PANEL DERECHO: DEFINICIÓN Y ESTRUCTURA ---
right_panel = tk.Frame(main_frame, bg="#f0f0f0")
right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

# Título y Cuadro de Log (Información del Sistema)
tk.Label(right_panel, text="Información del Sistema", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
info_text = scrolledtext.ScrolledText(right_panel, height=6, state='disabled', bg="white", font=("Consolas", 10))
info_text.pack(fill="x", pady=(0, 10))

# Título y Cuadro de Visualización (Plots)
tk.Label(right_panel, text="Visualización de Gráficos", font=("Arial", 10, "bold"), bg="#f0f0f0").pack(anchor="w")
plot_frame = tk.LabelFrame(right_panel, bg="white", height=420)
plot_frame.pack(fill="both", expand=True)
plot_frame.pack_propagate(False) # Bloquea el tamaño para que el plot no estire la ventana

# --- BOTONES INFERIORES ---
bottom_frame = tk.Frame(root, bg="#f0f0f0")
bottom_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
btn_style = {'width': 28, 'pady': 2}

group_airports = tk.LabelFrame(bottom_frame, text="Airports", padx=10, pady=5)
group_airports.pack(side="left", padx=5)
tk.Button(group_airports, text="Cargar aeropuertos", command=load_airports, **btn_style).pack()
tk.Button(group_airports, text="Añadir aeropuerto", command=add_airport, **btn_style).pack()
tk.Button(group_airports, text="Eliminar seleccionado", command=remove_airport, **btn_style).pack()
tk.Button(group_airports, text="Guardar Schengen (fichero)", command=save_schengen, **btn_style).pack()
tk.Button(group_airports, text="Plot Schengen/NoSchengen", command=lambda: mostrar_en_interfaz(PlotAirports, airports), **btn_style).pack()
tk.Button(group_airports, text="Mapa (Google Earth)", command=map_airports, **btn_style).pack()

group_arrivals = tk.LabelFrame(bottom_frame, text="Arrivals", padx=10, pady=5)
group_arrivals.pack(side="left", padx=5)
tk.Button(group_arrivals, text="Cargar vuelos", command=load_arrivals_wrapper, **btn_style).pack(pady=1)
tk.Button(group_arrivals, text="Plot llegadas/hora", command=lambda: mostrar_en_interfaz(PlotArrivals, aircrafts), **btn_style).pack(pady=1)
tk.Button(group_arrivals, text="Plot aerolíneas", command=lambda: mostrar_en_interfaz(PlotAirlines, aircrafts), **btn_style).pack(pady=1)
tk.Button(group_arrivals, text="Plot tipo de vuelo", command=lambda: mostrar_en_interfaz(PlotFlightsType, aircrafts), **btn_style).pack(pady=1)
tk.Button(group_arrivals, text="Vuelos larga distancia (>2k)", command=long_distance_filter, **btn_style).pack(pady=1)
tk.Button(group_arrivals, text="Mapa Trayectorias", command=map_flight_trajectories, **btn_style).pack(pady=1)

log_info("Sistema listo. Cargue datos para comenzar.")
root.mainloop()
