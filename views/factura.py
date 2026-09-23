import os
import sys
import subprocess
import platform
from datetime import datetime

import ui_utils as messagebox

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from database.database import obtener_detalle_pedido


# =========================================================
# CARPETA DONDE SE GUARDAN LAS FACTURAS
# =========================================================

CARPETA_FACTURAS = "facturas"


# =========================================================
# GENERAR EL PDF DE LA FACTURA
# =========================================================

def generar_factura_pdf(pedido_id):
    """
    Genera el PDF de la factura del pedido indicado y
    devuelve la ruta del archivo creado.

    Lanza una excepción si el pedido no existe o si algo
    falla al generar el archivo.
    """

    pedido, prendas = obtener_detalle_pedido(pedido_id)

    if pedido is None:
        raise ValueError("No se encontró el pedido.")

    os.makedirs(CARPETA_FACTURAS, exist_ok=True)

    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    nombre_archivo = f"Factura_Pedido_{pedido_id}.pdf"
    ruta_archivo = os.path.join(CARPETA_FACTURAS, nombre_archivo)

    documento = SimpleDocTemplate(
        ruta_archivo,
        pagesize=letter,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloFactura",
        parent=estilos["Title"],
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=2
    )

    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Normal"],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=14
    )

    estilo_normal = estilos["Normal"]

    estilo_total = ParagraphStyle(
        "Total",
        parent=estilos["Normal"],
        fontSize=13,
        alignment=TA_RIGHT,
        fontName="Helvetica-Bold"
    )

    elementos = []

    # -----------------------------------------------------
    # ENCABEZADO
    # -----------------------------------------------------

    elementos.append(Paragraph("SOMOS 10-4", estilo_titulo))
    elementos.append(Paragraph("Servicio de lavandería", estilo_subtitulo))

    elementos.append(
        Paragraph(f"<b>FACTURA - PEDIDO #{pedido_id}</b>", estilos["Heading2"])
    )

    elementos.append(
        Paragraph(f"Fecha de emisión: {fecha_generacion}", estilo_normal)
    )

    elementos.append(Spacer(1, 12))

    # -----------------------------------------------------
    # DATOS DEL CLIENTE Y DEL PEDIDO
    # -----------------------------------------------------

    estado_pago = "PAGADO" if pedido[7] else "PENDIENTE"

    datos_cliente = [
        ["Cliente:", pedido[1] or ""],
        ["Teléfono:", pedido[2] or "No registrado"],
        ["Fecha de recepción:", pedido[3] or ""],
        ["Fecha de entrega:", pedido[4] or "No definida"],
        ["Estado del pedido:", pedido[5] or ""],
        ["Estado de pago:", estado_pago],
    ]

    tabla_cliente = Table(datos_cliente, colWidths=[4.5 * cm, 10.5 * cm])

    tabla_cliente.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
        ])
    )

    elementos.append(tabla_cliente)
    elementos.append(Spacer(1, 18))

    # -----------------------------------------------------
    # TABLA DE PRENDAS
    # -----------------------------------------------------

    encabezado_prendas = ["Prenda", "Cantidad", "Precio unitario", "Subtotal"]

    filas_prendas = [encabezado_prendas]

    for prenda in prendas:
        filas_prendas.append([
            prenda[0],
            str(prenda[1]),
            f"${float(prenda[2]):.2f}",
            f"${float(prenda[3]):.2f}"
        ])

    tabla_prendas = Table(
        filas_prendas,
        colWidths=[6.5 * cm, 3 * cm, 3.5 * cm, 3 * cm]
    )

    tabla_prendas.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E293B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F4F6F9")]),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ])
    )

    elementos.append(tabla_prendas)
    elementos.append(Spacer(1, 16))

    # -----------------------------------------------------
    # TOTAL
    # -----------------------------------------------------

    elementos.append(
        Paragraph(f"TOTAL A PAGAR: ${float(pedido[6]):.2f}", estilo_total)
    )

    elementos.append(Spacer(1, 20))

    # -----------------------------------------------------
    # OBSERVACIONES
    # -----------------------------------------------------

    observaciones = pedido[8] if pedido[8] else "Sin observaciones"

    elementos.append(Paragraph("<b>Observaciones:</b>", estilo_normal))
    elementos.append(Paragraph(observaciones, estilo_normal))
    elementos.append(Spacer(1, 30))

    elementos.append(
        Paragraph(
            "Gracias por confiar en SOMOS 10-4.",
            estilo_subtitulo
        )
    )

    documento.build(elementos)

    return ruta_archivo


