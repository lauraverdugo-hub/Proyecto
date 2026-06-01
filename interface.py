<<<<<<< HEAD
# =====================================================================
# AIRPORT OPERATIONS SUITE — CENTRO DE CONTROL UNIFICADO (V4 ESTRICTO)
# =====================================================================
=======
"""
=====================================================================
AIRPORT OPERATIONS SUITE — INTERFAZ GRÁFICA PRINCIPAL
=====================================================================
   Descripción:
        Sistema gráfico desarrollado con Tkinter para la gestión visual de:
             V1 -> Aeropuertos
             V2 -> Tráfico aéreo
             V3 -> Gestión de puertas y terminales (LEBL)
   El programa permite:
        - Cargar aeropuertos desde archivos.
        - Gestionar vuelos entrantes.
        - Visualizar gráficos estadísticos.
        - Asignar puertas automáticamente.
        - Exportar rutas KML para Google Earth.
        - Mostrar información en tiempo real.
   Tecnologías utilizadas:
        - Tkinter
        - Matplotlib
        - Python estándar
        - Integración con módulos propios:
              airport.py
              aircraft.py
              LEBL.py
   Resultado:
         Interfaz gráfica interactiva de gestión aeroportuaria.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
import os
import sys
import subprocess
import warnings
import matplotlib
import pyglet

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Silenciamos warnings de matplotlib
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Importaciones de módulos propios
from airport import Airport, LoadAirports, SetSchengen, PlotAirports, SaveSchengenAirports
import aircraft
import LEBL

# Variables globales compartidas
airports = []
aircrafts = []
current_bcn = None
selected_flight_idx = None
vista_actual = "mapa"
archivo_estructura_guardado = None
hora_vista_actual = "00:00"  # Control de la hora activa para el mapa dinámico

# Variables globales para el control de música
audio_player = None
music_playing = False
MUSIC_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica.mp3")

# =====================================================================
# LÓGICA DE CONTROL DE LA INTERFAZ
# =====================================================================
<<<<<<< HEAD
=======

"""
    Muestra mensajes informativos en la consola integrada.
    Parámetros:
        message (str): Texto que se mostrará en el historial.
    Resultado:
        Inserta el mensaje en el widget ScrolledText.
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
def log_info(message):
   info_text.config(state='normal')
   info_text.insert(tk.END, f"> {message}\n")
   info_text.config(state='disabled')
   info_text.see(tk.END)

"""
    Actualiza la lista visual de aeropuertos.
    Resultado:
         Refresca el contenido del Listbox principal mostrando: ICAO | Latitud | Longitud | Tipo Schengen
"""
def update_list():
   listbox.delete(0, tk.END)
   for a in airports:
       listbox.insert(tk.END,
                      f" {a.icao_code}  |  {round(a.latitude, 4)}, {round(a.longitude, 4)}  |  {'Schengen' if a.schengen else 'No Schengen'}")

"""
    Actualiza la lista visual de vuelos.
    Resultado:
         Refresca el Listbox de vuelos mostrando: ID | Origen | Hora | Aerolínea
"""
def update_flights_list():
   listbox_vuelos.delete(0, tk.END)
   for f in aircrafts:
       arr_t = f.landing_time if f.landing_time else "--:--"
       dep_t = f.departure_time if f.departure_time else "--:--"
       listbox_vuelos.insert(tk.END, f" {f.aircraft_id:<8} | {f.airline_company:<4} | ARR: {arr_t} | DEP: {dep_t}")

"""
    Limpia los campos del formulario manual de aeropuertos.
    Resultado:
        Vacía:
            - Código ICAO
            - Latitud
            - Longitud
"""
def clear_entries():
   entry_code.delete(0, tk.END)
   entry_lat.delete(0, tk.END)
   entry_lon.delete(0, tk.END)

"""
    Selecciona un aeropuerto desde la lista visual.
    Parámetros:
        event (tkinter.Event): Evento generado por el Listbox.
    Resultado:
        Copia automáticamente los datos del aeropuerto seleccionado en el formulario editable.
"""
def select_airport(event):
   selected = listbox.curselection()
   if not selected: return
   a = airports[selected[0]]
   clear_entries()
   entry_code.insert(0, a.icao_code)
   entry_lat.insert(0, a.latitude)
   entry_lon.insert(0, a.longitude)

def select_flight(event):
   global selected_flight_idx
   selected = listbox_vuelos.curselection()
   if not selected: return
   selected_flight_idx = selected[0]
   ac = aircrafts[selected_flight_idx]
   entry_ac_id.delete(0, tk.END)
   entry_ac_id.insert(0, ac.aircraft_id)
   entry_ac_comp.delete(0, tk.END)
   entry_ac_comp.insert(0, ac.airline_company)
   entry_ac_orig.delete(0, tk.END)
   entry_ac_orig.insert(0, ac.origin_airport if ac.origin_airport else "LEBL")

def limpiar_contenedor_principal():
   for w in contenedor_principal.winfo_children():
       w.destroy()
   plt.close('all')

# =====================================================================
# CONTROL DE AUDIO CON PYGLET
# =====================================================================
def iniciar_musica():
  global audio_player, music_playing
  if not os.path.exists(MUSIC_FILE):
      messagebox.showerror(
          "Error de audio",
          f"No se encuentra el archivo de música:\n{MUSIC_FILE}"
      )
      return

  try:
      source = pyglet.media.load(MUSIC_FILE, streaming=True)

      audio_player = pyglet.media.Player()
      audio_player.queue(source)
      audio_player.loop = True
      audio_player.volume = volume_var.get() / 100

      audio_player.play()
      music_playing = True

      btn_music.config(text="⏹ Detener música")
      log_info("Música iniciada.")

  except Exception as e:
      messagebox.showerror("Error de audio", f"No se pudo reproducir la música:\n{e}")

