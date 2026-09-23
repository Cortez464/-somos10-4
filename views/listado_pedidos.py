import tkinter as tk
from tkinter import ttk
import ui_utils as messagebox
from datetime import date, datetime

from database.database import (
    obtener_pedidos,
    actualizar_estado,
    actualizar_pagado,
    eliminar_pedido
)

from views.pedidos_detalle import abrir_detalle
from views.pedidos_costos import abrir_costos_pedido
from views.pedidos_editar import abrir_editar_pedido


ESTADOS = [
    "Recibido",
    "Lavando",
    "Secando",
    "Planchando",
    "Listo",
    "Entregado"
]


# =========================================================
# LISTADO DE PEDIDOS
# =========================================================

def abrir_pedidos_listado(ventana_principal):
    """
    Abre la ventana principal del listado de pedidos.
    """

    ventana = tk.Toplevel(
        ventana_principal
    )

    ventana.title(
        "SOMOS 10-4 - Listado de pedidos"
    )

    ventana.geometry(
        "1250x650"
    )

    ventana.resizable(
        True,
        True
    )

    # =====================================================
    # ENCABEZADO
    # =====================================================

    marco_superior = tk.Frame(
        ventana,
        padx=15,
        pady=15
    )

    marco_superior.pack(
        fill="x"
    )

    tk.Label(
        marco_superior,
        text="LISTADO DE PEDIDOS",
        font=("Arial", 20, "bold")
    ).pack(
        side="left"
    )
    resumen_var = tk.StringVar(value="")

    tk.Label(
        marco_superior,
        textvariable=resumen_var,
        font=("Arial", 11)
    ).pack(
        side="left",
        padx=(20, 0)
    )
    # =====================================================
    # TABLA
    # =====================================================

    marco_tabla = tk.Frame(
        ventana,
        padx=15
    )

    marco_tabla.pack(
        fill="both",
        expand=True
    )

    columnas = (
        "id",
        "cliente",
        "recepcion",
        "entrega",
        "estado",
        "total",
        "pago"
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        height=18
    )

    tabla.heading(
        "id",
        text="ID"
    )

    tabla.heading(
        "cliente",
        text="Cliente"
    )

    tabla.heading(
        "recepcion",
        text="Recepción"
    )

    tabla.heading(
        "entrega",
        text="Entrega"
    )

    tabla.heading(
        "estado",
        text="Estado"
    )

    tabla.heading(
        "total",
        text="Total"
    )

    tabla.heading(
        "pago",
        text="Pago"
    )

    tabla.column(
        "id",
        width=55,
        anchor="center"
    )

    tabla.column(
        "cliente",
        width=180
    )

    tabla.column(
        "recepcion",
        width=110,
        anchor="center"
    )

    tabla.column(
        "entrega",
        width=110,
        anchor="center"
    )

    tabla.column(
        "estado",
        width=120,
        anchor="center"
    )

    tabla.column(
        "total",
        width=80,
        anchor="center"
    )

    tabla.column(
        "pago",
        width=100,
        anchor="center"
    )

    scrollbar = ttk.Scrollbar(
        marco_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(
        yscrollcommand=scrollbar.set
    )

    tabla.pack(
        side="left",
        fill="both",
        expand=True
    )
    tabla.tag_configure("atrasado", background="#FEE2E2")
    tabla.tag_configure("proximo", background="#FEF3C7")
    
    scrollbar.pack(
        side="right",
        fill="y"
    )

    # =====================================================
    # RUEDA DEL MOUSE
    # =====================================================

    def rueda_mouse(event):

        tabla.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    tabla.bind(
        "<MouseWheel>",
        rueda_mouse
    )

    # Linux
    tabla.bind(
        "<Button-4>",
        lambda event: tabla.yview_scroll(
            -1,
            "units"
        )
    )

    tabla.bind(
        "<Button-5>",
        lambda event: tabla.yview_scroll(
            1,
            "units"
        )
    )

    # =====================================================
    # CARGAR PEDIDOS
    # =====================================================

    def cargar_pedidos():

        for item in tabla.get_children():
            tabla.delete(item)

        try:

            pedidos = obtener_pedidos()
            hoy = date.today()

            suma_total = 0.0
            pendientes_pago = 0

            for pedido in pedidos:

                pago = (
                    "✅ Pagado"
                    if pedido[6]
                    else "⏳ Pendiente"
                )

                if not pedido[6]:
                    pendientes_pago += 1

                suma_total += float(pedido[5])

                tag = ""
                fecha_entrega_str = pedido[3]
                estado = pedido[4]

                if estado != "Entregado" and fecha_entrega_str:
                    try:
                        fecha_entrega = datetime.strptime(
                            fecha_entrega_str, "%Y-%m-%d"
                        ).date()

                        dias = (fecha_entrega - hoy).days

                        if dias < 0:
                            tag = "atrasado"
                        elif dias <= 1:
                            tag = "proximo"

                    except ValueError:
                        pass

                tabla.insert(
                    "",
                    "end",
                    values=(
                        pedido[0],
                        pedido[1],
                        pedido[2],
                        pedido[3] or "",
                        pedido[4],
                        f"${float(pedido[5]):.2f}",
                        pago
                    ),
                    tags=(tag,) if tag else ()
                )

            resumen_var.set(
                f"Mostrando {len(pedidos)} pedidos   •   "
                f"${suma_total:.2f} en total   •   "
                f"{pendientes_pago} pendientes de pago"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los pedidos.\n\n{e}"
            )

    # =====================================================
    # OBTENER SELECCIÓN
    # =====================================================

    def obtener_seleccion():

        seleccion = tabla.selection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar pedido",
                "Selecciona un pedido de la lista."
            )

            return None

        valores = tabla.item(
            seleccion[0],
            "values"
        )

        return int(valores[0])

    # =====================================================
    # VER PEDIDO
    # =====================================================

    def ver_pedido():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        abrir_detalle(
            ventana,
            pedido_id
        )

    # =====================================================
    # COSTOS
    # =====================================================

    def costos_pedido():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        abrir_costos_pedido(
            ventana,
            pedido_id
        )

    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    def cambiar_estado():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        seleccion = tabla.selection()[0]

        valores = tabla.item(
            seleccion,
            "values"
        )

        estado_actual = valores[4]

        ventana_estado = tk.Toplevel(
            ventana
        )

        ventana_estado.title(
            "Cambiar estado"
        )

        ventana_estado.geometry(
            "350x220"
        )

        ventana_estado.resizable(
            True,
            True
        )

        tk.Label(
            ventana_estado,
            text=f"Pedido #{pedido_id}",
            font=("Arial", 14, "bold")
        ).pack(
            pady=(20, 10)
        )

        tk.Label(
            ventana_estado,
            text="Nuevo estado:"
        ).pack()

        estado_var = tk.StringVar(
            value=estado_actual
        )

        combo_estado = ttk.Combobox(
            ventana_estado,
            textvariable=estado_var,
            values=ESTADOS,
            state="readonly",
            width=25
        )

        combo_estado.pack(
            pady=10
        )

        def guardar_estado():

            nuevo_estado = estado_var.get()

            if not nuevo_estado:
                return

            try:

                actualizar_estado(
                    pedido_id,
                    nuevo_estado
                )

                messagebox.showinfo(
                    "Estado actualizado",
                    f"El pedido #{pedido_id} ahora está:\n\n"
                    f"{nuevo_estado}"
                )

                ventana_estado.destroy()

                cargar_pedidos()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"No se pudo cambiar el estado.\n\n{e}"
                )

        tk.Button(
            ventana_estado,
            text="Guardar",
            width=15,
            command=guardar_estado
        ).pack(
            pady=10
        )

    # =====================================================
    # MARCAR PAGADO
    # =====================================================

    def marcar_pagado():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        seleccion = tabla.selection()[0]

        valores = tabla.item(
            seleccion,
            "values"
        )

        pago_actual = valores[6]

        if pago_actual == "✅ Pagado":

            messagebox.showinfo(
                "Pago",
                f"El pedido #{pedido_id} ya está marcado como pagado."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar pago",
            f"¿Confirmas que el pedido #{pedido_id} "
            f"ya fue pagado?"
        )

        if not confirmar:
            return

        try:

            actualizar_pagado(
                pedido_id,
                1
            )

            cargar_pedidos()

            messagebox.showinfo(
                "Pago registrado",
                f"El pedido #{pedido_id} ha sido marcado como pagado."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el pago.\n\n{e}"
            )

    # =====================================================
    # MARCAR ENTREGADO
    # =====================================================

    def marcar_entregado():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        seleccion = tabla.selection()[0]

        valores = tabla.item(
            seleccion,
            "values"
        )

        estado_actual = valores[4]

        if estado_actual == "Entregado":

            messagebox.showinfo(
                "Entrega",
                f"El pedido #{pedido_id} ya está marcado como entregado."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar entrega",
            f"¿Confirmas que el pedido #{pedido_id} "
            f"ya fue entregado al cliente?"
        )

        if not confirmar:
            return

        try:

            actualizar_estado(
                pedido_id,
                "Entregado"
            )

            cargar_pedidos()

            messagebox.showinfo(
                "Pedido entregado",
                f"El pedido #{pedido_id} ha sido marcado como entregado."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo marcar el pedido como entregado.\n\n{e}"
            )

    # =====================================================
    # EDITAR PEDIDO
    # =====================================================

    def editar_pedido():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        abrir_editar_pedido(
            ventana,
            pedido_id,
            al_guardar=cargar_pedidos
        )

    # =====================================================
    # ELIMINAR PEDIDO
    # =====================================================

    def eliminar_pedido_seleccionado():

        pedido_id = obtener_seleccion()

        if pedido_id is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que deseas eliminar el pedido #{pedido_id}?\n\n"
            f"Esta acción no se puede deshacer."
        )

        if not confirmar:
            return

        try:

            eliminar_pedido(
                pedido_id
            )

            cargar_pedidos()

            messagebox.showinfo(
                "Pedido eliminado",
                f"El pedido #{pedido_id} fue eliminado."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo eliminar el pedido.\n\n{e}"
            )

    # =====================================================
    # BOTONES
    # =====================================================

    marco_botones = tk.Frame(
        ventana,
        padx=15,
        pady=15
    )

    marco_botones.pack(
        fill="x"
    )

    tk.Button(
        marco_botones,
        text="Ver pedido",
        width=15,
        command=ver_pedido
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Costos del pedido",
        width=17,
        command=costos_pedido
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Cambiar estado",
        width=15,
        command=cambiar_estado
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Marcar pagado",
        width=15,
        command=marcar_pagado
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Marcar entregado",
        width=17,
        command=marcar_entregado
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Editar pedido",
        width=15,
        command=editar_pedido
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Eliminar pedido",
        width=15,
        command=eliminar_pedido_seleccionado
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Actualizar",
        width=13,
        command=cargar_pedidos
    ).pack(
        side="left",
        padx=4
    )

    tk.Button(
        marco_botones,
        text="Cerrar",
        width=12,
        command=ventana.destroy
    ).pack(
        side="right",
        padx=4
    )

    # =====================================================
    # CARGA INICIAL
    # =====================================================

    cargar_pedidos()