# =========================================================
# ENVIAR EL ARCHIVO A LA IMPRESORA / ABRIRLO PARA IMPRIMIR
# =========================================================

def _abrir_o_imprimir(ruta_archivo):
    """
    Intenta enviar el PDF directamente a la impresora
    predeterminada (comando 'lp' en Linux/macOS). Si no hay
    impresora configurada o el comando falla, abre el archivo
    con el visor de PDF predeterminado para que el usuario lo
    imprima manualmente (Ctrl+P).
    """

    sistema = platform.system()

    if sistema == "Linux":

        try:

            resultado = subprocess.run(
                ["lp", ruta_archivo],
                capture_output=True,
                text=True,
                timeout=10
            )

            if resultado.returncode == 0:
                return True, "enviado_impresora"

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        # No se pudo imprimir directamente: abrir con el visor
        try:
            subprocess.Popen(["xdg-open", ruta_archivo])
            return True, "abierto_visor"
        except FileNotFoundError:
            return False, "sin_visor"

    elif sistema == "Windows":

        try:
            os.startfile(ruta_archivo, "print")
            return True, "enviado_impresora"
        except Exception:
            try:
                os.startfile(ruta_archivo)
                return True, "abierto_visor"
            except Exception:
                return False, "sin_visor"

    elif sistema == "Darwin":

        try:
            subprocess.run(["lpr", ruta_archivo], check=True, timeout=10)
            return True, "enviado_impresora"
        except Exception:
            try:
                subprocess.Popen(["open", ruta_archivo])
                return True, "abierto_visor"
            except Exception:
                return False, "sin_visor"

    return False, "sistema_no_soportado"


# =========================================================
# FUNCIÓN PRINCIPAL: IMPRIMIR FACTURA DE UN PEDIDO
# =========================================================

def imprimir_factura(ventana_padre, pedido_id):
    """
    Genera la factura en PDF del pedido y la envía a imprimir.
    Muestra mensajes de confirmación o error al usuario.
    """

    try:

        ruta_archivo = generar_factura_pdf(pedido_id)

    except ValueError as e:

        messagebox.showerror("Error", str(e))
        return

    except Exception as e:

        messagebox.showerror(
            "Error",
            f"No se pudo generar la factura.\n\n{e}"
        )
        return

    exito, resultado = _abrir_o_imprimir(ruta_archivo)

    if resultado == "enviado_impresora":

        messagebox.showinfo(
            "Factura enviada",
            f"La factura del pedido #{pedido_id} se envió "
            f"a la impresora predeterminada.\n\n"
            f"Archivo guardado en:\n{ruta_archivo}"
        )

    elif resultado == "abierto_visor":

        messagebox.showinfo(
            "Factura generada",
            f"No se encontró una impresora configurada.\n\n"
            f"Se abrió la factura del pedido #{pedido_id} en el "
            f"visor de PDF; puedes imprimirla desde ahí (Ctrl+P).\n\n"
            f"Archivo guardado en:\n{ruta_archivo}"
        )

    else:

        messagebox.showwarning(
            "Factura generada",
            f"La factura se generó correctamente pero no se pudo "
            f"abrir automáticamente.\n\n"
            f"Ábrela manualmente desde:\n{ruta_archivo}"
        )
