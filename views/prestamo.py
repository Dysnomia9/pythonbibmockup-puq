# -*- coding: utf-8 -*-
"""
views/prestamo.py — Vista de Gestión de Préstamos
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
from config import *
from widgets import (make_card, make_treeview_style, apply_table_stripes,
                     make_section_header, make_dialog, dialog_action_buttons,
                     labeled_entry, darken, icon_or_none)


def build(parent: ctk.CTkFrame, icons: dict, app_root):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # ── Barra de búsqueda ────────────────────────────────────────
    search_card = ctk.CTkFrame(parent, fg_color="#0D3B2E", corner_radius=12)
    search_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    search_card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(search_card, text="Buscar Usuario",
                 font=("Segoe UI", 13, "bold"), text_color="#6EE7B7").grid(
        row=0, column=0, columnspan=4, padx=20, pady=(14, 8), sticky="w")

    ctk.CTkLabel(search_card, text="RUT:", font=FONT_SUBHEAD,
                 text_color="#A7F3D0").grid(row=1, column=0, padx=(20, 8), pady=(0, 16))

    rut_entry = ctk.CTkEntry(
        search_card, placeholder_text="Ej: 12.345.678-5",
        height=40, font=("Consolas", 14),
        corner_radius=10,
        border_color="#059669",
        fg_color="#064E3B",
        text_color="#ECFDF5",
        placeholder_text_color="#6EE7B7",
    )
    rut_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 16))

    def _fmt(event):
        from config import format_rut
        val = rut_entry.get()
        fmt = format_rut(val)
        # Limitar a 12 caracteres (formato "12.345.678-5")
        if len(fmt) > 12:
            fmt = fmt[:12]
        rut_entry.delete(0, "end")
        rut_entry.insert(0, fmt)

    rut_entry.bind("<KeyRelease>", _fmt)

    def _buscar():
        rut = rut_entry.get().strip()
        if not rut:
            messagebox.showwarning("Atención", "Ingrese un RUT.")
            return
        messagebox.showinfo("Usuario encontrado",
                            f"RUT: {rut}\nNombre: María González\nTipo: Estudiante")

    _ic_search = icon_or_none(icons, "btn_search")
    ctk.CTkButton(
        search_card,
        text="  Buscar" if _ic_search else "Buscar",
        image=_ic_search, compound="left" if _ic_search else "none",
        font=("Segoe UI", 13, "bold"),
        width=120, height=40, corner_radius=10,
        fg_color=UMAG_PURPLE, hover_color=darken(UMAG_PURPLE),
        command=_buscar,
    ).grid(row=1, column=2, padx=5, pady=(0, 16))

    _ic_plus = icon_or_none(icons, "btn_plus")
    ctk.CTkButton(
        search_card,
        text="  Nuevo Préstamo" if _ic_plus else "Nuevo Préstamo",
        image=_ic_plus, compound="left" if _ic_plus else "none",
        font=("Segoe UI", 13),
        width=165, height=40, corner_radius=10,
        fg_color=SUCCESS, hover_color=darken(SUCCESS),
        command=lambda: _nuevo_prestamo(app_root, icons),
    ).grid(row=1, column=3, padx=(5, 20), pady=(0, 16))

    # ── Datos del usuario (mock) ─────────────────────────────────
    user_card = make_card(parent)
    user_card.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    user_card.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    uh = ctk.CTkFrame(user_card, fg_color=UMAG_LIGHT, corner_radius=0, height=38)
    uh.grid(row=0, column=0, columnspan=5, sticky="ew")
    uh.grid_propagate(False)
    ctk.CTkLabel(uh, text="  Datos del Usuario",
                 font=("Segoe UI", 11, "bold"), text_color=UMAG_PURPLE).place(x=14, rely=0.5, anchor="w")

    fields = [("RUT", "12.345.678-5"), ("Nombre", "María González"),
              ("Tipo", "Estudiante"), ("Carrera", "Ing. Informática"), ("Estado", "Activo")]
    for i, (label, val) in enumerate(fields):
        ctk.CTkLabel(user_card, text=label, font=FONT_SMALL,
                     text_color=TEXT_SECONDARY).grid(row=1, column=i, padx=14, pady=(8, 0))
        color = SUCCESS if val == "Activo" else TEXT_PRIMARY
        ctk.CTkLabel(user_card, text=val, font=("Segoe UI", 12, "bold"),
                     text_color=color).grid(row=2, column=i, padx=14, pady=(2, 12))

    # ── Tabla de préstamos ───────────────────────────────────────
    table_card = make_card(parent)
    table_card.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
    table_card.grid_columnconfigure(0, weight=1)
    table_card.grid_rowconfigure(1, weight=1)

    make_section_header(table_card, "Préstamos del Usuario", row=0)

    make_treeview_style("Prestamo")
    tf = ctk.CTkFrame(table_card, fg_color="transparent")
    tf.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
    tf.grid_columnconfigure(0, weight=1)
    tf.grid_rowconfigure(0, weight=1)

    cols = ("ID", "Libro", "Código", "F. Préstamo", "F. Devolución", "Estado")
    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="Prestamo.Treeview", height=6)
    tree.heading("ID",            text="#");            tree.column("ID",            width=36,  anchor="center")
    tree.heading("Libro",         text="Libro");         tree.column("Libro",         width=280)
    tree.heading("Código",        text="Código");        tree.column("Código",        width=120, anchor="center")
    tree.heading("F. Préstamo",   text="F. Préstamo");   tree.column("F. Préstamo",   width=100, anchor="center")
    tree.heading("F. Devolución", text="Devolución");    tree.column("F. Devolución", width=100, anchor="center")
    tree.heading("Estado",        text="Estado");        tree.column("Estado",        width=100, anchor="center")

    from config import MOCK_PRESTAMOS
    for p in MOCK_PRESTAMOS:
        tree.insert("", "end",
                    values=(p["id"], p["libro"], p["codigo"],
                            p["fecha_prestamo"], p["fecha_devolucion"], p["estado"]),
                    tags=(p["estado"].lower(),))

    tree.tag_configure("activo",   foreground=INFO,    background="#EFF8FF")
    tree.tag_configure("atrasado", foreground=DANGER,  background="#FEF2F2")
    tree.tag_configure("devuelto", foreground=SUCCESS, background="#F0FDF4")

    apply_table_stripes(tree)

    tree.grid(row=0, column=0, sticky="nsew")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    sb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=sb.set)


# ── Diálogo Nuevo Préstamo ────────────────────────────────────────
def _nuevo_prestamo(app_root, icons):
    dialog = make_dialog(app_root, "Nuevo Préstamo", width=460, height=360)

    card = make_card(dialog)
    card.pack(fill="both", expand=True, padx=18, pady=18)
    card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(card, text="Registrar Nuevo Préstamo",
                 font=("Segoe UI", 15, "bold"), text_color=UMAG_PURPLE).grid(
        row=0, column=0, columnspan=2, padx=20, pady=(18, 10), sticky="w")

    # RUT del usuario (con límite de caracteres)
    e_rut = labeled_entry(card, "RUT usuario:", 1, default="12.345.678-5",
                          placeholder="Ej: 12.345.678-5", font=("Consolas", 13))

    def _fmt_rut(event):
        from config import format_rut
        val = e_rut.get()
        fmt = format_rut(val)
        if len(fmt) > 12:
            fmt = fmt[:12]
        e_rut.delete(0, "end")
        e_rut.insert(0, fmt)
    e_rut.bind("<KeyRelease>", _fmt_rut)

    # Código de barras del libro (campo grande para lector)
    ctk.CTkLabel(card, text="Cód. barras libro:", font=FONT_BODY,
                 text_color=TEXT_PRIMARY).grid(
        row=2, column=0, padx=(20, 10), pady=6, sticky="w")
    e_codigo = ctk.CTkEntry(
        card,
        placeholder_text="Escanee o ingrese el código del libro",
        height=40,
        corner_radius=8,
        border_color=UMAG_PURPLE,
        border_width=2,
        font=("Consolas", 14),
    )
    e_codigo.grid(row=2, column=1, padx=(0, 20), pady=6, sticky="ew")

    e_dias = labeled_entry(card, "Días préstamo:", 3, default="14")

    def _confirmar():
        codigo = e_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Ingrese o escanee el código de barras del libro.")
            return
        messagebox.showinfo("Préstamo Registrado",
                            f"Préstamo registrado (demo)\n\n"
                            f"RUT: {e_rut.get()}\n"
                            f"Código libro: {codigo}\n"
                            f"Días: {e_dias.get()}")
        dialog.destroy()

    dialog_action_buttons(card, "Registrar", icon_or_none(icons, "btn_check"),
                          _confirmar, dialog.destroy, row=4)
