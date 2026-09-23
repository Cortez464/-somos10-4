import tkinter as tk
from tkinter import ttk, messagebox

# Importaciones de la base de datos y vistas del sistema
from database.database import crear_base_datos, respaldar_base_datos
from views.dashboard import abrir_dashboard
from views.clientes import abrir_clientes
from views.pedidos import abrir_pedidos
from views.listado_pedidos import abrir_pedidos_listado
from views.gastos import abrir_gastos
from views.reportes import abrir_reportes


def centrar_ventana(ventana, ancho=920, alto=620):
    """
    Calcula las coordenadas para centrar la ventana en la pantalla.
    """
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


def iniciar_aplicacion():
    # --------------------------------------------------
    # INICIALIZAR BASE DE DATOS
    # --------------------------------------------------
    try:
        crear_base_datos()
        respaldar_base_datos()
    except Exception as error:
        messagebox.showerror(
            "Error al iniciar",
            f"No se pudo conectar o crear la base de datos:\n\n{error}"
        )
        return

    # --------------------------------------------------
    # VENTANA PRINCIPAL
    # --------------------------------------------------
    ventana = tk.Tk()
    ventana.title("SOMOS 10-4 - Gestión de Lavandería")
    centrar_ventana(ventana, 920, 620)
    ventana.resizable(True, True)
    ventana.configure(bg="#F4F6F9")

    # --------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------
    marco_cabecera = tk.Frame(ventana, bg="#1E293B", pady=22)
    marco_cabecera.pack(fill="x")

    titulo = tk.Label(
        marco_cabecera,
        text="SOMOS 10-4",
        font=("Arial", 28, "bold"),
        fg="#FFFFFF",
        bg="#1E293B"
    )
    titulo.pack()

    subtitulo = tk.Label(
        marco_cabecera,
        text="Sistema de Gestión y Control de Lavandería",
        font=("Arial", 12),
        fg="#94A3B8",
        bg="#1E293B"
    )
    subtitulo.pack(pady=(2, 0))

    # --------------------------------------------------
    # CONTENEDOR PRINCIPAL
    # --------------------------------------------------
    contenedor = tk.Frame(ventana, bg="#F4F6F9", padx=30, pady=20)
    contenedor.pack(fill="both", expand=True)

    marco_menu = tk.LabelFrame(
        contenedor,
        text="  Menú Principal  ",
        font=("Arial", 12, "bold"),
        fg="#334155",
        bg="#FFFFFF",
        padx=20,
        pady=20,
        bd=1,
        relief="solid"
    )
    marco_menu.pack(fill="both", expand=True)

    # Distribuir las columnas y filas uniformemente
    marco_menu.columnconfigure(0, weight=1)
    marco_menu.columnconfigure(1, weight=1)
    marco_menu.rowconfigure(0, weight=1)
    marco_menu.rowconfigure(1, weight=1)
    marco_menu.rowconfigure(2, weight=1)

    # Estilo base para los botones del menú
    estilo_boton = {
        "font": ("Arial", 11, "bold"),
        "bd": 0,
        "cursor": "hand2",
        "activeforeground": "#FFFFFF",
        "relief": "flat"
    }

    # --------------------------------------------------
    # BOTONES DEL MENÚ
    # --------------------------------------------------

    # 1. Dashboard
    btn_dashboard = tk.Button(
        marco_menu,
        text="📊   Dashboard",
        bg="#2563EB",
        fg="#FFFFFF",
        activebackground="#1D4ED8",
        command=lambda: abrir_dashboard(ventana),
        **estilo_boton
    )
    btn_dashboard.grid(row=0, column=0, padx=12, pady=10, sticky="nsew")

    # 2. Clientes
    btn_clientes = tk.Button(
        marco_menu,
        text="👥   Clientes",
        bg="#0D9488",
        fg="#FFFFFF",
        activebackground="#0F766E",
        command=lambda: abrir_clientes(ventana),
        **estilo_boton
    )
    btn_clientes.grid(row=0, column=1, padx=12, pady=10, sticky="nsew")

    # 3. Nuevo Pedido
    btn_pedidos = tk.Button(
        marco_menu,
        text="🧺   Nuevo Pedido",
        bg="#16A34A",
        fg="#FFFFFF",
        activebackground="#15803D",
        command=lambda: abrir_pedidos(ventana),
        **estilo_boton
    )
    btn_pedidos.grid(row=1, column=0, padx=12, pady=10, sticky="nsew")

    # 4. Listado de Pedidos
    btn_listado = tk.Button(
        marco_menu,
        text="📋   Listado de Pedidos",
        bg="#4F46E5",
        fg="#FFFFFF",
        activebackground="#4338CA",
        command=lambda: abrir_pedidos_listado(ventana),
        **estilo_boton
    )
    btn_listado.grid(row=1, column=1, padx=12, pady=10, sticky="nsew")

    # 5. Gastos
    btn_gastos = tk.Button(
        marco_menu,
        text="💸   Control de Gastos",
        bg="#EA580C",
        fg="#FFFFFF",
        activebackground="#C2410C",
        command=lambda: abrir_gastos(ventana),
        **estilo_boton
    )
    btn_gastos.grid(row=2, column=0, padx=12, pady=10, sticky="nsew")

    # 6. Reportes
    btn_reportes = tk.Button(
        marco_menu,
        text="📈   Reportes",
        bg="#7C3AED",
        fg="#FFFFFF",
        activebackground="#6D28D9",
        command=lambda: abrir_reportes(ventana),
        **estilo_boton
    )
    btn_reportes.grid(row=2, column=1, padx=12, pady=10, sticky="nsew")

    # --------------------------------------------------
    # BARRA DE ESTADO (FOOTER)
    # --------------------------------------------------
    barra_estado = tk.Frame(ventana, bg="#E2E8F0", height=28, padx=15)
    barra_estado.pack(fill="x", side="bottom")

    lbl_estado = tk.Label(
        barra_estado,
        text="● Base de datos conectada correctamente",
        font=("Arial", 9),
        fg="#16A34A",
        bg="#E2E8F0"
    )
    lbl_estado.pack(side="left")

    lbl_version = tk.Label(
        barra_estado,
        text="v1.0.0",
        font=("Arial", 9, "bold"),
        fg="#64748B",
        bg="#E2E8F0"
    )
    lbl_version.pack(side="right")

    # --------------------------------------------------
    # BUCLE PRINCIPAL
    # --------------------------------------------------
    ventana.mainloop()


# --------------------------------------------------
# EJECUCIÓN DIRECTA
# --------------------------------------------------
if __name__ == "__main__":
    iniciar_aplicacion()