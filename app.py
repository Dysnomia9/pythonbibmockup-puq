#  Ventana principal — Sistema Bibliotecario UMAG


import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
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

        self.icons = {}
        self._try_load_icons()

        self._view_cache: dict = {
            "dashboard": None,
            "entrada":   None,
            "prestamo":  None,
            "salas":     None,
            "reportes":  None,
            "usuarios":  None,
        }

        self._build_ui()
        self._bind_shortcuts()

    # ICONS

    def _try_load_icons(self):
        try:
            from views.icons import get_ctk_icon, get_badge_icon
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
                "btn_entrada":    get_ctk_icon("door",      24, "#FFFFFF"),
                "btn_prestamo":   get_ctk_icon("book",      24, "#FFFFFF"),
                "btn_reportes":   get_ctk_icon("chart",     24, "#FFFFFF"),
                "btn_usuarios":   get_ctk_icon("users",     24, "#FFFFFF"),
                "btn_salas":      get_ctk_icon("calendar",  24, "#FFFFFF"),
                "btn_check":      get_ctk_icon("check",     18, "#FFFFFF"),
                "btn_qr":         get_ctk_icon("qr",        18, "#FFFFFF"),
                "btn_search":     get_ctk_icon("search",    18, "#FFFFFF"),
                "btn_plus":       get_ctk_icon("plus",      18, "#FFFFFF"),
                "btn_return":     get_ctk_icon("return",    18, "#FFFFFF"),
                "alert_warning":  get_ctk_icon("warning",   18, WARNING),
                "alert_list":     get_ctk_icon("list",      18, INFO),
                "alert_key":      get_ctk_icon("key",       18, ACCENT_TEAL),
                "alert_books":    get_ctk_icon("books",     18, TEXT_SECONDARY),
                "bell":           get_ctk_icon("bell",      18, UMAG_PURPLE),
                "circle_green":   get_ctk_icon("circle_dot",18, SUCCESS),
            }
        except Exception:
            self.icons = {k: None for k in [
                "badge_users", "badge_door", "badge_books", "badge_warning",
                "badge_chart", "badge_trending", "badge_check", "badge_list",
                "badge_user", "badge_shield", "btn_entrada", "btn_prestamo",
                "btn_reportes", "btn_usuarios", "btn_salas", "btn_check",
                "btn_qr", "btn_search", "btn_plus", "btn_return",
                "alert_warning", "alert_list", "alert_key", "alert_books",
                "bell", "circle_green",
            ]}

    # ATAJOS
    def _bind_shortcuts(self):
        self.bind("<F1>", lambda e: self._show_module("dashboard"))
        self.bind("<F2>", lambda e: self._show_module("entrada"))
        self.bind("<F3>", lambda e: self._show_module("prestamo"))
        self.bind("<F4>", lambda e: self._show_module("salas"))

    # ESQUELETO UI
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0, minsize=52)
        self.grid_rowconfigure(1, weight=1)

        self._build_topnav()

        self.module_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.module_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=(10, 4))
        self.module_frame.grid_columnconfigure(0, weight=1)
        self.module_frame.grid_rowconfigure(0, weight=1)


    def _build_topnav(self):

        nav = tk.Frame(self, height=52, bg=NAV_BG)
        nav.grid(row=0, column=0, sticky="ew")
        nav.grid_propagate(False)

        nav.grid_columnconfigure(0, weight=0, minsize=210)
        nav.grid_columnconfigure(1, weight=1)

        brand = tk.Frame(nav, bg=NAV_BG)
        brand.grid(row=0, column=0, sticky="nsew", padx=(14, 0))

        spines_f = tk.Frame(brand, bg=NAV_BG)
        spines_f.pack(side="left", padx=(0, 10), pady=12)

        spine_heights = [18, 12, 22, 10, 16, 8]
        for color, h in zip(SPINE_COLORS, spine_heights):
            ctk.CTkFrame(
                spines_f, width=4, height=h,
                fg_color=color, corner_radius=1,
            ).pack(side="left", padx=1, pady=(22 - h) // 2)

        name_f = tk.Frame(brand, bg=NAV_BG)
        name_f.pack(side="left")
        ctk.CTkLabel(
            name_f, text="Biblioteca UMAG",
            font=("Segoe UI", 13, "bold"), text_color="#F9FAFB",
            fg_color=NAV_BG,
        ).pack(anchor="w")
        ctk.CTkLabel(
            name_f, text="SISTEMA BIBLIOTECARIO",
            font=("Segoe UI", 8), text_color=NAV_TEXT,
            fg_color=NAV_BG,
        ).pack(anchor="w")

        #  Ítems de navegación
        nav_items_f = tk.Frame(nav, bg=NAV_BG)
        nav_items_f.grid(row=0, column=1, sticky="ns")

        NAV_ITEMS = [
            ("dashboard", "Dashboard", "F1"),
            ("entrada",   "Entrada",   "F2"),
            ("prestamo",  "Préstamos", ""),
            ("salas",     "Salas",     "F4"),
            ("reportes",  "Reportes",  ""),
            ("usuarios",  "Usuarios",  ""),
        ]

        self.nav_buttons    = {}
        self._nav_indicators = {}

        for key, label, shortcut in NAV_ITEMS:
            item_f = tk.Frame(nav_items_f, bg=NAV_BG)
            item_f.pack(side="left")

            indicator = tk.Frame(item_f, height=2, bg=NAV_BG)
            indicator.pack(side="bottom", fill="x")
            self._nav_indicators[key] = indicator

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

    # NAVEGACIÓN-
    MODULE_COLOR = {
        "dashboard": UMAG_PURPLE,
        "entrada":   ACCENT_TEAL,
        "prestamo":  ACCENT_AMBER,
        "salas":     ACCENT_AMBER,
        "reportes":  ACCENT_ROSE,
        "usuarios":  INFO,
    }

    def _build_view(self, module_name: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.module_frame, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        builders = {
            "dashboard": lambda f: dashboard.build(
                f, self.icons,
                self.personas_en_sala, self.capacidad,
                self._show_module),
            "entrada":   lambda f: entrada.build(
                f, self.icons,
                self.personas_en_sala, self.capacidad),
            "prestamo":  lambda f: prestamo.build(
                f, self.icons, self),
            "salas":     lambda f: salas.build(
                f, self.icons, self),
            "reportes":  lambda f: reportes.build(
                f, self.icons),
            "usuarios":  lambda f: usuarios.build(
                f, self.icons, self),
        }
        builders.get(module_name, builders["dashboard"])(frame)
        return frame

    def _show_module(self, module_name: str):
        for key, btn in self.nav_buttons.items():
            if key == module_name:
                btn.configure(text_color=NAV_TEXT_ACTIVE, fg_color=NAV_ACTIVE_BG)
                self._nav_indicators[key].configure(
                    bg=self.MODULE_COLOR.get(key, NAV_ACTIVE_BORDER))
            else:
                btn.configure(text_color=NAV_TEXT, fg_color="transparent")
                self._nav_indicators[key].configure(bg=NAV_BG)

        if self._view_cache[module_name] is None:
            self._view_cache[module_name] = self._build_view(module_name)

        for key, frame in self._view_cache.items():
            if frame is not None:
                frame.grid_remove()

        self._view_cache[module_name].grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = BibliotecaUMAG()
    app.mainloop()