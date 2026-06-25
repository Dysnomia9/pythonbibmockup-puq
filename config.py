# -*- coding: utf-8 -*-
"""
config.py — Colores, constantes y datos mock del Sistema Bibliotecario UMAG
Paleta rediseñada 2026: navy + indigo + semánticos limpios
"""

import re

# ============================================================
# PALETA DE COLORES — Rediseño 2026
# ============================================================

# Navbar / chrome
NAV_BG            = "#111827"   # navy oscuro (antes SIDEBAR_BG opresivo)
NAV_HOVER         = "#1F2937"   # hover sutil
NAV_ACTIVE_BG     = "#1E1B4B"   # fondo ítem activo
NAV_ACTIVE_BORDER = "#4F46E5"   # línea inferior activo (indigo vibrante)
NAV_TEXT          = "#9CA3AF"   # texto inactivo
NAV_TEXT_ACTIVE   = "#FFFFFF"   # texto activo
NAV_BORDER        = "#1F2937"   # separadores en nav

# Mantener aliases legacy para no romper otros módulos
SIDEBAR_BG        = NAV_BG
SIDEBAR_HOVER     = NAV_HOVER
SIDEBAR_ACTIVE    = NAV_ACTIVE_BG
UMAG_PURPLE_DARK  = "#0F172A"
UMAG_PURPLE       = "#4F46E5"   # indigo principal (antes azul-morado genérico)
UMAG_INDIGO       = "#6366F1"   # indigo secundario
UMAG_LIGHT        = "#EEF2FF"   # fondo suave indigo
UMAG_ACCENT       = "#4F46E5"

# Superficie / layout
CARD_BG           = "#FFFFFF"
BG_MAIN           = "#F8FAFC"   # fondo general (antes F0F2FA, más grisáceo)
TEXT_PRIMARY      = "#111827"   # casi negro, mayor contraste WCAG
TEXT_SECONDARY    = "#6B7280"
BORDER_COLOR      = "#E5E7EB"   # borde más suave

# Estados semánticos
SUCCESS           = "#059669"
WARNING           = "#D97706"
DANGER            = "#DC2626"
INFO              = "#2563EB"

# Acentos de módulo (cada módulo tiene su color)
ACCENT_TEAL       = "#0D9488"   # Entrada
ACCENT_AMBER      = "#D97706"   # Salas
ACCENT_ROSE       = "#BE185D"   # Reportes / alertas
ACCENT_EMERALD    = "#10B981"   # disponible / ok

# Lomos decorativos (sidebar brand)
SPINE_COLORS = ["#4F46E5", "#0D9488", "#D97706", "#BE185D", "#059669", "#6366F1"]

