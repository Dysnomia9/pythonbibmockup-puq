# -*- coding: utf-8 -*-
"""
views/entrada.py — Vista de Registro de Entrada
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from widgets import (make_card, make_mini_stat, make_treeview_style,
                     make_section_header, darken, icon_or_none)


def build(parent: ctk.CTkFrame, icons: dict,
          personas_en_sala: int, capacidad: int):

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_rowconfigure(0, weight=1)

    # ── Panel izquierdo ─────────────────────────────────────────
    left = ctk.CTkFrame(parent, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(2, weight=1)

    # Mini stats aforo
    aforo_card = make_card(left)
    aforo_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    aforo_card.grid_columnconfigure((0, 1, 2), weight=1)
    make_mini_stat(aforo_card, icon_or_none(icons, "badge_users"), "En Sala",
                   f"{personas_en_sala}/{capacidad}", UMAG_PURPLE, 0)
    make_mini_stat(aforo_card, icon_or_none(icons, "badge_door"),  "Entradas Hoy",
                   "87", ACCENT_TEAL, 1)
    make_mini_stat(aforo_card, icon_or_none(icons, "badge_check"), "Disponibles",
                   f"{capacidad - personas_en_sala}", SUCCESS, 2)

    # Formulario RUT
    rut_card = make_card(left)
    rut_card.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    rut_card.grid_columnconfigure(1, weight=1)

    make_section_header(rut_card, "Registrar Entrada", row=0, colspan=4)

    ctk.CTkLabel(rut_card, text="RUT:", font=FONT_SUBHEAD,
                 text_color=TEXT_PRIMARY).grid(row=1, column=0, padx=(20, 8), pady=(0, 14))

    rut_entry = ctk.CTkEntry(
        rut_card, placeholder_text="Ej: 12.345.678-5",
        height=40, font=("Consolas", 14),
        corner_radius=10, border_color=BORDER_COLOR,
    )
    rut_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 14))

    def _format_rut(event):
        from config import format_rut
        val = rut_entry.get()
        fmt = format_rut(val)
        rut_entry.delete(0, "end")
        rut_entry.insert(0, fmt)

    rut_entry.bind("<KeyRelease>", _format_rut)

    def _registrar():
        from config import validar_rut
        rut = rut_entry.get().strip()
        if not rut:
            messagebox.showwarning("Atención", "Ingrese un RUT.")
            return
        if not validar_rut(rut):
            messagebox.showerror("RUT inválido", f"El RUT «{rut}» no es válido.")
            return
        messagebox.showinfo("Entrada Registrada",
                            f"Entrada registrada.\n\nRUT: {rut}\n"
                            f"Hora: {datetime.now().strftime('%H:%M')}")
        rut_entry.delete(0, "end")

    _ic_check = icon_or_none(icons, "btn_check")
    ctk.CTkButton(
        rut_card,
        text="  Registrar" if _ic_check else "Registrar",
        image=_ic_check, compound="left" if _ic_check else "none",
        font=("Segoe UI", 13, "bold"),
        width=140, height=40, corner_radius=10,
        fg_color=SUCCESS, hover_color=darken(SUCCESS),
        command=_registrar,
    ).grid(row=1, column=2, padx=5, pady=(0, 14))

    _ic_qr = icon_or_none(icons, "btn_qr")
    ctk.CTkButton(
        rut_card,
        text="  Lector QR" if _ic_qr else "Lector QR",
        image=_ic_qr, compound="left" if _ic_qr else "none",
        font=("Segoe UI", 12),
        width=110, height=40, corner_radius=10,
        fg_color=UMAG_PURPLE, hover_color=darken(UMAG_PURPLE),
        command=lambda: messagebox.showinfo("QR", "Simulación: Escáner QR activado."),
    ).grid(row=1, column=3, padx=(5, 20), pady=(0, 14))

    # Tabla de entradas
    table_card = make_card(left)
    table_card.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
    table_card.grid_columnconfigure(0, weight=1)
    table_card.grid_rowconfigure(1, weight=1)

    make_section_header(table_card, "Registros del Día", row=0)

    make_treeview_style("Entrada")
    tf = ctk.CTkFrame(table_card, fg_color="transparent")
    tf.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
    tf.grid_columnconfigure(0, weight=1)
    tf.grid_rowconfigure(0, weight=1)

    cols = ("N°", "Hora", "RUT", "Nombre", "Vía")
    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="Entrada.Treeview", height=8)
    tree.heading("N°",     text="N°");     tree.column("N°",     width=46, anchor="center")
    tree.heading("Hora",   text="Hora");   tree.column("Hora",   width=70, anchor="center")
    tree.heading("RUT",    text="RUT");    tree.column("RUT",    width=130, anchor="center")
    tree.heading("Nombre", text="Nombre"); tree.column("Nombre", width=200)
    tree.heading("Vía",    text="Vía");    tree.column("Vía",    width=110, anchor="center")

    from config import MOCK_ENTRADAS
    for e in MOCK_ENTRADAS:
        tree.insert("", "end", values=(e["id"], e["hora"], e["rut"], e["nombre"], e["via"]))

    tree.grid(row=0, column=0, sticky="nsew")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    sb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=sb.set)

    # ── Panel derecho (ficha de estado) ─────────────────────────
    right = make_card(parent, width=270)
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_propagate(False)
    right.grid_columnconfigure(0, weight=1)

    # Header coloreado
    hdr = ctk.CTkFrame(right, fg_color=UMAG_PURPLE, corner_radius=14, height=44)
    hdr.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
    hdr.grid_propagate(False)
    hdr.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(hdr, text="Panel de Operación",
                 font=("Segoe UI", 12, "bold"), text_color="white").place(
        relx=0.5, rely=0.5, anchor="center")

    def _sep(row):
        ctk.CTkFrame(right, height=1, fg_color=BORDER_COLOR).grid(
            row=row, column=0, sticky="ew", padx=16, pady=4)

    ctk.CTkLabel(right, text="N° REGISTRO", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).grid(row=1, column=0, pady=(14, 0))
    ctk.CTkLabel(right, text="395", font=("Consolas", 36, "bold"),
                 text_color=UMAG_PURPLE).grid(row=2, column=0)

    _sep(3)

    ctk.CTkLabel(right, text="AFORO ACTUAL", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_INDIGO).grid(row=4, column=0, pady=(10, 4))

    pct = personas_en_sala / capacidad
    bar_color = SUCCESS if pct < 0.5 else WARNING
    ctk.CTkLabel(right, text=str(personas_en_sala),
                 font=("Consolas", 50, "bold"), text_color=UMAG_PURPLE).grid(row=5, column=0)
    ctk.CTkLabel(right, text=f"de {capacidad} personas",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(row=6, column=0, pady=(0, 6))

    bar = ctk.CTkProgressBar(right, height=14, corner_radius=7,
                              progress_color=bar_color, fg_color=UMAG_LIGHT, width=190)
    bar.grid(row=7, column=0, pady=(0, 10))
    bar.set(pct)

    _sep(8)

    _ic_circle = icon_or_none(icons, "circle_green")
    st = ctk.CTkFrame(right, fg_color="transparent")
    st.grid(row=9, column=0, pady=(8, 4))
    if _ic_circle:
        ctk.CTkLabel(st, text="", image=_ic_circle).pack(side="left", padx=(0, 6))
    ctk.CTkLabel(st, text="OPERATIVO", font=("Segoe UI", 14, "bold"),
                 text_color=SUCCESS).pack(side="left")

    _sep(10)
    ctk.CTkLabel(right, text="ÚLTIMO INGRESO", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_INDIGO).grid(row=11, column=0, pady=(10, 2))
    ctk.CTkLabel(right, text="María González",
                 font=("Segoe UI", 12, "bold"), text_color=TEXT_PRIMARY).grid(row=12, column=0)
    ctk.CTkLabel(right, text="10:15 — Manual",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(row=13, column=0, pady=(0, 14))
