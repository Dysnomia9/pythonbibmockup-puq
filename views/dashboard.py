#  Dashboard


import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from config import *
from widgets import make_card, make_section_header, darken


def build(parent: ctk.CTkFrame, icons: dict, personas_en_sala: int,
          capacidad: int, navigate_cb):

    _extra = {}
    try:
        from views.icons import get_ctk_icon, get_badge_icon
        _extra = {
            "qa_entrada":   get_ctk_icon("door",        22, "#FFFFFF"),
            "qa_prestamo":  get_ctk_icon("book",        22, "#FFFFFF"),
            "qa_salas":     get_ctk_icon("calendar",    22, "#FFFFFF"),
            "qa_reportes":  get_ctk_icon("chart",       22, "#FFFFFF"),
            "act_prestamo": get_ctk_icon("book",        14, "#FFFFFF"),
            "act_entrada":  get_ctk_icon("door",        14, "#FFFFFF"),
            "act_sala":     get_ctk_icon("calendar",    14, "#FFFFFF"),
            "act_return":   get_ctk_icon("return",      14, "#FFFFFF"),
        }
    except Exception:
        pass

    all_icons = {**icons, **_extra}

    parent.grid_columnconfigure(0, weight=3)
    parent.grid_columnconfigure(1, weight=2)
    parent.grid_rowconfigure(1, weight=1)

    # COLUMNA IZQUIERDA
    left = ctk.CTkFrame(parent, fg_color="transparent")
    left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8))
    left.grid_columnconfigure(0, weight=1)
    left.grid_rowconfigure(2, weight=1)

    # ── KPI strip ─────────────────────────────────
    pct = personas_en_sala / capacidad
    bar_color = SUCCESS if pct < 0.50 else (WARNING if pct < 0.80 else DANGER)

    kpi_row = ctk.CTkFrame(left, fg_color="transparent")
    kpi_row.grid(row=0, column=0, sticky="ew", pady=(0, 10))
    kpi_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

    _kpi(kpi_row, all_icons.get("badge_users"),    "Personas en sala",
         f"{personas_en_sala}/{capacidad}", f"{pct*100:.0f}% aforo",
         UMAG_PURPLE,  "#EEF2FF", 0)
    _kpi(kpi_row, all_icons.get("badge_door"),     "Entradas hoy",
         "87", "+12% vs ayer",
         ACCENT_TEAL,  "#F0FDFA", 1)
    _kpi(kpi_row, all_icons.get("badge_books"),    "Préstamos activos",
         "23", "2 vencen hoy",
         ACCENT_AMBER, "#FFFBEB", 2)
    _kpi(kpi_row, all_icons.get("badge_warning"),  "Dev. pendientes",
         "5",  "3 con atraso",
         ACCENT_ROSE,  "#FFF1F2", 3)

    # ── Acciones rápidas ──────────────────────────
    QA = [
        ("entrada",  "Registro Entrada",  "F2 · acceso rápido",   ACCENT_TEAL,  "qa_entrada"),
        ("prestamo", "Préstamos",          "23 activos ahora",     ACCENT_AMBER, "qa_prestamo"),
        ("salas",    "Reserva de Salas",   "F4 · 12 disponibles",  "#7C3AED",    "qa_salas"),
        ("reportes", "Reportes",           "Estadísticas del día",  ACCENT_ROSE,  "qa_reportes"),
    ]

    qa_row = ctk.CTkFrame(left, fg_color="transparent")
    qa_row.grid(row=1, column=0, sticky="ew", pady=(0, 10))
    qa_row.grid_columnconfigure((0, 1, 2, 3), weight=1)

    for col, (mod, lbl, sub, color, ico_key) in enumerate(QA):
        _quick_btn(qa_row, lbl, sub, color, all_icons.get(ico_key),
                   row=0, col=col, command=lambda m=mod: navigate_cb(m))

    # ── Gráfico asistencia semanal ─────────────────
    chart_card = make_card(left)
    chart_card.grid(row=2, column=0, sticky="nsew", pady=(0, 4))
    chart_card.grid_columnconfigure(0, weight=1)
    chart_card.grid_rowconfigure(1, weight=1)

    _chart_header(chart_card, all_icons)

    canvas = tk.Canvas(chart_card, bg=CARD_BG, highlightthickness=0, height=165)
    canvas.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))

    def _draw(event=None):
        canvas.delete("all")
        w, h = canvas.winfo_width(), canvas.winfo_height()
        if w < 60 or h < 40:
            return

        PAD_L, PAD_R, PAD_T, PAD_B = 36, 14, 18, 28
        data   = MOCK_ASISTENCIA
        max_v  = max(d["entradas"] for d in data)
        n      = len(data)
        usable_w = w - PAD_L - PAD_R
        slot_w   = usable_w / n
        bar_w    = slot_w * 0.55
        bar_gap  = (slot_w - bar_w) / 2

        for i in range(5):
            gy  = PAD_T + (h - PAD_T - PAD_B) * i / 4
            canvas.create_line(PAD_L, gy, w - PAD_R, gy, fill="#EEF0F8", width=1)
            val = int(max_v * (1 - i / 4))
            canvas.create_text(PAD_L - 5, gy, text=str(val),
                               font=("Segoe UI", 8), fill="#B0B8D0", anchor="e")

        today_idx  = datetime.now().weekday()
        colors_bar = [UMAG_PURPLE if i <= today_idx else "#D4D8F0" for i in range(n)]

        for i, d in enumerate(data):
            x0    = PAD_L + i * slot_w + bar_gap
            x1    = x0 + bar_w
            bar_h = (d["entradas"] / max_v) * (h - PAD_T - PAD_B)
            y0    = h - PAD_B - bar_h
            y1    = h - PAD_B
            col_fill = colors_bar[i]

            canvas.create_rectangle(x0+2, y0+4, x1+2, y1+2, fill="#E8EAFA", outline="")
            canvas.create_rectangle(x0, y0, x1, y1, fill=col_fill, outline="")
            canvas.create_oval(x0, y0-4, x1, y0+6, fill=col_fill, outline="")
            canvas.create_text((x0+x1)/2, y0-10, text=str(d["entradas"]),
                               font=("Segoe UI", 8, "bold"), fill=col_fill)
            canvas.create_text((x0+x1)/2, h-PAD_B+12, text=d["dia"][:3],
                               font=("Segoe UI", 9), fill=TEXT_SECONDARY)


    canvas.bind("<Configure>", _draw)
    canvas.update_idletasks()
    _draw()

    # COLUMNA DERECHA
    right = ctk.CTkFrame(parent, fg_color="transparent")
    right.grid(row=0, column=1, rowspan=2, sticky="nsew")
    right.grid_columnconfigure(0, weight=1)
    right.grid_rowconfigure(1, weight=1)

    # Aforo visual
    aforo_card = make_card(right)
    aforo_card.grid(row=0, column=0, sticky="ew", pady=(0, 8))
    aforo_card.grid_columnconfigure(0, weight=1)
    make_section_header(aforo_card, "Aforo en Tiempo Real", row=0)

    aforo_inner = ctk.CTkFrame(aforo_card, fg_color="transparent")
    aforo_inner.grid(row=1, column=0, sticky="ew", padx=18, pady=(4, 14))
    aforo_inner.grid_columnconfigure(1, weight=1)

    donut = tk.Canvas(aforo_inner, width=90, height=90, bg=CARD_BG, highlightthickness=0)
    donut.grid(row=0, column=0, rowspan=3, padx=(0, 14))

    def _draw_donut(event=None):
        donut.delete("all")
        cx, cy, r_out, r_in = 45, 45, 40, 26
        angle = pct * 360
        donut.create_oval(cx-r_out, cy-r_out, cx+r_out, cy+r_out, fill="#EEF2FF", outline="")
        if angle > 0:
            donut.create_arc(cx-r_out, cy-r_out, cx+r_out, cy+r_out,
                             start=90, extent=-angle, fill=bar_color, outline="", style="pieslice")
        donut.create_oval(cx-r_in, cy-r_in, cx+r_in, cy+r_in, fill=CARD_BG, outline="")
        donut.create_text(cx, cy-7, text=f"{pct*100:.0f}%",
                          font=("Segoe UI", 13, "bold"), fill=bar_color)
        donut.create_text(cx, cy+8, text="aforo",
                          font=("Segoe UI", 8), fill=TEXT_SECONDARY)

    _draw_donut()

    ctk.CTkLabel(aforo_inner, text=str(personas_en_sala),
                 font=("Segoe UI", 32, "bold"), text_color=UMAG_PURPLE,
                 anchor="w").grid(row=0, column=1, sticky="sw")
    ctk.CTkLabel(aforo_inner, text=f"de {capacidad} personas",
                 font=FONT_SMALL, text_color=TEXT_SECONDARY,
                 anchor="w").grid(row=1, column=1, sticky="nw")
    bar_aforo = ctk.CTkProgressBar(aforo_inner, height=6, corner_radius=3,
                                    progress_color=bar_color, fg_color=UMAG_LIGHT)
    bar_aforo.grid(row=2, column=1, sticky="ew", pady=(6, 0))
    bar_aforo.set(pct)

    # Actividad reciente 
    act_card = make_card(right)
    act_card.grid(row=1, column=0, sticky="nsew", pady=(0, 4))
    act_card.grid_columnconfigure(0, weight=1)
    act_card.grid_rowconfigure(1, weight=1)
    make_section_header(act_card, "Actividad Reciente", row=0)

    scroll_act = ctk.CTkScrollableFrame(act_card, fg_color="transparent")
    scroll_act.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 10))
    scroll_act.grid_columnconfigure(0, weight=1)

    # Íconos de actividad: (nombre, acción, hora, color_badge, clave_ícono)
    activity = [
        ("María González",     "Préstamo registrado", "10:15", UMAG_PURPLE,  "act_prestamo"),
        ("Carlos Muñoz",       "Entrada registrada",  "10:02", ACCENT_TEAL,  "act_entrada"),
        ("Javiera Soto",       "Sala 3 reservada",    "09:48", "#7C3AED",    "act_sala"),
        ("Andrés Pizarro",     "Libro devuelto",      "09:33", SUCCESS,      "act_return"),
        ("Camila Reyes",       "Entrada registrada",  "09:17", ACCENT_AMBER, "act_entrada"),
        ("Felipe Carvajal",    "Préstamo registrado", "09:00", INFO,         "act_prestamo"),
        ("Valentina Espinoza", "Sala 1 reservada",    "08:45", ACCENT_ROSE,  "act_sala"),
    ]

    for i, (name, action, time, color, ico_key) in enumerate(activity):
        row_f = ctk.CTkFrame(
            scroll_act,
            fg_color="#F8FAFC" if i % 2 == 0 else CARD_BG,
            corner_radius=8, height=48,
        )
        row_f.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
        row_f.grid_propagate(False)
        row_f.grid_columnconfigure(1, weight=1)

        # Badge cuadrado con ícono vectorial
        badge_f = ctk.CTkFrame(row_f, width=30, height=30,
                               fg_color=color, corner_radius=6)
        badge_f.grid(row=0, column=0, padx=(10, 8), pady=9)
        badge_f.grid_propagate(False)
        ico = all_icons.get(ico_key)
        if ico:
            ctk.CTkLabel(badge_f, text="", image=ico).place(
                relx=0.5, rely=0.5, anchor="center")

        info_f = ctk.CTkFrame(row_f, fg_color="transparent")
        info_f.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(info_f, text=name,
                     font=("Segoe UI", 11, "bold"), text_color=TEXT_PRIMARY,
                     anchor="w").pack(anchor="w", pady=(9, 0))
        ctk.CTkLabel(info_f, text=action,
                     font=FONT_SMALL, text_color=TEXT_SECONDARY,
                     anchor="w").pack(anchor="w")

        ctk.CTkLabel(row_f, text=time,
                     font=("Consolas", 9), text_color=TEXT_SECONDARY).grid(
            row=0, column=2, padx=(4, 12))