def detener_musica():
  global audio_player, music_playing

  try:
      if audio_player:
          audio_player.pause()
          audio_player.delete()
  except Exception:
      pass

  audio_player = None
  music_playing = False

  try:
      btn_music.config(text="🎵 Reproducir música")
      log_info("Música detenida.")
  except Exception:
      pass

def toggle_music():
  if music_playing:
      detener_musica()
  else:
      iniciar_musica()

def cambiar_volumen(valor):
  global audio_player
  volumen = float(valor) / 100
  if audio_player:
      audio_player.volume = volumen

def cerrar_programa():
  detener_musica()
  root.destroy()

# --- Gestor de Vistas e Inyección de Gráficos --- #
def cambiar_vista(tipo_vista):
   global vista_actual
   vista_actual = tipo_vista
   limpiar_contenedor_principal()

   btn_ver_mapa.config(relief="groove", bg="#f2eefb" if tipo_vista == "mapa" else "#eef0f2")
   btn_ver_graf_24h.config(relief="groove", bg="#f2eefb" if tipo_vista == "graf_24h" else "#eef0f2")
   btn_ver_graf_air.config(relief="groove", bg="#f2eefb" if tipo_vista == "graf_air" else "#eef0f2")
   btn_ver_graf_tipo.config(relief="groove", bg="#f2eefb" if tipo_vista == "graf_tipo" else "#eef0f2")
   btn_ver_graf_sch.config(relief="groove", bg="#f2eefb" if tipo_vista == "graf_sch" else "#eef0f2")
   btn_ver_graf_arr.config(relief="groove",bg="#f2eefb" if tipo_vista == "graf_arr" else "#eef0f2")

   if tipo_vista == "mapa":
       construir_vista_mapa_pasarelas()
   elif tipo_vista == "graf_24h":
       if not current_bcn or not aircrafts:
           messagebox.showinfo("Aviso", "Requierre cargar la estructura LEBL y el tráfico de vuelos primero.")
           cambiar_vista("mapa")
           return
       inyectar_grafico_24h_enunciado()
   elif tipo_vista == "graf_air":
       inyectar_grafico_matplot(
           lambda ax: aircraft.PlotAirlines(aircrafts, ax) if aircrafts else messagebox.showinfo("Aviso",
                                                                                                 "Carga el tráfico de vuelos primero."),
           optimizar_fuentes=True)
   elif tipo_vista == "graf_tipo":
       inyectar_grafico_matplot(
           lambda ax: aircraft.PlotFlightsType(aircrafts, ax)
           if aircrafts else
           messagebox.showinfo("Aviso",
                               "Carga el tráfico de vuelos primero.")
       )

   elif tipo_vista == "graf_sch":
       inyectar_grafico_matplot(
           lambda ax: PlotAirports(airports, ax)
           if airports else
           messagebox.showinfo("Aviso",
                               "Carga el fichero de aeropuertos primero.")
       )

   elif tipo_vista == "graf_arr":
       if not aircrafts:
           messagebox.showinfo(
               "Aviso",
               "Carga el tráfico de vuelos primero."
           )
           cambiar_vista("mapa")
           return

       inyectar_grafico_matplot(
           lambda ax: aircraft.PlotArrivals(aircrafts, ax)
       )
   elif tipo_vista == "earth":
       LEBL.mostrar_google_earth()

def inyectar_grafico_matplot(funcion_dibujado, optimizar_fuentes=False):
   fig = plt.Figure(figsize=(9, 5), dpi=100)
   ax = fig.add_subplot(111)

   try:
       funcion_dibujado(ax)
       if optimizar_fuentes:
           ax.tick_params(axis='x', labelsize=7, rotation=45)
           fig.subplots_adjust(bottom=0.25)
       else:
           fig.autofmt_xdate(rotation=30, ha='right')
           fig.subplots_adjust(bottom=0.20)

       fig.tight_layout()
       canvas = FigureCanvasTkAgg(fig, master=contenedor_principal)
       canvas.draw()
       canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
   except Exception:
       limpiar_contenedor_principal()
       tk.Label(contenedor_principal, text="Complete la carga de datos previa para activar esta analítica.",
                bg="#ffffff", font=font_ui).pack(pady=40)

def inyectar_grafico_24h_enunciado():
   global current_bcn, aircrafts, archivo_estructura_guardado

   show_original = plt.show
   plt.show = lambda *args, **kwargs: None
   plt.ioff()

   try:
       plt.close('all')

       # Generar clon limpio del inicio del día como exige el enunciado
       if archivo_estructura_guardado:
           bcn_inicial = LEBL.LoadAirportStructure(archivo_estructura_guardado)
       else:
           bcn_inicial = current_bcn

       night_list, _ = aircraft.NightAircraft(aircrafts)
       if night_list:
           aircraft.AssignNightGates(bcn_inicial, night_list)

       # Llamamos a tu función obligatoria de la V4
       try:
           aircraft.PlotDayOccupancy(bcn_inicial, aircrafts)
       except Exception:
           # Fallback por si requiere pasar el eje ax directamente
           fig_temp = plt.Figure(figsize=(9, 4.8))
           ax_temp = fig_temp.add_subplot(111)
           aircraft.PlotDayOccupancy(bcn_inicial, aircrafts, ax_temp)

       fig_actual = plt.gcf()
       fig_actual.set_size_inches(9, 4.8)
       fig_actual.tight_layout()

       canvas = FigureCanvasTkAgg(fig_actual, master=contenedor_principal)
       canvas.draw()
       canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

   except Exception as e:
       tk.Label(contenedor_principal, text="Error al ejecutar el PlotDayOccupancy del alumno.", bg="#ffffff",
                font=font_ui).pack(pady=40)
   finally:
       plt.show = show_original
       plt.ion()

