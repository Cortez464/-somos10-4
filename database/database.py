import sqlite3
import shutil
from pathlib import Path
from datetime import datetime


# --------------------------------------------------
# RUTAS DEL PROYECTO
# --------------------------------------------------

CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATOS = CARPETA_PROYECTO / "data"

CARPETA_DATOS.mkdir(exist_ok=True)

NOMBRE_BASE_DATOS = CARPETA_DATOS / "somos10_4.db"

CARPETA_BACKUPS = CARPETA_PROYECTO / "backups"
MAX_BACKUPS = 10


def respaldar_base_datos():
    """
    Copia la base de datos actual a la carpeta 'backups' con
    fecha y hora en el nombre. Conserva solo los MAX_BACKUPS
    respaldos mas recientes para no llenar el disco.
    """
    if not NOMBRE_BASE_DATOS.exists():
        return

    CARPETA_BACKUPS.mkdir(exist_ok=True)

    marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = CARPETA_BACKUPS / f"somos10_4_{marca_tiempo}.db"

    shutil.copy2(NOMBRE_BASE_DATOS, destino)

    respaldos = sorted(CARPETA_BACKUPS.glob("somos10_4_*.db"))
    while len(respaldos) > MAX_BACKUPS:
        respaldos[0].unlink()
        respaldos.pop(0)

# --------------------------------------------------
# CONEXIÓN
# --------------------------------------------------

def conectar():
    return sqlite3.connect(NOMBRE_BASE_DATOS)


# --------------------------------------------------
# CREAR BASE DE DATOS
# --------------------------------------------------

def crear_base_datos():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT,
            observaciones TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            fecha_recepcion TEXT NOT NULL,
            fecha_entrega TEXT,
            estado TEXT NOT NULL DEFAULT 'Recibido',
            total REAL NOT NULL DEFAULT 0,
            pagado INTEGER NOT NULL DEFAULT 0,
            observaciones TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            prenda TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            monto REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS costos_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            concepto TEXT NOT NULL,
            monto REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos creada correctamente.")
    print(f"Ubicación: {NOMBRE_BASE_DATOS}")


# --------------------------------------------------
# CLIENTES
# --------------------------------------------------

def guardar_cliente(nombre, telefono, direccion, observaciones):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nombre, telefono, direccion, observaciones)
        VALUES (?, ?, ?, ?)
    """, (
        nombre,
        telefono,
        direccion,
        observaciones
    ))

    conexion.commit()
    conexion.close()


def obtener_clientes():

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT
            id,
            nombre,
            telefono,
            direccion,
            observaciones
        FROM clientes
        ORDER BY id DESC
    """)

    clientes = cursor.fetchall()

    conexion.close()

    return clientes


def actualizar_cliente(id_cliente, nombre, telefono, direccion, observaciones):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE clientes
        SET nombre = ?,
            telefono = ?,
            direccion = ?,
            observaciones = ?
        WHERE id = ?
    """, (
        nombre,
        telefono,
        direccion,
        observaciones,
        id_cliente
    ))

    conexion.commit()
    conexion.close()


def eliminar_cliente(id_cliente):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id = ?
    """, (id_cliente,))

    conexion.commit()
    conexion.close()


# --------------------------------------------------
# PEDIDOS
# --------------------------------------------------

def guardar_pedido_completo(
    cliente_id,
    fecha_recepcion,
    fecha_entrega,
    observaciones,
    total,
    prendas
):

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO pedidos
            (
                cliente_id,
                fecha_recepcion,
                fecha_entrega,
                estado,
                total,
                pagado,
                observaciones
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente_id,
            fecha_recepcion,
            fecha_entrega,
            "Recibido",
            total,
            0,
            observaciones
        ))

        pedido_id = cursor.lastrowid

        for prenda in prendas:

            cursor.execute("""
                INSERT INTO detalle_pedido
                (
                    pedido_id,
                    prenda,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                pedido_id,
                prenda["nombre"],
                prenda["cantidad"],
                prenda["precio_unitario"],
                prenda["subtotal"]
            ))

        conexion.commit()

        return pedido_id

    except Exception:

        conexion.rollback()
        raise

    finally:

        conexion.close()


def guardar_pedido(
    cliente_id,
    fecha_recepcion,
    fecha_entrega,
    observaciones
):

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO pedidos
        (
            cliente_id,
            fecha_recepcion,
            fecha_entrega,
            observaciones
        )
        VALUES (?, ?, ?, ?)
    """, (
        cliente_id,
        fecha_recepcion,
        fecha_entrega,
        observaciones
    ))

    pedido_id = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return pedido_id


