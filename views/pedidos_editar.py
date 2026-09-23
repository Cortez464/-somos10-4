import tkinter as tk
import ui_utils as messagebox

from database.database import (
    obtener_clientes,
    obtener_detalle_pedido,
    actualizar_pedido_completo
)

from views.pedidos import PRECIOS_PRENDAS


# =========================================================
# EDITAR PEDIDO (completo: cliente, fechas, prendas, obs.)
# =========================================================

def abrir_editar_pedido(ventana_padre, pedido_id, al_guardar=None):
    """
    Abre una ventana para editar un pedido existente por
    completo: cliente, fechas, prendas y observaciones.

    'al_guardar' es un callback opcional que se ejecuta
    después de guardar con éxito (por ejemplo, para
    refrescar la tabla del listado).
    """

    # ======================================================
    # CARGAR DATOS ACTUALES DEL PEDIDO
    # ======================================================

    try:

        pedido, detalle_actual = obtener_detalle_pedido(
            pedido_id
        )

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

    cliente_id_actual = pedido[9]
    fecha_recepcion_actual = pedido[3]
    fecha_entrega_actual = pedido[4] or ""
    observaciones_actual = pedido[8] or ""

    # Lista interna de prendas, precargada con el detalle actual
    prendas = []

    for fila in detalle_actual:

        prendas.append({
            "nombre": fila[0],
            "cantidad": fila[1],
            "precio_unitario": fila[2],
            "subtotal": fila[3]
        })

    # ======================================================
    # VENTANA
    # ======================================================

    ventana = tk.Toplevel(ventana_padre)

    ventana.title(
        f"Editar pedido #{pedido_id}"
    )

    ventana.geometry("650x700")

    ventana.resizable(True, True)

    # ======================================================
    # CONTENEDOR CON SCROLL (por si la lista de prendas crece)
    # ======================================================

    contenedor = tk.Frame(ventana)

    contenedor.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        contenedor,
        highlightthickness=0
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

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

    marco_contenido = tk.Frame(canvas)

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=marco_contenido,
        anchor="nw"
    )

    def actualizar_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    marco_contenido.bind(
        "<Configure>",
        actualizar_scroll
    )

    def ajustar_ancho(event):

        canvas.itemconfig(
            ventana_canvas,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        ajustar_ancho
    )

    def scroll_mouse(event):

        if event.num == 4:
            canvas.yview_scroll(-3, "units")

        elif event.num == 5:
            canvas.yview_scroll(3, "units")

        elif event.delta:

            canvas.yview_scroll(
                -3 if event.delta > 0 else 3,
                "units"
            )

    ventana.bind("<Button-4>", scroll_mouse)
    ventana.bind("<Button-5>", scroll_mouse)
    ventana.bind("<MouseWheel>", scroll_mouse)

    # ======================================================
    # TÍTULO
    # ======================================================

    tk.Label(
        marco_contenido,
        text=f"Editar pedido #{pedido_id}",
        font=("Arial", 20, "bold")
    ).pack(
        pady=(15, 15)
    )

    # ======================================================
    # CLIENTES
    # ======================================================

    clientes = obtener_clientes()

    clientes_diccionario = {}
    texto_cliente_actual = None

    for cliente in clientes:

        cliente_id = cliente[0]
        nombre = cliente[1]
        telefono = cliente[2]

        texto = f"{nombre} - {telefono}"

        clientes_diccionario[texto] = cliente_id

        if cliente_id == cliente_id_actual:
            texto_cliente_actual = texto

    formulario = tk.Frame(marco_contenido)

    formulario.pack(pady=5)

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

    nombres_clientes = list(clientes_diccionario.keys())

    cliente_seleccionado = tk.StringVar()

    if texto_cliente_actual:
        cliente_seleccionado.set(texto_cliente_actual)
    elif nombres_clientes:
        cliente_seleccionado.set(nombres_clientes[0])
    else:
        cliente_seleccionado.set("No hay clientes")

    menu_clientes = tk.OptionMenu(
        formulario,
        cliente_seleccionado,
        *(nombres_clientes if nombres_clientes else ["No hay clientes"])
    )

    menu_clientes.config(width=35)

    menu_clientes.grid(
        row=0,
        column=1,
        padx=10,
        pady=8
    )

    # ======================================================
    # FECHAS
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

    entrada_fecha_recepcion = tk.Entry(formulario, width=38)

    entrada_fecha_recepcion.insert(0, fecha_recepcion_actual)

    entrada_fecha_recepcion.grid(
        row=1,
        column=1,
        padx=10,
        pady=8
    )

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

    entrada_fecha_entrega = tk.Entry(formulario, width=38)

    entrada_fecha_entrega.insert(0, fecha_entrega_actual)

    entrada_fecha_entrega.grid(
        row=2,
        column=1,
        padx=10,
        pady=8
    )

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

    marco_prendas = tk.Frame(marco_contenido)

    marco_prendas.pack()

    tk.Label(
        marco_prendas,
        text="Prenda:"
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    opciones_prendas = list(PRECIOS_PRENDAS.keys())

    prenda_seleccionada = tk.StringVar()

    prenda_seleccionada.set(opciones_prendas[0])

    menu_prendas = tk.OptionMenu(
        marco_prendas,
        prenda_seleccionada,
        *opciones_prendas
    )

    menu_prendas.config(width=18)

    menu_prendas.grid(
        row=0,
        column=1,
        padx=5,
        pady=5
    )

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
        value=f"${PRECIOS_PRENDAS[opciones_prendas[0]]:.2f}"
    )

    tk.Label(
        marco_prendas,
        textvariable=precio_var,
        font=("Arial", 11, "bold")
    ).grid(
        row=0,
        column=3,
        padx=5,
        pady=5
    )

    def actualizar_precio(*args):

        nombre = prenda_seleccionada.get()

        precio = PRECIOS_PRENDAS.get(nombre, 0.50)

        precio_var.set(f"${precio:.2f}")

    prenda_seleccionada.trace_add("write", actualizar_precio)

    tk.Label(
        marco_prendas,
        text="Cantidad:"
    ).grid(
        row=0,
        column=4,
        padx=5,
        pady=5
    )

    entrada_cantidad = tk.Entry(marco_prendas, width=8)

    entrada_cantidad.insert(0, "1")

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

    lista_prendas.pack(pady=10)

    # ======================================================
    # TOTAL
    # ======================================================

    total_label = tk.Label(
        marco_contenido,
        text="TOTAL: $0.00",
        font=("Arial", 18, "bold")
    )

    total_label.pack(pady=10)

    def calcular_total():

        total = 0.00

        for prenda in prendas:
            total += prenda["subtotal"]

        total_label.config(
            text=f"TOTAL: ${total:.2f}"
        )

        return total

    def actualizar_lista():

        lista_prendas.delete(0, tk.END)

        for prenda in prendas:

            texto = (
                f'{prenda["nombre"]} '
                f'x{prenda["cantidad"]} '
                f'@ ${prenda["precio_unitario"]:.2f} '
                f'= ${prenda["subtotal"]:.2f}'
            )

            lista_prendas.insert(tk.END, texto)

        calcular_total()

    def agregar_prenda():

        nombre = prenda_seleccionada.get()

        try:

            cantidad = int(entrada_cantidad.get())

            if cantidad <= 0:
                raise ValueError

        except ValueError:

            messagebox.showwarning(
                "Cantidad incorrecta",
                "La cantidad debe ser un número mayor que cero."
            )

            return

        precio_unitario = PRECIOS_PRENDAS.get(nombre, 0.50)

        # Si ya existe la prenda, sumar cantidad
        for prenda in prendas:

            if prenda["nombre"] == nombre:

                prenda["cantidad"] += cantidad

                prenda["subtotal"] = (
                    prenda["cantidad"] * prenda["precio_unitario"]
                )

                actualizar_lista()

                return

        subtotal = cantidad * precio_unitario

        prendas.append({
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

        actualizar_lista()

        entrada_cantidad.delete(0, tk.END)
        entrada_cantidad.insert(0, "1")

    def eliminar_prenda():

        seleccion = lista_prendas.curselection()

        if not seleccion:

            messagebox.showwarning(
                "Seleccionar prenda",
                "Selecciona una prenda para eliminar."
            )

            return

        prendas.pop(seleccion[0])

        actualizar_lista()

    tk.Button(
        marco_contenido,
        text="Agregar prenda",
        width=20,
        command=agregar_prenda
    ).pack(pady=5)

    tk.Button(
        marco_contenido,
        text="Eliminar prenda",
        width=20,
        command=eliminar_prenda
    ).pack(pady=5)

    # ======================================================
    # OBSERVACIONES
    # ======================================================

    marco_observaciones = tk.Frame(marco_contenido)

    marco_observaciones.pack(pady=10)

    tk.Label(
        marco_observaciones,
        text="Observaciones:"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    entrada_observaciones = tk.Entry(marco_observaciones, width=50)

    entrada_observaciones.insert(0, observaciones_actual)

    entrada_observaciones.grid(
        row=0,
        column=1,
        padx=5
    )

    # ======================================================
    # GUARDAR
    # ======================================================

    def guardar():

        if not clientes_diccionario:

            messagebox.showwarning(
                "Sin clientes",
                "No hay clientes registrados."
            )

            return

        cliente_id = clientes_diccionario.get(
            cliente_seleccionado.get()
        )

        if cliente_id is None:

            messagebox.showwarning(
                "Cliente",
                "Selecciona un cliente."
            )

            return

        fecha_recepcion = entrada_fecha_recepcion.get().strip()
        fecha_entrega = entrada_fecha_entrega.get().strip()
        observaciones = entrada_observaciones.get().strip()

        if not fecha_recepcion:

            messagebox.showwarning(
                "Fecha",
                "La fecha de recepción es obligatoria."
            )

            return

        if not prendas:

            messagebox.showwarning(
                "Sin prendas",
                "El pedido debe tener al menos una prenda."
            )

            return

        total = calcular_total()

        if total <= 0:

            messagebox.showwarning(
                "Total",
                "El total del pedido debe ser mayor que cero."
            )

            return

        try:

            actualizar_pedido_completo(
                pedido_id,
                cliente_id,
                fecha_recepcion,
                fecha_entrega,
                observaciones,
                total,
                prendas
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el pedido.\n\n{e}"
            )

            return

        messagebox.showinfo(
            "Pedido actualizado",
            f"El pedido #{pedido_id} se actualizó correctamente.\n\n"
            f"Nuevo total: ${total:.2f}"
        )

        ventana.destroy()

        if al_guardar:
            al_guardar()

    tk.Button(
        marco_contenido,
        text="GUARDAR CAMBIOS",
        width=25,
        height=2,
        command=guardar
    ).pack(pady=20)

    # ======================================================
    # MOSTRAR PRENDAS PRECARGADAS Y SUBIR SCROLL AL INICIO
    # ======================================================

    actualizar_lista()

    canvas.yview_moveto(0)