# --- EXTRA FUNCIONALIDAD: Simulación del estado del mapa por hora ("On Demand") --- #
def ui_cambiar_hora_simulacion(event=None):
   global current_bcn, aircrafts, archivo_estructura_guardado, hora_vista_actual
   if not current_bcn or not aircrafts or not archivo_estructura_guardado: return

   hora_vista_actual = combo_hora.get()
   hora_limite = int(hora_vista_actual.split(":")[0])

   # 1. Resetear el aeropuerto al inicio del día
   current_bcn = LEBL.LoadAirportStructure(archivo_estructura_guardado)

   # 2. Asignar aviones de la noche
   night_list, _ = aircraft.NightAircraft(aircrafts)
   if night_list:
       aircraft.AssignNightGates(current_bcn, night_list)

   # 3. Correr la simulación dinámica hora a hora usando AssignGatesAtTime hasta la hora elegida
   for h in range(1, hora_limite + 1):
       aircraft.AssignGatesAtTime(current_bcn, aircrafts, f"{h:02d}:00")

   # 4. Refrescar la vista del mapa
   construir_vista_mapa_pasarelas()

def construir_vista_mapa_pasarelas():
   global current_bcn

   # Limpiamos el contenedor antes de dibujar
   for w in contenedor_principal.winfo_children(): w.destroy()

   mapa_canvas = tk.Canvas(contenedor_principal, bg="#ffffff", bd=0, highlightthickness=0)
   mapa_scrollbar = tk.Scrollbar(contenedor_principal, orient="vertical", command=mapa_canvas.yview)
   mapa_container = tk.Frame(mapa_canvas, bg="#ffffff")

   mapa_scrollbar.pack(side="right", fill="y")
   mapa_canvas.pack(side="left", fill="both", expand=True)

   canvas_frame_id = mapa_canvas.create_window((0, 0), window=mapa_container, anchor="nw")

   def ajustar_scroll_estricto(event):
       mapa_canvas.configure(scrollregion=mapa_canvas.bbox("all"))

   mapa_container.bind("<Configure>", ajustar_scroll_estricto)
   mapa_canvas.bind("<Configure>", lambda e: mapa_canvas.itemconfig(canvas_frame_id, width=e.width))
   mapa_canvas.configure(yscrollcommand=mapa_scrollbar.set)

   if not current_bcn:
       tk.Label(mapa_container,
                text="Estructura de aeropuerto no inicializada.\nUse el botón 'Construir Estructura LEBL' de la barra inferior.",
                bg="#ffffff", font=font_ui, fg="#7f8c8d").pack(pady=100)
       return

   filter_comp = entry_filter_comp.get().strip().upper()
   terminals_list = getattr(current_bcn, 'terminals', getattr(current_bcn, 'terminales', []))

   for term in terminals_list:
       t_name = getattr(term, 'name', getattr(term, 'nombre', 'T'))
       t_frame = tk.LabelFrame(mapa_container, text=f" Terminal {t_name} ", font=font_title, bg="#ffffff", bd=1,
                               relief="solid")
       t_frame.pack(fill="x", padx=10, pady=8)

       areas_list = getattr(term, 'boarding_areas', getattr(term, 'areas', []))

       for area in areas_list:
           a_name = getattr(area, 'name', getattr(area, 'nombre', 'Area'))
           a_type = getattr(area, 'type', getattr(area, 'area_type', 'Schengen'))

           a_frame = tk.Frame(t_frame, bg="#ffffff", pady=5)
           a_frame.pack(fill="x", padx=5, pady=2)

           tk.Label(a_frame, text=f"Área {a_name} ({a_type}):", font=("Segoe UI", 9, "bold"), bg="#ffffff",
                    fg="#444444", width=22, anchor="w").pack(side="top", anchor="w", padx=5, pady=(0, 4))

           gates_subframe = tk.Frame(a_frame, bg="#ffffff")
           gates_subframe.pack(side="top", fill="x", expand=True, padx=20)

           gates_list = getattr(area, 'gates', getattr(area, 'puertas', []))
           MAX_PUERTAS_POR_FILA = 12

           for index, gate in enumerate(gates_list):
               g_id = getattr(gate, 'name', '??')
               g_occ = getattr(gate, 'occupied', False)
               g_ac = getattr(gate, 'aircraft_id', "")

               saco_aerolineas = []
               if g_ac:
                   saco_aerolineas.append(g_ac.upper())
                   if len(g_ac) >= 3: saco_aerolineas.append(g_ac[:3].upper())

                   global aircrafts
                   for flight in aircrafts:
                       if getattr(flight, 'aircraft_id', '').upper() == g_ac.upper():
                           if hasattr(flight, 'airline_company'):
                               saco_aerolineas.append(str(flight.airline_company).upper())

               bg_color = "#e2f0d9" if not g_occ else "#fce4d6"
               fg_color = "#385723" if not g_occ else "#c65911"
               text_gate = f"{g_id}\n[Libre]" if not g_occ else f"{g_id}\n[{g_ac}]"

               if g_occ and filter_comp:
                   coincide = False
                   for d in saco_aerolineas:
                       if filter_comp in d:
                           coincide = True;
                           break
                   if coincide:
                       bg_color = "#fff2cc";
                       fg_color = "#b27a00"
                   else:
                       bg_color = "#f2f2f2";
                       fg_color = "#a6a6a6"

               fila = index // MAX_PUERTAS_POR_FILA
               columna = index % MAX_PUERTAS_POR_FILA

               lbl = tk.Label(gates_subframe, text=text_gate, font=("Consolas", 8, "bold"), bg=bg_color, fg=fg_color,
                              bd=1, relief="solid", width=10, height=2)
               lbl.grid(row=fila, column=columna, padx=3, pady=3, sticky="nsew")

   def _on_mousewheel(event):
       mapa_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

   def bind_recursive(widget):
       widget.bind("<MouseWheel>", _on_mousewheel)
       for child in widget.winfo_children(): bind_recursive(child)

   bind_recursive(mapa_canvas)
   bind_recursive(mapa_container)

   root.after(50, lambda: mapa_canvas.configure(scrollregion=mapa_canvas.bbox("all")))

