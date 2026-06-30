# Vista de Gestión de Usuarios


import customtkinter as ctk
from tkinter import ttk, messagebox
from config import *
from widgets import (make_card, make_stat_card, make_section_header,
                     make_treeview_style, make_dialog, dialog_action_buttons,
                     labeled_entry, darken, icon_or_none)


def build(parent: ctk.CTkFrame, icons: dict, app_root):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(2, weight=1)

    # Barra búsqueda + nuevo usuario 
    top = make_card(parent)
    top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    top.grid_columnconfigure(1, weight=1)

    _ic_search = icon_or_none(icons, "btn_search")
    if _ic_search:
        ctk.CTkLabel(top, text="", image=_ic_search).grid(
            row=0, column=0, padx=(18, 5), pady=14)

    search_e = ctk.CTkEntry(top,
                             placeholder_text="Buscar por nombre, RUT o carrera…",
                             height=40, corner_radius=10, border_color=BORDER_COLOR)
    search_e.grid(row=0, column=1, sticky="ew", padx=5, pady=14)

    ctk.CTkButton(
        top,
        text="  Buscar" if _ic_search else "Buscar",
        image=_ic_search, compound="left" if _ic_search else "none",
        font=("Segoe UI", 12),
        width=110, height=40, corner_radius=10,
        fg_color=UMAG_PURPLE, hover_color=darken(UMAG_PURPLE),
        command=lambda: messagebox.showinfo("Búsqueda", "Resultados filtrados (demo)"),
    ).grid(row=0, column=2, padx=5, pady=14)

    _ic_plus = icon_or_none(icons, "btn_plus")
    ctk.CTkButton(
        top,
        text="  Nuevo Usuario" if _ic_plus else "Nuevo Usuario",
        image=_ic_plus, compound="left" if _ic_plus else "none",
        font=("Segoe UI", 12),
        width=155, height=40, corner_radius=10,
        fg_color=SUCCESS, hover_color=darken(SUCCESS),
        command=lambda: _nuevo_usuario(app_root, icons),
    ).grid(row=0, column=3, padx=(5, 18), pady=14)

    # KPI stats
    stats = ctk.CTkFrame(parent, fg_color="transparent")
    stats.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    stats.grid_columnconfigure((0, 1, 2, 3), weight=1)

    activos     = sum(1 for u in MOCK_USUARIOS if u["activo"])
    estudiantes = sum(1 for u in MOCK_USUARIOS if u["tipo"] == "Estudiante")
    docentes    = sum(1 for u in MOCK_USUARIOS if u["tipo"] == "Docente")

    make_stat_card(stats, icon_or_none(icons, "badge_users"), "Total Usuarios",  len(MOCK_USUARIOS), UMAG_PURPLE,  0, 0)
    make_stat_card(stats, icon_or_none(icons, "badge_check"), "Activos",         activos,            SUCCESS,      0, 1)
    make_stat_card(stats, icon_or_none(icons, "badge_user"),  "Estudiantes",     estudiantes,        INFO,         0, 2)
    make_stat_card(stats, icon_or_none(icons, "badge_list"),  "Docentes",        docentes,           ACCENT_AMBER, 0, 3)

    # Tabla usuarios 
    table_card = make_card(parent)
    table_card.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
    table_card.grid_columnconfigure(0, weight=1)
    table_card.grid_rowconfigure(1, weight=1)

    make_section_header(table_card, "Listado de Usuarios", row=0)

    make_treeview_style("Usuarios")
    tf = ctk.CTkFrame(table_card, fg_color="transparent")
    tf.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 14))
    tf.grid_columnconfigure(0, weight=1)
    tf.grid_rowconfigure(0, weight=1)

    cols = ("RUT", "Nombre", "Tipo", "Carrera", "Estado")
    tree = ttk.Treeview(tf, columns=cols, show="headings",
                        style="Usuarios.Treeview", height=8)
    tree.heading("RUT",     text="RUT");     tree.column("RUT",     width=130, anchor="center")
    tree.heading("Nombre",  text="Nombre");  tree.column("Nombre",  width=200)
    tree.heading("Tipo",    text="Tipo");    tree.column("Tipo",    width=100, anchor="center")
    tree.heading("Carrera", text="Carrera"); tree.column("Carrera", width=180)
    tree.heading("Estado",  text="Estado");  tree.column("Estado",  width=100, anchor="center")

    for u in MOCK_USUARIOS:
        estado = "ACTIVO" if u["activo"] else "INACTIVO"
        tree.insert("", "end",
                    values=(u["rut"], u["nombre"], u["tipo"], u["carrera"], estado),
                    tags=("activo" if u["activo"] else "inactivo",))
    tree.tag_configure("activo",   foreground=SUCCESS)
    tree.tag_configure("inactivo", foreground=DANGER)

    tree.grid(row=0, column=0, sticky="nsew")
    sb = ttk.Scrollbar(tf, orient="vertical", command=tree.yview)
    sb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=sb.set)


# Diálogo Nuevo Usuario
def _nuevo_usuario(app_root, icons):
    dialog = make_dialog(app_root, "Nuevo Usuario", width=460, height=440)

    card = make_card(dialog)
    card.pack(fill="both", expand=True, padx=18, pady=18)
    card.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(card, text="Registrar Nuevo Usuario",
                 font=("Segoe UI", 15, "bold"), text_color=UMAG_PURPLE).grid(
        row=0, column=0, columnspan=2, padx=20, pady=(18, 10), sticky="w")

    fields = [
        ("RUT:",      "",           "Ej: 12.345.678-5"),
        ("Nombre:",   "",           "Nombre(s)"),
        ("Apellido:", "",           "Apellido(s)"),
        ("Email:",    "",           "correo@umag.cl"),
        ("Tipo:",     "Estudiante", ""),
        ("Carrera:",  "",           ""),
    ]
    entries = []
    for i, (label, default, ph) in enumerate(fields):
        e = labeled_entry(card, label, i + 1, default=default, placeholder=ph)
        entries.append(e)

    def _confirmar():
        if not entries[0].get().strip():
            messagebox.showwarning("Atención", "Ingrese el RUT del usuario.")
            return
        messagebox.showinfo("Usuario Registrado",
                            f"Usuario registrado (demo)\nRUT: {entries[0].get()}")
        dialog.destroy()

    dialog_action_buttons(card, "Registrar", icon_or_none(icons, "btn_check"),
                          _confirmar, dialog.destroy, row=8)
