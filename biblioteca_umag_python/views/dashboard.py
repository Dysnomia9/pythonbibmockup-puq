# -*- coding: utf-8 -*-
"""
views/dashboard.py — Vista Dashboard del Sistema Bibliotecario UMAG
"""

import customtkinter as ctk
from config import *
from widgets import make_card, make_stat_card, make_section_header, darken


def build(parent: ctk.CTkFrame, icons: dict, personas_en_sala: int,
          capacidad: int, navigate_cb):
    """
    Construye el módulo Dashboard.
    navigate_cb(module_name) navega a otro módulo.
    """
    parent.grid_columnconfigure((0, 1), weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # ── Fila 0: KPI cards ──────────────────────────────────────
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    make_stat_card(stats, icons["badge_users"],  "Personas en Sala",
                   f"{personas_en_sala}/{capacidad}", UMAG_PURPLE,   0, 0)
    make_stat_card(stats, icons["badge_door"],   "Entradas Hoy",
                   "87",  ACCENT_TEAL,   0, 1)
    make_stat_card(stats, icons["badge_books"],  "Préstamos Activos",
                   "23",  ACCENT_AMBER,  0, 2)
    make_stat_card(stats, icons["badge_warning"],"Dev. Pendientes",
                   "5",   ACCENT_ROSE,   0, 3)

    # ── Fila 1: Barra de aforo ──────────────────────────────────
    cap_card = make_card(parent)
    cap_card.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=(0, 8))
    cap_card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(cap_card, text="", image=icons["badge_chart"]).grid(
        row=0, column=0, rowspan=2, padx=(14, 8), pady=14)

    pct = personas_en_sala / capacidad
    bar_color = SUCCESS if pct < 0.50 else (WARNING if pct < 0.80 else DANGER)

    inner = ctk.CTkFrame(cap_card, fg_color="transparent")
    inner.grid(row=0, column=1, rowspan=2, sticky="ew", padx=(0, 20), pady=14)
    inner.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(inner, text="Aforo de la Biblioteca",
                 font=FONT_SUBHEAD, text_color=TEXT_PRIMARY,
                 anchor="w").grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(inner,
                 text=f"{personas_en_sala} de {capacidad} personas  ({pct*100:.0f}%)",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY,
                 anchor="w").grid(row=1, column=0, sticky="w", pady=(2, 4))

    bar = ctk.CTkProgressBar(inner, height=16, corner_radius=8,
                              progress_color=bar_color, fg_color=UMAG_LIGHT)
    bar.grid(row=2, column=0, sticky="ew", pady=(0, 2))
    bar.set(pct)

    # ── Fila 2 izq: Acciones rápidas ────────────────────────────
    act_card = make_card(parent)
    act_card.grid(row=2, column=0, sticky="nsew", padx=(4, 4), pady=(0, 4))
    act_card.grid_columnconfigure((0, 1), weight=1)

    make_section_header(act_card, "Acciones Rápidas", row=0, colspan=2)

    actions = [
        ("Registrar Entrada", "F2", UMAG_PURPLE,   "entrada",   "btn_entrada",  1, 0),
        ("Préstamo de Libro", "F3", ACCENT_TEAL,   "prestamo",  "btn_prestamo", 1, 1),
        ("Reservar Sala",     "F4", ACCENT_AMBER,  "salas",     "btn_reportes", 2, 0),
        ("Gestionar Usuarios","",   ACCENT_ROSE,   "usuarios",  "btn_usuarios", 2, 1),
    ]
    for text, sc, color, module, icon_key, r, c in actions:
        label_text = f"{text}  {sc}" if sc else text
        btn = ctk.CTkButton(
            act_card, text=label_text,
            image=icons[icon_key], compound="left",
            font=("Segoe UI", 12, "bold"),
            height=68, corner_radius=12,
            fg_color=color, hover_color=darken(color),
            command=lambda m=module: navigate_cb(m),
        )
        btn.grid(row=r, column=c, padx=12, pady=5, sticky="ew")

    ctk.CTkLabel(act_card, text="").grid(row=3, pady=4)  # spacer

    # ── Fila 2 der: Requiere atención ───────────────────────────
    alert_card = make_card(parent)
    alert_card.grid(row=2, column=1, sticky="nsew", padx=(0, 4), pady=(0, 4))
    alert_card.grid_columnconfigure(0, weight=1)

    # Header con campana
    ah = ctk.CTkFrame(alert_card, fg_color="transparent")
    ah.grid(row=0, column=0, padx=20, pady=(16, 8), sticky="w")
    ctk.CTkLabel(ah, text="", image=icons["bell"]).pack(side="left", padx=(0, 8))
    ctk.CTkLabel(ah, text="Requiere Atención",
                 font=FONT_SUBHEAD, text_color=TEXT_PRIMARY).pack(side="left")

    alerts = [
        ("alert_warning", "3 préstamos vencidos sin devolver",    WARNING),
        ("alert_list",    "2 reservas de sala por confirmar",     INFO),
        ("alert_key",     "1 llave de casillero pendiente",       ACCENT_TEAL),
        ("alert_books",   "5 libros en reparación",               TEXT_SECONDARY),
    ]
    for i, (ik, text, color) in enumerate(alerts):
        row_f = ctk.CTkFrame(alert_card, fg_color="#F5F7FF",
                              corner_radius=8, height=40)
        row_f.grid(row=i + 1, column=0, sticky="ew", padx=14, pady=3)
        row_f.grid_propagate(False)
        row_f.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row_f, text="", image=icons[ik]).grid(
            row=0, column=0, padx=(12, 8), pady=8)
        ctk.CTkLabel(row_f, text=text, font=FONT_SMALL,
                     text_color=color, anchor="w").grid(row=0, column=1, sticky="w")

    ctk.CTkLabel(alert_card, text="").grid(row=6, pady=6)
