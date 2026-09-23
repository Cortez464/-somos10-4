import tkinter as tk
from tkinter import ttk
import ui_utils as messagebox

from database.database import (
    obtener_detalle_pedido,
    obtener_resumen_financiero_pedido
)

from views.pedidos_costos import abrir_costos_pedido


# =========================================================
# DETALLE DEL PEDIDO
# =========================================================

def abrir_detalle(ventana_padre, pedido_id):
    """
    Abre una ventana con el detalle del pedido,
    incluyendo costo total y ganancia.
    """

    try:

        pedido, prendas = obtener_detalle_pedido(
            pedido_id
        )

        resumen = obtener_resumen_financiero_pedido(
            pedido_id
        )

        costo_total = resumen["costo_total"]
        ganancia = resumen["ganancia"]

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo obtener el pedido.\n\n{e}"
        )

        return

    if pedido is None:

        messagebox.showerror(
            "Error",
            "No se encontró el pedido."
        )

        return

    ventana = tk.Toplevel(
        ventana_padre
    )

    ventana.title(
        f"SOMOS 10-4 - Pedido #{pedido_id}"
    )

    ventana.geometry(
        "650x650"
    )

    ventana.resizable(
        True,
        True
    )

    marco = tk.Frame(
        ventana,
        padx=20,
        pady=15
    )

    marco.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # TÍTULO
    # =====================================================

    tk.Label(
        marco,
        text=f"PEDIDO #{pedido[0]}",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(0, 15)
    )

    # =====================================================
    # INFORMACIÓN
    # =====================================================

    informacion = tk.Frame(
        marco
    )

    informacion.pack(
        fill="x"
    )

    tk.Label(
        informacion,
        text=f"Cliente: {pedido[1]}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    tk.Label(
        informacion,
        text=f"Teléfono: {pedido[2] or 'No registrado'}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    tk.Label(
        informacion,
        text=f"Fecha de recepción: {pedido[3]}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    tk.Label(
        informacion,
        text=f"Fecha de entrega: {pedido[4] or 'No definida'}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    tk.Label(
        informacion,
        text=f"Estado: {pedido[5]}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    estado_pago = (
        "PAGADO"
        if pedido[7]
        else "PENDIENTE"
    )

    tk.Label(
        informacion,
        text=f"Pago: {estado_pago}",
        font=("Arial", 11)
    ).pack(
        anchor="w",
        pady=2
    )

    # =====================================================
    # RESUMEN FINANCIERO
    # =====================================================

    tk.Label(
        informacion,
        text=f"Total del pedido: ${float(pedido[6]):.2f}",
        font=("Arial", 13, "bold")
    ).pack(
        anchor="w",
        pady=(8, 2)
    )

    tk.Label(
        informacion,
        text=f"Costo total: ${costo_total:.2f}",
        font=("Arial", 12)
    ).pack(
        anchor="w",
        pady=2
    )

    tk.Label(
        informacion,
        text=f"Ganancia: ${ganancia:.2f}",
        font=("Arial", 13, "bold")
    ).pack(
        anchor="w",
        pady=2
    )

    # =====================================================
    # PRENDAS
    # =====================================================

    tk.Label(
        marco,
        text="Prendas",
        font=("Arial", 13, "bold")
    ).pack(
        anchor="w",
        pady=(20, 5)
    )

    columnas = (
        "prenda",
        "cantidad",
        "precio",
        "subtotal"
    )

    tabla = ttk.Treeview(
        marco,
        columns=columnas,
        show="headings",
        height=8
    )

    tabla.heading(
        "prenda",
        text="Prenda"
    )

    tabla.heading(
        "cantidad",
        text="Cantidad"
    )

    tabla.heading(
        "precio",
        text="Precio"
    )

    tabla.heading(
        "subtotal",
        text="Subtotal"
    )

    tabla.column(
        "prenda",
        width=220
    )

    tabla.column(
        "cantidad",
        width=80,
        anchor="center"
    )

    tabla.column(
        "precio",
        width=100,
        anchor="center"
    )

    tabla.column(
        "subtotal",
        width=100,
        anchor="center"
    )

    tabla.pack(
        fill="x"
    )

    for prenda in prendas:

        tabla.insert(
            "",
            "end",
            values=(
                prenda[0],
                prenda[1],
                f"${float(prenda[2]):.2f}",
                f"${float(prenda[3]):.2f}"
            )
        )

    # =====================================================
    # OBSERVACIONES
    # =====================================================

    tk.Label(
        marco,
        text="Observaciones",
        font=("Arial", 13, "bold")
    ).pack(
        anchor="w",
        pady=(20, 5)
    )

    observaciones = (
        pedido[8]
        if pedido[8]
        else "Sin observaciones"
    )

    tk.Label(
        marco,
        text=observaciones,
        anchor="w",
        justify="left",
        wraplength=580
    ).pack(
        anchor="w"
    )

    # =====================================================
    # BOTONES
    # =====================================================

    marco_botones = tk.Frame(
        marco
    )

    marco_botones.pack(
        pady=20
    )

    tk.Button(
        marco_botones,
        text="Ver costos",
        width=15,
        command=lambda: abrir_costos_pedido(
            ventana,
            pedido_id
        )
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco_botones,
        text="Cerrar",
        width=15,
        command=ventana.destroy
    ).pack(
        side="left",
        padx=5
    )

