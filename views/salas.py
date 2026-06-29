# -*- coding: utf-8 -*-
"""
views/salas.py — Vista de Reserva de Salas de Estudio
Rediseño: celdas con estado visual claro, cabecera de sala con color,
selector de personas dinámico con campos RUT por persona.
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from config import *
from widgets import (make_card, make_stat_card, make_section_header,
                     make_dialog, dialog_action_buttons, labeled_entry, darken)

RUT_MAXLEN = 12  # "12.345.678-5"

# Paleta de estado de celdas
_COLOR_LIBRE    = "#10B981"   # esmeralda
_COLOR_OCUPADO  = "#BE185D"   # rosa
_COLOR_HOV_LIB  = "#059669"
_COLOR_HOV_OCP  = "#9D174D"


def build(parent: ctk.CTkFrame, icons: dict, app_root):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # ── KPI strip con fondos de color ────────────────────────────────────────
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    total_salas   = len(SALAS_CONFIG)
    total_bloques = total_salas * len(BLOQUES_HORARIOS)
    ocupados      = len(RESERVAS_MOCK)
    disponibles   = total_bloques - ocupados

    _kpi_colored(stats, icons["badge_list"],    "Total Salas",  total_salas,
                 UMAG_PURPLE, "#EEF2FF", 0)
    _kpi_colored(stats, icons["badge_check"],   "Disponibles",  disponibles,
                 SUCCESS,     "#F0FDF4", 1)
    _kpi_colored(stats, icons["badge_users"],   "Ocupadas",     ocupados,
                 ACCENT_ROSE, "#FFF1F2", 2)
    _kpi_colored(stats, icons["badge_trending"],"Uso del Día",
                 f"{ocupados*100//total_bloques}%",
                 ACCENT_TEAL, "#F0FDFA", 3)

    # ── Barra de controles: fecha + leyenda ──────────────────────
    ctrl = make_card(parent)
    ctrl.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    ctrl.grid_columnconfigure(2, weight=1)

    ctk.CTkLabel(ctrl, text="Fecha:", font=FONT_SUBHEAD,
                 text_color=TEXT_PRIMARY).grid(row=0, column=0, padx=(20, 8), pady=12)

    date_e = ctk.CTkEntry(ctrl, width=130, height=36, corner_radius=8,
                          border_color=BORDER_COLOR, font=("Consolas", 12))
    date_e.grid(row=0, column=1, pady=12)
    date_e.insert(0, datetime.now().strftime("%d/%m/%Y"))

    # Leyenda visual mejorada
    legend = ctk.CTkFrame(ctrl, fg_color="transparent")
    legend.grid(row=0, column=3, padx=20, pady=12)

    for col_l, (color, txt) in enumerate([
        (_COLOR_LIBRE,   "Libre"),
        (_COLOR_OCUPADO, "Ocupada"),
    ]):
        pip = ctk.CTkFrame(legend, width=12, height=12,
                           fg_color=color, corner_radius=6)
        pip.grid(row=0, column=col_l * 2,     padx=(0, 4))
        ctk.CTkLabel(legend, text=txt, font=FONT_SMALL,
                     text_color=TEXT_SECONDARY).grid(
            row=0, column=col_l * 2 + 1, padx=(0, 16))

    # ── Grid de salas ────────────────────────────────────────────
    grid_card = make_card(parent)
    grid_card.grid(row=2, column=0, sticky="nsew")
    grid_card.grid_columnconfigure(0, weight=1)
    grid_card.grid_rowconfigure(1, weight=1)

    # Cabecera de bloques horarios
    N_BLOQUES = len(BLOQUES_HORARIOS)
    hdr = ctk.CTkFrame(grid_card, fg_color="#EEF2FF", height=44, corner_radius=8)
    hdr.grid(row=0, column=0, sticky="ew", padx=6, pady=(8, 0))
    hdr.grid_propagate(False)
    hdr.grid_columnconfigure(0, weight=0, minsize=115)
    hdr.grid_columnconfigure(1, weight=0, minsize=44)
    for b in range(N_BLOQUES):
        hdr.grid_columnconfigure(b + 2, weight=1, minsize=96)

    ctk.CTkLabel(hdr, text="Sala", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_PURPLE).grid(row=0, column=0, padx=(14, 4), pady=10, sticky="w")
    ctk.CTkLabel(hdr, text="Cap.", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_PURPLE).grid(row=0, column=1, padx=4, pady=10)
    for b, blq in enumerate(BLOQUES_HORARIOS):
        ctk.CTkLabel(hdr, text=blq, font=("Segoe UI", 9, "bold"),
                     text_color=UMAG_PURPLE).grid(row=0, column=b + 2, padx=3, pady=10)

    # Scroll
    scroll = ctk.CTkScrollableFrame(grid_card, fg_color="transparent")
    scroll.grid(row=1, column=0, sticky="nsew", padx=6, pady=(4, 8))
    scroll.grid_columnconfigure(0, weight=0, minsize=115)
    scroll.grid_columnconfigure(1, weight=0, minsize=44)
    for b in range(N_BLOQUES):
        scroll.grid_columnconfigure(b + 2, weight=1, minsize=96)

    _fill_grid(scroll, icons, app_root)


def _fill_grid(scroll: ctk.CTkScrollableFrame, icons: dict, app_root):
    for s_idx, sala in enumerate(SALAS_CONFIG):
        # Nombre de sala — fondo alternado
        row_bg = "#F8FAFF" if s_idx % 2 == 0 else CARD_BG
        name_f = ctk.CTkFrame(scroll, fg_color=row_bg, corner_radius=0, height=36)
        name_f.grid(row=s_idx, column=0, padx=(2, 2), pady=1, sticky="nsew")
        name_f.grid_propagate(False)
        ctk.CTkLabel(name_f, text=sala["nombre"],
                     font=("Segoe UI", 10, "bold"),
                     text_color=UMAG_PURPLE if s_idx < 5 else TEXT_PRIMARY,
                     anchor="w").place(x=10, rely=0.5, anchor="w")

        # Capacidad
        cap_f = ctk.CTkFrame(scroll, fg_color=row_bg, corner_radius=0, height=36)
        cap_f.grid(row=s_idx, column=1, padx=1, pady=1, sticky="nsew")
        cap_f.grid_propagate(False)
        ctk.CTkLabel(cap_f, text=str(sala["capacidad"]),
                     font=("Consolas", 10), text_color=TEXT_SECONDARY).place(
            relx=0.5, rely=0.5, anchor="center")

        # Celdas de bloque
        for b_idx in range(len(BLOQUES_HORARIOS)):
            key = (sala["id"], b_idx)
            if key in RESERVAS_MOCK:
                res = RESERVAS_MOCK[key]
                _cell_ocupada(scroll, res, sala, s_idx, b_idx)
            else:
                _cell_libre(scroll, icons, app_root, sala,
                            BLOQUES_HORARIOS[b_idx], s_idx, b_idx)


def _cell_libre(scroll, icons, app_root, sala, bloque, row, col):
    """Celda disponible — verde con checkmark."""
    btn = ctk.CTkButton(
        scroll,
        text="✓ Libre",
        font=("Segoe UI", 9, "bold"),
        height=32, corner_radius=6,
        fg_color=_COLOR_LIBRE,
        hover_color=_COLOR_HOV_LIB,
        text_color="white",
        command=lambda s=sala, b=bloque: _reservar(app_root, icons, s, b),
    )
    btn.grid(row=row, column=col + 2, padx=3, pady=3, sticky="ew")


def _cell_ocupada(scroll, res, sala, row, col):
    """Celda ocupada — roja con iniciales."""
    parts   = res["nombre"].split()
    initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else parts[0][:2].upper()
    btn = ctk.CTkButton(
        scroll,
        text=f"● {initials}",
        font=("Segoe UI", 9, "bold"),
        height=32, corner_radius=6,
        fg_color=_COLOR_OCUPADO,
        hover_color=_COLOR_HOV_OCP,
        text_color="white",
        command=lambda r=res, s=sala: messagebox.showinfo(
            "Reserva Ocupada",
            f"Sala: {s['nombre']}\n"
            f"Reservada por: {r['nombre']}\n"
            f"RUT: {r['rut']}"),
    )
    btn.grid(row=row, column=col + 2, padx=3, pady=3, sticky="ew")


def _apply_rut_format(entry: ctk.CTkEntry, event=None):
    from config import format_rut
    raw = entry.get()
    fmt = format_rut(raw)
    if len(fmt) > RUT_MAXLEN:
        fmt = fmt[:RUT_MAXLEN]
    entry.delete(0, "end")
    entry.insert(0, fmt)


def _reservar(app_root, icons, sala: dict, bloque: str):
    cap        = sala["capacidad"]
    dlg_height = min(580, 400 + max(0, cap - 1) * 42)
    dialog     = make_dialog(app_root, "Reservar Sala", width=490, height=dlg_height)

    outer = make_card(dialog)
    outer.pack(fill="both", expand=True, padx=18, pady=18)
    outer.grid_columnconfigure(1, weight=1)

    # Encabezado con color de módulo
    head = ctk.CTkFrame(outer, fg_color=ACCENT_AMBER, corner_radius=10, height=52)
    head.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 0))
    head.grid_propagate(False)
    ctk.CTkLabel(head,
                 text=f"🚪  {sala['nombre']}  ·  {bloque}  ·  máx {cap} personas",
                 font=("Segoe UI", 12, "bold"), text_color="white").place(
        x=16, rely=0.5, anchor="w")

    # Selector cantidad
    ctk.CTkLabel(outer, text="Número de personas:", font=FONT_BODY,
                 text_color=TEXT_PRIMARY).grid(
        row=1, column=0, padx=(20, 10), pady=(14, 6), sticky="w")

    cantidad_var = ctk.StringVar(value="1")
    opciones     = [str(i) for i in range(1, cap + 1)]
    ctk.CTkOptionMenu(
        outer, values=opciones, variable=cantidad_var,
        width=100, height=34,
        fg_color=UMAG_PURPLE, button_color=darken(UMAG_PURPLE),
        font=FONT_BODY,
    ).grid(row=1, column=1, padx=(0, 20), pady=(14, 6), sticky="w")

    # Separador
    ctk.CTkFrame(outer, height=1, fg_color=BORDER_COLOR).grid(
        row=2, column=0, columnspan=2, sticky="ew", padx=14, pady=4)

    # Contenedor RUTs
    rut_container = ctk.CTkScrollableFrame(outer, fg_color="#F8FAFF",
                                           corner_radius=8, height=190)
    rut_container.grid(row=3, column=0, columnspan=2, sticky="ew",
                       padx=14, pady=(0, 4))
    rut_container.grid_columnconfigure(1, weight=1)

    rut_entries: list[ctk.CTkEntry] = []

    def _rebuild(*_):
        for w in rut_container.winfo_children():
            w.destroy()
        rut_entries.clear()
        try:
            n = int(cantidad_var.get())
        except ValueError:
            n = 1
        for i in range(n):
            lbl_txt = "RUT:" if n == 1 else f"RUT persona {i+1}:"
            ctk.CTkLabel(rut_container, text=lbl_txt,
                         font=FONT_BODY, text_color=TEXT_PRIMARY).grid(
                row=i, column=0, padx=(12, 8), pady=5, sticky="w")
            e = ctk.CTkEntry(
                rut_container,
                placeholder_text="12.345.678-5",
                height=34, corner_radius=8,
                border_color=UMAG_PURPLE, border_width=1,
                font=("Consolas", 13),
            )
            e.grid(row=i, column=1, padx=(0, 12), pady=5, sticky="ew")
            e.bind("<KeyRelease>", lambda ev, entry=e: _apply_rut_format(entry, ev))
            rut_entries.append(e)

    _rebuild()
    cantidad_var.trace_add("write", _rebuild)

    def _confirmar():
        ruts   = [e.get().strip() for e in rut_entries]
        vacios = [r for r in ruts if not r]
        if vacios:
            messagebox.showwarning("Atención",
                                   f"Ingrese el RUT de todas las personas ({len(vacios)} faltante/s).")
            return
        resumen = "\n".join(f"  Persona {i+1}: {r}" for i, r in enumerate(ruts))
        messagebox.showinfo("Reserva Confirmada",
                            f"✔ {sala['nombre']} reservada (demo)\n"
                            f"Bloque: {bloque}\n\nRUTs:\n{resumen}")
        dialog.destroy()

    dialog_action_buttons(outer, "Confirmar", icons.get("btn_check"),
                          _confirmar, dialog.destroy, row=4)


# ── Helper: KPI card cuadrada con fondo de color ─────────────────────────────
def _kpi_colored(parent, badge_icon, label: str, value, color: str, bg: str, col: int):
    """Tarjeta KPI con fondo suave, borde de color y badge cuadrado."""
    card = ctk.CTkFrame(parent, fg_color=bg, corner_radius=12,
                        border_width=1, border_color=color)
    card.grid(row=0, column=col, sticky="nsew", padx=5, pady=4)
    card.grid_columnconfigure(0, weight=1)

    # Badge cuadrado con ícono
    badge_f = ctk.CTkFrame(card, width=42, height=42,
                           fg_color=color, corner_radius=8)
    badge_f.grid(row=0, column=0, padx=(14, 0), pady=(14, 6), sticky="w")
    badge_f.grid_propagate(False)
    if badge_icon is not None:
        ctk.CTkLabel(badge_f, text="", image=badge_icon).place(
            relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card, text=label, font=("Segoe UI", 10),
                 text_color=color, anchor="w").grid(
        row=1, column=0, padx=14, sticky="w")
    ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 20, "bold"),
                 text_color=color, anchor="w").grid(
        row=2, column=0, padx=14, pady=(0, 14), sticky="w")
