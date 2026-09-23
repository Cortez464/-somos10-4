import tkinter as tk
from tkinter import ttk
import ui_utils as messagebox

from database.database import (
    guardar_cliente,
    obtener_clientes,
    actualizar_cliente,
    eliminar_cliente
)
from theme import COLORS, FONTS, crear_boton_moderno


def abrir_clientes(ventana_principal):

    ventana_clientes = tk.Toplevel(ventana_principal)
    ventana_clientes.title("SOMOS 10-4 - Clientes")
    ventana_clientes.geometry("820x580")
    ventana_clientes.configure(bg=COLORS["bg"])
    ventana_clientes.resizable(True, True)

    # TÍTULO
    tk.Label(
        ventana_clientes,
        text="Gestión de Clientes",
        font=FONTS["h1"],
        bg=COLORS["bg"],
        fg=COLORS["text_main"]
    ).pack(pady=(20, 10))

    # TABLA
    marco_tabla = tk.Frame(ventana_clientes, bg=COLORS["bg"], padx=20)
    marco_tabla.pack(fill="both", expand=True, pady=10)

    columnas = ("id", "nombre", "telefono")
    tabla_clientes = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        height=12
    )
    tabla_clientes.heading("id", text="ID")
    tabla_clientes.heading("nombre", text="Nombre")
    tabla_clientes.heading("telefono", text="Teléfono")

    tabla_clientes.column("id", width=70, anchor="center")
    tabla_clientes.column("nombre", width=420)
    tabla_clientes.column("telefono", width=200, anchor="center")

    scrollbar = ttk.Scrollbar(
        marco_tabla,
        orient="vertical",
        command=tabla_clientes.yview
    )
    tabla_clientes.configure(yscrollcommand=scrollbar.set)

    tabla_clientes.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def cargar_clientes():
        for item in tabla_clientes.get_children():
            tabla_clientes.delete(item)

        clientes = obtener_clientes()
        for cliente in clientes:
            tabla_clientes.insert("", "end", values=(cliente[0], cliente[1], cliente[2]))

    def nuevo_cliente():
        formulario = tk.Toplevel(ventana_clientes)
        formulario.title("Nuevo cliente")
        formulario.geometry("500x450")
        formulario.configure(bg=COLORS["bg"])
        formulario.resizable(True, True)

        tk.Label(
            formulario,
            text="Registrar Cliente",
            font=FONTS["h1"],
            bg=COLORS["bg"],
            fg=COLORS["text_main"]
        ).pack(pady=20)

        marco = tk.Frame(
            formulario,
            bg=COLORS["card_bg"],
            highlightbackground=COLORS["card_border"],
            highlightthickness=1,
            padx=20,
            pady=20
        )
        marco.pack(padx=20, fill="both", expand=True)

        campos = [("Nombre:", 0), ("Teléfono:", 1), ("Dirección:", 2), ("Observaciones:", 3)]
        entradas = {}

        for label_text, row in campos:
            tk.Label(
                marco,
                text=label_text,
                font=FONTS["body_bold"],
                bg=COLORS["card_bg"],
                fg=COLORS["text_main"]
            ).grid(row=row, column=0, padx=10, pady=8, sticky="e")

            entry = ttk.Entry(marco, width=32)
            entry.grid(row=row, column=1, padx=10, pady=8)
            entradas[label_text] = entry

        def guardar():
            nombre = entradas["Nombre:"].get().strip()
            telefono = entradas["Teléfono:"].get().strip()
            direccion = entradas["Dirección:"].get().strip()
            observaciones = entradas["Observaciones:"].get().strip()

            if not nombre or not telefono:
                messagebox.showwarning("Dato requerido", "Debes ingresar nombre y teléfono.")
                return

            guardar_cliente(nombre, telefono, direccion, observaciones)
            messagebox.showinfo("Éxito", "El cliente fue registrado correctamente.")
            formulario.destroy()
            cargar_clientes()

        crear_boton_moderno(
            formulario, "Guardar cliente", guardar, style_type="primary"
        ).pack(pady=15)

    def editar_cliente():
        seleccion = tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Selecciona un cliente de la lista.")
            return

        item = tabla_clientes.item(seleccion[0], "values")
        id_cliente = item[0]

        formulario = tk.Toplevel(ventana_clientes)
        formulario.title("Editar cliente")
        formulario.geometry("500x450")
        formulario.configure(bg=COLORS["bg"])
        formulario.resizable(True, True)

        tk.Label(
            formulario,
            text="Editar Cliente",
            font=FONTS["h1"],
            bg=COLORS["bg"],
            fg=COLORS["text_main"]
        ).pack(pady=20)

        marco = tk.Frame(
            formulario,
            bg=COLORS["card_bg"],
            highlightbackground=COLORS["card_border"],
            highlightthickness=1,
            padx=20,
            pady=20
        )
        marco.pack(padx=20, fill="both", expand=True)

        campos = [("Nombre:", 0), ("Teléfono:", 1), ("Dirección:", 2), ("Observaciones:", 3)]
        entradas = {}

        for label_text, row in campos:
            tk.Label(
                marco,
                text=label_text,
                font=FONTS["body_bold"],
                bg=COLORS["card_bg"],
                fg=COLORS["text_main"]
            ).grid(row=row, column=0, padx=10, pady=8, sticky="e")

            entry = ttk.Entry(marco, width=32)
            entry.grid(row=row, column=1, padx=10, pady=8)
            entradas[label_text] = entry

        entradas["Nombre:"].insert(0, item[1])
        entradas["Teléfono:"].insert(0, item[2])

        def actualizar():
            nombre = entradas["Nombre:"].get().strip()
            telefono = entradas["Teléfono:"].get().strip()
            direccion = entradas["Dirección:"].get().strip()
            observaciones = entradas["Observaciones:"].get().strip()

            if not nombre or not telefono:
                messagebox.showwarning("Dato requerido", "Debes ingresar nombre y teléfono.")
                return

            actualizar_cliente(id_cliente, nombre, telefono, direccion, observaciones)
            messagebox.showinfo("Éxito", "El cliente fue actualizado correctamente.")
            formulario.destroy()
            cargar_clientes()

        crear_boton_moderno(
            formulario, "Guardar cambios", actualizar, style_type="primary"
        ).pack(pady=15)

    def eliminar_cliente_accion():
        seleccion = tabla_clientes.selection()
        if not seleccion:
            messagebox.showwarning("Selección requerida", "Selecciona un cliente de la lista.")
            return

        item = tabla_clientes.item(seleccion[0], "values")
        id_cliente = item[0]

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar el cliente seleccionado?"):
            eliminar_cliente(id_cliente)
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            cargar_clientes()

    # BOTONES DE ACCIÓN
    marco_botones = tk.Frame(ventana_clientes, bg=COLORS["bg"])
    marco_botones.pack(pady=15)

    crear_boton_moderno(marco_botones, "Nuevo cliente", nuevo_cliente, style_type="primary").grid(row=0, column=0, padx=6)
    crear_boton_moderno(marco_botones, "Editar cliente", editar_cliente, style_type="secondary").grid(row=0, column=1, padx=6)
    crear_boton_moderno(marco_botones, "Eliminar cliente", eliminar_cliente_accion, style_type="danger").grid(row=0, column=2, padx=6)
    crear_boton_moderno(marco_botones, "Actualizar", cargar_clientes, style_type="outline").grid(row=0, column=3, padx=6)
    crear_boton_moderno(marco_botones, "Cerrar", ventana_clientes.destroy, style_type="outline").grid(row=0, column=4, padx=6)

    cargar_clientes()