# ── Helpers ──────────────────────────────────────────────────────────────────

def _kpi(parent, badge_icon, label, value, sub, color, bg, col):
    card = ctk.CTkFrame(parent, fg_color=bg, corner_radius=12,
                        border_width=1, border_color=color)
    card.grid(row=0, column=col, sticky="nsew", padx=4, pady=4)
    card.grid_columnconfigure(0, weight=1)

    # Badge cuadrado
    badge_f = ctk.CTkFrame(card, width=40, height=40, fg_color=color, corner_radius=8)
    badge_f.grid(row=0, column=0, padx=(12, 0), pady=(12, 6), sticky="w")
    badge_f.grid_propagate(False)
    if badge_icon:
        ctk.CTkLabel(badge_f, text="", image=badge_icon).place(
            relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(card, text=label, font=("Segoe UI", 9),
                 text_color=color, anchor="w").grid(row=1, column=0, padx=12, sticky="w")
    ctk.CTkLabel(card, text=str(value), font=("Segoe UI", 20, "bold"),
                 text_color=color, anchor="w").grid(row=2, column=0, padx=12, sticky="w")
    ctk.CTkLabel(card, text=sub, font=("Segoe UI", 8),
                 text_color=TEXT_SECONDARY, anchor="w").grid(
        row=3, column=0, padx=12, pady=(0, 12), sticky="w")


def _quick_btn(parent, label, sublabel, color, icon_img, row, col, command):
    hover = darken(color, 0.88)
    btn_f = ctk.CTkFrame(parent, fg_color=color, corner_radius=12)
    btn_f.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
    btn_f.configure(cursor="hand2")
    btn_f.grid_columnconfigure(0, weight=1)

    # Ícono vectorial en badge cuadrado pequeño
    if icon_img:
        ico_f = ctk.CTkFrame(btn_f, width=32, height=32,
                             fg_color=darken(color, 0.80), corner_radius=6)
        ico_f.grid(row=0, column=0, padx=(12, 0), pady=(10, 4), sticky="w")
        ico_f.grid_propagate(False)
        ctk.CTkLabel(ico_f, text="", image=icon_img).place(
            relx=0.5, rely=0.5, anchor="center")
    else:
        ctk.CTkFrame(btn_f, width=32, height=32,
                     fg_color=darken(color, 0.80), corner_radius=6).grid(
            row=0, column=0, padx=(12, 0), pady=(10, 4), sticky="w")

    ctk.CTkLabel(btn_f, text=label, font=("Segoe UI", 11, "bold"),
                 text_color="#FFFFFF", anchor="w").grid(
        row=1, column=0, padx=12, sticky="w")
    ctk.CTkLabel(btn_f, text=sublabel, font=("Segoe UI", 9),
                 text_color="#C7D2FE", anchor="w").grid(
        row=2, column=0, padx=12, pady=(0, 10), sticky="w")

    for w in [btn_f] + list(btn_f.winfo_children()):
        w.bind("<Button-1>", lambda e, cmd=command: cmd())
        w.bind("<Enter>",  lambda e, f=btn_f, c=hover:  f.configure(fg_color=c))
        w.bind("<Leave>",  lambda e, f=btn_f, c=color:  f.configure(fg_color=c))


def _chart_header(parent, icons):
    hdr = ctk.CTkFrame(parent, fg_color="transparent")
    hdr.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 6))

    ctk.CTkFrame(hdr, width=3, height=18,
                 fg_color=UMAG_PURPLE, corner_radius=2).pack(side="left", padx=(0, 8))
    ctk.CTkLabel(hdr, text="Asistencia Semanal",
                 font=FONT_SUBHEAD, text_color=TEXT_PRIMARY).pack(side="left")

    legend_f = ctk.CTkFrame(hdr, fg_color="transparent")
    legend_f.pack(side="right")
    ctk.CTkFrame(legend_f, width=10, height=10,
                 fg_color=UMAG_PURPLE, corner_radius=2).pack(side="left", padx=(0, 4))
    ctk.CTkLabel(legend_f, text="Días pasados",
                 font=("Segoe UI", 9), text_color=TEXT_SECONDARY).pack(side="left", padx=(0, 10))
    ctk.CTkFrame(legend_f, width=10, height=10,
                 fg_color="#D4D8F0", corner_radius=2).pack(side="left", padx=(0, 4))
    ctk.CTkLabel(legend_f, text="Próximos",
                 font=("Segoe UI", 9), text_color=TEXT_SECONDARY).pack(side="left")