# -*- coding: utf-8 -*-
"""
biblioteca_umag.py — Entry point del Sistema Bibliotecario UMAG
Universidad de Magallanes

Atajos: F1=Dashboard | F2=Entrada | F3=Préstamo | F4=Salas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from app import BibliotecaUMAG
from config import NAV_BG, TEXT_SECONDARY, SUCCESS
from datetime import datetime


# ============================================================
# STATUS BAR
# ============================================================
class StatusBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, height=24, fg_color=NAV_BG, corner_radius=0)
        self.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self, text="  USUARIO: ADMIN",
            font=("Consolas", 8), text_color="#4B5563",
            anchor="w",
        ).grid(row=0, column=0, padx=10, pady=3, sticky="w")

        ctk.CTkLabel(
            self, text="ROL: Administrador",
            font=("Consolas", 8), text_color="#4B5563",
        ).grid(row=0, column=1, pady=3)

        self.dt_label = ctk.CTkLabel(
            self, text="",
            font=("Consolas", 8), text_color="#4B5563", anchor="e",
        )
        self.dt_label.grid(row=0, column=2, padx=10, pady=3, sticky="e")
        self._update()

    def _update(self):
        now = datetime.now()
        self.dt_label.configure(
            text=f"FECHA: {now.strftime('%d/%m/%Y')}    HORA: {now.strftime('%H:%M:%S')}  ")
        self.after(1000, self._update)


# ============================================================
# MAIN
# ============================================================
def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = BibliotecaUMAG()

    # Status bar en row=2 (row=0 topnav, row=1 contenido)
    app.grid_rowconfigure(2, weight=0)
    status = StatusBar(app)
    status.grid(row=2, column=0, sticky="ew")

    app.mainloop()


if __name__ == "__main__":
    main()
