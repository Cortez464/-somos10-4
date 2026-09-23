import os
import tkinter as tk
from tkinter import ttk, messagebox

from database.database import obtener_resumen_dashboard


# ==================================================
# RUTA DEL LOGO (independiente de dónde se ejecute el script)
# ==================================================
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGO = os.path.join(RUTA_BASE, "assets", "logo_somos104.png")
RUTA_MARCA_AGUA = os.path.join(RUTA_BASE, "assets", "logo_marca_agua.png")


# ==================================================
# PALETA DE COLORES Y ESTILOS UI
# ==================================================
COLOR_FONDO = "#F8FAFC"        # Slate muy claro
COLOR_TARJETA = "#FFFFFF"      # Blanco puro
COLOR_BORDE = "#E2E8F0"        # Gris tenue para bordes
COLOR_TEXTO_MAIN = "#0F172A"   # Azul oscuro / Slate
COLOR_TEXTO_MUTED = "#64748B"  # Gris medio para etiquetas

# Acentos métricos
COLOR_EXITO = "#059669"        # Verde ventas
COLOR_PELIGRO = "#E11D48"      # Rojo/Rosa gastos
COLOR_PRIMARY = "#2563EB"      # Azul ganancia/principal
COLOR_ALERTA = "#D97706"       # Ámbar pendientes


# ==================================================
# DASHBOARD
# ==================================================