# --- Acciones de Carga e Interacción --- #
def ui_refresh_gates_grid():
   if vista_actual == "mapa":
       construir_vista_mapa_pasarelas()

<<<<<<< HEAD
=======
# --- Acciones V1 y V2 --- #

"""
    Carga un fichero de aeropuertos desde interfaz.
    Funcionamiento:
        - Abre selector de archivos.
        - Carga aeropuertos.
        - Determina automáticamente si son Schengen.
    Resultado:
        Actualiza:
            - Lista de aeropuertos
            - Consola informativa
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
def load_airports_ui():
   filename = filedialog.askopenfilename(title="Cargar Aeropuertos (V1)")
   if filename:
       global airports
       airports = LoadAirports(filename)
       for a in airports: SetSchengen(a)
       update_list()
       log_info(f"Cargados {len(airports)} aeropuertos.")
       if vista_actual == "graf_sch": cambiar_vista("graf_sch")

"""
    Inserta manualmente un aeropuerto.
    Datos requeridos:
        - Código ICAO
        - Latitud
        - Longitud
    Resultado:
        Añade el aeropuerto al sistema y actualiza la interfaz gráfica.
"""
def add_airport_ui():
   code, lat, lon = entry_code.get().upper(), entry_lat.get(), entry_lon.get()
   if not code or not lat or not lon: return
   try:
       a = Airport(code, float(lat), float(lon))
       SetSchengen(a);
       airports.append(a);
       update_list();
       clear_entries()
       log_info(f"Aeropuerto {code} incorporado.")
       if vista_actual == "graf_sch": cambiar_vista("graf_sch")
   except ValueError:
       messagebox.showerror("Error", "Valores numéricos inválidos.")

"""
    Elimina el aeropuerto seleccionado.
    Resultado:
        Borra el aeropuerto activo del sistema y actualiza la lista visual.
"""
def remove_airport_ui():
   selected = listbox.curselection()
   if not selected: return
   del airports[selected[0]]
   update_list();
   log_info("Aeropuerto eliminado.")
   if vista_actual == "graf_sch": cambiar_vista("graf_sch")

<<<<<<< HEAD
def save_schengen_airports_ui():
    global airports

    if not airports:
        messagebox.showwarning(
            "Sin datos",
            "No hay aeropuertos cargados."
        )
        return

    filename = filedialog.asksaveasfilename(
        title="Guardar aeropuertos Schengen",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )

    if not filename:
        return

    try:
        SaveSchengenAirports(airports, filename)
        log_info(f"Fichero Schengen exportado: {os.path.basename(filename)}")
        messagebox.showinfo("Exportación completada","Aeropuertos Schengen guardados correctamente.")

    except Exception as e:
        messagebox.showerror("Error",f"No se pudo guardar el fichero:\n{e}")

def load_v4_data_ui():
   file_arr = filedialog.askopenfilename(title="Seleccionar archivo de LLEGADAS (Arrivals)")
   if not file_arr: return
   file_dep = filedialog.askopenfilename(title="Seleccionar archivo de SALIDAS (Departures)")
   if not file_dep: return
   arrivals, err1 = aircraft.LoadArrivals(file_arr)
   departures, err2 = aircraft.LoadDepartures(file_dep)
   if err1 == -1 or err2 == -1: return
   global aircrafts
   aircrafts, err3 = aircraft.MergeMovements(arrivals, departures)
   update_flights_list()
   log_info(f"V4: Flujo combinado listo. {len(aircrafts)} aeronaves mapeadas.")
   if vista_actual in [
       "graf_air",
       "graf_tipo",
       "graf_24h",
       "graf_arr"
   ]:
       cambiar_vista(vista_actual)

def ui_build_airport_structure():
   global current_bcn, archivo_estructura_guardado
   filename = filedialog.askopenfilename(title="Seleccionar Estructura (Terminals.txt)")
   if filename:
       archivo_estructura_guardado = filename
       current_bcn = LEBL.LoadAirportStructure(filename)
       if current_bcn:
           log_info(f"Estructura operativa de {current_bcn.code} desplegada con éxito.")
           cambiar_vista("mapa")

def ui_apply_filter():
   cambiar_vista("mapa")

def ui_clear_filter():
   entry_filter_comp.delete(0, tk.END)
   cambiar_vista("mapa")

def ui_assign_gate_manually():
   global current_bcn
   if not current_bcn: return
   a_id, a_comp, a_orig = entry_ac_id.get().strip().upper(), entry_ac_comp.get().strip().upper(), entry_ac_orig.get().strip().upper()
   if not a_id or not a_comp or not a_orig: return
   is_schengen = messagebox.askyesno("Control Schengen", "¿El vuelo es de zona Schengen?")
   try:
       test_ac = LEBL.Aircraft(a_id, a_comp, a_orig, "00:00", is_schengen=is_schengen)
       if LEBL.AssignGate(current_bcn, test_ac) is None:
           log_info(f"Asignación manual exitosa: {a_id}")
           ui_refresh_gates_grid();
           return
   except Exception:
       pass
   ui_refresh_gates_grid()

def ui_operator_forced_assignment():
   global current_bcn, aircrafts
   if not current_bcn or not aircrafts: return
   selected = listbox_vuelos.curselection()
   if not selected: return
   ac = aircrafts[selected[0]]
   raw_target = entry_forced_gate.get().strip().lower()
   if not raw_target: return
   for term in current_bcn.terminals:
       for area in term.boarding_areas:
           for g in area.gates:
               if raw_target in g.name.lower():
                   if g.occupied: return
                   g.occupied = True;
                   g.aircraft_id = ac.aircraft_id
                   log_info(f"Operador forzó {ac.aircraft_id} en {g.name}.")
                   ui_refresh_gates_grid();
                   entry_forced_gate.delete(0, tk.END);
                   return

def ui_free_gate_manual():
   global current_bcn
   if not current_bcn: return
   a_id = entry_ac_id.get().strip().upper()
   if not a_id: return
   res = aircraft.FreeGate(current_bcn, a_id)
   log_info(f"Puerta del avión {a_id} liberada.")
   ui_refresh_gates_grid()

def ui_assign_all_automatically():
   global current_bcn, aircrafts
   if not current_bcn or not aircrafts: return
   night_list, _ = aircraft.NightAircraft(aircrafts)
   if night_list: aircraft.AssignNightGates(current_bcn, night_list)
   total_unassigned = 0
   for h in range(24): total_unassigned += aircraft.AssignGatesAtTime(current_bcn, aircrafts, f"{h:02d}:00")
   log_info(f"Asignación automática masiva lista. Sin pasarela hoy: {total_unassigned}")
   # Al terminar la asignación total, dejamos el mapa en las 23:00 para ver la ocupación final
   combo_hora.set("23:00")
   ui_cambiar_hora_simulacion()

def ui_export_kml_v4():
   global current_bcn, aircrafts, airports
   if not current_bcn or not aircrafts: return
   fn = LEBL.ExportFlightsToKMLWithTerminal(aircrafts, current_bcn, airports)
   log_info(f"KML generado con éxito: '{fn}'.")

   if messagebox.askyesno("Google Earth", f"¿Desea forzar el lanzamiento de '{fn}' en Google Earth Windows ahora?"):
       try:
           ruta_absoluta = os.path.abspath(fn)
           if sys.platform.startswith('win'):
               subprocess.Popen(f'start "" "{ruta_absoluta}"', shell=True)
           elif sys.platform == 'darwin':
               subprocess.call(('open', ruta_absoluta))
           else:
               subprocess.call(('xdg-open', ruta_absoluta))
       except Exception:
           messagebox.showerror("Error",
                                "Windows no pudo arrancar el visor. Asegúrate de tener instalado Google Earth Pro.")
=======
"""
    Carga vuelos desde un archivo externo.
    Resultado:
        - Actualiza la lista de vuelos.
        - Muestra información en consola.
