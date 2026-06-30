#views/entrada.py  Vista de Registro de Entrada

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from config import *
from widgets import (make_card, make_treeview_style,
                     apply_table_stripes, make_section_header, darken, icon_or_none)


# Colores de fondo para cada stat card
_STAT_BACKGROUNDS = [
    ("#EEF2FF", UMAG_PURPLE),  
    ("#F0FDFA", ACCENT_TEAL),  
    ("#F0FDF4", SUCCESS),      
]


def build(parent: ctk.CTkFrame, icons: dict,
          personas_en_sala: int, capacidad: int):

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=0)
    parent.grid_rowconfigure(0, weight=1)

    # ── Panel izquierdo ─────────────────────────────────────────
    left = ctk.CTkFrame(parent, fg_color="transparent")
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(2, weight=1)

    # ── Mini stats con fondo de color ────────────────────────────
    stats_row = ctk.CTkFrame(left, fg_color="transparent")
    stats_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    stats_row.grid_columnconfigure((0, 1, 2), weight=1)

    stat_data = [
        ("badge_users", "En Sala",       f"{personas_en_sala}/{capacidad}"),
        ("badge_door",  "Entradas Hoy",  "87"),
        ("badge_check", "Disponibles",   f"{capacidad - personas_en_sala}"),
    ]
    for col, ((badge_key, label, value), (bg, color)) in enumerate(
            zip(stat_data, _STAT_BACKGROUNDS)):
        _stat_box(stats_row, icon_or_none(icons, badge_key),
                  label, value, color, bg, col)

    # ── Formulario RUT ────────────────────────────────────────────
    rut_card = ctk.CTkFrame(left, fg_color="#1E1B4B", corner_radius=12)
    rut_card.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    rut_card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(rut_card, text="Registrar Entrada",
                 font=("Segoe UI", 13, "bold"), text_color="#C7D2FE").grid(
        row=0, column=0, columnspan=4, padx=20, pady=(14, 8), sticky="w")

    ctk.CTkLabel(rut_card, text="RUT:", font=FONT_SUBHEAD,
                 text_color="#E0E7FF").grid(row=1, column=0, padx=(20, 8), pady=(0, 14))

    rut_entry = ctk.CTkEntry(
        rut_card, placeholder_text="Ej: 12.345.678-5",
        height=40, font=("Consolas", 14),
        corner_radius=10,
        border_color="#4F46E5",
        fg_color="#2D2A6E",
        text_color="#F0F0FF",
        placeholder_text_color="#818CF8",
    )
    rut_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=(0, 14))

    def _format_rut(event):
        from config import format_rut
        val = rut_entry.get()
        fmt = format_rut(val)
        if len(fmt) > 12:
            fmt = fmt[:12]
        rut_entry.delete(0, "end")
        rut_entry.insert(0, fmt)

    rut_entry.bind("<KeyRelease>", _format_rut)

    def _registrar():
        from config import validar_rut
        rut = rut_entry.get().strip()
        if not rut:
            messagebox.showwarning("Atención", "Ingrese un RUT.")
            return
        if not validar_rut(rut):
            messagebox.showerror("RUT inválido", f"El RUT «{rut}» no es válido.")
            return
        messagebox.showinfo("Entrada Registrada",
                            f"Entrada registrada.\n\nRUT: {rut}\n"
                            f"Hora: {datetime.now().strftime('%H:%M')}")
        rut_entry.delete(0, "end")

    _ic_check = icon_or_none(icons, "btn_check")
    ctk.CTkButton(
        rut_card,
        text="  Registrar" if _ic_check else "Registrar",
        image=_ic_check, compound="left" if _ic_check else "none",
        font=("Segoe UI", 13, "bold"),
        width=140, height=40, corner_radius=10,
        fg_color=SUCCESS, hover_color=darken(SUCCESS),
        command=_registrar,
    ).grid(row=1, column=2, padx=5, pady=(0, 14))

    _ic_qr = icon_or_none(icons, "btn_qr")
    ctk.CTkButton(
        rut_card,
        text="  Lector QR" if _ic_qr else "Lector QR",
        image=_ic_qr, compound="left" if _ic_qr else "none",
        font=("Segoe UI", 12),
        width=110, height=40, corner_radius=10,
        fg_color="#4F46E5", hover_color=darken("#4F46E5"),
        command=lambda: messagebox.showinfo("QR", "Simulación: Escáner QR activado."),
    ).grid(row=1, column=3, padx=(5, 20), pady=(0, 14))

    # ── Tabla de entradas ─────────────────────────────────────────
    table_card = make_card(left)
    table_card.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
    table_card.grid_columnconfigure(0, weight=1)
    table_card.grid_rowconfigure(1, weight=1)

    make_section_header(table_card, "Registros del Día", row=0)

    make_treeview_style("Entrada")
    tf = ctk.CTkFrame(table_card, fg_color="transparent")
    tf.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
    tf.grid_columnconfigure(0, weight=1)
    tf.grid_rowconfigure(0, weight=1)

    cols = ("N°", "Hora", "RUT", "Nombre", "Vía")
    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="Entrada.Treeview", height=8)
    tree.heading("N°",     text="#");       tree.column("N°",     width=40,  anchor="center")
    tree.heading("Hora",   text="Hora");    tree.column("Hora",   width=70,  anchor="center")
    tree.heading("RUT",    text="RUT");     tree.column("RUT",    width=130, anchor="center")
    tree.heading("Nombre", text="Nombre");  tree.column("Nombre", width=200)
    tree.heading("Vía",    text="Vía");     tree.column("Vía",    width=110, anchor="center")

    from config import MOCK_ENTRADAS
    for e in MOCK_ENTRADAS:
        tree.insert("", "end", values=(e["id"], e["hora"], e["rut"], e["nombre"], e["via"]))

    apply_table_stripes(tree)
    tree.grid(row=0, column=0, sticky="nsew")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    sb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=sb.set)

    # ── Panel derecho (ficha de estado) ─────────────────────────
    right = make_card(parent, width=270)
    right.grid(row=0, column=1, sticky="nsew")
    right.grid_propagate(False)
    right.grid_columnconfigure(0, weight=1)

    hdr = ctk.CTkFrame(right, fg_color=UMAG_PURPLE, corner_radius=14, height=44)
    hdr.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
    hdr.grid_propagate(False)
    hdr.grid_columnconfigure(0, weight=1)
    ctk.CTkLabel(hdr, text="Panel de Operación",
                 font=("Segoe UI", 12, "bold"), text_color="white").place(
        relx=0.5, rely=0.5, anchor="center")

    def _sep(row):
        ctk.CTkFrame(right, height=1, fg_color=BORDER_COLOR).grid(
            row=row, column=0, sticky="ew", padx=16, pady=4)

    ctk.CTkLabel(right, text="N° REGISTRO", font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).grid(row=1, column=0, pady=(14, 0))
    ctk.CTkLabel(right, text="395", font=("Consolas", 36, "bold"),
                 text_color=UMAG_PURPLE).grid(row=2, column=0)
    _sep(3)

    ctk.CTkLabel(right, text="AFORO ACTUAL", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_INDIGO).grid(row=4, column=0, pady=(10, 4))

    pct = personas_en_sala / capacidad
    bar_color = SUCCESS if pct < 0.5 else WARNING
    ctk.CTkLabel(right, text=str(personas_en_sala),
                 font=("Consolas", 50, "bold"), text_color=UMAG_PURPLE).grid(row=5, column=0)
    ctk.CTkLabel(right, text=f"de {capacidad} personas",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(row=6, column=0, pady=(0, 6))

    bar = ctk.CTkProgressBar(right, height=14, corner_radius=7,
                              progress_color=bar_color, fg_color=UMAG_LIGHT, width=190)
    bar.grid(row=7, column=0, pady=(0, 10))
    bar.set(pct)
    _sep(8)

    _ic_circle = icon_or_none(icons, "circle_green")
    st = ctk.CTkFrame(right, fg_color="transparent")
    st.grid(row=9, column=0, pady=(8, 4))
    if _ic_circle:
        ctk.CTkLabel(st, text="", image=_ic_circle).pack(side="left", padx=(0, 6))
    ctk.CTkLabel(st, text="OPERATIVO", font=("Segoe UI", 14, "bold"),
                 text_color=SUCCESS).pack(side="left")
    _sep(10)

    ctk.CTkLabel(right, text="ÚLTIMO INGRESO", font=("Segoe UI", 10, "bold"),
                 text_color=UMAG_INDIGO).grid(row=11, column=0, pady=(10, 2))
    ctk.CTkLabel(right, text="María González",
                 font=("Segoe UI", 12, "bold"), text_color=TEXT_PRIMARY).grid(row=12, column=0)
    ctk.CTkLabel(right, text="10:15 — Manual",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY).grid(row=13, column=0, pady=(0, 14))


#  Helper stat box cuadrado con fondo de color 
def _stat_box(parent, badge_icon, label: str, value, color: str, bg: str, col: int):
    """Tarjeta stat cuadrada con fondo de color suave, badge cuadrado y valor."""
    card = ctk.CTkFrame(parent, fg_color=bg, corner_radius=12,
                        border_width=1, border_color=BORDER_COLOR)
    card.grid(row=0, column=col, sticky="nsew", padx=5, pady=4)
    card.grid_columnconfigure(0, weight=1)

    # Badge cuadrado (sin imagen CTk si no carga, fallback a frame cuadrado)
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
