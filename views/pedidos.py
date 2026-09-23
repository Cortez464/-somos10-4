import tkinter as tk
import ui_utils as messagebox
from datetime import date

from database.database import (
    obtener_clientes,
    guardar_pedido_completo
)


# ==========================================================
# PRECIOS DE LAS PRENDAS
# ==========================================================

PRECIOS_PRENDAS = {
    "Pantalón": 0.75,
    "Camisa": 0.75,
    "Camiseta": 0.50,
    "Short": 0.50,
    "Ropa interior": 0.50,
    "Otro": 0.50
}


# ==========================================================
# ABRIR VENTANA DE NUEVO PEDIDO
# ==========================================================

def abrir_pedidos(ventana_principal):

    ventana_pedidos = tk.Toplevel(ventana_principal)

    ventana_pedidos.title("SOMOS 10-4 - Nuevo pedido")
    ventana_pedidos.geometry("800x650")
    ventana_pedidos.resizable(True, True)

    # ======================================================
    # CONTENEDOR PRINCIPAL
    # ======================================================

    contenedor = tk.Frame(ventana_pedidos)

    contenedor.pack(
        fill="both",
        expand=True
    )

    # ======================================================
    # CANVAS
    # ======================================================

    canvas = tk.Canvas(
        contenedor,
        highlightthickness=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    # ======================================================
    # BARRA LATERAL
    # ======================================================

    scrollbar = tk.Scrollbar(
        contenedor,
        orient="vertical",
        command=canvas.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    # ======================================================
    # MARCO DEL FORMULARIO
    # ======================================================

    marco_contenido = tk.Frame(canvas)

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=marco_contenido,
        anchor="nw"
    )

    # ======================================================
    # ACTUALIZAR SCROLL
    # ======================================================

    def actualizar_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    marco_contenido.bind(
        "<Configure>",
        actualizar_scroll
    )

    # ======================================================
    # AJUSTAR ANCHO
    # ======================================================

    def ajustar_ancho(event):

        canvas.itemconfig(
            ventana_canvas,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        ajustar_ancho
    )

    # ======================================================
    # RUEDA DEL MOUSE
    # ======================================================

    def scroll_mouse(event):

        if event.num == 4:

            canvas.yview_scroll(
                -3,
                "units"
            )

        elif event.num == 5:

            canvas.yview_scroll(
                3,
                "units"
            )

        elif event.delta:

            if event.delta > 0:

                canvas.yview_scroll(
                    -3,
                    "units"
                )

            else:

                canvas.yview_scroll(
                    3,
                    "units"
                )

    ventana_pedidos.bind(
        "<Button-4>",
        scroll_mouse
    )

    ventana_pedidos.bind(
        "<Button-5>",
        scroll_mouse
    )

    ventana_pedidos.bind(
        "<MouseWheel>",
        scroll_mouse
    )

    # ======================================================
    # TÍTULO
    # ======================================================

    titulo = tk.Label(
        marco_contenido,
        text="Nuevo pedido",
        font=("Arial", 24, "bold")
    )

    titulo.pack(
        pady=20
    )

    # ======================================================
    # CLIENTES
    # ======================================================

    clientes = obtener_clientes()

    clientes_diccionario = {}

    for cliente in clientes:

        cliente_id = cliente[0]
        nombre = cliente[1]
        telefono = cliente[2]

        texto = f"{nombre} - {telefono}"

        clientes_diccionario[texto] = cliente_id

    # ======================================================
    # FORMULARIO
    # ======================================================

    formulario = tk.Frame(
        marco_contenido
    )

    formulario.pack(
        pady=5
    )

    # ======================================================
    # CLIENTE
    # ======================================================

    tk.Label(
        formulario,
        text="Cliente:"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=8,
        sticky="e"
    )

    cliente_seleccionado = tk.StringVar()

    nombres_clientes = list(
        clientes_diccionario.keys()
    )

    if nombres_clientes:

        cliente_seleccionado.set(
            nombres_clientes[0]
        )

    else:

        cliente_seleccionado.set(
            "No hay clientes"
        )

    menu_clientes = tk.OptionMenu(
        formulario,
        cliente_seleccionado,
        *nombres_clientes
    )

    menu_clientes.config(
        width=35
    )

    menu_clientes.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    # ======================================================
    # FECHA DE RECEPCIÓN
    # ======================================================

    tk.Label(
        formulario,
        text="Fecha recepción:"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=8,
        sticky="e"
    )

    entrada_fecha_recepcion = tk.Entry(
        formulario,
        width=38
    )

    entrada_fecha_recepcion.insert(
        0,
        date.today().strftime("%Y-%m-%d")
    )

    entrada_fecha_recepcion.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

    # ======================================================
    # FECHA DE ENTREGA
    # ======================================================

    tk.Label(
        formulario,
        text="Fecha entrega:"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=8,
        sticky="e"
    )

    entrada_fecha_entrega = tk.Entry(
        formulario,
        width=38
    )

    entrada_fecha_entrega.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

    # ======================================================
    # SERVICIO
    # ======================================================

    tk.Label(
        marco_contenido,
        text="Servicio",
        font=("Arial", 16, "bold")
    ).pack(
        pady=(20, 5)
    )

    tk.Label(
        marco_contenido,
        text="Los precios se calculan según cada prenda.",
        font=("Arial", 11)
    ).pack()

    # ======================================================
    # PRENDAS
    # ======================================================

    tk.Label(
        marco_contenido,
        text="Prendas",
        font=("Arial", 16, "bold")
    ).pack(
        pady=(20, 5)
    )

    marco_prendas = tk.Frame(
        marco_contenido
    )

    marco_prendas.pack()

    # ======================================================
    # TIPO DE PRENDA
    # ======================================================

    tk.Label(
        marco_prendas,
        text="Prenda:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    opciones_prendas = [
        "Camisa",
        "Camiseta",
        "Pantalón",
        "Short",
        "Ropa interior",
        "Otro"
    ]

    prenda_seleccionada = tk.StringVar()

    prenda_seleccionada.set(
        opciones_prendas[0]
    )

    menu_prendas = tk.OptionMenu(
        marco_prendas,
        prenda_seleccionada,
        *opciones_prendas
    )

    menu_prendas.config(
        width=18
    )

    menu_prendas.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

    # ======================================================
    # PRECIO UNITARIO
    # ======================================================

    tk.Label(
        marco_prendas,
        text="Precio:"
    ).grid(
        row=0,
        column=2,
        padx=5,
        pady=5
    )

    precio_var = tk.StringVar(
        value="$0.75"
    )

    etiqueta_precio = tk.Label(
        marco_prendas,
        textvariable=precio_var,
        font=("Arial", 11, "bold")
    )

    etiqueta_precio.grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    def actualizar_precio(*args):

        nombre = prenda_seleccionada.get()

        precio = PRECIOS_PRENDAS.get(
        nombre,
        0.50
    )

        precio_var.set(
        f"${precio:.2f}"
    )

    prenda_seleccionada.trace_add(
        "write",
        actualizar_precio
    )


    # ======================================================
    # CANTIDAD
    # ======================================================

    tk.Label(
        marco_prendas,
        text="Cantidad:"
    ).grid(
        row=0,
        column=4,
        padx=5,
        pady=5
    )

    entrada_cantidad = tk.Entry(
        marco_prendas,
        width=8
    )

    entrada_cantidad.insert(
        0,
        "1"
    )

    entrada_cantidad.grid(
        row=0,
        column=5,
        padx=5,
        pady=5
    )

    # ======================================================
    # LISTA DE PRENDAS
    # ======================================================

    lista_prendas = tk.Listbox(
        marco_contenido,
        width=80,
        height=8
    )

    lista_prendas.pack(
        pady=10
    )

    # Lista interna
    prendas = []

    # ======================================================
    # CALCULAR TOTAL
    # ======================================================

    def calcular_total():

        total = 0.00

        for prenda in prendas:

            total += prenda["subtotal"]

        total_label.config(
            text=f"TOTAL: ${total:.2f}"
        )

        return total

    # ======================================================
    # ACTUALIZAR LISTA
    # ======================================================

    def actualizar_lista():

        lista_prendas.delete(
            0,
            tk.END
        )

        for prenda in prendas:

            texto = (
                f'{prenda["nombre"]} '
                f'x{prenda["cantidad"]} '
                f'@ ${prenda["precio_unitario"]:.2f} '
                f'= ${prenda["subtotal"]:.2f}'
            )

            lista_prendas.insert(
                tk.END,
                texto
            )

        calcular_total()

    # ======================================================
    # AGREGAR PRENDA
    # ======================================================

    def agregar_prenda():

        nombre = prenda_seleccionada.get()

        try:

            cantidad = int(
                entrada_cantidad.get()
            )

            if cantidad <= 0:

                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Cantidad incorrecta",
                "La cantidad debe ser un número mayor que cero."
            )

            return

        precio_unitario = PRECIOS_PRENDAS.get(
            nombre,
            0.50
        )

        # --------------------------------------------------
        # Si ya existe la prenda, sumar cantidad
        # --------------------------------------------------

        for prenda in prendas:

            if prenda["nombre"] == nombre:

                prenda["cantidad"] += cantidad

                prenda["subtotal"] = (
                    prenda["cantidad"]
                    * prenda["precio_unitario"]
                )

                actualizar_lista()

                return

        # --------------------------------------------------
        # Nueva prenda
        # --------------------------------------------------

        subtotal = (
            cantidad
            * precio_unitario
        )

        prendas.append({

            "nombre": nombre,

            "cantidad": cantidad,

            "precio_unitario": precio_unitario,

            "subtotal": subtotal

        })

        actualizar_lista()

        # --------------------------------------------------
        # Reiniciar cantidad
        # --------------------------------------------------

        entrada_cantidad.delete(
            0,
            tk.END
        )

        entrada_cantidad.insert(
            0,
            "1"
        )

    # ======================================================
    # BOTÓN AGREGAR PRENDA
    # ======================================================

    boton_agregar = tk.Button(
        marco_contenido,
        text="Agregar prenda",
        width=20,
        command=agregar_prenda
    )

    boton_agregar.pack(
        pady=5
    )

    # ======================================================
    # ELIMINAR PRENDA
    # ======================================================

    def eliminar_prenda():

        seleccion = lista_prendas.curselection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar prenda",
                "Selecciona una prenda para eliminar."
            )

            return

        indice = seleccion[0]

        prendas.pop(
            indice
        )

        actualizar_lista()

    # ======================================================
    # BOTÓN ELIMINAR PRENDA
    # ======================================================

    boton_eliminar = tk.Button(
        marco_contenido,
        text="Eliminar prenda",
        width=20,
        command=eliminar_prenda
    )

    boton_eliminar.pack(
        pady=5
    )

    # ======================================================
    # TOTAL
    # ======================================================

    total_label = tk.Label(
        marco_contenido,
        text="TOTAL: $0.00",
        font=("Arial", 18, "bold")
    )

    total_label.pack(
        pady=15
    )

    # ======================================================
    # OBSERVACIONES
    # ======================================================

    marco_observaciones = tk.Frame(
        marco_contenido
    )

    marco_observaciones.pack(
        pady=5
    )

    tk.Label(
        marco_observaciones,
        text="Observaciones:"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    entrada_observaciones = tk.Entry(
        marco_observaciones,
        width=50
    )

    entrada_observaciones.grid(
        row=0,
        column=1,
        padx=5
    )

    # ======================================================
    # FUNCIÓN GUARDAR PEDIDO
    # ======================================================

    def guardar():

        # --------------------------------------------------
        # Verificar clientes
        # --------------------------------------------------

        if not clientes:

            messagebox.showwarning(
                "Sin clientes",
                "Primero debes registrar un cliente."
            )

            return

        # --------------------------------------------------
        # Verificar prendas
        # --------------------------------------------------

        if not prendas:

            messagebox.showwarning(
                "Sin prendas",
                "Debes agregar al menos una prenda."
            )

            return

        # --------------------------------------------------
        # Obtener cliente
        # --------------------------------------------------

        cliente_id = clientes_diccionario.get(
            cliente_seleccionado.get()
        )

        if cliente_id is None:

            messagebox.showwarning(
                "Cliente",
                "Selecciona un cliente."
            )

            return

        # --------------------------------------------------
        # Fechas
        # --------------------------------------------------

        fecha_recepcion = (
            entrada_fecha_recepcion
            .get()
            .strip()
        )

        fecha_entrega = (
            entrada_fecha_entrega
            .get()
            .strip()
        )

        # --------------------------------------------------
        # Observaciones
        # --------------------------------------------------

        observaciones = (
            entrada_observaciones
            .get()
            .strip()
        )

        # --------------------------------------------------
        # Validar recepción
        # --------------------------------------------------

        if not fecha_recepcion:

            messagebox.showwarning(
                "Fecha",
                "La fecha de recepción es obligatoria."
            )

            return

        # --------------------------------------------------
        # CALCULAR TOTAL FINAL
        # --------------------------------------------------

        total = calcular_total()

        if total <= 0:

            messagebox.showwarning(
                "Total",
                "El total del pedido debe ser mayor que cero."
            )

            return

        # ==================================================
        # GUARDAR EN BASE DE DATOS
        # ==================================================

        try:

            pedido_id = guardar_pedido_completo(

                cliente_id,

                fecha_recepcion,

                fecha_entrega,

                observaciones,

                total,

                prendas

            )

        except Exception as error:

            messagebox.showerror(

                "Error",

                f"No se pudo guardar el pedido:\n{error}"

            )

            return

        # ==================================================
        # CONFIRMACIÓN
        # ==================================================

        messagebox.showinfo(

            "Pedido creado",

            f"Pedido #{pedido_id} creado correctamente.\n\n"
            f"Total: ${total:.2f}"

        )

        # Cerrar ventana
        ventana_pedidos.destroy()

    # ======================================================
    # BOTÓN GUARDAR
    # ======================================================

    boton_guardar = tk.Button(

        marco_contenido,

        text="GUARDAR PEDIDO",

        width=25,

        height=2,

        command=guardar

    )

    boton_guardar.pack(
        pady=20
    )

    # ======================================================
    # INICIAR ARRIBA
    # ======================================================

    canvas.yview_moveto(0)