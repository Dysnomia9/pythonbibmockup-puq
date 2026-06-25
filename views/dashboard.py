# -*- coding: utf-8 -*-
"""
views/dashboard.py — Dashboard rediseñado 2026
Cambios: sin panel "Acciones Rápidas" propio.
En su lugar: fila de 4 botones de acceso rápido con color sólido por módulo.
"""

import tkinter as tk
import customtkinter as ctk
from config import *
from widgets import make_card, make_stat_card, make_section_header, darken


# ── Colores y metadatos de cada botón de acceso rápido ─────────────────────
_QUICK_ACTIONS = [
    # (módulo,      label,              sublabel,              color_fondo,  ícono_texto)
    ("entrada",   "Registro entrada",  "F2 · acceso rápido",  ACCENT_TEAL,  "→"),
    ("prestamo",  "Préstamos",         "23 activos ahora",    ACCENT_AMBER, "→"),
    ("salas",     "Reserva de salas",  "F4 · 12 disponibles", "#7C3AED",   "→"),
    ("reportes",  "Reportes",          "Estadísticas del día", ACCENT_ROSE, "→"),
]


def build(parent: ctk.CTkFrame, icons: dict, personas_en_sala: int,
          capacidad: int, navigate_cb):
    parent.grid_columnconfigure((0, 1), weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # ── Fila 0: KPI cards ──────────────────────────────────────
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    _kpi_card(stats, icons, "badge_users",   "Personas en sala",
              f"{personas_en_sala}/{capacidad}", UMAG_PURPLE,  0, 0,
              sub=f"{personas_en_sala*100//capacidad}% de aforo")
    _kpi_card(stats, icons, "badge_door",    "Entradas hoy",
              "87", ACCENT_TEAL,   0, 1, sub="+12% vs ayer")
    _kpi_card(stats, icons, "badge_books",   "Préstamos activos",
              "23", ACCENT_AMBER,  0, 2, sub="2 vencen hoy")
    _kpi_card(stats, icons, "badge_warning", "Dev. pendientes",
              "5",  ACCENT_ROSE,   0, 3, sub="3 con atraso")

    # ── Fila 1: Botones acceso rápido ──────────────────────────
    qa_frame = ctk.CTkFrame(parent, fg_color="transparent")
    qa_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    qa_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    for col, (module, label, sublabel, color, _arrow) in enumerate(_QUICK_ACTIONS):
        _quick_btn(qa_frame, label, sublabel, color, row=0, col=col,
                   command=lambda m=module: navigate_cb(m))

    # ── Fila 2 izq: Aforo + gráfico semanal ────────────────────
    left_card = make_card(parent)
    left_card.grid(row=2, column=0, sticky="nsew", padx=(0, 6), pady=(0, 4))
    left_card.grid_columnconfigure(0, weight=1)
    left_card.grid_rowconfigure(2, weight=1)

    make_section_header(left_card, "Aforo de la Biblioteca", row=0)

    # Barra de aforo
    aforo_f = ctk.CTkFrame(left_card, fg_color="transparent")
    aforo_f.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
    aforo_f.grid_columnconfigure(0, weight=1)

    pct = personas_en_sala / capacidad
    bar_color = SUCCESS if pct < 0.50 else (WARNING if pct < 0.80 else DANGER)

    # Número grande + meta
    nums_f = ctk.CTkFrame(aforo_f, fg_color="transparent")
    nums_f.grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(
        nums_f, text=str(personas_en_sala),
        font=("Segoe UI", 30, "bold"), text_color=UMAG_PURPLE,
    ).pack(side="left")
    ctk.CTkLabel(
        nums_f, text=f" / {capacidad}",
        font=("Segoe UI", 18), text_color=TEXT_SECONDARY,
    ).pack(side="left", pady=(6, 0))
    ctk.CTkLabel(
        aforo_f, text=f"{pct*100:.0f}% ocupado",
        font=FONT_SMALL, text_color=TEXT_SECONDARY,
    ).grid(row=0, column=1, sticky="e")

    bar = ctk.CTkProgressBar(
        aforo_f, height=8, corner_radius=4,
        progress_color=bar_color, fg_color=UMAG_LIGHT,
    )
    bar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 0))
    bar.set(pct)

    # Leyenda
    leg_f = ctk.CTkFrame(aforo_f, fg_color="transparent")
    leg_f.grid(row=2, column=0, columnspan=2, sticky="w", pady=(6, 0))
    _legend_dot(leg_f, UMAG_PURPLE, f"Ocupados ({personas_en_sala})", 0)
    _legend_dot(leg_f, BORDER_COLOR, f"Disponibles ({capacidad - personas_en_sala})", 1)

    # Gráfico de asistencia semanal
    make_section_header(left_card, "Asistencia Semanal", row=2)

    chart_f = ctk.CTkFrame(left_card, fg_color="transparent")
    chart_f.grid(row=3, column=0, sticky="nsew", padx=16, pady=(0, 14))
    chart_f.grid_columnconfigure(0, weight=1)
    chart_f.grid_rowconfigure(0, weight=1)

    canvas = tk.Canvas(chart_f, bg=CARD_BG, highlightthickness=0, height=130)
    canvas.grid(row=0, column=0, sticky="ew")

    PALETTE = [UMAG_PURPLE, UMAG_PURPLE, UMAG_PURPLE, UMAG_PURPLE,
               UMAG_PURPLE, BORDER_COLOR, BORDER_COLOR]

    def _draw(event=None):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 50 or h < 30:
            return
        pad_x, pad_y = 30, 24
        max_val = max(d["entradas"] for d in MOCK_ASISTENCIA)
        n       = len(MOCK_ASISTENCIA)
        bar_w   = (w - pad_x * 2) / n - 6

        for i in range(5):
            gy = pad_y + (h - pad_y * 2) * i / 4
            canvas.create_line(pad_x, gy, w - pad_x, gy,
                               fill="#F3F4F6", width=1)

        for i, d in enumerate(MOCK_ASISTENCIA):
            x     = pad_x + i * (bar_w + 6)
            bar_h = (d["entradas"] / max_val) * (h - pad_y * 2)
            y     = h - pad_y - bar_h
            color = PALETTE[i]
            alpha = "" if i < 5 else ""

            canvas.create_rectangle(x, y, x + bar_w, h - pad_y,
                                    fill=color, outline="", width=0)
            canvas.create_text(x + bar_w / 2, h - pad_y + 12,
                               text=d["dia"][:3],
                               font=("Segoe UI", 8), fill=TEXT_SECONDARY)
            canvas.create_text(x + bar_w / 2, y - 8,
                               text=str(d["entradas"]),
                               font=("Segoe UI", 8, "bold"), fill=color)

    canvas.bind("<Configure>", _draw)

    # ── Fila 2 der: alertas ─────────────────────────────────────
    right_card = make_card(parent)
    right_card.grid(row=2, column=1, sticky="nsew", padx=(6, 0), pady=(0, 4))
    right_card.grid_columnconfigure(0, weight=1)

    make_section_header(right_card, "Requiere Atención", row=0)

    alerts = [
        ("⚠", "3 préstamos vencidos sin devolver",   WARNING,       "hoy"),
        ("📋", "2 reservas de sala por confirmar",    INFO,          "hoy"),
        ("🔑", "1 llave de casillero pendiente",      ACCENT_TEAL,   "ayer"),
        ("📚", "5 libros en reparación",              TEXT_SECONDARY,"sem."),
    ]
    for i, (icon, text, color, time_str) in enumerate(alerts):
        rf = ctk.CTkFrame(right_card, fg_color="#F8FAFC" if i % 2 == 0 else CARD_BG,
                          corner_radius=8, height=42)
        rf.grid(row=i + 1, column=0, sticky="ew", padx=14, pady=2)
        rf.grid_propagate(False)
        rf.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(rf, text=icon, font=("Segoe UI", 14)).grid(
            row=0, column=0, padx=(12, 8), pady=8)
        ctk.CTkLabel(rf, text=text, font=FONT_SMALL,
                     text_color=color, anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(rf, text=time_str, font=("Segoe UI", 9),
                     text_color=TEXT_SECONDARY).grid(row=0, column=2, padx=(4, 14))

    # Spacer
    ctk.CTkLabel(right_card, text="").grid(row=6, pady=4)


# ── Helpers ────────────────────────────────────────────────────────────────

def _kpi_card(parent, icons, badge_key, label, value, color,
              row, col, sub=""):
    """KPI card con borde lateral de color, valor grande y sublabel."""
    card = ctk.CTkFrame(
        parent,
        fg_color=CARD_BG,
        corner_radius=12,
        border_width=1,
        border_color=BORDER_COLOR,
    )
    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=4)
    card.grid_columnconfigure(0, weight=1)

    # Borde izquierdo de color (simulado con un frame estrecho)
    accent_bar = ctk.CTkFrame(card, width=3, fg_color=color, corner_radius=0)
    accent_bar.place(x=0, y=0, relheight=1)

    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=10)
    inner.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(inner, text=label, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY, anchor="w").grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(inner, text=str(value),
                 font=("Segoe UI", 26, "bold"), text_color=color,
                 anchor="w").grid(row=1, column=0, sticky="w")
    if sub:
        ctk.CTkLabel(inner, text=sub, font=("Segoe UI", 9),
                     text_color=TEXT_SECONDARY, anchor="w").grid(row=2, column=0, sticky="w")
    return card


