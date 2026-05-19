import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import os
import warnings
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Silenciamos warnings de optimización de gráficos para mantener limpia la consola
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# =====================================================================
# IMPORTACIONES DE MÓDULOS PROPIOS
# =====================================================================

from airport import Airport, LoadAirports, SetSchengen, PlotAirports
from aircraft import LoadArrivals, PlotArrivals, PlotAirlines, PlotFlightsType
import LEBL  # Contiene BarcelonaAP, AssignGate, GateOccupancy, PlotOccupancyChart, ExportFlightsToKMLWithTerminal

# Variables globales compartidas
airports = []
aircrafts = []
current_bcn = None

# =====================================================================
# LÓGICA DE CONTROL DE LA INTERFAZ
# =====================================================================

def log_info(message):
    info_text.config(state='normal')
    info_text.insert(tk.END, f"> {message}\n")
    info_text.config(state='disabled')
    info_text.see(tk.END)

def update_list():
    listbox.delete(0, tk.END)
    for a in airports:
        listbox.insert(tk.END,
                       f" {a.icao_code}  |  {round(a.latitude, 4)}, {round(a.longitude, 4)}  |  {'Schengen' if a.schengen else 'No Schengen'}")

def update_flights_list():
    listbox_vuelos.delete(0, tk.END)
    for f in aircrafts:
        listbox_vuelos.insert(tk.END,
                              f" {f.aircraft_id}  |  {f.origin_airport}  |  {f.landing_time}  |  {f.airline_company}")

def clear_entries():
    entry_code.delete(0, tk.END)
    entry_lat.delete(0, tk.END)
    entry_lon.delete(0, tk.END)

def select_airport(event):
    selected = listbox.curselection()
    if not selected: return
    a = airports[selected[0]]
    entry_code.delete(0, tk.END);
    entry_code.insert(0, a.icao_code)
    entry_lat.delete(0, tk.END);
    entry_lat.insert(0, a.latitude)
    entry_lon.delete(0, tk.END);
    entry_lon.insert(0, a.longitude)

# --- Acciones V1 y V2 --- #
def load_airports_ui():
    filename = filedialog.askopenfilename()
    if filename:
        global airports
        airports = LoadAirports(filename)
        for a in airports: SetSchengen(a)
        update_list()
        log_info(f"Cargados {len(airports)} aeropuertos en el sistema.")

def add_airport_ui():
    code, lat, lon = entry_code.get().upper(), entry_lat.get(), entry_lon.get()
    if not code or not lat or not lon:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    try:
        a = Airport(code, float(lat), float(lon))
        SetSchengen(a)
        airports.append(a)
        update_list();
        clear_entries()
        log_info(f"Aeropuerto {code} incorporado de forma manual.")
    except ValueError:
        messagebox.showerror("Error", "Latitud y Longitud deben ser valores numéricos.")

def remove_airport_ui():
    selected = listbox.curselection()
    if not selected: return
    del airports[selected[0]]
    update_list()
    log_info("Aeropuerto seleccionado eliminado de los registros.")

def load_arrivals_ui():
    filename = filedialog.askopenfilename()
    if filename:
        global aircrafts
        aircrafts = LoadArrivals(filename)
        if aircrafts:
            log_info(f"Cargados {len(aircrafts)} registros de vuelos entrantes.")
            update_flights_list()

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
def ui_build_airport_structure():
    global current_bcn
    filename = filedialog.askopenfilename(title="Seleccionar Estructura (Terminals.txt)")
    if filename:
        current_bcn = LEBL.LoadAirportStructure(filename)
        if current_bcn:
            log_info(f"Estructura operativa de {current_bcn.code} desplegada con éxito.")
            ui_refresh_gates_grid()
            ui_draw_v3_chart()

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

def ui_refresh_gates_grid():
    listbox_gates.delete(0, tk.END)
    for g_info in LEBL.GateOccupancy(current_bcn):
        line = f" Puerta: {g_info[0]:<12} | Estado: {g_info[1]:<10}"
        if g_info[2]: line += f" | ID Vuelo: {g_info[2]}"
        listbox_gates.insert(tk.END, line)

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
            messagebox.showerror("Error",
                                 "No se detectó un visor KML (como Google Earth Pro) instalado de forma nativa.")

# =====================================================================
# DISEÑO ESTÉTICO DE LA INTERFAZ (ESTILO JAPONÉS MINIMALISTA)
# =====================================================================

root = tk.Tk()
root.title("Airport Operations Suite — Minimalist Edition")
root.geometry("1300x820")
root.configure(bg="#fcfcfc")  # Gris piedra zen muy suave

# Fuentes tipográficas limpias
font_title = ("Segoe UI", 10, "bold")
font_ui = ("Segoe UI", 9)
font_mono = ("Consolas", 9)

