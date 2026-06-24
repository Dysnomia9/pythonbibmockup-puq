# -*- coding: utf-8 -*-
"""
views/reportes.py — Vista de Reportes y Estadísticas
"""

import tkinter as tk
import customtkinter as ctk
from config import *
from widgets import make_card, make_stat_card, make_section_header


def build(parent: ctk.CTkFrame, icons: dict):
    parent.grid_columnconfigure((0, 1), weight=1)
    parent.grid_rowconfigure(1, weight=1)

    # ── KPI stats ────────────────────────────────────────────────
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    total    = sum(d["entradas"] for d in MOCK_ASISTENCIA)
    promedio = total // 7

    make_stat_card(stats, icons["badge_chart"],   "Total Semanal",       total,    UMAG_PURPLE,  0, 0)
    make_stat_card(stats, icons["badge_trending"],"Promedio Diario",     promedio, ACCENT_TEAL,  0, 1)
    make_stat_card(stats, icons["badge_books"],   "Préstamos Activos",   "23",     ACCENT_AMBER, 0, 2)
    make_stat_card(stats, icons["badge_user"],    "Usuarios Registrados","156",    INFO,         0, 3)

    # ── Gráfico barras ───────────────────────────────────────────
    chart_card = make_card(parent)
    chart_card.grid(row=1, column=0, sticky="nsew", padx=(4, 4), pady=(0, 4))
    chart_card.grid_columnconfigure(0, weight=1)
    chart_card.grid_rowconfigure(1, weight=1)

    make_section_header(chart_card, "Asistencia Semanal", row=0)

    canvas = tk.Canvas(chart_card, bg=CARD_BG, highlightthickness=0, height=260)
    canvas.grid(row=1, column=0, sticky="nsew", padx=18, pady=(4, 18))

    PALETTE = [UMAG_PURPLE, UMAG_ACCENT, ACCENT_TEAL, ACCENT_AMBER,
               ACCENT_ROSE, INFO, TEXT_SECONDARY]

    def _draw(event=None):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 50 or h < 50:
            return
        pad_x, pad_y = 44, 36
        max_val = max(d["entradas"] for d in MOCK_ASISTENCIA)
        n       = len(MOCK_ASISTENCIA)
        bar_w   = (w - pad_x * 2) / n - 8

        # Líneas de guía horizontales
        guide_steps = 4
        for i in range(guide_steps + 1):
            gy = pad_y + (h - pad_y * 2) * i / guide_steps
            canvas.create_line(pad_x, gy, w - pad_x, gy,
                               fill="#E8ECF8", width=1, dash=(4, 4))
            val_label = int(max_val * (1 - i / guide_steps))
            canvas.create_text(pad_x - 6, gy, text=str(val_label),
                               font=("Segoe UI", 9), fill=TEXT_SECONDARY, anchor="e")

        for i, d in enumerate(MOCK_ASISTENCIA):
            x     = pad_x + i * (bar_w + 8)
            bar_h = (d["entradas"] / max_val) * (h - pad_y * 2)
            y     = h - pad_y - bar_h
            color = PALETTE[i % len(PALETTE)]

            # Sombra barra
            canvas.create_rectangle(x + 2, y + 6, x + bar_w + 2, h - pad_y + 2,
                                     fill="#E0E7FF", outline="")
            # Barra
            canvas.create_rectangle(x, y, x + bar_w, h - pad_y,
                                     fill=color, outline="", width=0)
            # Cima redondeada (óvalo)
            canvas.create_oval(x, y - 3, x + bar_w, y + 7,
                               fill=color, outline="")
            # Valor encima
            canvas.create_text(x + bar_w / 2, y - 12, text=str(d["entradas"]),
                               font=("Segoe UI", 9, "bold"), fill=color)
            # Etiqueta día
            canvas.create_text(x + bar_w / 2, h - pad_y + 16,
                               text=d["dia"][:3], font=("Segoe UI", 9), fill=TEXT_SECONDARY)

    canvas.bind("<Configure>", _draw)

    # ── Top libros ───────────────────────────────────────────────
    books_card = make_card(parent)
    books_card.grid(row=1, column=1, sticky="nsew", padx=(0, 4), pady=(0, 4))
    books_card.grid_columnconfigure(0, weight=1)

    make_section_header(books_card, "Libros Más Prestados", row=0)

    top_books = [
        ("Intro. Programación Python", 34, UMAG_PURPLE),
        ("Cálculo — Stewart",          28, UMAG_ACCENT),
        ("Física — Sears",             22, ACCENT_TEAL),
        ("Álgebra — Grossman",         19, ACCENT_AMBER),
        ("Química — Chang",            15, ACCENT_ROSE),
        ("Historia Patagonia",         12, INFO),
        ("Botánica Austral",            9, SUCCESS),
    ]
    for i, (title, count, color) in enumerate(top_books):
        rf = ctk.CTkFrame(books_card,
                          fg_color="#F5F7FF" if i % 2 == 0 else CARD_BG,
                          corner_radius=8, height=38)
        rf.grid(row=i + 1, column=0, sticky="ew", padx=14, pady=2)
        rf.grid_propagate(False)
        rf.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(rf, text=f" {i+1}.", font=("Consolas", 11, "bold"),
                     text_color=color, width=30).grid(row=0, column=0, padx=(10, 4), pady=6)
        ctk.CTkLabel(rf, text=title, font=("Segoe UI", 11),
                     text_color=TEXT_PRIMARY, anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(rf, text=f"{count} préstamos", font=FONT_SMALL,
                     text_color=TEXT_SECONDARY).grid(row=0, column=2, padx=(4, 14))

    ctk.CTkLabel(books_card, text="").grid(row=9, pady=4)