"""
def load_arrivals_ui():
    filename = filedialog.askopenfilename()
    if filename:
        global aircrafts
        aircrafts = LoadArrivals(filename)
        if aircrafts:
            log_info(f"Cargados {len(aircrafts)} registros de vuelos entrantes.")
            update_flights_list()

"""
    Genera gráficos dinámicos dentro de Tkinter.
    Parámetros:
        funcion_plot (function): Función externa que genera el gráfico.
        datos (list): Datos a representar.
    Resultado:
        Inserta el gráfico Matplotlib dentro del panel gráfico de la interfaz.
"""
def mostrar_grafico_v2(funcion_plot, datos):
    if not datos:
        messagebox.showerror("Aviso","No existen datos cargados para generar este gráfico.")
        return

    # Limpiar gráficos anteriores del frame
    for w in plot_frame.winfo_children():
        w.destroy()

    # Cerrar figuras anteriores de matplotlib
    plt.close('all')

    # Crear nueva figura
    fig = plt.Figure(figsize=(5.8, 3.4),dpi=100)

    # Crear eje
    ax = fig.add_subplot(111)

    # Fondo blanco minimalista
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")

    # Dibujar gráfico
    funcion_plot(datos, ax)

    # Ajuste automático
    fig.tight_layout()

    # Insertar en Tkinter
    canvas = FigureCanvasTkAgg(fig,master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both",expand=True)

# --- Acciones V3 (Gates) --- #

"""
    Construye la estructura operativa del aeropuerto.
    Funcionamiento:
        - Carga archivo Terminals.txt
        - Genera terminales y puertas
        - Actualiza visualización
    Resultado:
        Inicializa el sistema V3.
"""
def ui_build_airport_structure():
    global current_bcn
    filename = filedialog.askopenfilename(title="Seleccionar Estructura (Terminals.txt)")
    if filename:
        current_bcn = LEBL.LoadAirportStructure(filename)
        if current_bcn:
            log_info(f"Estructura operativa de {current_bcn.code} desplegada con éxito.")
            ui_refresh_gates_grid()
            ui_draw_v3_chart()

"""
    Simula la asignación manual de una puerta.
    Datos requeridos:
        - ID avión
        - Aerolínea
        - Origen
    Resultado:
        Asigna una puerta compatible si existe disponibilidad.
"""
def ui_assign_gate_manually():
    global current_bcn
    if not current_bcn:
        messagebox.showerror("Error", "Debe inicializar primero la estructura de terminales.")
        return
    a_id = entry_ac_id.get().strip().upper()
    a_comp = entry_ac_comp.get().strip().upper()
    a_orig = entry_ac_orig.get().strip().upper()

    if not a_id or not a_comp or not a_orig:
        messagebox.showerror("Aviso", "Por favor, complete todos los campos informativos del avión.")
        return

    is_schengen = messagebox.askyesno("Control V3", "¿El vuelo proviene de zona Schengen?")

    test_ac = LEBL.Aircraft(a_id, a_comp, a_orig, "00:00", is_schengen=is_schengen)
    if LEBL.AssignGate(current_bcn, test_ac) is None:
        log_info(f"V3: Aeronave {a_id} estacionada en pasarela correctamente.")
        entry_ac_id.delete(0, tk.END);
        entry_ac_comp.delete(0, tk.END);
        entry_ac_orig.delete(0, tk.END)
        ui_refresh_gates_grid()
        ui_draw_v3_chart()
    else:
        log_info(f"V3: Conflicto de asignación para {a_id}. Sin espacio compatible.")
        messagebox.showwarning("Aviso de Ocupación", "No quedan puertas compatibles libres.")

"""
    Actualiza la tabla visual de puertas de embarque.
    Funcionamiento:
        - Consulta el estado de ocupación desde LEBL.
        - Limpia el Listbox actual.
        - Inserta nuevamente todas las puertas.
    Formato mostrado:
        Puerta: <ID> | Estado: <Libre/Ocupada> | ID Vuelo
    Resultado:
        Refresco visual completo del panel de gates.