# Estilos de botones Pastel Japoneses
btn_base = {"font": ("Segoe UI", 9, "bold"), "width": 24, "pady": 4, "bd": 1, "relief": "groove"}
style_v1_v2 = {"bg": "#e9eef4", "fg": "#1f4e79", "activebackground": "#d9e2ec"}  # Azul Neblina
style_v3_main = {"bg": "#e2f0d9", "fg": "#385723", "activebackground": "#d0e8c4"}  # Verde Matcha
style_v3_alt = {"bg": "#f2eefb", "fg": "#60497a", "activebackground": "#e4daf5"}  # Lavanda Suave
style_filter = {"bg": "#fce4d6", "fg": "#c65911", "activebackground": "#f8cfb6"}  # Salmón Pálido

main_frame = tk.Frame(root, bg="#fcfcfc")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# --- PANEL IZQUIERDO: Listas V1 y V2 ---
panel_izq = tk.Frame(main_frame, bg="#fcfcfc")
panel_izq.pack(side="left", fill="both", expand=True, padx=(0, 15))

tk.Label(panel_izq, text="Aeropuertos Registrados (V1)", font=font_title, bg="#fcfcfc", fg="#444444").pack(anchor="w")
listbox = tk.Listbox(panel_izq, height=7, font=font_ui, bd=1, highlightbackground="#eef0f2", relief="solid")
listbox.pack(fill="x", pady=(3, 10))
listbox.bind("<<ListboxSelect>>", select_airport)

tk.Label(panel_izq, text="Vuelos en Proceso de Llegada (V2)", font=font_title, bg="#fcfcfc", fg="#444444").pack(
    anchor="w")
listbox_vuelos = tk.Listbox(panel_izq, height=7, font=font_ui, bd=1, highlightbackground="#eef0f2", relief="solid")
listbox_vuelos.pack(fill="x", pady=(3, 10))

# Formulario Manual V1
f_apt = tk.LabelFrame(panel_izq, text=" Registro Manual Aeropuerto ", font=font_title, bg="#ffffff", bd=1,
                      relief="solid", fg="#555555")
f_apt.pack(fill="x", pady=5)
f_apt.config(padx=10, pady=8)

tk.Label(f_apt, text="ICAO:", font=font_ui, bg="#ffffff").grid(row=0, column=0, padx=2)
entry_code = tk.Entry(f_apt, width=6, font=font_ui);
entry_code.grid(row=0, column=1, padx=5)
tk.Label(f_apt, text="Lat:", font=font_ui, bg="#ffffff").grid(row=0, column=2, padx=2)
entry_lat = tk.Entry(f_apt, width=8, font=font_ui);
entry_lat.grid(row=0, column=3, padx=5)
tk.Label(f_apt, text="Lon:", font=font_ui, bg="#ffffff").grid(row=0, column=4, padx=2)
entry_lon = tk.Entry(f_apt, width=8, font=font_ui);
entry_lon.grid(row=0, column=5, padx=5)

# --- PANEL CENTRAL: Gestión de Puertas V3 ---
panel_centro = tk.Frame(main_frame, bg="#fcfcfc")
panel_centro.pack(side="left", fill="both", expand=True, padx=15)

tk.Label(panel_centro, text="Control de Pasarelas y Puertas (V3)", font=font_title, bg="#fcfcfc", fg="#2c3e50").pack(
    anchor="w")
listbox_gates = tk.Listbox(panel_centro, height=15, font=font_mono, bd=1, highlightbackground="#eef0f2", relief="solid")
listbox_gates.pack(fill="both", expand=True, pady=(3, 10))

# Entrada de Avión V3
f_ac = tk.LabelFrame(panel_centro, text=" Simular Asignación Inmediata ", font=font_title, bg="#ffffff", bd=1,
                     relief="solid", fg="#555555")
f_ac.pack(fill="x", pady=4)
f_ac.config(padx=8, pady=6)
tk.Label(f_ac, text="ID:", font=font_ui, bg="#ffffff").grid(row=0, column=0, padx=2)
entry_ac_id = tk.Entry(f_ac, width=7, font=font_ui);
entry_ac_id.grid(row=0, column=1, padx=4)
tk.Label(f_ac, text="Cía:", font=font_ui, bg="#ffffff").grid(row=0, column=2, padx=2)
entry_ac_comp = tk.Entry(f_ac, width=6, font=font_ui);
entry_ac_comp.grid(row=0, column=3, padx=4)
tk.Label(f_ac, text="Ori:", font=font_ui, bg="#ffffff").grid(row=0, column=4, padx=2)
entry_ac_orig = tk.Entry(f_ac, width=6, font=font_ui);
entry_ac_orig.grid(row=0, column=5, padx=4)
tk.Button(f_ac, text="Asignar", command=ui_assign_gate_manually, font=("Segoe UI", 8, "bold"), bg="#e9eef4",
          fg="#1f4e79", bd=1, relief="groove").grid(row=0, column=6, padx=4)

