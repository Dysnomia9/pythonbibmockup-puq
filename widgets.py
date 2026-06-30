# Componentes reutilizables del Sistema Bibliotecario UMAG


import customtkinter as ctk
from tkinter import ttk, messagebox
from config import *



def safe_grab_set(dialog: ctk.CTkToplevel, delay: int = 150):
    def _do_grab():
        try:
            dialog.grab_set()
        except Exception:
            dialog.after(100, _do_grab)
    dialog.after(delay, _do_grab)


# HELPER

def icon_or_none(icons: dict, key: str):
    """Retorna el icono si existe y no es None, de lo contrario None."""
    return icons.get(key) or None



# COMPONENTES BASE
def make_card(parent, **kwargs) -> ctk.CTkFrame:
    """Tarjeta blanca con borde sutil y esquinas redondeadas."""
    return ctk.CTkFrame(
        parent,
        fg_color=CARD_BG,
        corner_radius=12,
        border_width=1,
        border_color=BORDER_COLOR,
        **kwargs,
    )


def make_section_header(parent, text: str, row: int = 0,
                        col: int = 0, colspan: int = 1):
    """Título de sección con línea decorativa izquierda."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=row, column=col, columnspan=colspan,
               padx=16, pady=(14, 6), sticky="w")

    ctk.CTkFrame(frame, width=3, height=18,
                 fg_color=UMAG_PURPLE, corner_radius=2).pack(side="left", padx=(0, 8))
    ctk.CTkLabel(frame, text=text, font=FONT_SUBHEAD,
                 text_color=TEXT_PRIMARY).pack(side="left")
    return frame


def make_stat_card(parent, badge_icon, title: str, value, color: str,
                   row: int = 0, col: int = 0) -> ctk.CTkFrame:
    """Tarjeta de estadística con badge cuadrado, título y valor."""
    card = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12,
                        border_width=1, border_color=BORDER_COLOR)
    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    card.grid_columnconfigure(1, weight=1)

    # Badge cuadrado con fondo de color
    badge_f = ctk.CTkFrame(card, width=42, height=42,
                           fg_color=color, corner_radius=8)
    badge_f.grid(row=0, column=0, rowspan=2, padx=(14, 10), pady=14)
    badge_f.grid_propagate(False)
    if badge_icon is not None:
        ctk.CTkLabel(badge_f, text="", image=badge_icon).place(
            relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card, text=title, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY, anchor="w").grid(
        row=0, column=1, sticky="sw", padx=(0, 12), pady=(14, 1))
    ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 22, "bold"),
                 text_color=color, anchor="w").grid(
        row=1, column=1, sticky="nw", padx=(0, 12), pady=(0, 14))
    return card


def make_mini_stat(parent, badge_icon, label: str, value, color: str, col: int):
    """Estadística pequeña para paneles compactos — badge cuadrado."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=0, column=col, padx=12, pady=10)

    badge_f = ctk.CTkFrame(frame, width=36, height=36,
                           fg_color=color, corner_radius=8)
    badge_f.pack(pady=(0, 4))
    badge_f.pack_propagate(False)
    if badge_icon is not None:
        ctk.CTkLabel(badge_f, text="", image=badge_icon).place(
            relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(frame, text=label, font=FONT_SMALL,
                 text_color=TEXT_SECONDARY).pack()
    ctk.CTkLabel(frame, text=str(value), font=("Segoe UI", 17, "bold"),
                 text_color=color).pack()


def make_treeview_style(style_name: str):

    style = ttk.Style()
    style.theme_use('clam')

    # Tabla principal
    style.configure(
        f"{style_name}.Treeview",
        background=CARD_BG,
        fieldbackground=CARD_BG,
        foreground=TEXT_PRIMARY,
        font=("Segoe UI", 11),
        rowheight=34,
        borderwidth=0,
        relief="flat",
    )
    style.configure(
        f"{style_name}.Treeview.Heading",
        background="#EEF2FF",
        foreground=UMAG_PURPLE,
        font=("Segoe UI", 10, "bold"),
        borderwidth=0,
        relief="flat",
        padding=(8, 6),
    )
    style.map(
        f"{style_name}.Treeview.Heading",
        background=[("active", "#E0E7FF")],
        relief=[("active", "flat")],
    )
    style.map(
        f"{style_name}.Treeview",
        background=[("selected", "#EEF2FF")],
        foreground=[("selected", UMAG_PURPLE)],
    )


def apply_table_stripes(tree: "ttk.Treeview", stripe_color: str = "#F8FAFF"):
    """Aplica filas alternadas (zebra) a un Treeview existente."""
    tree.tag_configure("even", background=stripe_color)
    tree.tag_configure("odd",  background=CARD_BG)
    for i, iid in enumerate(tree.get_children()):
        current_tags = list(tree.item(iid, "tags"))
  
        current_tags = [t for t in current_tags if t not in ("even", "odd")]
        current_tags.append("even" if i % 2 == 0 else "odd")
        tree.item(iid, tags=current_tags)


def darken(hex_color: str, factor: float = 0.82) -> str:
    """Oscurece un color hex."""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"#{max(0,int(r*factor)):02x}{max(0,int(g*factor)):02x}{max(0,int(b*factor)):02x}"


# DIÁLOGOS

def make_dialog(parent, title: str,
                width: int = 460, height: int = 360) -> ctk.CTkToplevel:
    """CTkToplevel centrado con grab_set diferido (fix Python 3.14+)."""
    dialog = ctk.CTkToplevel(parent)
    dialog.title(title)
    dialog.configure(fg_color=BG_MAIN)
    dialog.resizable(False, False)

    def _center_and_grab():
        dialog.update_idletasks()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        pw = parent.winfo_width()
        ph = parent.winfo_height()
        x  = px + (pw - width)  // 2
        y  = py + (ph - height) // 2
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        safe_grab_set(dialog)

    dialog.after(50, _center_and_grab)
    return dialog


def dialog_action_buttons(parent, confirm_text: str, confirm_icon,
                          on_confirm, on_cancel, row: int = 99):
    """Fila Confirmar / Cancelar para diálogos."""
    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.grid(row=row, column=0, columnspan=2, pady=16)


    if confirm_icon is not None:
        ctk.CTkButton(
            btn_frame,
            text=f"  {confirm_text}",
            image=confirm_icon,
            compound="left",
            font=("Segoe UI", 13, "bold"),
            width=150, height=38, corner_radius=9,
            fg_color=SUCCESS, hover_color=darken(SUCCESS),
            command=on_confirm,
        ).pack(side="left", padx=6)
    else:
        ctk.CTkButton(
            btn_frame,
            text=confirm_text,
            font=("Segoe UI", 13, "bold"),
            width=150, height=38, corner_radius=9,
            fg_color=SUCCESS, hover_color=darken(SUCCESS),
            command=on_confirm,
        ).pack(side="left", padx=6)

    ctk.CTkButton(
        btn_frame,
        text="Cancelar",
        font=("Segoe UI", 12),
        width=130, height=38, corner_radius=9,
        fg_color="#6B7280", hover_color="#4B5563",
        command=on_cancel,
    ).pack(side="left", padx=6)


def labeled_entry(parent, label: str, row: int,
                  default: str = "", placeholder: str = "",
                  font=None) -> ctk.CTkEntry:
    """Campo con etiqueta alineada a la izquierda."""
    ctk.CTkLabel(parent, text=label, font=font or FONT_BODY,
                 text_color=TEXT_PRIMARY).grid(
        row=row, column=0, padx=(20, 10), pady=6, sticky="w")
    entry = ctk.CTkEntry(
        parent, height=36, corner_radius=8,
        border_color=BORDER_COLOR,
        placeholder_text=placeholder,
        font=font or FONT_BODY,
    )
    entry.grid(row=row, column=1, padx=(0, 20), pady=6, sticky="ew")
    if default:
        entry.insert(0, default)
    return entry