def abrir_dashboard(ventana_principal):

    ventana_dashboard = tk.Toplevel(ventana_principal)
    ventana_dashboard.title("SOMOS 10-4 - Panel de Control & Dashboard")
    ventana_dashboard.geometry("980x680")
    ventana_dashboard.configure(bg=COLOR_FONDO)
    ventana_dashboard.resizable(True, True)
    ventana_dashboard.minsize(860, 560)

    # Ícono de la ventana (aparece en la barra de título / barra de tareas)
    try:
        icono_ventana = tk.PhotoImage(file=RUTA_LOGO)
        ventana_dashboard.iconphoto(False, icono_ventana)
        ventana_dashboard.icono_ventana = icono_ventana
    except Exception:
        pass

    # --------------------------------------------------
    # ENCABEZADO SUPERIOR
    # --------------------------------------------------

    marco_header = tk.Frame(ventana_dashboard, bg=COLOR_FONDO)
    marco_header.pack(fill="x", padx=30, pady=(25, 15))

    # Cargar el logo (PNG). Si el archivo no existe, la app sigue funcionando
    # sin el logo en lugar de fallar.
    try:
        imagen_logo = tk.PhotoImage(file=RUTA_LOGO)
        # Guardamos la referencia en la propia ventana para que Python no
        # la elimine de memoria (garbage collector) y el logo desaparezca.
        ventana_dashboard.imagen_logo = imagen_logo
    except Exception:
        imagen_logo = None

    if imagen_logo is not None:
        lbl_logo = tk.Label(marco_header, image=imagen_logo, bg=COLOR_FONDO)
        lbl_logo.pack(side="left", padx=(0, 15))

    frame_titulos = tk.Frame(marco_header, bg=COLOR_FONDO)
    frame_titulos.pack(side="left")

    titulo = tk.Label(
        frame_titulos,
        text="Dashboard Financiero",
        font=("Segoe UI", 22, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_MAIN
    )
    titulo.pack(anchor="w")

    subtitulo = tk.Label(
        frame_titulos,
        text="Resumen ejecutivo y métricas en tiempo real - SOMOS 10-4",
        font=("Segoe UI", 10),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_MUTED
    )
    subtitulo.pack(anchor="w")

    # --------------------------------------------------
    # FILTRO DE PERÍODO (Estilizado)
    # --------------------------------------------------

    marco_filtro = tk.Frame(marco_header, bg=COLOR_FONDO)
    marco_filtro.pack(side="right", anchor="e")

    tk.Label(
        marco_filtro,
        text="Período:",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TEXTO_MAIN
    ).pack(side="left", padx=(0, 8))

    periodo_seleccionado = tk.StringVar(value="Todo")

    selector_periodo = ttk.Combobox(
        marco_filtro,
        textvariable=periodo_seleccionado,
        values=["Todo", "Hoy", "Esta semana", "Este mes"],
        state="readonly",
        width=14,
        font=("Segoe UI", 10)
    )
    selector_periodo.pack(side="left")

    # --------------------------------------------------
    # CONTENEDOR PRINCIPAL DE TARJETAS (CANVAS + MARCA DE AGUA)
    # --------------------------------------------------
    # Usamos un Canvas (en vez de un Frame con .grid) para poder dibujar el
    # logo grande de fondo y que se siga viendo en los espacios entre
    # tarjetas, tal como en el diseño de referencia.

    marco_grid = tk.Canvas(ventana_dashboard, bg=COLOR_FONDO, highlightthickness=0)
    marco_grid.pack(padx=30, pady=10, fill="both", expand=True)

    # Cargar la marca de agua (si existe) como un único item de canvas que
    # se reposicionará cada vez que cambie el tamaño de la ventana.
    id_marca_agua = None
    try:
        imagen_marca_agua = tk.PhotoImage(file=RUTA_MARCA_AGUA)
        ventana_dashboard.imagen_marca_agua = imagen_marca_agua
        id_marca_agua = marco_grid.create_image(0, 0, image=imagen_marca_agua, anchor="n")
    except Exception:
        pass

    # --------------------------------------------------
    # CREADOR DE TARJETAS TIPO KPI
    # --------------------------------------------------

    def crear_tarjeta_kpi(parent, titulo, valor_inicial, icono, color_acento):
        # Contenedor exterior de la tarjeta (sin colocar todavía)
        tarjeta = tk.Frame(
            parent,
            bg=COLOR_TARJETA,
            highlightbackground=COLOR_BORDE,
            highlightthickness=1,
            bd=0
        )

        # Padding interno
        inner = tk.Frame(tarjeta, bg=COLOR_TARJETA, padx=16, pady=16)
        inner.pack(fill="both", expand=True)

        # Fila superior: Icono + Título
        top_row = tk.Frame(inner, bg=COLOR_TARJETA)
        top_row.pack(fill="x", anchor="w")

        lbl_icono = tk.Label(
            top_row,
            text=icono,
            font=("Segoe UI Emoji", 14),
            bg=COLOR_TARJETA,
            fg=color_acento
        )
        lbl_icono.pack(side="left", padx=(0, 6))

        lbl_titulo = tk.Label(
            top_row,
            text=titulo.upper(),
            font=("Segoe UI", 8, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO_MUTED
        )
        lbl_titulo.pack(side="left")

        # Fila inferior: Valor numérico/monetario
        etiqueta_valor = tk.Label(
            inner,
            text=valor_inicial,
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_TARJETA,
            fg=COLOR_TEXTO_MAIN
        )
        etiqueta_valor.pack(anchor="w", pady=(12, 0))

        return tarjeta, etiqueta_valor

    # --------------------------------------------------
    # MATRIZ DE TARJETAS KPI (4 Columnas x 2 Filas)
    # --------------------------------------------------

    definicion_tarjetas = [
        ("Ventas Totales", "$0.00", "💰", COLOR_EXITO, 0, 0),
        ("Gastos Generales", "$0.00", "💸", COLOR_PELIGRO, 0, 1),
        ("Costos de Pedidos", "$0.00", "🛠️", COLOR_ALERTA, 0, 2),
        ("Ganancia Estimada", "$0.00", "📈", COLOR_PRIMARY, 0, 3),
        ("Pedidos Totales", "0", "📋", COLOR_TEXTO_MAIN, 1, 0),
        ("Pedidos Pendientes", "0", "⏳", COLOR_ALERTA, 1, 1),
        ("Pedidos Entregados", "0", "✅", COLOR_EXITO, 1, 2),
        ("Por Cobrar", "$0.00", "💳", COLOR_PELIGRO, 1, 3),
    ]

    GAP = 14
    COLUMNAS, FILAS = 4, 2

    etiquetas_por_titulo = {}
    ids_tarjetas = {}

    for titulo_tarjeta, valor_inicial, icono, color, fila, columna in definicion_tarjetas:
        tarjeta, etiqueta_valor = crear_tarjeta_kpi(
            marco_grid, titulo_tarjeta, valor_inicial, icono, color
        )
        id_ventana = marco_grid.create_window(0, 0, window=tarjeta, anchor="nw")
        ids_tarjetas[titulo_tarjeta] = (id_ventana, fila, columna)
        etiquetas_por_titulo[titulo_tarjeta] = etiqueta_valor

    etiqueta_ventas = etiquetas_por_titulo["Ventas Totales"]
    etiqueta_gastos = etiquetas_por_titulo["Gastos Generales"]
    etiqueta_costos = etiquetas_por_titulo["Costos de Pedidos"]
    etiqueta_ganancia = etiquetas_por_titulo["Ganancia Estimada"]
    etiqueta_pedidos = etiquetas_por_titulo["Pedidos Totales"]
    etiqueta_pendientes = etiquetas_por_titulo["Pedidos Pendientes"]
    etiqueta_entregados = etiquetas_por_titulo["Pedidos Entregados"]
    etiqueta_cobro = etiquetas_por_titulo["Por Cobrar"]

    # --------------------------------------------------
    # REACOMODAR TARJETAS Y MARCA DE AGUA AL CAMBIAR DE TAMAÑO
    # --------------------------------------------------
    # Se ejecuta al abrir la ventana y cada vez que se redimensiona o
    # maximiza, para que las tarjetas y el logo de fondo se ajusten al
    # nuevo tamaño disponible en vez de quedar cortados o mal ubicados.

    def reajustar_layout(event=None):
        ancho = marco_grid.winfo_width()
        alto = marco_grid.winfo_height()
        if ancho < 10 or alto < 10:
            return

        if id_marca_agua is not None:
            marco_grid.coords(id_marca_agua, int(ancho * 0.68), int(alto * -0.06))

        ancho_tarjeta = (ancho - GAP * (COLUMNAS + 1)) / COLUMNAS
        alto_tarjeta = (alto - GAP * (FILAS + 1)) / FILAS

        for id_ventana, fila, columna in ids_tarjetas.values():
            x = GAP + columna * (ancho_tarjeta + GAP)
            y = GAP + fila * (alto_tarjeta + GAP)
            marco_grid.coords(id_ventana, x, y)
            marco_grid.itemconfig(id_ventana, width=ancho_tarjeta, height=alto_tarjeta)

    marco_grid.bind("<Configure>", reajustar_layout)

    # Cálculo inicial (además del que dispara <Configure> al mapearse)
    ventana_dashboard.update_idletasks()
    reajustar_layout()

    # --------------------------------------------------
    # ACTUALIZAR DATOS EN PANTALLA
    # --------------------------------------------------

    def actualizar_dashboard():
        try:
            periodo = periodo_seleccionado.get()
            datos = obtener_resumen_dashboard(periodo)

            # Ventas
            etiqueta_ventas.config(text=f"${datos['ventas']:,.2f}")
            
            # Gastos
            etiqueta_gastos.config(text=f"${datos['gastos']:,.2f}")
            
            # Costos
            etiqueta_costos.config(text=f"${datos['costos_pedidos']:,.2f}")

            # Ganancia
            ganancia_val = datos['ganancia']
            etiqueta_ganancia.config(
                text=f"${ganancia_val:,.2f}",
                fg=COLOR_EXITO if ganancia_val >= 0 else COLOR_PELIGRO
            )

            # Pedidos Registrados
            etiqueta_pedidos.config(text=str(datos['pedidos_registrados']))

            # Pedidos Pendientes
            etiqueta_pendientes.config(text=str(datos['pedidos_pendientes']))

            # Pedidos Entregados
            etiqueta_entregados.config(text=str(datos['pedidos_entregados']))

            # Dinero Pendiente de Cobro
            etiqueta_cobro.config(text=f"${datos['dinero_pendiente']:,.2f}")

        except Exception as error:
            messagebox.showerror(
                "Error de Carga",
                f"No se pudieron refrescar los datos del Dashboard.\n\nDetalle: {error}"
            )

    # Detectar cambio en el Combobox de período
    periodo_seleccionado.trace_add(
        "write",
        lambda *args: actualizar_dashboard()
    )

    # --------------------------------------------------
    # BARRA INFERIOR DE ACCIONES Y BOTONES
    # --------------------------------------------------

    marco_footer = tk.Frame(ventana_dashboard, bg=COLOR_FONDO)
    marco_footer.pack(fill="x", padx=30, pady=(15, 25))

    boton_actualizar = tk.Button(
        marco_footer,
        text="🔄  Actualizar Datos",
        font=("Segoe UI", 10, "bold"),
        bg=COLOR_PRIMARY,
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=actualizar_dashboard
    )
    boton_actualizar.pack(side="left")

    boton_cerrar = tk.Button(
        marco_footer,
        text="Cerrar",
        font=("Segoe UI", 10),
        bg="#E2E8F0",
        fg=COLOR_TEXTO_MAIN,
        activebackground="#CBD5E1",
        activeforeground=COLOR_TEXTO_MAIN,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=ventana_dashboard.destroy
    )
    boton_cerrar.pack(side="right")

    # Carga inicial al abrir
    actualizar_dashboard()