# --------------------------------------------------
# COSTOS DE PEDIDOS
# --------------------------------------------------

def guardar_costo_pedido(
    pedido_id,
    concepto,
    monto
):

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO costos_pedido
            (
                pedido_id,
                concepto,
                monto
            )
            VALUES (?, ?, ?)
        """, (
            pedido_id,
            concepto,
            monto
        ))

        conexion.commit()

    except Exception:

        conexion.rollback()
        raise

    finally:

        conexion.close()


def obtener_costos_pedido(pedido_id):

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                concepto,
                monto
            FROM costos_pedido
            WHERE pedido_id = ?
            ORDER BY id ASC
        """, (pedido_id,))

        return cursor.fetchall()

    finally:

        conexion.close()


def obtener_costo_total_pedido(pedido_id):
    """
    Calcula automáticamente el costo total
    asociado a un pedido.
    """

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                COALESCE(SUM(monto), 0)
            FROM costos_pedido
            WHERE pedido_id = ?
        """, (pedido_id,))

        resultado = cursor.fetchone()[0]

        return float(resultado)

    finally:

        conexion.close()


def obtener_ganancia_pedido(pedido_id):
    """
    Calcula la ganancia de un pedido:

    Ganancia = Total cobrado - Costos del pedido
    """

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                COALESCE(total, 0)
            FROM pedidos
            WHERE id = ?
        """, (pedido_id,))

        resultado = cursor.fetchone()

        if resultado is None:
            return 0.0

        total_pedido = float(resultado[0])

    finally:

        conexion.close()

    costo_total = obtener_costo_total_pedido(
        pedido_id
    )

    ganancia = total_pedido - costo_total

    return ganancia


def obtener_resumen_financiero_pedido(pedido_id):
    """
    Devuelve un resumen financiero completo
    de un pedido.
    """

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                total
            FROM pedidos
            WHERE id = ?
        """, (pedido_id,))

        resultado = cursor.fetchone()

        if resultado is None:

            return {
                "total": 0.0,
                "costo_total": 0.0,
                "ganancia": 0.0
            }

        total = float(resultado[0])

    finally:

        conexion.close()

    costo_total = obtener_costo_total_pedido(
        pedido_id
    )

    ganancia = total - costo_total

    return {
        "total": total,
        "costo_total": costo_total,
        "ganancia": ganancia
    }


# --------------------------------------------------
# DATOS PARA DASHBOARD
# --------------------------------------------------

def obtener_resumen_dashboard(periodo="Todo"):

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        # --------------------------------
        # DEFINIR FILTRO DE FECHAS
        # --------------------------------

        filtro_fecha = ""
        parametros = ()

        if periodo == "Hoy":

            filtro_fecha = """
                AND DATE(fecha_recepcion)
                    = DATE('now', 'localtime')
            """

        elif periodo == "Esta semana":

            filtro_fecha = """
                AND DATE(fecha_recepcion)
                    >= DATE('now', 'localtime', '-6 days')
            """

        elif periodo == "Este mes":

            filtro_fecha = """
                AND strftime('%Y-%m', fecha_recepcion)
                    = strftime('%Y-%m', 'now', 'localtime')
            """

        # --------------------------------
        # PEDIDOS REGISTRADOS
        # --------------------------------

        cursor.execute(f"""
            SELECT COUNT(*)
            FROM pedidos
            WHERE 1=1
            {filtro_fecha}
        """, parametros)

        pedidos_registrados = cursor.fetchone()[0]

        # --------------------------------
        # VENTAS
        # --------------------------------

        cursor.execute(f"""
            SELECT COALESCE(SUM(total), 0)
            FROM pedidos
            WHERE 1=1
            {filtro_fecha}
        """, parametros)

        ventas = float(
            cursor.fetchone()[0]
        )

        # --------------------------------
        # GASTOS GENERALES
        # --------------------------------

        if periodo == "Hoy":

            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM gastos
                WHERE DATE(fecha)
                    = DATE('now', 'localtime')
            """)

        elif periodo == "Esta semana":

            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM gastos
                WHERE DATE(fecha)
                    >= DATE('now', 'localtime', '-6 days')
            """)

        elif periodo == "Este mes":

            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM gastos
                WHERE strftime('%Y-%m', fecha)
                    = strftime('%Y-%m', 'now', 'localtime')
            """)

        else:

            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM gastos
            """)

        gastos = float(
            cursor.fetchone()[0]
        )

        # --------------------------------
        # COSTOS DE PEDIDOS
        # --------------------------------

        if periodo == "Todo":

            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0)
                FROM costos_pedido
            """)

        else:

            cursor.execute(f"""
                SELECT COALESCE(SUM(cp.monto), 0)
                FROM costos_pedido cp

                INNER JOIN pedidos p
                    ON cp.pedido_id = p.id

                WHERE 1=1
                {filtro_fecha}
            """, parametros)

        costos_pedidos = float(
            cursor.fetchone()[0]
        )

        # --------------------------------
        # GANANCIA
        # --------------------------------

        ganancia = (
            ventas
            - gastos
            - costos_pedidos
        )

        # --------------------------------
        # PEDIDOS PENDIENTES
        # --------------------------------

        cursor.execute(f"""
            SELECT COUNT(*)
            FROM pedidos
            WHERE estado != 'Entregado'
            {filtro_fecha}
        """, parametros)

        pedidos_pendientes = cursor.fetchone()[0]

        # --------------------------------
        # PEDIDOS ENTREGADOS
        # --------------------------------

        cursor.execute(f"""
            SELECT COUNT(*)
            FROM pedidos
            WHERE estado = 'Entregado'
            {filtro_fecha}
        """, parametros)

        pedidos_entregados = cursor.fetchone()[0]

        # --------------------------------
        # DINERO PENDIENTE DE COBRO
        # --------------------------------

        cursor.execute(f"""
            SELECT COALESCE(SUM(total), 0)
            FROM pedidos
            WHERE pagado = 0
            {filtro_fecha}
        """, parametros)

        dinero_pendiente = float(
            cursor.fetchone()[0]
        )

        # --------------------------------
        # RESULTADO
        # --------------------------------

        return {
            "pedidos_registrados": pedidos_registrados,
            "ventas": ventas,
            "gastos": gastos,
            "costos_pedidos": costos_pedidos,
            "ganancia": ganancia,
            "pedidos_pendientes": pedidos_pendientes,
            "pedidos_entregados": pedidos_entregados,
            "dinero_pendiente": dinero_pendiente
        }

    finally:

        conexion.close()