# Panel de Filtro de Aerolínea V3
f_filter = tk.LabelFrame(panel_centro, text=" Filtro de Compañía para Gráfico ", font=font_title, bg="#ffffff", bd=1,
                         relief="solid", fg="#555555")
f_filter.pack(fill="x", pady=4)
f_filter.config(padx=8, pady=6)
tk.Label(f_filter, text="Código (ICAO):", font=font_ui, bg="#ffffff").pack(side="left", padx=2)
entry_filter_airline = tk.Entry(f_filter, width=8, font=font_ui)
entry_filter_airline.pack(side="left", padx=5)
btn_apply_filter = tk.Button(f_filter, text="Filtrar Gráfico", command=ui_draw_v3_chart, font=("Segoe UI", 8, "bold"),
                             **style_filter)
btn_apply_filter.pack(side="left", padx=5)

# --- PANEL DERECHO: Visor de Gráficos e Historial ---
panel_der = tk.Frame(main_frame, bg="#fcfcfc")
panel_der.pack(side="right", fill="both", expand=True, padx=(15, 0))

info_text = scrolledtext.ScrolledText(panel_der, height=4, state='disabled', bg="#ffffff", font=font_mono, bd=1,
                                      highlightbackground="#eef0f2", relief="solid")
info_text.pack(fill="x", pady=(0, 15))

plot_frame = tk.LabelFrame(panel_der, text=" Cuadro de Mapeo Visual (Matplotlib) ", font=font_title, bg="#ffffff", bd=1,
                           relief="solid", fg="#555555", height=380)
plot_frame.pack(fill="both", expand=True)
plot_frame.pack_propagate(False)

# --- CONTROL INFERIOR: BOTONERAS DE OPERACIONES ---
bottom_bar = tk.Frame(root, bg="#fcfcfc")
bottom_bar.pack(fill="x", padx=20, pady=(0, 20))

g1 = tk.LabelFrame(bottom_bar, text=" Aeropuertos (V1) ", font=font_title, bg="#fcfcfc", fg="#666666", padx=5, pady=5)
g1.pack(side="left", padx=4)
tk.Button(g1, text="Cargar Fichero Aeropuertos", command=load_airports_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1, text="Insertar Nodo Manual", command=add_airport_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1, text="Eliminar Nodo Activo", command=remove_airport_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g1, text="Gráfico Cobertura Schengen", command=lambda: mostrar_grafico_v2(PlotAirports, airports), **btn_base,
          **style_v1_v2).pack(pady=1)

g2 = tk.LabelFrame(bottom_bar, text=" Tráfico Aéreo (V2) ", font=font_title, bg="#fcfcfc", fg="#666666", padx=5, pady=5)
g2.pack(side="left", padx=4)
tk.Button(g2, text="Cargar Fichero Vuelos", command=load_arrivals_ui, **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g2, text="Gráfico Distribución Horaria", command=lambda: mostrar_grafico_v2(PlotArrivals, aircrafts),
          **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g2, text="Gráfico Volumen Aerolíneas", command=lambda: mostrar_grafico_v2(PlotAirlines, aircrafts),
          **btn_base, **style_v1_v2).pack(pady=1)
tk.Button(g2, text="Gráfico Tipología de Vuelo", command=lambda: mostrar_grafico_v2(PlotFlightsType, aircrafts),
          **btn_base, **style_v1_v2).pack(pady=1)

g3 = tk.LabelFrame(bottom_bar, text=" Módulo de Gestión de Gates (V3) ", font=font_title, bg="#fcfcfc", fg="#1f4e79",
                   padx=5, pady=5)
g3 = tk.LabelFrame(bottom_bar, text=" Módulo de Gestión de Gates (V3) ", font=font_title, bg="#fcfcfc", fg="#1f4e79",
                   padx=5, pady=5)
g3.pack(side="left", padx=4)
tk.Button(g3, text="🔨 Construir Estructura LEBL", command=ui_build_airport_structure, **btn_base, **style_v3_main).pack(
    pady=2)
tk.Button(g3, text="📊 Mostrar Ocupación de Gates", command=lambda: [ui_refresh_gates_grid(), ui_draw_v3_chart()],
          **btn_base, **style_v3_main).pack(pady=2)
tk.Button(g3, text="🌍 Lanzar Cartografía en App (KML)", command=ui_export_kml_v3, **btn_base, **style_v3_alt).pack(
    pady=2)
log_info("Consola unificada inicializada de acuerdo al estándar de diseño minimalista.")
root.mainloop()