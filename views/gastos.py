import tkinter as tk
from tkinter import ttk
import ui_utils as messagebox
from datetime import date

# --------------------------------------------------
# CATEGORÍAS DE GASTOS
# --------------------------------------------------

CATEGORIAS = [
    "Detergente",
    "Suavizante",
    "Jabón",
    "Gasolina",
    "Agua",
    "Electricidad",
    "Internet",
    "Empaque",
    "Otros"
]

# --------------------------------------------------
# FUNCIONES DE BASE DE DATOS
# --------------------------------------------------

def guardar_gasto(fecha, categoria, descripcion, monto):
    from database.database import conectar

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO gastos (
                fecha,
                categoria,
                descripcion,
                monto
            )
            VALUES (?, ?, ?, ?)
        """, (
            fecha,
            categoria,
            descripcion,
            monto
        ))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def obtener_gastos():
    from database.database import conectar

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT
                id,
                fecha,
                categoria,
                descripcion,
                monto
            FROM gastos
            ORDER BY id DESC
        """)
        return cursor.fetchall()
    finally:
        conexion.close()


def actualizar_gasto(gasto_id, fecha, categoria, descripcion, monto):
    from database.database import conectar

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE gastos
            SET fecha = ?,
                categoria = ?,
                descripcion = ?,
                monto = ?
            WHERE id = ?
        """, (
            fecha,
            categoria,
            descripcion,
            monto,
            gasto_id
        ))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


def eliminar_gasto(gasto_id):
    from database.database import conectar

    conexion = conectar()
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


# --------------------------------------------------
# INTERFAZ GRÁFICA
# --------------------------------------------------

def abrir_gastos(ventana_principal):

    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Gastos - SOMOS 10-4")
    ventana.geometry("900x650")
    ventana.resizable(True, True)

    # -------------------------
    # TÍTULO
    # -------------------------

    tk.Label(
        ventana,
        text="CONTROL DE GASTOS",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    # -------------------------
    # FORMULARIO
    # -------------------------

    marco_formulario = tk.Frame(ventana)
    marco_formulario.pack(pady=10)

    tk.Label(
        marco_formulario,
        text="Fecha:"
    ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entrada_fecha = tk.Entry(marco_formulario, width=20)
    entrada_fecha.grid(row=0, column=1, padx=5, pady=5)
    entrada_fecha.insert(0, date.today().strftime("%Y-%m-%d"))

    tk.Label(
        marco_formulario,
        text="Categoría:"
    ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

    combo_categoria = ttk.Combobox(
        marco_formulario,
        values=CATEGORIAS,
        state="readonly",
        width=18
    )
    combo_categoria.grid(row=1, column=1, padx=5, pady=5)
    combo_categoria.current(0)

    tk.Label(
        marco_formulario,
        text="Descripción:"
    ).grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entrada_descripcion = tk.Entry(
        marco_formulario,
        width=40
    )
    entrada_descripcion.grid(
        row=2,
        column=1,
        padx=5,
        pady=5
    )

    tk.Label(
        marco_formulario,
        text="Monto ($):"
    ).grid(row=3, column=0, padx=5, pady=5, sticky="e")

    entrada_monto = tk.Entry(
        marco_formulario,
        width=20
    )
    entrada_monto.grid(
        row=3,
        column=1,
        padx=5,
        pady=5
    )

    # -------------------------
    # TABLA DE GASTOS
    # -------------------------

    marco_tabla = tk.Frame(ventana)
    marco_tabla.pack(fill="both", expand=True, padx=20, pady=10)

    columnas = (
        "id",
        "fecha",
        "categoria",
        "descripcion",
        "monto"
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        height=10
    )

    tabla.heading("id", text="ID")
    tabla.heading("fecha", text="Fecha")
    tabla.heading("categoria", text="Categoría")
    tabla.heading("descripcion", text="Descripción")
    tabla.heading("monto", text="Monto")

    tabla.column("id", width=60, anchor="center")
    tabla.column("fecha", width=110, anchor="center")
    tabla.column("categoria", width=140)
    tabla.column("descripcion", width=320)
    tabla.column("monto", width=110, anchor="e")

    scrollbar = ttk.Scrollbar(
        marco_tabla,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=scrollbar.set)

    tabla.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Soporte para la rueda del mouse (Scroll)
    def rueda_mouse(event):
        tabla.yview_scroll(int(-1 * (event.delta / 120)), "units")

    tabla.bind("<MouseWheel>", rueda_mouse)
    tabla.bind("<Button-4>", lambda event: tabla.yview_scroll(-1, "units"))
    tabla.bind("<Button-5>", lambda event: tabla.yview_scroll(1, "units"))

    # -------------------------
    # ETIQUETA DE TOTAL
    # -------------------------

    total_gastos_var = tk.StringVar(value="Total en gastos: $0.00")

    label_total = tk.Label(
        ventana,
        textvariable=total_gastos_var,
        font=("Arial", 12, "bold"),
        fg="#B00020"
    )
    label_total.pack(anchor="e", padx=25, pady=(0, 5))

    # -------------------------
    # CARGAR GASTOS
    # -------------------------

    def cargar_gastos():
        for item in tabla.get_children():
            tabla.delete(item)

        try:
            gastos = obtener_gastos()
            total_acumulado = 0.0

            for gasto in gastos:
                monto_float = float(gasto[4])
                total_acumulado += monto_float

                tabla.insert(
                    "",
                    "end",
                    values=(
                        gasto[0],
                        gasto[1],
                        gasto[2],
                        gasto[3],
                        f"${monto_float:.2f}"
                    )
                )

            total_gastos_var.set(f"Total registrado en gastos: ${total_acumulado:.2f}")

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los gastos.\n\n{e}"
            )

    # -------------------------
    # OBTENER SELECCIÓN
    # -------------------------

    def obtener_seleccion_gasto():
        seleccion = tabla.selection()

        if not seleccion:
            messagebox.showwarning(
                "Seleccionar gasto",
                "Debes seleccionar un gasto de la lista."
            )
            return None

        valores = tabla.item(seleccion[0], "values")
        return int(valores[0])

    # -------------------------
    # EDITAR GASTO
    # -------------------------

    def editar_gasto():
        gasto_id = obtener_seleccion_gasto()
        if gasto_id is None:
            return

        seleccion = tabla.selection()[0]
        valores = tabla.item(seleccion, "values")

        fecha_actual = valores[1]
        categoria_actual = valores[2]
        descripcion_actual = valores[3]
        monto_actual = str(valores[4]).replace("$", "").strip()

        ventana_editar = tk.Toplevel(ventana)
        ventana_editar.title(f"Editar gasto #{gasto_id}")
        ventana_editar.geometry("380x350")
        ventana_editar.resizable(True, True)

        tk.Label(
            ventana_editar,
            text=f"Editar Gasto #{gasto_id}",
            font=("Arial", 14, "bold")
        ).pack(pady=(15, 10))

        tk.Label(ventana_editar, text="Fecha:").pack()
        entrada_fecha_editar = tk.Entry(ventana_editar, width=25)
        entrada_fecha_editar.insert(0, fecha_actual)
        entrada_fecha_editar.pack(pady=(0, 10))

        tk.Label(ventana_editar, text="Categoría:").pack()
        combo_categoria_editar = ttk.Combobox(
            ventana_editar,
            values=CATEGORIAS,
            state="readonly",
            width=23
        )

        if categoria_actual in CATEGORIAS:
            combo_categoria_editar.set(categoria_actual)
        else:
            combo_categoria_editar.current(0)

        combo_categoria_editar.pack(pady=(0, 10))

        tk.Label(ventana_editar, text="Descripción:").pack()
        entrada_descripcion_editar = tk.Entry(ventana_editar, width=32)
        entrada_descripcion_editar.insert(0, descripcion_actual)
        entrada_descripcion_editar.pack(pady=(0, 10))

        tk.Label(ventana_editar, text="Monto ($):").pack()
        entrada_monto_editar = tk.Entry(ventana_editar, width=25)
        entrada_monto_editar.insert(0, monto_actual)
        entrada_monto_editar.pack(pady=(0, 15))

        def guardar_edicion_gasto():
            nueva_fecha = entrada_fecha_editar.get().strip()
            nueva_categoria = combo_categoria_editar.get().strip()
            nueva_descripcion = entrada_descripcion_editar.get().strip()
            nuevo_monto_texto = entrada_monto_editar.get().strip().replace(",", ".")

            if not nueva_fecha or not nueva_categoria or not nuevo_monto_texto:
                messagebox.showwarning(
                    "Falta información",
                    "Por favor, completa los campos requeridos."
                )
                return

            try:
                nuevo_monto = float(nuevo_monto_texto)
            except ValueError:
                messagebox.showerror(
                    "Monto inválido",
                    "El monto debe ser un número válido."
                )
                return

            if nuevo_monto <= 0:
                messagebox.showwarning(
                    "Monto inválido",
                    "El monto debe ser mayor que cero."
                )
                return

            try:
                actualizar_gasto(
                    gasto_id,
                    nueva_fecha,
                    nueva_categoria,
                    nueva_descripcion,
                    nuevo_monto
                )

                messagebox.showinfo(
                    "Gasto actualizado",
                    "El gasto se actualizó correctamente."
                )

                ventana_editar.destroy()
                cargar_gastos()

            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo actualizar el gasto:\n{error}"
                )

        tk.Button(
            ventana_editar,
            text="Guardar cambios",
            width=18,
            command=guardar_edicion_gasto
        ).pack(pady=5)

    # -------------------------
    # ELIMINAR GASTO
    # -------------------------

    def eliminar_gasto_accion():
        gasto_id = obtener_seleccion_gasto()
        if gasto_id is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el gasto #{gasto_id}?\n\nEsta acción no se puede deshacer."
        )

        if confirmar:
            try:
                eliminar_gasto(gasto_id)
                cargar_gastos()
                messagebox.showinfo(
                    "Gasto eliminado",
                    f"El gasto #{gasto_id} fue eliminado correctamente."
                )
            except Exception as error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el gasto:\n{error}"
                )

    # -------------------------
    # GUARDAR NUEVO GASTO
    # -------------------------

    def guardar():
        fecha = entrada_fecha.get().strip()
        categoria = combo_categoria.get().strip()
        descripcion = entrada_descripcion.get().strip()
        monto_texto = entrada_monto.get().strip().replace(",", ".")

        if not fecha:
            messagebox.showwarning("Falta información", "Ingrese la fecha.")
            return

        if not categoria:
            messagebox.showwarning("Falta información", "Seleccione una categoría.")
            return

        if not monto_texto:
            messagebox.showwarning("Falta información", "Ingrese el monto.")
            return

        try:
            monto = float(monto_texto)
        except ValueError:
            messagebox.showerror("Monto inválido", "El monto debe ser un número válido.")
            return

        if monto <= 0:
            messagebox.showwarning("Monto inválido", "El monto debe ser mayor que cero.")
            return

        try:
            guardar_gasto(fecha, categoria, descripcion, monto)

            messagebox.showinfo(
                "Gasto guardado",
                "El gasto se registró correctamente."
            )

            entrada_descripcion.delete(0, tk.END)
            entrada_monto.delete(0, tk.END)

            cargar_gastos()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar el gasto:\n{error}"
            )

    # -------------------------
    # BOTONES DE ACCIÓN
    # -------------------------

    marco_botones = tk.Frame(ventana)
    marco_botones.pack(pady=15)

    tk.Button(
        marco_botones,
        text="Guardar gasto",
        width=16,
        height=2,
        command=guardar
    ).grid(row=0, column=0, padx=6)

    tk.Button(
        marco_botones,
        text="Editar gasto",
        width=16,
        height=2,
        command=editar_gasto
    ).grid(row=0, column=1, padx=6)

    tk.Button(
        marco_botones,
        text="Eliminar gasto",
        width=16,
        height=2,
        command=eliminar_gasto_accion
    ).grid(row=0, column=2, padx=6)

    tk.Button(
        marco_botones,
        text="Actualizar",
        width=14,
        height=2,
        command=cargar_gastos
    ).grid(row=0, column=3, padx=6)

    tk.Button(
        marco_botones,
        text="Cerrar",
        width=12,
        height=2,
        command=ventana.destroy
    ).grid(row=0, column=4, padx=6)

    # Cargar datos iniciales
    cargar_gastos()