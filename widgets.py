# -*- coding: utf-8 -*-
"""
widgets.py — Componentes y helpers reutilizables del Sistema Bibliotecario UMAG
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from config import *


# ============================================================
# FIX: grab_set seguro para Python 3.14+
# El problema ocurre porque CTkToplevel no está completamente
# renderizado cuando se llama grab_set(). Solución: diferir.
# ============================================================
def safe_grab_set(dialog: ctk.CTkToplevel, delay: int = 150):
    """Aplica grab_set solo cuando la ventana ya es visible."""
    def _do_grab():
        try:
            dialog.grab_set()
        except Exception:
            dialog.after(100, _do_grab)
    dialog.after(delay, _do_grab)


# ============================================================
# COMPONENTES BASE
# ============================================================
def make_card(parent, **kwargs) -> ctk.CTkFrame:
    """Tarjeta blanca con borde sutil y esquinas redondeadas."""
    return ctk.CTkFrame(
        parent,
        fg_color=CARD_BG,
        corner_radius=14,
        border_width=1,
        border_color=BORDER_COLOR,
        **kwargs,
    )


def make_section_header(parent, text: str, row: int = 0, col: int = 0, colspan: int = 1):
    """Título de sección con línea decorativa izquierda."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=row, column=col, columnspan=colspan,
               padx=20, pady=(16, 8), sticky="w")

    accent = ctk.CTkFrame(frame, width=4, height=22,
                          fg_color=UMAG_INDIGO, corner_radius=2)
    accent.pack(side="left", padx=(0, 10))
    ctk.CTkLabel(frame, text=text, font=FONT_SUBHEAD,
                 text_color=TEXT_PRIMARY).pack(side="left")
    return frame


def make_stat_card(parent, badge_icon, title: str, value, color: str,
                   row: int = 0, col: int = 0) -> ctk.CTkFrame:
    """Tarjeta de estadística con icono badge, título y valor."""
    card = make_card(parent)
    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(card, text="", image=badge_icon).grid(
        row=0, column=0, rowspan=2, padx=14, pady=14)

    ctk.CTkLabel(card, text=title, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY, anchor="w").grid(
        row=0, column=1, sticky="sw", padx=(0, 14), pady=(14, 1))

    ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 24, "bold"),
                 text_color=color, anchor="w").grid(
        row=1, column=1, sticky="nw", padx=(0, 14), pady=(0, 14))
    return card


def make_mini_stat(parent, badge_icon, label: str, value, color: str, col: int):
    """Estadística pequeña para paneles compactos."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=0, column=col, padx=14, pady=12)
    ctk.CTkLabel(frame, text="", image=badge_icon).pack(pady=(0, 4))
    ctk.CTkLabel(frame, text=label, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack()
    ctk.CTkLabel(frame, text=str(value), font=("Segoe UI", 18, "bold"),
                 text_color=color).pack()


def make_treeview_style(style_name: str):
    """Aplica estilo visual consistente a un Treeview."""
    style = ttk.Style()
    style.theme_use('clam')
    style.configure(
        f"{style_name}.Treeview",
        background=CARD_BG,
        fieldbackground=CARD_BG,
        foreground=TEXT_PRIMARY,
        font=("Segoe UI", 11),
        rowheight=34,
        borderwidth=0,
    )
    style.configure(
        f"{style_name}.Treeview.Heading",
        background=UMAG_LIGHT,
        foreground=UMAG_PURPLE_DARK,
        font=("Segoe UI", 11, "bold"),
        borderwidth=0,
        relief="flat",
    )
    style.map(f"{style_name}.Treeview",
              background=[("selected", "#DBEAFE")])


def darken(hex_color: str, factor: float = 0.82) -> str:
    """Oscurece un color hex por un factor dado."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"#{max(0,int(r*factor)):02x}{max(0,int(g*factor)):02x}{max(0,int(b*factor)):02x}"


# ============================================================
# DIÁLOGOS REUTILIZABLES
# ============================================================
def make_dialog(parent, title: str, width: int = 460, height: int = 360) -> ctk.CTkToplevel:
    """
    Crea un CTkToplevel centrado con grab_set diferido (fix Python 3.14+).
    Retorna el dialog listo para agregar widgets.
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.configure(fg_color=BG_MAIN)
    dialog.resizable(False, False)

    # Esperar a que la ventana esté lista antes de grab_set
    def _center_and_grab():
        dialog.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        safe_grab_set(dialog)

    dialog.after(50, _center_and_grab)
    return dialog


def dialog_action_buttons(parent, confirm_text: str, confirm_icon,
                           on_confirm, on_cancel, row: int = 99):
    """Fila de botones Confirmar / Cancelar para diálogos."""
    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.grid(row=row, column=0, columnspan=2, pady=18)

    ctk.CTkButton(
        btn_frame, text=f"  {confirm_text}",
        image=confirm_icon, compound="left",
        font=("Segoe UI", 13, "bold"),
        width=150, height=40, corner_radius=10,
        fg_color=SUCCESS, hover_color=darken(SUCCESS),
        command=on_confirm,
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        btn_frame, text="Cancelar",
        font=("Segoe UI", 13),
        width=140, height=40, corner_radius=10,
        fg_color="#6B7280", hover_color="#4B5563",
        command=on_cancel,
    ).pack(side="left", padx=8)


def labeled_entry(parent, label: str, row: int,
                  default: str = "", placeholder: str = "",
                  font=None) -> ctk.CTkEntry:
    """Campo con etiqueta alineada a la izquierda."""
    ctk.CTkLabel(parent, text=label, font=font or FONT_BODY,
                 text_color=TEXT_PRIMARY).grid(
        row=row, column=0, padx=(22, 10), pady=7, sticky="w")
    entry = ctk.CTkEntry(
        parent, height=38, corner_radius=9,
        border_color=BORDER_COLOR,
        placeholder_text=placeholder,
        font=font or FONT_BODY,
    )
    entry.grid(row=row, column=1, padx=(0, 22), pady=7, sticky="ew")
    if default:
        entry.insert(0, default)
    return entry