"""
def ui_refresh_gates_grid():
    listbox_gates.delete(0, tk.END)
    for g_info in LEBL.GateOccupancy(current_bcn):
        line = f" Puerta: {g_info[0]:<12} | Estado: {g_info[1]:<10}"
        if g_info[2]: line += f" | ID Vuelo: {g_info[2]}"
        listbox_gates.insert(tk.END, line)

"""
    Genera el gráfico de ocupación de puertas.
    Funcionamiento:
        - Obtiene el filtro ICAO opcional.
        - Limpia gráficos previos.
        - Genera gráfico Matplotlib.
        - Inserta el gráfico en Tkinter.
    Filtro:
        Si se especifica una aerolínea:
            - Se resaltan únicamente sus puertas ocupadas.
    Resultado:
        Visualización dinámica del estado operativo de terminales y puertas.
"""
def ui_draw_v3_chart():
    global current_bcn
    if not current_bcn: return

    airline_filter = entry_filter_airline.get().strip().upper()
    if airline_filter == "": airline_filter = None

    for w in plot_frame.winfo_children(): w.destroy()
    fig = LEBL.PlotOccupancyChart(current_bcn, target_frame=plot_frame, airline_filter=airline_filter)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

"""
    Exporta los vuelos en formato KML.
    Requisitos:
        - Estructura LEBL cargada.
        - Vuelos cargados.
        - Aeropuertos disponibles.
    Funcionamiento:
        - Genera archivo .kml
        - Compatible con Google Earth.
        - Permite abrir automáticamente el mapa.
    Resultado:
        Archivo KML exportado correctamente.
"""
def ui_export_kml_v3():
    global current_bcn, aircrafts, airports
    if not current_bcn or not aircrafts:
        messagebox.showerror("Error", "Se requiere la carga previa de Vuelos (V2) y Estructura (V3).")
        return

    fn = LEBL.ExportFlightsToKMLWithTerminal(aircrafts, current_bcn, airports)
    log_info(f"Exportación KML completada con éxito: {fn}.")

    quiere_abrir = messagebox.askyesno(
        "Cartografía Externa",
        f"Se ha compilado el mapa interactivo '{fn}' (T1=Azul, T2=Verde).\n\n¿Desea lanzar la aplicación de mapas del sistema operativo para visualizarlo ahora?"
    )

    if quiere_abrir:
        log_info("Iniciando visor cartográfico del sistema...")
        try:
            os.startfile(fn)
        except AttributeError:
            import subprocess
            subprocess.call(('open', fn))
        except Exception:
            messagebox.showerror("Error", "No se detectó un visor KML (como Google Earth Pro) instalado de forma nativa.")
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6

# =====================================================================
# DISEÑO ESTÉTICO DE LA INTERFAZ MAIN WINDOW
# =====================================================================
<<<<<<< HEAD
=======

"""
   Toda la sección siguiente construye visualmente la aplicación mediante Tkinter.
   Estructura principal:
       - Ventana principal
       - Panel izquierdo
       - Panel central
       - Panel derecho
       - Barra inferior de controles
   Estilo visual:
       Inspiración japonesa minimalista:
           - Colores suaves pastel
           - Tipografía limpia
           - Distribución zen y ordenada
"""

"""
   Configuración global de la aplicación.
   Características:
       - Resolución inicial
       - Color de fondo
       - Título del programa
