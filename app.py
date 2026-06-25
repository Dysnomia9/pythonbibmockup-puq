# -*- coding: utf-8 -*-
"""
app.py — Ventana principal con TOPNAV horizontal — Sistema Bibliotecario UMAG
Rediseño 2026: navbar superior en lugar de sidebar lateral.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from datetime import datetime
from config import *

from views import dashboard, entrada, prestamo, salas, reportes, usuarios


class BibliotecaUMAG(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca UMAG — Sistema Bibliotecario")
        self.geometry("1300x820")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_MAIN)

        self.personas_en_sala = 47
        self.capacidad        = 220

        # icons: dict vacío por defecto — se llena si el módulo icons está disponible
        self.icons = {}
        self._try_load_icons()

        self._build_ui()
        self._bind_shortcuts()
        self._show_module("dashboard")

    # ----------------------------------------------------------
    # ICONS (opcional — no rompe si el módulo no existe)
    # ----------------------------------------------------------
    def _try_load_icons(self):
        try:
            from biblioteca_umag_python.views.icons import get_ctk_icon, get_badge_icon
            self.icons = {
                "badge_users":    get_badge_icon("users",       44, "#FFFFFF", UMAG_PURPLE),
                "badge_door":     get_badge_icon("door",        44, "#FFFFFF", ACCENT_TEAL),
                "badge_books":    get_badge_icon("books",       44, "#FFFFFF", ACCENT_AMBER),
                "badge_warning":  get_badge_icon("warning",     44, "#FFFFFF", ACCENT_ROSE),
                "badge_chart":    get_badge_icon("chart",       44, "#FFFFFF", UMAG_PURPLE),
                "badge_trending": get_badge_icon("trending_up", 44, "#FFFFFF", ACCENT_TEAL),
                "badge_check":    get_badge_icon("check",       44, "#FFFFFF", ACCENT_EMERALD),
                "badge_list":     get_badge_icon("list",        44, "#FFFFFF", INFO),
                "badge_user":     get_badge_icon("user",        44, "#FFFFFF", INFO),
                "badge_shield":   get_badge_icon("shield",      44, "#FFFFFF", SUCCESS),
                "btn_entrada":    get_ctk_icon("door",   24, "#FFFFFF"),
                "btn_prestamo":   get_ctk_icon("book",   24, "#FFFFFF"),
                "btn_reportes":   get_ctk_icon("chart",  24, "#FFFFFF"),
                "btn_usuarios":   get_ctk_icon("users",  24, "#FFFFFF"),
                "btn_salas":      get_ctk_icon("calendar", 24, "#FFFFFF"),
                "btn_check":      get_ctk_icon("check",  18, "#FFFFFF"),
                "btn_qr":         get_ctk_icon("qr",     18, "#FFFFFF"),
                "btn_search":     get_ctk_icon("search", 18, "#FFFFFF"),
                "btn_plus":       get_ctk_icon("plus",   18, "#FFFFFF"),
                "btn_return":     get_ctk_icon("return", 18, "#FFFFFF"),
                "alert_warning":  get_ctk_icon("warning", 18, WARNING),
                "alert_list":     get_ctk_icon("list",    18, INFO),
                "alert_key":      get_ctk_icon("key",     18, ACCENT_TEAL),
                "alert_books":    get_ctk_icon("books",   18, TEXT_SECONDARY),
                "bell":           get_ctk_icon("bell",    18, UMAG_PURPLE),
                "circle_green":   get_ctk_icon("circle_dot", 18, SUCCESS),
            }
        except Exception:
            self.icons = {}

    # ----------------------------------------------------------
    # ATAJOS DE TECLADO
    # ----------------------------------------------------------
    def _bind_shortcuts(self):
        self.bind("<F1>", lambda e: self._show_module("dashboard"))
        self.bind("<F2>", lambda e: self._show_module("entrada"))
        self.bind("<F3>", lambda e: self._show_module("prestamo"))
        self.bind("<F4>", lambda e: self._show_module("salas"))

    # ----------------------------------------------------------
    # ESQUELETO UI
    # ----------------------------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)   # row 0 = topnav, row 1 = contenido, row 2 = statusbar

        self._build_topnav()

        self.module_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.module_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(10, 4))
        self.module_frame.grid_columnconfigure(0, weight=1)
        self.module_frame.grid_rowconfigure(0, weight=1)

    # ----------------------------------------------------------
    # TOPNAV HORIZONTAL
    # ----------------------------------------------------------
    def _build_topnav(self):
        nav = ctk.CTkFrame(self, height=52, fg_color=NAV_BG, corner_radius=0)
        nav.grid(row=0, column=0, sticky="ew")
        nav.grid_propagate(False)
        nav.grid_columnconfigure(1, weight=1)   # zona nav items estira

        # ── Brand (logo + lomos decorativos) ──────────────────
        brand = ctk.CTkFrame(nav, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ns", padx=(14, 0))

        # Lomos de libros decorativos
        spines_f = ctk.CTkFrame(brand, fg_color="transparent")
        spines_f.pack(side="left", padx=(0, 10), pady=12)
        spine_heights = [18, 12, 22, 10, 16, 8]
        for color, h in zip(SPINE_COLORS, spine_heights):
            ctk.CTkFrame(
                spines_f, width=4, height=h,
                fg_color=color, corner_radius=1,
            ).pack(side="left", padx=1, pady=(22 - h) // 2)  # alineados al fondo

        name_f = ctk.CTkFrame(brand, fg_color="transparent")
        name_f.pack(side="left", pady=0)
        ctk.CTkLabel(
            name_f, text="Biblioteca UMAG",
            font=("Segoe UI", 13, "bold"), text_color="#F9FAFB",
        ).pack(anchor="w")
        ctk.CTkLabel(
            name_f, text="SISTEMA BIBLIOTECARIO",
            font=("Segoe UI", 8), text_color=NAV_TEXT,
        ).pack(anchor="w")

        # Separador vertical
        ctk.CTkFrame(nav, width=1, fg_color="#1F2937").grid(
            row=0, column=0, sticky="ns", padx=(180, 0), pady=8)

        # ── Ítems de navegación ───────────────────────────────
        nav_items_f = ctk.CTkFrame(nav, fg_color="transparent")
        nav_items_f.grid(row=0, column=1, sticky="ns", padx=6)

        NAV_ITEMS = [
            ("dashboard", "Dashboard", "F1"),
            ("entrada",   "Entrada",   "F2"),
            ("prestamo",  "Préstamos", ""),
            ("salas",     "Salas",     "F4"),
            ("reportes",  "Reportes",  ""),
            ("usuarios",  "Usuarios",  ""),
        ]

        self.nav_buttons = {}
        self._nav_indicators = {}

        for key, label, shortcut in NAV_ITEMS:
            item_f = ctk.CTkFrame(nav_items_f, fg_color="transparent")
            item_f.pack(side="left")

            # Indicador activo (línea inferior de color)
            indicator = ctk.CTkFrame(item_f, height=2, fg_color="transparent", corner_radius=0)
            indicator.pack(side="bottom", fill="x")
            self._nav_indicators[key] = indicator

            # Texto del label + shortcut
            display = f"{label}  {shortcut}" if shortcut else label

            btn = ctk.CTkButton(
                item_f,
                text=display,
                font=("Segoe UI", 12),
                fg_color="transparent",
                hover_color=NAV_HOVER,
                text_color=NAV_TEXT,
                height=48,
                corner_radius=0,
                width=0,
                anchor="center",
                command=lambda k=key: self._show_module(k),
            )
            btn.pack(side="top", padx=4)
            self.nav_buttons[key] = btn

        # ── Zona derecha: búsqueda + reloj + usuario ──────────
        right_f = ctk.CTkFrame(nav, fg_color="transparent")
        right_f.grid(row=0, column=2, sticky="ns", padx=(0, 14))

        # Buscador
        search_wrap = ctk.CTkFrame(right_f, fg_color="transparent")
        search_wrap.pack(side="left", padx=(0, 12), pady=11)
        ctk.CTkEntry(
            search_wrap,
            placeholder_text="Buscar…",
            width=190, height=30,
            corner_radius=15,
            border_color="#374151",
            fg_color="#1F2937",
            text_color="#E5E7EB",
            placeholder_text_color=NAV_TEXT,
            font=("Segoe UI", 11),
        ).pack()

        # Separador
        ctk.CTkFrame(right_f, width=1, fg_color="#1F2937").pack(
            side="left", fill="y", pady=10, padx=4)

        # Reloj
        clock_f = ctk.CTkFrame(right_f, fg_color="transparent")
        clock_f.pack(side="left", padx=(4, 12), pady=0)

        self.nav_date_label = ctk.CTkLabel(
            clock_f, text="",
            font=("Consolas", 10), text_color=NAV_TEXT,
        )
        self.nav_date_label.pack()
        self.nav_time_label = ctk.CTkLabel(
            clock_f, text="",
            font=("Consolas", 11, "bold"), text_color="#E5E7EB",
        )
        self.nav_time_label.pack()
        self._update_clock()

        # Badge de notificaciones
        notif_f = ctk.CTkFrame(
            right_f, width=30, height=30,
            fg_color="#1F2937", corner_radius=8,
            border_width=1, border_color="#374151",
        )
        notif_f.pack(side="left", padx=(0, 10))
        notif_f.pack_propagate(False)
        ctk.CTkLabel(
            notif_f, text="🔔",
            font=("Segoe UI", 13), text_color=NAV_TEXT,
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Dot rojo notificaciones
        dot = ctk.CTkFrame(right_f if False else notif_f,
                           width=8, height=8, fg_color="#E11D48", corner_radius=4)
        dot.place(relx=0.75, rely=0.18)

        # Avatar usuario
        avatar_f = ctk.CTkFrame(
            right_f, width=30, height=30,
            fg_color=UMAG_PURPLE, corner_radius=15,
        )
        avatar_f.pack(side="left")
        avatar_f.pack_propagate(False)
        ctk.CTkLabel(
            avatar_f, text="AD",
            font=("Segoe UI", 10, "bold"), text_color="#FFFFFF",
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ----------------------------------------------------------
    # RELOJ
    # ----------------------------------------------------------
    def _update_clock(self):
        now = datetime.now()
        self.nav_date_label.configure(text=now.strftime("%d/%m/%Y"))
        self.nav_time_label.configure(text=now.strftime("%H:%M:%S"))
        self.after(1000, self._update_clock)

    # ----------------------------------------------------------
    # NAVEGACIÓN
    # ----------------------------------------------------------
    TITLES = {
        "dashboard": "Dashboard",
        "entrada":   "Registro de Entrada",
        "prestamo":  "Gestión de Préstamos",
        "salas":     "Reserva de Salas",
        "reportes":  "Reportes y Estadísticas",
        "usuarios":  "Gestión de Usuarios",
    }

    # Color de acento por módulo (indicador inferior + tinte activo)
    MODULE_COLOR = {
        "dashboard": UMAG_PURPLE,
        "entrada":   ACCENT_TEAL,
        "prestamo":  ACCENT_AMBER,
        "salas":     ACCENT_AMBER,
        "reportes":  ACCENT_ROSE,
        "usuarios":  INFO,
    }

    def _show_module(self, module_name: str):
        for key, btn in self.nav_buttons.items():
            if key == module_name:
                btn.configure(text_color=NAV_TEXT_ACTIVE, fg_color=NAV_ACTIVE_BG)
                self._nav_indicators[key].configure(
                    fg_color=self.MODULE_COLOR.get(key, NAV_ACTIVE_BORDER))
            else:
                btn.configure(text_color=NAV_TEXT, fg_color="transparent")
                self._nav_indicators[key].configure(fg_color="transparent")

        # Limpiar contenido
        for w in self.module_frame.winfo_children():
            w.destroy()

        # Renderizar vista
        builders = {
            "dashboard": lambda: dashboard.build(
                self.module_frame, self.icons,
                self.personas_en_sala, self.capacidad,
                self._show_module),
            "entrada":   lambda: entrada.build(
                self.module_frame, self.icons,
                self.personas_en_sala, self.capacidad),
            "prestamo":  lambda: prestamo.build(
                self.module_frame, self.icons, self),
            "salas":     lambda: salas.build(
                self.module_frame, self.icons, self),
            "reportes":  lambda: reportes.build(
                self.module_frame, self.icons),
            "usuarios":  lambda: usuarios.build(
                self.module_frame, self.icons, self),
        }
        builders.get(module_name, builders["dashboard"])()