# --------------------------------------------------
# PEDIDOS - LISTADO Y GESTIÓN
# --------------------------------------------------

def obtener_pedidos():
    """
    Obtiene todos los pedidos junto con el nombre del cliente.
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                p.id,
                c.nombre,
                p.fecha_recepcion,
                p.fecha_entrega,
                p.estado,
                p.total,
                p.pagado,
                p.observaciones
            FROM pedidos p
            INNER JOIN clientes c
                ON p.cliente_id = c.id
            ORDER BY p.id DESC
        """)

        return cursor.fetchall()

    finally:
        conexion.close()


def actualizar_estado(pedido_id, nuevo_estado):
    """
    Cambia el estado de un pedido.
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET estado = ?
            WHERE id = ?
        """, (nuevo_estado, pedido_id))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def actualizar_pagado(pedido_id, pagado):
    """
    Marca un pedido como pagado o pendiente.
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET pagado = ?
            WHERE id = ?
        """, (pagado, pedido_id))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def actualizar_pedido_completo(
    pedido_id,
    cliente_id,
    fecha_recepcion,
    fecha_entrega,
    observaciones,
    total,
    prendas
):
    """
    Actualiza un pedido existente por completo: cliente,
    fechas, observaciones, total y las prendas del detalle
    (se reemplaza el detalle anterior por el nuevo).
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE pedidos
            SET cliente_id = ?,
                fecha_recepcion = ?,
                fecha_entrega = ?,
                observaciones = ?,
                total = ?
            WHERE id = ?
        """, (
            cliente_id,
            fecha_recepcion,
            fecha_entrega,
            observaciones,
            total,
            pedido_id
        ))

        cursor.execute(
            "DELETE FROM detalle_pedido WHERE pedido_id = ?",
            (pedido_id,)
        )

        for prenda in prendas:

            cursor.execute("""
                INSERT INTO detalle_pedido
                (
                    pedido_id,
                    prenda,
                    cantidad,
                    precio_unitario,
                    subtotal
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                pedido_id,
                prenda["nombre"],
                prenda["cantidad"],
                prenda["precio_unitario"],
                prenda["subtotal"]
            ))

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def eliminar_pedido(pedido_id):
    """
    Elimina un pedido junto con su detalle y sus costos asociados.
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM detalle_pedido WHERE pedido_id = ?",
            (pedido_id,)
        )

        try:
            cursor.execute(
                "DELETE FROM costos_pedido WHERE pedido_id = ?",
                (pedido_id,)
            )
        except Exception:
            pass

        cursor.execute(
            "DELETE FROM pedidos WHERE id = ?",
            (pedido_id,)
        )

        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        conexion.close()


