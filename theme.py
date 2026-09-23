import tkinter as tk
from tkinter import ttk

# =========================================================
# PALETA DE COLORES MODERNA (Slate System)
# =========================================================
COLORS = {
    "bg": "#F8FAFC",             # Fondo principal (Slate 50)
    "card_bg": "#FFFFFF",        # Fondo de tarjetas/contenedores
    "card_border": "#E2E8F0",    # Borde suave
    "text_main": "#0F172A",      # Texto principal (Slate 900)
    "text_muted": "#64748B",     # Texto secundario (Slate 500)
    
    # Acciones
    "primary": "#2563EB",        # Azul moderno
    "primary_hover": "#1D4ED8",
    "secondary": "#475569",      # Slate oscuro
    "secondary_hover": "#334155",
    "danger": "#DC2626",         # Rojo
    "danger_hover": "#B91C1C",
    "success": "#10B981",        # Esmeralda / Verde
    "warning": "#F59E0B",        # Ámbar / Amarillo
    
    # Tablas
    "table_header": "#F1F5F9",
    "table_alt_row": "#F8FAFC",
    "table_select": "#E0E7FF"
}

FONTS = {
    "h1": ("Segoe UI", 20, "bold"),
    "h2": ("Segoe UI", 15, "bold"),
    "h3": ("Segoe UI", 12, "bold"),
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    "metric_value": ("Segoe UI", 22, "bold")
}


def aplicar_estilo_global(root):
    """Aplica la configuración global de ttk.Style"""
    style = ttk.Style(root)
    style.theme_use("clam")

    # Configuración de Fondo de la Ventana Root
    root.configure(bg=COLORS["bg"])

    # TTK Frame
    style.configure("TFrame", background=COLORS["bg"])
    style.configure("Card.TFrame", background=COLORS["card_bg"], relief="flat")

    # TTK Label
    style.configure("TLabel", background=COLORS["bg"], foreground=COLORS["text_main"], font=FONTS["body"])
    style.configure("Muted.TLabel", foreground=COLORS["text_muted"], font=FONTS["small"])
    style.configure("Title.TLabel", font=FONTS["h1"], foreground=COLORS["text_main"])
    style.configure("Subtitle.TLabel", font=FONTS["body"], foreground=COLORS["text_muted"])

    # TTK Entry y Combobox
    style.configure("TEntry", fieldbackground="#FFFFFF", foreground=COLORS["text_main"], padding=6)
    style.configure("TCombobox", fieldbackground="#FFFFFF", foreground=COLORS["text_main"], padding=5)

    # TTK Treeview (Tablas)
    style.configure(
        "Treeview",
        background="#FFFFFF",
        foreground=COLORS["text_main"],
        rowheight=32,
        fieldbackground="#FFFFFF",
        font=FONTS["body"],
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background=COLORS["table_header"],
        foreground=COLORS["text_main"],
        font=FONTS["body_bold"],
        relief="flat",
        padding=8
    )
    style.map("Treeview", background=[("selected", COLORS["table_select"])], foreground=[("selected", COLORS["text_main"])])


def crear_tarjeta(parent, title="", value="", bg_color=None):
    """Crea un contenedor tipo tarjeta moderna con borde y sombra visual"""
    card = tk.Frame(
        parent,
        bg=bg_color if bg_color else COLORS["card_bg"],
        highlightbackground=COLORS["card_border"],
        highlightthickness=1,
        bd=0,
        padx=18,
        pady=16
    )
    if title:
        lbl_title = tk.Label(
            card,
            text=title,
            font=FONTS["small"],
            bg=bg_color if bg_color else COLORS["card_bg"],
            fg=COLORS["text_muted"]
        )
        lbl_title.pack(anchor="w")

    if value is not None:
        lbl_val = tk.Label(
            card,
            text=value,
            font=FONTS["metric_value"],
            bg=bg_color if bg_color else COLORS["card_bg"],
            fg=COLORS["text_main"]
        )
        lbl_val.pack(anchor="w", pady=(4, 0))

    return card, lbl_val if value is not None else None


def crear_boton_moderno(parent, text, command, style_type="primary", width=None, height=None):
    """Crea botones limpios con efecto hover"""
    bg = COLORS["primary"]
    fg = "#FFFFFF"
    active_bg = COLORS["primary_hover"]

    if style_type == "secondary":
        bg = COLORS["secondary"]
        active_bg = COLORS["secondary_hover"]
    elif style_type == "danger":
        bg = COLORS["danger"]
        active_bg = COLORS["danger_hover"]
    elif style_type == "outline":
        bg = "#FFFFFF"
        fg = COLORS["text_main"]
        active_bg = COLORS["table_header"]

    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=FONTS["body_bold"],
        bg=bg,
        fg=fg,
        activebackground=active_bg,
        activeforeground=fg,
        bd=0,
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=8
    )

    if style_type == "outline":
        btn.config(highlightbackground=COLORS["card_border"], highlightthickness=1)

    return btn