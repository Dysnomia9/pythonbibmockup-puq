# -*- coding: utf-8 -*-
"""
app.py — Ventana principal, sidebar y topbar del Sistema Bibliotecario UMAG
"""

import sys
import os
# Asegurar que el directorio del proyecto esté en el path,
# independiente de desde dónde se ejecute el script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from datetime import datetime
from config import *

# Importar vistas
from views import dashboard, entrada, prestamo, salas, reportes, usuarios


class BibliotecaUMAG(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Biblioteca UMAG — Sistema Bibliotecario")
        self.geometry("1300x800")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_MAIN)

        self.personas_en_sala = 47
        self.capacidad        = 220

        self._load_icons()
        self._build_ui()
        self._bind_shortcuts()
        self._show_module("dashboard")

    # ----------------------------------------------------------
    # ICONS
    # ----------------------------------------------------------
    def _load_icons(self):
        from biblioteca_umag_python.views.icons import get_ctk_icon, get_badge_icon
        self.icons = {
            # Sidebar
            "sidebar_dashboard":         get_ctk_icon("dashboard", 20, "#C7D2FE"),
            "sidebar_entrada":           get_ctk_icon("door",      20, "#C7D2FE"),
            "sidebar_prestamo":          get_ctk_icon("book",      20, "#C7D2FE"),
            "sidebar_reportes":          get_ctk_icon("chart",     20, "#C7D2FE"),
            "sidebar_salas":             get_ctk_icon("calendar",  20, "#C7D2FE"),
            "sidebar_usuarios":          get_ctk_icon("users",     20, "#C7D2FE"),
            "sidebar_dashboard_active":  get_ctk_icon("dashboard", 20, "#FFFFFF"),
            "sidebar_entrada_active":    get_ctk_icon("door",      20, "#FFFFFF"),
            "sidebar_prestamo_active":   get_ctk_icon("book",      20, "#FFFFFF"),
            "sidebar_salas_active":      get_ctk_icon("calendar",  20, "#FFFFFF"),
            "sidebar_reportes_active":   get_ctk_icon("chart",     20, "#FFFFFF"),
            "sidebar_usuarios_active":   get_ctk_icon("users",     20, "#FFFFFF"),
            # Badges
            "badge_users":    get_badge_icon("users",      44, "#FFFFFF", UMAG_PURPLE),
            "badge_door":     get_badge_icon("door",       44, "#FFFFFF", ACCENT_TEAL),
            "badge_books":    get_badge_icon("books",      44, "#FFFFFF", ACCENT_AMBER),
            "badge_warning":  get_badge_icon("warning",    44, "#FFFFFF", ACCENT_ROSE),
            "badge_chart":    get_badge_icon("chart",      44, "#FFFFFF", UMAG_PURPLE),
            "badge_trending": get_badge_icon("trending_up",44, "#FFFFFF", ACCENT_TEAL),
            "badge_check":    get_badge_icon("check",      44, "#FFFFFF", ACCENT_EMERALD),
            "badge_list":     get_badge_icon("list",       44, "#FFFFFF", INFO),
            "badge_user":     get_badge_icon("user",       44, "#FFFFFF", INFO),
            "badge_shield":   get_badge_icon("shield",     44, "#FFFFFF", SUCCESS),
            # Topbar
            "search":   get_ctk_icon("search",   16, TEXT_SECONDARY),
            "calendar": get_ctk_icon("calendar", 16, TEXT_SECONDARY),
            "clock":    get_ctk_icon("clock",    16, TEXT_SECONDARY),
            # Botones acción
            "btn_entrada":  get_ctk_icon("door",   24, "#FFFFFF"),
            "btn_prestamo": get_ctk_icon("book",   24, "#FFFFFF"),
            "btn_reportes": get_ctk_icon("chart",  24, "#FFFFFF"),
            "btn_usuarios": get_ctk_icon("users",  24, "#FFFFFF"),
            "btn_check":    get_ctk_icon("check",  18, "#FFFFFF"),
            "btn_qr":       get_ctk_icon("qr",     18, "#FFFFFF"),
            "btn_search":   get_ctk_icon("search", 18, "#FFFFFF"),
            "btn_plus":     get_ctk_icon("plus",   18, "#FFFFFF"),
            "btn_return":   get_ctk_icon("return", 18, "#FFFFFF"),
            # Alertas
            "alert_warning": get_ctk_icon("warning", 18, WARNING),
            "alert_list":    get_ctk_icon("list",    18, INFO),
            "alert_key":     get_ctk_icon("key",     18, ACCENT_TEAL),
            "alert_books":   get_ctk_icon("books",   18, TEXT_SECONDARY),
            # Otros
            "bell":         get_ctk_icon("bell",      18, UMAG_PURPLE),
            "logo":         get_badge_icon("books",   48, "#FFFFFF", UMAG_PURPLE),
            "user_sm":      get_ctk_icon("user",      24, "#FFFFFF"),
            "circle_green": get_ctk_icon("circle_dot",18, SUCCESS),
        }

    # ----------------------------------------------------------
    # SHORTCUTS
    # ----------------------------------------------------------
    def _bind_shortcuts(self):
        self.bind("<F1>", lambda e: self._show_module("dashboard"))
        self.bind("<F2>", lambda e: self._show_module("entrada"))
        self.bind("<F3>", lambda e: self._show_module("prestamo"))
        self.bind("<F4>", lambda e: self._show_module("salas"))

    # ----------------------------------------------------------
    # BUILD UI SKELETON
    # ----------------------------------------------------------
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self.content_frame = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self._build_topbar()

        self.module_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.module_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(10, 18))
        self.module_frame.grid_columnconfigure(0, weight=1)
        self.module_frame.grid_rowconfigure(0, weight=1)

    # ----------------------------------------------------------
    # SIDEBAR
    # ----------------------------------------------------------
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=234, fg_color=SIDEBAR_BG, corner_radius=0)
        sb.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)

        # Logo area
        logo_f = ctk.CTkFrame(sb, fg_color="transparent", height=116)
        logo_f.grid(row=0, column=0, sticky="ew", padx=14, pady=(22, 4))
        logo_f.grid_propagate(False)
        logo_f.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(logo_f, text="", image=self.icons["logo"]).grid(row=0, column=0, pady=(6, 4))
        ctk.CTkLabel(logo_f, text="Biblioteca UMAG",
                     font=("Segoe UI", 16, "bold"), text_color="white").grid(row=1, column=0)
        ctk.CTkLabel(logo_f, text="Sistema Bibliotecario",
                     font=("Segoe UI", 10), text_color="#818CF8").grid(row=2, column=0)

        ctk.CTkFrame(sb, height=1, fg_color="#2D2566").grid(
            row=1, column=0, sticky="ew", padx=18, pady=8)

        # Navegación
        nav_items = [
            ("dashboard", "Dashboard",  "F1"),
            ("entrada",   "Entrada",    "F2"),
            ("prestamo",  "Préstamo",   "F3"),
            ("salas",     "Salas",      "F4"),
            ("reportes",  "Reportes",   ""),
            ("usuarios",  "Usuarios",   ""),
        ]
        self.nav_buttons = {}
        for i, (key, label, shortcut) in enumerate(nav_items):
            row_f = ctk.CTkFrame(sb, fg_color="transparent", height=44)
            row_f.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=2)
            row_f.grid_propagate(False)
            row_f.grid_columnconfigure(0, weight=1)

            btn = ctk.CTkButton(
                row_f, text=f"   {label}",
                image=self.icons[f"sidebar_{key}"], compound="left",
                font=("Segoe UI", 13), anchor="w",
                height=40, corner_radius=10,
                fg_color="transparent", hover_color=SIDEBAR_HOVER,
                text_color="#C7D2FE",
                command=lambda k=key: self._show_module(k),
            )
            btn.grid(row=0, column=0, sticky="ew")

            if shortcut:
                ctk.CTkLabel(row_f, text=shortcut,
                             font=("Consolas", 9, "bold"), text_color="#FFFFFF",
                             fg_color="#3730A3", corner_radius=4,
                             width=28, height=18).grid(row=0, column=1, padx=(0, 6))

            self.nav_buttons[key] = btn

        sb.grid_rowconfigure(10, weight=1)

        # Usuario activo
        user_f = ctk.CTkFrame(sb, fg_color="#1E1A4B", corner_radius=12, height=72)
        user_f.grid(row=11, column=0, sticky="ew", padx=10, pady=(0, 14))
        user_f.grid_propagate(False)
        user_f.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(user_f, text="", image=self.icons["user_sm"]).grid(
            row=0, column=0, rowspan=2, padx=(12, 8), pady=10)
        ctk.CTkLabel(user_f, text="Administrador",
                     font=("Segoe UI", 12, "bold"), text_color="white",
                     anchor="w").grid(row=0, column=1, sticky="w", pady=(14, 0))
        ctk.CTkLabel(user_f, text="Staff Biblioteca",
                     font=("Segoe UI", 10), text_color="#818CF8",
                     anchor="w").grid(row=1, column=1, sticky="w", pady=(0, 14))

    # ----------------------------------------------------------
    # TOPBAR
    # ----------------------------------------------------------
    def _build_topbar(self):
        tb = ctk.CTkFrame(self.content_frame, height=58, fg_color=CARD_BG, corner_radius=0)
        tb.grid(row=0, column=0, sticky="ew")
        tb.grid_propagate(False)
        tb.grid_columnconfigure(1, weight=1)

        # Título dinámico con acento vertical
        title_f = ctk.CTkFrame(tb, fg_color="transparent")
        title_f.grid(row=0, column=0, padx=20, pady=14, sticky="w")
        ctk.CTkFrame(title_f, width=4, height=24,
                     fg_color=UMAG_INDIGO, corner_radius=2).pack(side="left", padx=(0, 10))
        self.topbar_title = ctk.CTkLabel(title_f, text="Dashboard",
                                          font=FONT_TITLE, text_color=TEXT_PRIMARY)
        self.topbar_title.pack(side="left")

        # Búsqueda central
        sf = ctk.CTkFrame(tb, fg_color="transparent")
        sf.grid(row=0, column=1, pady=12)
        ctk.CTkLabel(sf, text="", image=self.icons["search"]).pack(side="left", padx=(0, 5))
        ctk.CTkEntry(sf, placeholder_text="Buscar en el sistema…",
                     width=290, height=36, corner_radius=18,
                     border_color="#E0E7FF", fg_color="#F8FAFC").pack(side="left")

        # Fecha y hora
        tf = ctk.CTkFrame(tb, fg_color="transparent")
        tf.grid(row=0, column=2, padx=20)
        ctk.CTkLabel(tf, text="", image=self.icons["calendar"]).pack(side="left", padx=(0, 4))
        self.date_label = ctk.CTkLabel(tf, text="", font=("Consolas", 11),
                                        text_color=TEXT_SECONDARY)
        self.date_label.pack(side="left", padx=(0, 12))
        ctk.CTkLabel(tf, text="", image=self.icons["clock"]).pack(side="left", padx=(0, 4))
        self.time_label = ctk.CTkLabel(tf, text="", font=("Consolas", 11),
                                        text_color=TEXT_SECONDARY)
        self.time_label.pack(side="left")
        self._update_clock()

    def _update_clock(self):
        now = datetime.now()
        self.date_label.configure(text=now.strftime("%d/%m/%Y"))
        self.time_label.configure(text=now.strftime("%H:%M:%S"))
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

    def _show_module(self, module_name: str):
        # Actualizar estado visual de la sidebar
        for key, btn in self.nav_buttons.items():
            if key == module_name:
                btn.configure(fg_color=SIDEBAR_ACTIVE, text_color="white",
                              image=self.icons[f"sidebar_{key}_active"])
            else:
                btn.configure(fg_color="transparent", text_color="#C7D2FE",
                              image=self.icons[f"sidebar_{key}"])

        self.topbar_title.configure(text=self.TITLES.get(module_name, ""))

        # Limpiar frame de contenido
        for w in self.module_frame.winfo_children():
            w.destroy()

        # Llamar al builder de la vista correspondiente
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