"""
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
root = tk.Tk()
root.title("Airport Operations Suite — Centro de Control Unificado V4")
root.geometry("1300x800")
root.state('zoomed')
root.configure(bg="#fcfcfc")

font_title = ("Segoe UI", 10, "bold")
font_ui = ("Segoe UI", 9)
font_mono = ("Consolas", 9)

btn_base = {"font": ("Segoe UI", 9, "bold"), "width": 24, "pady": 2, "bd": 1, "relief": "groove"}
style_v1_v2 = {"bg": "#e9eef4", "fg": "#1f4e79", "activebackground": "#d9e2ec"}
style_v3_main = {"bg": "#e2f0d9", "fg": "#385723", "activebackground": "#d0e8c4"}
style_v4_core = {"bg": "#f2eefb", "fg": "#60497a", "activebackground": "#e4daf5"}
style_operator = {"bg": "#fcf3cf", "fg": "#7e5109", "activebackground": "#f9e79f"}

main_frame = tk.Frame(root, bg="#fcfcfc")
main_frame.pack(fill="both", expand=True, padx=12, pady=12)

<<<<<<< HEAD
# --- PANEL IZQUIERDO --- #
panel_izq = tk.Frame(main_frame, bg="#fcfcfc", width=340)
panel_izq.pack(side="left", fill="y", expand=False, padx=(0, 12))
panel_izq.pack_propagate(False)
=======
# --- PANEL IZQUIERDO: Listas V1 y V2 --- #
panel_izq = tk.Frame(main_frame, bg="#fcfcfc")
panel_izq.pack(side="left", fill="both", expand=True, padx=(0, 15))
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6

tk.Label(panel_izq, text="Aeropuertos Registrados (V1)", font=font_title, bg="#fcfcfc", fg="#444444").pack(anchor="w")
listbox = tk.Listbox(panel_izq, height=4, font=font_ui, bd=1, relief="solid")
listbox.pack(fill="x", pady=(2, 4))
listbox.bind("<<ListboxSelect>>", select_airport)

tk.Label(panel_izq, text="Plan de Vuelos Unificado (V4)", font=font_title, bg="#fcfcfc", fg="#1f4e79").pack(anchor="w")
listbox_vuelos = tk.Listbox(panel_izq, height=12, font=("Consolas", 10, "bold"), bd=1, relief="solid", bg="#fafafa",
                           selectbackground="#60497a")
listbox_vuelos.pack(fill="both", expand=True, pady=(2, 4))
listbox_vuelos.bind("<<ListboxSelect>>", select_flight)

f_apt = tk.LabelFrame(panel_izq, text=" Nodo Aeropuerto ", font=font_title, bg="#ffffff", bd=1, relief="solid",
                     fg="#555555", padx=4, pady=2)
f_apt.pack(fill="x", pady=2)
tk.Label(f_apt, text="ICAO:", font=font_ui, bg="#ffffff").grid(row=0, column=0)
entry_code = tk.Entry(f_apt, width=5, font=font_ui);
entry_code.grid(row=0, column=1, padx=1)
tk.Label(f_apt, text="Lat:", font=font_ui, bg="#ffffff").grid(row=0, column=2)
entry_lat = tk.Entry(f_apt, width=7, font=font_ui);
entry_lat.grid(row=0, column=3, padx=1)
tk.Label(f_apt, text="Lon:", font=font_ui, bg="#ffffff").grid(row=0, column=4)
entry_lon = tk.Entry(f_apt, width=7, font=font_ui);
entry_lon.grid(row=0, column=5, padx=1)

f_ac = tk.LabelFrame(panel_izq, text=" Ficha Operador / Rampa ", font=font_title, bg="#ffffff", bd=1, relief="solid",
                    fg="#555555", padx=4, pady=2)
f_ac.pack(fill="x", pady=2)
tk.Label(f_ac, text="ID:", font=font_ui, bg="#ffffff").grid(row=0, column=0)
entry_ac_id = tk.Entry(f_ac, width=8, font=font_ui);
entry_ac_id.grid(row=0, column=1, padx=1)
tk.Label(f_ac, text="Cía:", font=font_ui, bg="#ffffff").grid(row=0, column=2)
entry_ac_comp = tk.Entry(f_ac, width=5, font=font_ui);
entry_ac_comp.grid(row=0, column=3, padx=1)
tk.Label(f_ac, text="Ori:", font=font_ui, bg="#ffffff").grid(row=0, column=4)
entry_ac_orig = tk.Entry(f_ac, width=5, font=font_ui);
entry_ac_orig.grid(row=0, column=5, padx=1)

<<<<<<< HEAD
f_forced = tk.Frame(f_ac, bg="#ffffff", pady=2)
f_forced.grid(row=1, column=0, columnspan=6, sticky="w")
tk.Label(f_forced, text="Forzar Pta:", font=font_ui, bg="#ffffff", fg="#7e5109").pack(side="left")
entry_forced_gate = tk.Entry(f_forced, width=8, font=font_mono)
entry_forced_gate.pack(side="left", padx=2)
tk.Button(f_forced, text="Forzar", command=ui_operator_forced_assignment, font=("Segoe UI", 8, "bold"),
         **style_operator).pack(side="left")
=======
# --- PANEL CENTRAL: Gestión de Puertas V3 --- #
panel_centro = tk.Frame(main_frame, bg="#fcfcfc")
panel_centro.pack(side="left", fill="both", expand=True, padx=15)
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6

info_text = scrolledtext.ScrolledText(panel_izq, height=3, state='disabled', bg="#ffffff", font=font_mono, bd=1,
                                     relief="solid")
info_text.pack(fill="x", pady=(4, 0))

# --- PANEL CENTRAL DE VISUALIZACIÓN --- #
panel_display_grande = tk.Frame(main_frame, bg="#fcfcfc")
panel_display_grande.pack(side="right", fill="both", expand=True)

barra_selectora = tk.Frame(panel_display_grande, bg="#fcfcfc")
barra_selectora.pack(fill="x", pady=(0, 4))

<<<<<<< HEAD
btn_ver_mapa = tk.Button(barra_selectora, text="🗺️Mapa Puertas Real-Time", font=("Segoe UI", 9, "bold"),
                        command=lambda: cambiar_vista("mapa"), width=25, bg="#f2eefb", relief="groove")
btn_ver_mapa.pack(side="left", padx=2)
=======
# --- PANEL DERECHO: Visor de Gráficos e Historial --- #
panel_der = tk.Frame(main_frame, bg="#fcfcfc")
panel_der.pack(side="right", fill="both", expand=True, padx=(15, 0))
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6

btn_ver_graf_24h = tk.Button(barra_selectora, text="📈 Simulación Evolutiva 24h", font=("Segoe UI", 9, "bold"),
                            command=lambda: cambiar_vista("graf_24h"), width=23, bg="#eef0f2", relief="groove")
btn_ver_graf_24h.pack(side="left", padx=2)

btn_ver_graf_arr = tk.Button(barra_selectora,text="🛬 Landing Frequency",font=("Segoe UI", 9, "bold"),
                             command=lambda: cambiar_vista("graf_arr"),width=18,bg="#eef0f2",relief="groove")
btn_ver_graf_arr.pack(side="left", padx=2)

<<<<<<< HEAD
btn_ver_graf_air = tk.Button(barra_selectora, text="📊 Tráfico por Aerolínea", font=("Segoe UI", 9, "bold"),
                            command=lambda: cambiar_vista("graf_air"), width=19, bg="#eef0f2", relief="groove")
btn_ver_graf_air.pack(side="left", padx=2)

btn_ver_graf_tipo = tk.Button(barra_selectora, text="✈️ Flotas y Modelos", font=("Segoe UI", 9, "bold"),
                             command=lambda: cambiar_vista("graf_tipo"), width=16, bg="#eef0f2", relief="groove")
btn_ver_graf_tipo.pack(side="left", padx=2)

btn_ver_graf_sch = tk.Button(barra_selectora, text="🇪🇺 Cobertura Schengen", font=("Segoe UI", 9, "bold"),
                            command=lambda: cambiar_vista("graf_sch"), width=19, bg="#eef0f2", relief="groove")
btn_ver_graf_sch.pack(side="left", padx=2)

# Herramientas de Filtro y el "Extra" del selector de hora
filter_frame_tool = tk.Frame(barra_selectora, bg="#fcfcfc")
filter_frame_tool.pack(side="right")

# --- CONTROL DE SELECCIÓN DE HORA (FUNCIONALIDAD EXTRA ESPECTACULAR V4) ---
tk.Label(filter_frame_tool, text="🕒 Hora:", font=("Segoe UI", 9, "bold"), bg="#fcfcfc", fg="#60497a").pack(side="left",
                                                                                                          padx=(5, 2))
horas_dia = [f"{h:02d}:00" for h in range(24)]
combo_hora = ttk.Combobox(filter_frame_tool, values=horas_dia, width=6, state="readonly", font=font_mono)
combo_hora.set("00:00")
combo_hora.pack(side="left", padx=2)
combo_hora.bind("<<ComboboxSelected>>", ui_cambiar_hora_simulacion)

entry_filter_comp = tk.Entry(filter_frame_tool, width=4, font=font_mono, justify="center")
entry_filter_comp.pack(side="left", padx=(10, 2))
tk.Button(filter_frame_tool, text="🔍", command=ui_apply_filter, font=("Segoe UI", 8, "bold"), bg="#ffffff", bd=1).pack(
   side="left", padx=1)
tk.Button(filter_frame_tool, text="X", command=ui_clear_filter, font=("Segoe UI", 8, "bold"), bg="#fdf2f2",
         fg="#9c0006", bd=1).pack(side="left", padx=1)

contenedor_principal = tk.Frame(panel_display_grande, bg="#ffffff", bd=1, relief="solid")
contenedor_principal.pack(fill="both", expand=True, pady=2)

# --- BARRA INFERIOR DE ACCIONES --- #
=======
# --- CONTROL INFERIOR: BOTONERAS DE OPERACIONES --- #
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
bottom_bar = tk.Frame(root, bg="#fcfcfc")
bottom_bar.pack(fill="x", padx=12, pady=(0, 12))

g1 = tk.LabelFrame(bottom_bar, text=" BBDD Aeropuertos (V1) ", font=font_title, bg="#fcfcfc", fg="#666666", padx=3,
                  pady=2)
g1.pack(side="left", padx=2)
tk.Button(g1, text="Cargar Fichero Nodos", command=load_airports_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1, text="Insertar Aeropuerto Manual", command=add_airport_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1, text="Eliminar Aeropuerto Selec.", command=remove_airport_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1,text="💾 Exportar Schengen",command=save_schengen_airports_ui,**btn_base,**style_v1_v2).pack(pady=1)

g2 = tk.LabelFrame(bottom_bar, text=" Planes de Tráfico (V2/V4) ", font=font_title, bg="#fcfcfc", fg="#666666", padx=3,
                  pady=2)
g2.pack(side="left", padx=2)
tk.Button(g2, text="📂 Cargar Arrivals + Departures", command=load_v4_data_ui, **btn_base, **style_v4_core).pack(pady=1)
tk.Button(g2, text="🌍 Exportar Traza KML Google Earth", command=ui_export_kml_v4, **btn_base, **style_v4_core).pack(
   pady=1)

g3 = tk.LabelFrame(bottom_bar, text=" Control de Rampa y Asignaciones (V4) ", font=font_title, bg="#fcfcfc",
                  fg="#1f4e79", padx=3, pady=2)
g3.pack(side="left", padx=2)
tk.Button(g3, text="🔨 Construir Estructura LEBL", command=ui_build_airport_structure, **btn_base, **style_v3_main).pack(
<<<<<<< HEAD
   pady=1)
tk.Button(g3, text="⚡ Asignación Auto MASIVA", command=ui_assign_all_automatically, **btn_base, **style_v3_main).pack(
   pady=1)
tk.Button(g3, text="Asignar Puerta Individual", command=ui_assign_gate_manually, **btn_base, **style_v3_main).pack(
   pady=1)
tk.Button(g3, text="❌ Liberar / Vaciar Puerta", command=ui_free_gate_manual, **btn_base, **style_operator).pack(pady=1)

g4 = tk.LabelFrame(bottom_bar, text=" Control de Audio ", font=font_title, bg="#fcfcfc",
                 fg="#60497a", padx=3, pady=2)
g4.pack(side="left", padx=2)

volume_var = tk.IntVar(value=50)

btn_music = tk.Button(
  g4,
  text="🎵 Reproducir música",
  command=toggle_music,
  **btn_base,
  **style_v4_core
)
btn_music.pack(pady=1)

tk.Label(
  g4,
  text="Volumen",
  font=font_ui,
  bg="#fcfcfc",
  fg="#60497a"
).pack(pady=(2, 0))

scale_volume = tk.Scale(
  g4,
  from_=0,
  to=100,
  orient="horizontal",
  variable=volume_var,
  command=cambiar_volumen,
  length=180,
  bg="#fcfcfc",
  font=("Segoe UI", 8)
)
scale_volume.pack(pady=1)

#Lanzamiento inicial
cambiar_vista("mapa")
log_info("Consola Unificada Profesional V4 desplegada.")
root.protocol("WM_DELETE_WINDOW", cerrar_programa)
root.mainloop()
=======
    pady=2)
tk.Button(g3, text="📊 Mostrar Ocupación de Gates", command=lambda: [ui_refresh_gates_grid(), ui_draw_v3_chart()],
          **btn_base, **style_v3_main).pack(pady=2)
tk.Button(g3, text="🌍 Lanzar Cartografía en App (KML)", command=ui_export_kml_v3, **btn_base, **style_v3_alt).pack(
    pady=2)
log_info("Consola unificada inicializada de acuerdo al estándar de diseño minimalista.")
root.mainloop()
>>>>>>> 8ca15a8046b32c0f294278d29e336e17f94900e6