def _quick_btn(parent, label: str, sublabel: str, color: str,
               row: int, col: int, command):
    """Botón de acceso rápido con fondo sólido de color de módulo."""
    hover = darken(color, 0.88)

    btn_f = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
    btn_f.grid(row=row, column=col, sticky="nsew", padx=5, pady=4)
    btn_f.grid_columnconfigure(0, weight=1)
    btn_f.configure(cursor="hand2")

    inner = ctk.CTkFrame(btn_f, fg_color="transparent")
    inner.grid(row=0, column=0, sticky="nsew", padx=14, pady=12)
    inner.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(inner, text=label,
                 font=("Segoe UI", 13, "bold"), text_color="#FFFFFF",
                 anchor="w").grid(row=0, column=0, sticky="w")
    ctk.CTkLabel(inner, text=sublabel,
                 font=("Segoe UI", 10), text_color="rgba(255,255,255,0.75)",
                 anchor="w").grid(row=1, column=0, sticky="w")

    arrow = ctk.CTkLabel(inner, text="→",
                         font=("Segoe UI", 16), text_color="rgba(255,255,255,0.6)")
    arrow.grid(row=0, column=1, rowspan=2, padx=(8, 0))

    # Hacer todo el frame clickeable
    for widget in [btn_f, inner] + inner.winfo_children():
        widget.bind("<Button-1>", lambda e, cmd=command: cmd())
        widget.bind("<Enter>",
                    lambda e, f=btn_f, c=hover: f.configure(fg_color=c))
        widget.bind("<Leave>",
                    lambda e, f=btn_f, c=color: f.configure(fg_color=c))


def _legend_dot(parent, color, text, col):
    f = ctk.CTkFrame(parent, fg_color="transparent")
    f.grid(row=0, column=col, padx=(0, 14))
    ctk.CTkFrame(f, width=8, height=8, fg_color=color, corner_radius=2).pack(
        side="left", padx=(0, 4))
    ctk.CTkLabel(f, text=text, font=("Segoe UI", 9),
                 text_color=TEXT_SECONDARY).pack(side="left")
