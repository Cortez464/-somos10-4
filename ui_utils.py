"""
ui_utils.py
-----------
Reemplazo "drop-in" para tkinter.messagebox.

PROBLEMA QUE RESUELVE
----------------------
En una app con varias ventanas (Toplevel), si al llamar a
messagebox.showinfo / showwarning / showerror / askyesno NO se indica
el argumento `parent`, Tkinter centra el cuadro de diálogo sobre la
ventana raíz oculta del programa (o sobre la pantalla), en vez de
sobre la ventana Toplevel que el usuario tiene abierta en ese momento.
Por eso el aviso "aparece en otro lugar" y cuesta encontrarlo, sobre
todo cuando hay varias ventanas abiertas a la vez.

SOLUCIÓN
--------
Este módulo detecta automáticamente cuál es la ventana activa
(la que tiene el foco) y se la pasa como `parent` al cuadro de
diálogo, para que siempre aparezca centrado sobre esa ventana.

CÓMO USARLO
-----------
En cualquier archivo que antes tenía:

    from tkinter import ttk, messagebox

Cámbialo por:

    from tkinter import ttk
    import ui_utils as messagebox

El resto del código NO cambia: messagebox.showinfo(...),
messagebox.showwarning(...), messagebox.showerror(...) y
messagebox.askyesno(...) se siguen llamando exactamente igual.
"""

import tkinter as tk
from tkinter import messagebox as _messagebox


def _ventana_activa():
    """
    Devuelve la ventana (Toplevel o raíz) que está actualmente
    enfocada, para usarla como 'parent' del cuadro de diálogo.
    Si no se puede determinar, devuelve la ventana raíz.
    """
    raiz = tk._default_root

    if raiz is None:
        return None

    try:
        widget_enfocado = raiz.focus_get()
    except Exception:
        widget_enfocado = None

    if widget_enfocado is not None:
        return widget_enfocado.winfo_toplevel()

    return raiz


def showinfo(titulo, mensaje, **kwargs):
    kwargs.setdefault("parent", _ventana_activa())
    return _messagebox.showinfo(titulo, mensaje, **kwargs)


def showwarning(titulo, mensaje, **kwargs):
    kwargs.setdefault("parent", _ventana_activa())
    return _messagebox.showwarning(titulo, mensaje, **kwargs)


def showerror(titulo, mensaje, **kwargs):
    kwargs.setdefault("parent", _ventana_activa())
    return _messagebox.showerror(titulo, mensaje, **kwargs)


def askyesno(titulo, mensaje, **kwargs):
    kwargs.setdefault("parent", _ventana_activa())
    return _messagebox.askyesno(titulo, mensaje, **kwargs)