def obtener_detalle_pedido(pedido_id):
    """
    Obtiene la información completa de un pedido.
    """

    conexion = conectar()

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                p.id,
                c.nombre,
                c.telefono,
                p.fecha_recepcion,
                p.fecha_entrega,
                p.estado,
                p.total,
                p.pagado,
                p.observaciones,
                p.cliente_id
            FROM pedidos p
            INNER JOIN clientes c
                ON p.cliente_id = c.id
            WHERE p.id = ?
        """, (pedido_id,))

        pedido = cursor.fetchone()

        cursor.execute("""
            SELECT
                prenda,
                cantidad,
                precio_unitario,
                subtotal
            FROM detalle_pedido
            WHERE pedido_id = ?
            ORDER BY id ASC
        """, (pedido_id,))

        prendas = cursor.fetchall()

        return pedido, prendas

    finally:
        conexion.close()

# --------------------------------------------------
# REPORTES DETALLADOS
# --------------------------------------------------

def obtener_reporte_detallado(periodo="Todo"):
    """
    Obtiene métricas detalladas para el módulo de reportes:
    - Top prendas/servicios más solicitados.
    - Top clientes con más ingresos.
    - Gastos acumulados por categoría.
    """
    conexion = conectar()

    try:
        cursor = conexion.cursor()

        filtro_pedidos = ""
        filtro_gastos = ""

        if periodo == "Hoy":
            filtro_pedidos = "WHERE DATE(p.fecha_recepcion) = DATE('now', 'localtime')"
            filtro_gastos = "WHERE DATE(fecha) = DATE('now', 'localtime')"
        elif periodo == "Esta semana":
            filtro_pedidos = "WHERE DATE(p.fecha_recepcion) >= DATE('now', 'localtime', '-6 days')"
            filtro_gastos = "WHERE DATE(fecha) >= DATE('now', 'localtime', '-6 days')"
        elif periodo == "Este mes":
            filtro_pedidos = "WHERE strftime('%Y-%m', p.fecha_recepcion) = strftime('%Y-%m', 'now', 'localtime')"
            filtro_gastos = "WHERE strftime('%Y-%m', fecha) = strftime('%Y-%m', 'now', 'localtime')"

        # Top 5 Prendas
        cursor.execute(f"""
            SELECT 
                dp.prenda, 
                SUM(dp.cantidad) AS total_cant, 
                SUM(dp.subtotal) AS total_monto
            FROM detalle_pedido dp
            INNER JOIN pedidos p ON dp.pedido_id = p.id
            {filtro_pedidos}
            GROUP BY dp.prenda
            ORDER BY total_cant DESC
            LIMIT 5
        """)
        top_prendas = cursor.fetchall()

        # Top 5 Clientes
        cursor.execute(f"""
            SELECT 
                c.nombre, 
                COUNT(p.id) AS num_pedidos, 
                COALESCE(SUM(p.total), 0) AS total_facturado
            FROM clientes c
            INNER JOIN pedidos p ON c.id = p.cliente_id
            {filtro_pedidos}
            GROUP BY c.id
            ORDER BY total_facturado DESC
            LIMIT 5
        """)
        top_clientes = cursor.fetchall()

        # Gastos por Categoría
        cursor.execute(f"""
            SELECT 
                categoria, 
                COALESCE(SUM(monto), 0) AS total_categoria
            FROM gastos
            {filtro_gastos}
            GROUP BY categoria
            ORDER BY total_categoria DESC
        """)
        gastos_categoria = cursor.fetchall()

        return {
            "top_prendas": top_prendas,
            "top_clientes": top_clientes,
            "gastos_categoria": gastos_categoria
        }

    finally:
        conexion.close()
        
# --------------------------------------------------
# PRUEBA DIRECTA
# --------------------------------------------------

if __name__ == "__main__":

    crear_base_datos()