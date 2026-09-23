import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime

from database.database import (
    obtener_resumen_dashboard,
    obtener_reporte_detallado
)


def abrir_reportes(ventana_principal):
    """
    Abre la ventana principal del Módulo de Reportes Financieros y Operativos.
    """
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("SOMOS 10-4 - Módulo de Reportes")
    ventana.geometry("980x680")
    ventana.resizable(True, True)
    ventana.configure(bg="#F4F6F9")

    # --------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------
    marco_cabecera = tk.Frame(ventana, bg="#1E293B", pady=15, padx=20)
    marco_cabecera.pack(fill="x")

    lbl_titulo = tk.Label(
        marco_cabecera,
        text="📈 Módulo de Reportes y Estadísticas",
        font=("Arial", 20, "bold"),
        fg="#FFFFFF",
        bg="#1E293B"
    )
    lbl_titulo.pack(anchor="w")

    lbl_subtitulo = tk.Label(
        marco_cabecera,
        text="Análisis financiero, control de ingresos, costos y rendimiento del negocio",
        font=("Arial", 10),
        fg="#94A3B8",
        bg="#1E293B"
    )
    lbl_subtitulo.pack(anchor="w")

    # --------------------------------------------------
    # FILTRO DE PERÍODO Y ACCIONES
    # --------------------------------------------------
    marco_controles = tk.Frame(ventana, bg="#F4F6F9", padx=20, pady=12)
    marco_controles.pack(fill="x")

    tk.Label(
        marco_controles,
        text="Período del Reporte:",
        font=("Arial", 11, "bold"),
        bg="#F4F6F9",
        fg="#334155"
    ).pack(side="left", padx=(0, 10))

    var_periodo = tk.StringVar(value="Todo")
    selector_periodo = ttk.Combobox(
        marco_controles,
        textvariable=var_periodo,
        values=["Todo", "Hoy", "Esta semana", "Este mes"],
        state="readonly",
        width=15,
        font=("Arial", 10)
    )
    selector_periodo.pack(side="left", padx=(0, 15))

    # --------------------------------------------------
    # CONTENEDOR PRINCIPAL CON PESTAÑAS
    # --------------------------------------------------
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    # Pestaña 1: Resumen Financiero
    tab_resumen = tk.Frame(notebook, bg="#FFFFFF", padx=15, pady=15)
    notebook.add(tab_resumen, text="📊 Resumen Financiero")

    # Pestaña 2: Rendimiento y Clientes
    tab_rendimiento = tk.Frame(notebook, bg="#FFFFFF", padx=15, pady=15)
    notebook.add(tab_rendimiento, text="👥 Clientes y Servicios")

    # Pestaña 3: Desglose de Gastos
    tab_gastos = tk.Frame(notebook, bg="#FFFFFF", padx=15, pady=15)
    notebook.add(tab_gastos, text="💸 Categorías de Gastos")

    # ==================================================
    # PESTAÑA 1: TARJETAS FINANCIERAS
    # ==================================================
    marco_tarjetas = tk.Frame(tab_resumen, bg="#FFFFFF")
    marco_tarjetas.pack(fill="x", pady=10)

    def crear_tarjeta_reporte(parent, titulo, color_borde):
        f = tk.Frame(parent, bg="#F8FAFC", bd=1, relief="solid", highlightbackground=color_borde, highlightthickness=2)
        tk.Label(f, text=titulo, font=("Arial", 10, "bold"), fg="#64748B", bg="#F8FAFC").pack(pady=(10, 2))
        lbl_val = tk.Label(f, text="$0.00", font=("Arial", 18, "bold"), fg="#0F172A", bg="#F8FAFC")
        lbl_val.pack(pady=(0, 10))
        return f, lbl_val

    f1, lbl_r_ventas = crear_tarjeta_reporte(marco_tarjetas, "Ventas Totales", "#2563EB")
    f1.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")

    f2, lbl_r_gastos = crear_tarjeta_reporte(marco_tarjetas, "Gastos Generales", "#EA580C")
    f2.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")

    f3, lbl_r_costos = crear_tarjeta_reporte(marco_tarjetas, "Costos Directos Pedidos", "#D97706")
    f3.grid(row=0, column=2, padx=8, pady=5, sticky="nsew")

    f4, lbl_r_ganancia = crear_tarjeta_reporte(marco_tarjetas, "Ganancia Neta", "#16A34A")
    f4.grid(row=0, column=3, padx=8, pady=5, sticky="nsew")

    for i in range(4):
        marco_tarjetas.columnconfigure(i, weight=1)

    # Cuadro informativo de balances de pedidos
    marco_info_pedidos = tk.LabelFrame(
        tab_resumen, text=" Estado Operativo de Pedidos ",
        font=("Arial", 11, "bold"), fg="#334155", bg="#FFFFFF", padx=15, pady=15
    )
    marco_info_pedidos.pack(fill="both", expand=True, pady=15)

    lbl_pedidos_totales = tk.Label(marco_info_pedidos, text="Total Pedidos Registrados: 0", font=("Arial", 11), bg="#FFFFFF")
    lbl_pedidos_totales.pack(anchor="w", pady=4)

    lbl_pedidos_pend = tk.Label(marco_info_pedidos, text="Pedidos en Proceso / Pendientes: 0", font=("Arial", 11), bg="#FFFFFF")
    lbl_pedidos_pend.pack(anchor="w", pady=4)

    lbl_pedidos_ent = tk.Label(marco_info_pedidos, text="Pedidos Entregados: 0", font=("Arial", 11), bg="#FFFFFF")
    lbl_pedidos_ent.pack(anchor="w", pady=4)

    lbl_dinero_pendiente = tk.Label(
        marco_info_pedidos, text="Dinero Pendiente de Cobro: $0.00",
        font=("Arial", 11, "bold"), fg="#DC2626", bg="#FFFFFF"
    )
    lbl_dinero_pendiente.pack(anchor="w", pady=4)

    # ==================================================
    # PESTAÑA 2: CLIENTES Y PRENDAS
    # ==================================================
    marco_p2_izq = tk.LabelFrame(tab_rendimiento, text=" Top 5 Clientes ", font=("Arial", 10, "bold"), bg="#FFFFFF")
    marco_p2_izq.pack(side="left", fill="both", expand=True, padx=(0, 5))

    tabla_clientes = ttk.Treeview(marco_p2_izq, columns=("nombre", "pedidos", "total"), show="headings", height=10)
    tabla_clientes.heading("nombre", text="Cliente")
    tabla_clientes.heading("pedidos", text="Pedidos")
    tabla_clientes.heading("total", text="Total Facturado")
    tabla_clientes.column("nombre", width=140)
    tabla_clientes.column("pedidos", width=70, anchor="center")
    tabla_clientes.column("total", width=100, anchor="e")
    tabla_clientes.pack(fill="both", expand=True, padx=5, pady=5)

    marco_p2_der = tk.LabelFrame(tab_rendimiento, text=" Top 5 Servicios / Prendas ", font=("Arial", 10, "bold"), bg="#FFFFFF")
    marco_p2_der.pack(side="right", fill="both", expand=True, padx=(5, 0))

    tabla_prendas = ttk.Treeview(marco_p2_der, columns=("prenda", "cantidad", "monto"), show="headings", height=10)
    tabla_prendas.heading("prenda", text="Prenda / Servicio")
    tabla_prendas.heading("cantidad", text="Cant.")
    tabla_prendas.heading("monto", text="Subtotal")
    tabla_prendas.column("prenda", width=140)
    tabla_prendas.column("cantidad", width=60, anchor="center")
    tabla_prendas.column("monto", width=100, anchor="e")
    tabla_prendas.pack(fill="both", expand=True, padx=5, pady=5)

    # ==================================================
    # PESTAÑA 3: GASTOS POR CATEGORÍA
    # ==================================================
    tabla_gastos_cat = ttk.Treeview(tab_gastos, columns=("categoria", "monto"), show="headings", height=12)
    tabla_gastos_cat.heading("categoria", text="Categoría de Gasto")
    tabla_gastos_cat.heading("monto", text="Monto Acumulado")
    tabla_gastos_cat.column("categoria", width=250)
    tabla_gastos_cat.column("monto", width=150, anchor="e")
    tabla_gastos_cat.pack(fill="both", expand=True, padx=10, pady=10)

    # --------------------------------------------------
    # LÓGICA DE ACTUALIZACIÓN
    # --------------------------------------------------
    def actualizar_reportes():
        periodo = var_periodo.get()

        try:
            # 1. Cargar datos financieros generales
            datos = obtener_resumen_dashboard(periodo)

            lbl_r_ventas.config(text=f"${datos['ventas']:.2f}")
            lbl_r_gastos.config(text=f"${datos['gastos']:.2f}")
            lbl_r_costos.config(text=f"${datos['costos_pedidos']:.2f}")

            # Estilo dinámico para ganancia
            ganancia = datos['ganancia']
            lbl_r_ganancia.config(
                text=f"${ganancia:.2f}",
                fg="#16A34A" if ganancia >= 0 else "#DC2626"
            )

            lbl_pedidos_totales.config(text=f"Total Pedidos Registrados: {datos['pedidos_registrados']}")
            lbl_pedidos_pend.config(text=f"Pedidos en Proceso / Pendientes: {datos['pedidos_pendientes']}")
            lbl_pedidos_ent.config(text=f"Pedidos Entregados: {datos['pedidos_entregados']}")
            lbl_dinero_pendiente.config(text=f"Dinero Pendiente de Cobro: ${datos['dinero_pendiente']:.2f}")

            # 2. Cargar tablas detalladas
            detalles = obtener_reporte_detallado(periodo)

            # Limpiar tablas
            for item in tabla_clientes.get_children():
                tabla_clientes.delete(item)
            for item in tabla_prendas.get_children():
                tabla_prendas.delete(item)
            for item in tabla_gastos_cat.get_children():
                tabla_gastos_cat.delete(item)

            # Insertar Top Clientes
            for cli in detalles["top_clientes"]:
                tabla_clientes.insert("", "end", values=(cli[0], cli[1], f"${cli[2]:.2f}"))

            # Insertar Top Prendas
            for pre in detalles["top_prendas"]:
                tabla_prendas.insert("", "end", values=(pre[0], pre[1], f"${pre[2]:.2f}"))

            # Insertar Gastos por categoría
            for gas in detalles["gastos_categoria"]:
                tabla_gastos_cat.insert("", "end", values=(gas[0], f"${gas[1]:.2f}"))

        except Exception as err:
            messagebox.showerror("Error de Carga", f"No se pudieron generar los reportes:\n{err}")

    # Evento de cambio en el selector
    selector_periodo.bind("<<ComboboxSelected>>", lambda e: actualizar_reportes())

    # --------------------------------------------------
    # EXPORTAR REPORTE A TEXTO
    # --------------------------------------------------
    def exportar_reporte():
        periodo = var_periodo.get()
        datos = obtener_resumen_dashboard(periodo)
        detalles = obtener_reporte_detallado(periodo)

        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        contenido = f"""==================================================
           SOMOS 10-4 - REPORTE DE GESTIÓN
==================================================
Fecha de generación: {fecha_actual}
Período analizado  : {periodo}

--------------------------------------------------
1. RESUMEN FINANCIERO
--------------------------------------------------
Ventas Totales           : ${datos['ventas']:.2f}
Gastos Generales         : ${datos['gastos']:.2f}
Costos Directos Pedidos  : ${datos['costos_pedidos']:.2f}
--------------------------------------------------
GANANCIA NETA ESTIMADA   : ${datos['ganancia']:.2f}
--------------------------------------------------

--------------------------------------------------
2. BALANCE OPERATIVO
--------------------------------------------------
Total Pedidos            : {datos['pedidos_registrados']}
Pedidos Pendientes       : {datos['pedidos_pendientes']}
Pedidos Entregados       : {datos['pedidos_entregados']}
Dinero Pendiente Cobro   : ${datos['dinero_pendiente']:.2f}

--------------------------------------------------
3. TOP CLIENTES
--------------------------------------------------
"""
        for cli in detalles["top_clientes"]:
            contenido += f"- {cli[0]}: {cli[1]} pedidos | Total: ${cli[2]:.2f}\n"

        contenido += "\n--------------------------------------------------\n4. PRENDAS / SERVICIOS MÁS SOLICITADOS\n--------------------------------------------------\n"
        for pre in detalles["top_prendas"]:
            contenido += f"- {pre[0]}: {pre[1]} unidades | Subtotal: ${pre[2]:.2f}\n"

        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar Reporte",
            initialfile=f"Reporte_Somos10-4_{periodo.replace(' ', '_')}.txt"
        )

        if archivo:
            try:
                with open(archivo, "w", encoding="utf-8") as f:
                    f.write(contenido)
                messagebox.showinfo("Reporte Exportado", "El reporte se guardó correctamente.")
            except Exception as e:
                messagebox.showerror("Error al Guardar", f"No se pudo exportar el archivo:\n{e}")

    # --------------------------------------------------
    # BOTONES INFERIORES
    # --------------------------------------------------
    btn_actualizar = tk.Button(
        marco_controles, text="🔄 Actualizar", font=("Arial", 9, "bold"),
        bg="#2563EB", fg="#FFFFFF", relief="flat", cursor="hand2", command=actualizar_reportes
    )
    btn_actualizar.pack(side="left", padx=5)

    btn_exportar = tk.Button(
        marco_controles, text="📄 Exportar a TXT", font=("Arial", 9, "bold"),
        bg="#16A34A", fg="#FFFFFF", relief="flat", cursor="hand2", command=exportar_reporte
    )
    btn_exportar.pack(side="left", padx=5)

    btn_cerrar = tk.Button(
        marco_controles, text="Cerrar", font=("Arial", 9, "bold"),
        bg="#64748B", fg="#FFFFFF", relief="flat", cursor="hand2", command=ventana.destroy
    )
    btn_cerrar.pack(side="right", padx=5)

    # Cargar datos al abrir
    actualizar_reportes()