# ============================================================
# TIPOGRAFÍA
# ============================================================
FONT_TITLE   = ("Segoe UI", 16, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_SUBHEAD = ("Segoe UI", 12, "bold")
FONT_BODY    = ("Segoe UI", 12)
FONT_SMALL   = ("Segoe UI", 10)
FONT_MONO    = ("Consolas", 12)
FONT_MONO_LG = ("Consolas", 32, "bold")

# ============================================================
# UTILIDADES RUT
# ============================================================
def calcular_dv(rut: int) -> str:
    suma, mult = 0, 2
    for d in reversed(str(rut)):
        suma += int(d) * mult
        mult = 2 if mult == 7 else mult + 1
    resto = 11 - (suma % 11)
    if resto == 11: return '0'
    if resto == 10: return 'K'
    return str(resto)

def validar_rut(rut: str) -> bool:
    cleaned = rut.replace('.', '').replace('-', '').strip()
    if len(cleaned) < 2: return False
    body, dv = cleaned[:-1], cleaned[-1].upper()
    try:
        num = int(body)
    except ValueError:
        return False
    return calcular_dv(num) == dv

def format_rut(value: str) -> str:
    cleaned = re.sub(r'[^0-9kK]', '', value)
    if not cleaned: return ''
    dv = ''
    if len(cleaned) > 1:
        dv = cleaned[-1].upper()
        cleaned = cleaned[:-1]
    formatted = ''
    for i, c in enumerate(reversed(cleaned)):
        if i > 0 and i % 3 == 0:
            formatted = '.' + formatted
        formatted = c + formatted
    return f"{formatted}-{dv}" if dv else formatted

# ============================================================
# DATOS MOCK
# ============================================================
MOCK_ENTRADAS = [
    {"id": 1, "hora": "10:15", "via": "Manual",       "rut": "12.345.678-5", "nombre": "María González"},
    {"id": 2, "hora": "10:02", "via": "QR",           "rut": "16.789.012-3", "nombre": "Carlos Muñoz"},
    {"id": 3, "hora": "09:48", "via": "Autoservicio", "rut": "19.234.567-8", "nombre": "Javiera Soto"},
    {"id": 4, "hora": "09:33", "via": "Manual",       "rut": "14.567.890-1", "nombre": "Andrés Pizarro"},
    {"id": 5, "hora": "09:17", "via": "QR",           "rut": "20.123.456-7", "nombre": "Camila Reyes"},
    {"id": 6, "hora": "09:00", "via": "Autoservicio", "rut": "17.890.123-4", "nombre": "Felipe Carvajal"},
    {"id": 7, "hora": "08:45", "via": "Manual",       "rut": "15.678.901-2", "nombre": "Valentina Espinoza"},
    {"id": 8, "hora": "08:30", "via": "QR",           "rut": "18.456.789-0", "nombre": "Nicolás Fuentes"},
]

MOCK_PRESTAMOS = [
    {"id": 1, "libro": "Introducción a la Programación en Python", "codigo": "9789561228351",
     "fecha_prestamo": "28/05/2026", "fecha_devolucion": "11/06/2026", "estado": "ACTIVO"},
    {"id": 2, "libro": "Cálculo Diferencial - Stewart",            "codigo": "9789706868824",
     "fecha_prestamo": "01/06/2026", "fecha_devolucion": "15/06/2026", "estado": "ACTIVO"},
    {"id": 3, "libro": "Física Universitaria - Sears",             "codigo": "9786073237826",
     "fecha_prestamo": "15/05/2026", "fecha_devolucion": "29/05/2026", "estado": "ATRASADO"},
    {"id": 4, "libro": "Álgebra Lineal - Grossman",                "codigo": "9786071509789",
     "fecha_prestamo": "01/05/2026", "fecha_devolucion": "15/05/2026", "estado": "DEVUELTO"},
    {"id": 5, "libro": "Química General - Chang",                  "codigo": "9786071513939",
     "fecha_prestamo": "20/04/2026", "fecha_devolucion": "04/05/2026", "estado": "DEVUELTO"},
]

MOCK_USUARIOS = [
    {"rut": "12.345.678-5", "nombre": "María González",     "tipo": "Estudiante", "carrera": "Ing. Informática",  "activo": True},
    {"rut": "16.789.012-3", "nombre": "Carlos Muñoz",       "tipo": "Estudiante", "carrera": "Medicina",          "activo": True},
    {"rut": "19.234.567-8", "nombre": "Javiera Soto",       "tipo": "Estudiante", "carrera": "Derecho",           "activo": True},
    {"rut": "14.567.890-1", "nombre": "Andrés Pizarro",     "tipo": "Docente",    "carrera": "Dpto. Ingeniería",  "activo": True},
    {"rut": "20.123.456-7", "nombre": "Camila Reyes",       "tipo": "Estudiante", "carrera": "Enfermería",        "activo": False},
    {"rut": "17.890.123-4", "nombre": "Felipe Carvajal",    "tipo": "Externo",    "carrera": "—",                 "activo": True},
    {"rut": "15.678.901-2", "nombre": "Valentina Espinoza", "tipo": "Estudiante", "carrera": "Kinesiología",      "activo": True},
]

MOCK_ASISTENCIA = [
    {"dia": "Lunes",     "entradas": 145},
    {"dia": "Martes",    "entradas": 167},
    {"dia": "Miércoles", "entradas": 132},
    {"dia": "Jueves",    "entradas": 178},
    {"dia": "Viernes",   "entradas": 156},
    {"dia": "Sábado",    "entradas": 89},
    {"dia": "Domingo",   "entradas": 34},
]

SALAS_CONFIG = [
    {"id": i+1, "nombre": f"Sala {i+1}", "capacidad": cap, "piso": "1er Piso"}
    for i, cap in enumerate([4,4,2,2,4,3,2,4,3,2,4,2,3,4,2,4,3,2,4,2,3,4,2,3,4])
]

BLOQUES_HORARIOS = [
    "08:00–10:00", "10:00–12:00", "12:00–14:00",
    "14:00–16:00", "16:00–18:00", "18:00–20:00",
]

RESERVAS_MOCK = {
    (1, 0):  {"rut": "12.345.678-5", "nombre": "María González"},
    (1, 1):  {"rut": "16.789.012-3", "nombre": "Carlos Muñoz"},
    (3, 2):  {"rut": "19.234.567-8", "nombre": "Javiera Soto"},
    (5, 0):  {"rut": "14.567.890-1", "nombre": "Andrés Pizarro"},
    (5, 1):  {"rut": "14.567.890-1", "nombre": "Andrés Pizarro"},
    (7, 3):  {"rut": "20.123.456-7", "nombre": "Camila Reyes"},
    (10, 4): {"rut": "17.890.123-4", "nombre": "Felipe Carvajal"},
    (12, 0): {"rut": "15.678.901-2", "nombre": "Valentina Espinoza"},
    (15, 2): {"rut": "18.456.789-0", "nombre": "Nicolás Fuentes"},
    (2, 3):  {"rut": "12.345.678-5", "nombre": "María González"},
    (8, 1):  {"rut": "16.789.012-3", "nombre": "Carlos Muñoz"},
    (20, 0): {"rut": "19.234.567-8", "nombre": "Javiera Soto"},
}
