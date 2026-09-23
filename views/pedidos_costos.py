import tkinter as tk
from tkinter import ttk
import ui_utils as messagebox

from database.database import (
    guardar_costo_pedido,
    obtener_costos_pedido
)


# =========================================================
# COSTOS DEL PEDIDO
# =========================================================

def abrir_costos_pedido(ventana_padre, pedido_id):
    """
    Abre una ventana para consultar y registrar
    los costos asociados a un pedido.
    """

    ventana = tk.Toplevel(ventana_padre)

    ventana.title(
        f"SOMOS 10-4 - Costos pedido #{pedido_id}"
    )

    ventana.geometry("600x500")
    ventana.resizable(True, True)

    marco = tk.Frame(
        ventana,
        padx=20,
        pady=20
    )

    marco.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        marco,
        text=f"COSTOS DEL PEDIDO #{pedido_id}",
        font=("Arial", 18, "bold")
    ).pack(
        pady=(0, 20)
    )

    # =====================================================
    # FORMULARIO
    # =====================================================

    formulario = tk.Frame(marco)

    formulario.pack(
        fill="x"
    )

    tk.Label(
        formulario,
        text="Concepto:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky="w"
    )

    concepto_var = tk.StringVar()

    combo_concepto = ttk.Combobox(
        formulario,
        textvariable=concepto_var,
        values=[
            "Detergente",
            "Suavizante",
            "Agua",
            "Electricidad",
            "Internet",
            "Bolsa / empaque",
            "Transporte",
            "Desgaste de jabón",
            "Otro"
        ],
        width=25
    )

    combo_concepto.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    tk.Label(
        formulario,
        text="Monto:"
    ).grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky="w"
    )

    monto_var = tk.StringVar()

    entrada_monto = tk.Entry(
        formulario,
        textvariable=monto_var,
        width=28
    )

    entrada_monto.grid(
        row=1,
        column=1,
        padx=5,
        pady=5
    )

    # =====================================================
    # TABLA DE COSTOS
    # =====================================================

    tk.Label(
        marco,
        text="Costos registrados",
        font=("Arial", 13, "bold")
    ).pack(
        anchor="w",
        pady=(25, 5)
    )

    columnas = (
        "concepto",
        "monto"
    )

    tabla_costos = ttk.Treeview(
        marco,
        columns=columnas,
        show="headings",
        height=10
    )

    tabla_costos.heading(
        "concepto",
        text="Concepto"
    )

    tabla_costos.heading(
        "monto",
        text="Monto"
    )

    tabla_costos.column(
        "concepto",
        width=350
    )

    tabla_costos.column(
        "monto",
        width=120,
        anchor="center"
    )

    tabla_costos.pack(
        fill="x"
    )

    # =====================================================
    # TOTAL DE COSTOS
    # =====================================================

    total_costos_var = tk.StringVar(
        value="Total de costos: $0.00"
    )

    tk.Label(
        marco,
        textvariable=total_costos_var,
        font=("Arial", 13, "bold")
    ).pack(
        anchor="e",
        pady=10
    )

    # =====================================================
    # CARGAR COSTOS
    # =====================================================

    def cargar_costos():

        for item in tabla_costos.get_children():
            tabla_costos.delete(item)

        try:
            costos = obtener_costos_pedido(pedido_id)

            total = 0.0

            for costo in costos:

                concepto = costo[0]
                monto = float(costo[1])

                total += monto

                tabla_costos.insert(
                    "",
                    "end",
                    values=(
                        concepto,
                        f"${monto:.2f}"
                    )
                )

            total_costos_var.set(
                f"Total de costos: ${total:.2f}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los costos.\n\n{e}"
            )

    # =====================================================
    # GUARDAR COSTO
    # =====================================================

    def guardar_costo():

        concepto = concepto_var.get().strip()

        monto_texto = (
            monto_var
            .get()
            .strip()
            .replace(",", ".")
        )

        if not concepto:

            messagebox.showwarning(
                "Dato requerido",
                "Selecciona o escribe un concepto."
            )

            return

        if not monto_texto:

            messagebox.showwarning(
                "Dato requerido",
                "Ingresa el monto del costo."
            )

            return

        try:

            monto = float(monto_texto)

        except ValueError:

            messagebox.showerror(
                "Monto inválido",
                "El monto debe ser un número.\n\n"
                "Ejemplo: 0.20"
            )

            return

        if monto <= 0:

            messagebox.showwarning(
                "Monto inválido",
                "El monto debe ser mayor que cero."
            )

            return

        try:

            guardar_costo_pedido(
                pedido_id,
                concepto,
                monto
            )

            concepto_var.set("")
            monto_var.set("")

            cargar_costos()

            messagebox.showinfo(
                "Costo registrado",
                f"Se registró correctamente:\n\n"
                f"{concepto}: ${monto:.2f}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo guardar el costo.\n\n{e}"
            )

    # =====================================================
    # BOTÓN AGREGAR COSTO
    # =====================================================

    tk.Button(
        formulario,
        text="Agregar costo",
        width=18,
        command=guardar_costo
    ).grid(
        row=2,
        column=1,
        pady=10
    )

    # =====================================================
    # BOTÓN CERRAR
    # =====================================================

    tk.Button(
        marco,
        text="Cerrar",
        width=15,
        command=ventana.destroy
    ).pack(
        pady=10
    )

    cargar_costos()

