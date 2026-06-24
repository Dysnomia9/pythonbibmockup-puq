# -*- coding: utf-8 -*-
"""
views/salas.py — Vista de Reserva de Salas de Estudio
La grilla se construye de forma diferida (after_idle) para evitar el lag
al cambiar de pestaña.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from config import *
from widgets import (make_card, make_stat_card, make_section_header,
                     make_dialog, dialog_action_buttons, labeled_entry, darken)


def build(parent: ctk.CTkFrame, icons: dict, app_root):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # ── KPI stats ────────────────────────────────────────────────
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    total_salas   = len(SALAS_CONFIG)
    total_bloques = total_salas * len(BLOQUES_HORARIOS)
    ocupados      = len(RESERVAS_MOCK)
    disponibles   = total_bloques - ocupados

    make_stat_card(stats, icons["badge_list"],    "Total Salas",    total_salas,   UMAG_PURPLE,  0, 0)
    make_stat_card(stats, icons["badge_check"],   "Disponibles",    disponibles,   SUCCESS,      0, 1)
    make_stat_card(stats, icons["badge_users"],   "Ocupadas",       ocupados,      ACCENT_ROSE,  0, 2)
    make_stat_card(stats, icons["badge_trending"],"Uso del Día",
                   f"{ocupados*100//total_bloques}%", ACCENT_TEAL, 0, 3)

    # ── Selector de fecha + leyenda ──────────────────────────────
    ctrl = make_card(parent)
    ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    ctrl.grid_columnconfigure(2, weight=1)

    ctk.CTkLabel(ctrl, text="Fecha:", font=FONT_SUBHEAD,
                 text_color=TEXT_PRIMARY).grid(row=0, column=0, padx=(20, 8), pady=12)

    date_e = ctk.CTkEntry(ctrl, width=130, height=36, corner_radius=8,
                           border_color=BORDER_COLOR, font=("Consolas", 12))
    date_e.grid(row=0, column=1, pady=12)
    date_e.insert(0, datetime.now().strftime("%d/%m/%Y"))

    legend = ctk.CTkFrame(ctrl, fg_color="transparent")
    legend.grid(row=0, column=3, padx=20, pady=12)

    ctk.CTkFrame(legend, width=14, height=14, corner_radius=4,
                 fg_color=ACCENT_EMERALD).grid(row=0, column=0, padx=(0, 4))
    ctk.CTkLabel(legend, text="Disponible", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).grid(row=0, column=1, padx=(0, 14))
    ctk.CTkFrame(legend, width=14, height=14, corner_radius=4,
                 fg_color=ACCENT_ROSE).grid(row=0, column=2, padx=(0, 4))
    ctk.CTkLabel(legend, text="Ocupada", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).grid(row=0, column=3)

    # ── Contenedor principal de la grilla ───────────────────────
    grid_card = make_card(parent)
    grid_card.grid(row=2, column=0, sticky="nsew")
    grid_card.grid_columnconfigure(0, weight=1)
    grid_card.grid_rowconfigure(1, weight=1)

    # Cabecera fija de bloques horarios
    hdr = ctk.CTkFrame(grid_card, fg_color=UMAG_LIGHT, height=40, corner_radius=0)
    hdr.grid(row=0, column=0, sticky="ew")
    hdr.grid_propagate(False)
    hdr.grid_columnconfigure(0, weight=0, minsize=110)
    hdr.grid_columnconfigure(1, weight=0, minsize=46)
    for b in range(len(BLOQUES_HORARIOS)):
        hdr.grid_columnconfigure(b + 2, weight=1, minsize=95)

    ctk.CTkLabel(hdr, text="Sala", font=("Segoe UI", 11, "bold"),
                 text_color=UMAG_PURPLE_DARK).grid(row=0, column=0, padx=(14, 4), pady=9, sticky="w")
    ctk.CTkLabel(hdr, text="Cap.", font=("Segoe UI", 11, "bold"),
                 text_color=UMAG_PURPLE_DARK).grid(row=0, column=1, padx=4, pady=9)
    for b, blq in enumerate(BLOQUES_HORARIOS):
        ctk.CTkLabel(hdr, text=blq, font=("Segoe UI", 9, "bold"),
                     text_color=UMAG_PURPLE_DARK).grid(row=0, column=b + 2, padx=3, pady=9)

    # Área scrollable — se llena de forma diferida para evitar lag
    scroll = ctk.CTkScrollableFrame(grid_card, fg_color="transparent")
    scroll.grid(row=1, column=0, sticky="nsew", padx=4, pady=(0, 8))
    scroll.grid_columnconfigure(0, weight=0, minsize=110)
    scroll.grid_columnconfigure(1, weight=0, minsize=46)
    for b in range(len(BLOQUES_HORARIOS)):
        scroll.grid_columnconfigure(b + 2, weight=1, minsize=95)

    # Diferir la construcción de la grilla para que no bloquee la UI
    parent.after_idle(lambda: _fill_grid(scroll, icons, app_root))


def _fill_grid(scroll: ctk.CTkScrollableFrame, icons: dict, app_root):
    """Llena la grilla de salas de forma lazy (llamado vía after_idle)."""
    CHUNK = 5  # filas por ciclo de evento

    def _render_chunk(start: int):
        end = min(start + CHUNK, len(SALAS_CONFIG))
        for s_idx in range(start, end):
            sala = SALAS_CONFIG[s_idx]

            ctk.CTkLabel(scroll, text=sala["nombre"],
                         font=("Segoe UI", 11, "bold" if s_idx < 5 else "normal"),
                         text_color=TEXT_PRIMARY, anchor="w").grid(
                row=s_idx, column=0, padx=(14, 4), pady=3, sticky="w")

            ctk.CTkLabel(scroll, text=str(sala["capacidad"]),
                         font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(
                row=s_idx, column=1, padx=4, pady=3)

            for b_idx in range(len(BLOQUES_HORARIOS)):
                key = (sala["id"], b_idx)
                if key in RESERVAS_MOCK:
                    res = RESERVAS_MOCK[key]
                    btn = ctk.CTkButton(
                        scroll, text=res["nombre"][:12],
                        font=("Segoe UI", 9), height=28, corner_radius=6,
                        fg_color=ACCENT_ROSE, hover_color=darken(ACCENT_ROSE),
                        text_color="white",
                        command=lambda r=res, s=sala: messagebox.showinfo(
                            "Reserva Ocupada",
                            f"Sala: {s['nombre']}\nReservada por: {r['nombre']}\nRUT: {r['rut']}"),
                    )
                else:
                    btn = ctk.CTkButton(
                        scroll, text="Libre",
                        font=("Segoe UI", 9), height=28, corner_radius=6,
                        fg_color=ACCENT_EMERALD, hover_color=darken(ACCENT_EMERALD),
                        text_color="white",
                        command=lambda s=sala, b=BLOQUES_HORARIOS[b_idx]: _reservar(
                            app_root, icons, s, b),
                    )
                btn.grid(row=s_idx, column=b_idx + 2, padx=3, pady=3, sticky="ew")

        if end < len(SALAS_CONFIG):
            scroll.after(10, lambda: _render_chunk(end))

    _render_chunk(0)


def _reservar(app_root, icons, sala: dict, bloque: str):
    dialog = make_dialog(app_root, "Reservar Sala", width=420, height=310)

    card = make_card(dialog)
    card.pack(fill="both", expand=True, padx=18, pady=18)
    card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(card, text=f"Reservar {sala['nombre']}",
                 font=("Segoe UI", 15, "bold"), text_color=UMAG_PURPLE).grid(
        row=0, column=0, columnspan=2, padx=20, pady=(18, 2), sticky="w")
    ctk.CTkLabel(card, text=f"Bloque: {bloque}  ·  Capacidad: {sala['capacidad']} personas",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(
        row=1, column=0, columnspan=2, padx=20, pady=(0, 12), sticky="w")

    e_rut  = labeled_entry(card, "RUT:",    2, placeholder="Ej: 12.345.678-5")
    e_name = labeled_entry(card, "Nombre:", 3)

    def _confirmar():
        if not e_rut.get().strip():
            messagebox.showwarning("Atención", "Ingrese un RUT.")
            return
        messagebox.showinfo("Reserva Confirmada",
                            f"{sala['nombre']} reservada (demo)\n"
                            f"Bloque: {bloque}\nRUT: {e_rut.get()}")
        dialog.destroy()

    dialog_action_buttons(card, "Confirmar", icons["btn_check"],
                          _confirmar, dialog.destroy, row=4)
