import tkinter as tk # interfaz gráfica
from tkinter import messagebox, filedialog # ventanas de error y guardar/abrir archivos
import os # manejar rutas de archivo
import webbrowser # abrir Google Earth automáticamente
from airport import * # funciones de airport.py

airports = [] # lista de todos los aeropuertos guardados/creados

# ---------------- FUNCIONES ---------------- #

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

def update_list(): # para actualizar la lista cada vez que se carga o se elimina algo
    listbox.delete(0, tk.END) # borra_todo lo que haya en la lista actualmente
    for a in airports:
        listbox.insert(tk.END,f"{a.icao_code} | {round(a.latitude,4)}, {round(a.longitude,4)} | {'Schengen' if a.schengen else 'No Schengen'}")
        # inserta la información necesaria de cada aeropuerto

def clear_entries(): # sirve para vaciar/limpiar los campos de texto
    entry_code.delete(0, tk.END) # se borra_todo el contenido desde el primer carácter hasta el último
    entry_lat.delete(0, tk.END)
    entry_lon.delete(0, tk.END)

# ---------------- INTERFAZ ---------------- #

root = tk.Tk()
root.title("AIRPORT MANAGER")
root.geometry("600x420")

# Centrado
# Esto hace que las columnas 0 y 1 se repartan el espacio y centren el contenido
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Inputs
tk.Label(root, text="ICAO Code").grid(row=0, column=0, sticky="e", padx=5, pady=2)
entry_code = tk.Entry(root)
entry_code.grid(row=0, column=1, sticky="w", padx=5, pady=2)

tk.Label(root, text="Latitude").grid(row=1, column=0, sticky="e", padx=5, pady=2)
entry_lat = tk.Entry(root)
entry_lat.grid(row=1, column=1, sticky="w", padx=5, pady=2)

tk.Label(root, text="Longitude").grid(row=2, column=0, sticky="e", padx=5, pady=2)
entry_lon = tk.Entry(root)
entry_lon.grid(row=2, column=1, sticky="w", padx=5, pady=2)

# Botones
tk.Button(root, text="1. Load File", width=20, command=load_airports).grid(row=3, column=0, pady=2, padx=5, sticky="e")
tk.Button(root, text="2. Add Airport", width=20, command=add_airport).grid(row=4, column=0, pady=2, padx=5, sticky="e")
tk.Button(root, text="3. Remove Airport", width=20, command=remove_airport).grid(row=5, column=0, pady=2, padx=5, sticky="e")

tk.Button(root, text="4. Save Schengen", width=20, command=save_schengen).grid(row=3, column=1, pady=2, padx=5, sticky="w")
tk.Button(root, text="5. Plot Airports", width=20, command=plot_airports).grid(row=4, column=1, pady=2, padx=5, sticky="w")
tk.Button(root, text="6. Map (Google Earth)", width=20, command=map_airports).grid(row=5, column=1, pady=2, padx=5, sticky="w")

# Lista
listbox = tk.Listbox(root, width=80, height=12)
listbox.grid(row=9, column=0, columnspan=2, pady=15, padx=20)

# Cuando haces click carga datos en los inputs
listbox.bind("<<ListboxSelect>>", select_airport)

# Ejecuta
root.mainloop()