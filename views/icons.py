#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Iconos - Biblioteca UMAG
Genera iconos vectoriales usando Pillow (estilo Lucide/Heroicons)
Cada icono es dibujado programáticamente con líneas y formas limpias.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Cache de iconos
_icon_cache = {}

def _get_icon_image(name: str, size: int = 24, color: str = "#FFFFFF", bg: str = None, padding: int = 0) -> Image.Image:
    """Genera un icono PIL Image."""
    key = f"{name}_{size}_{color}_{bg}_{padding}"
    if key in _icon_cache:
        return _icon_cache[key]
    
    total = size + padding * 2
    if bg:
        img = Image.new("RGBA", (total, total), bg)
    else:
        img = Image.new("RGBA", (total, total), (0, 0, 0, 0))
    
    draw = ImageDraw.Draw(img)
    
    # Offset for padding
    ox, oy = padding, padding
    
    # Parse color
    c = color.lstrip('#')
    r, g, b = int(c[:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    clr = (r, g, b, 255)
    w = max(2, size // 12)  # line width
    
    # Draw icon based on name
    if name == "dashboard" or name == "home":
        # House icon
        s = size
        # Roof triangle
        draw.polygon([
            (ox + s//2, oy + s*2//10),
            (ox + s*2//10, oy + s*5//10),
            (ox + s*8//10, oy + s*5//10)
        ], outline=clr, width=w)
        # Body rectangle
        draw.rectangle([ox + s*3//10, oy + s*5//10, ox + s*7//10, oy + s*8//10], outline=clr, width=w)
        # Door
        draw.rectangle([ox + s*4//10, oy + s*6//10, ox + s*6//10, oy + s*8//10], fill=clr)
    
    elif name == "door" or name == "entrada":
        # Door with arrow
        s = size
        # Door frame
        draw.rectangle([ox + s*3//10, oy + s*2//10, ox + s*7//10, oy + s*8//10], outline=clr, width=w)
        # Handle
        draw.ellipse([ox + s*55//100, oy + s*45//100, ox + s*63//100, oy + s*55//100], fill=clr)
        # Arrow entering
        draw.line([(ox + s*1//10, oy + s//2), (ox + s*3//10, oy + s//2)], fill=clr, width=w)
        # Arrow head
        draw.polygon([
            (ox + s*25//100, oy + s*4//10),
            (ox + s*35//100, oy + s//2),
            (ox + s*25//100, oy + s*6//10)
        ], fill=clr)
    
    elif name == "book" or name == "prestamo":
        # Open book
        s = size
        # Left page
        draw.rectangle([ox + s*15//100, oy + s*2//10, ox + s//2, oy + s*8//10], outline=clr, width=w)
        # Right page
        draw.rectangle([ox + s//2, oy + s*2//10, ox + s*85//100, oy + s*8//10], outline=clr, width=w)
        # Spine
        draw.line([(ox + s//2, oy + s*15//100), (ox + s//2, oy + s*85//100)], fill=clr, width=w)
        # Text lines left
        draw.line([(ox + s*25//100, oy + s*35//100), (ox + s*43//100, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*25//100, oy + s*45//100), (ox + s*40//100, oy + s*45//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*25//100, oy + s*55//100), (ox + s*43//100, oy + s*55//100)], fill=clr, width=max(1, w-1))
        # Text lines right
        draw.line([(ox + s*57//100, oy + s*35//100), (ox + s*75//100, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*57//100, oy + s*45//100), (ox + s*72//100, oy + s*45//100)], fill=clr, width=max(1, w-1))
    
    elif name == "chart" or name == "reportes":
        # Bar chart
        s = size
        # Axes
        draw.line([(ox + s*2//10, oy + s*2//10), (ox + s*2//10, oy + s*8//10)], fill=clr, width=w)
        draw.line([(ox + s*2//10, oy + s*8//10), (ox + s*85//100, oy + s*8//10)], fill=clr, width=w)
        # Bars
        bw = s * 12 // 100
        draw.rectangle([ox + s*28//100, oy + s*5//10, ox + s*28//100 + bw, oy + s*75//100], fill=clr)
        draw.rectangle([ox + s*45//100, oy + s*3//10, ox + s*45//100 + bw, oy + s*75//100], fill=clr)
        draw.rectangle([ox + s*62//100, oy + s*4//10, ox + s*62//100 + bw, oy + s*75//100], fill=clr)
    
    elif name == "users" or name == "usuarios":
        # Two people
        s = size
        # Person 1 (front)
        draw.ellipse([ox + s*3//10, oy + s*15//100, ox + s*55//100, oy + s*4//10], outline=clr, width=w)
        draw.arc([ox + s*15//100, oy + s*45//100, ox + s*7//10, oy + s*85//100], 200, 340, fill=clr, width=w)
        # Person 2 (behind)
        draw.ellipse([ox + s*5//10, oy + s*1//10, ox + s*72//100, oy + s*32//100], outline=clr, width=w)
        draw.arc([ox + s*4//10, oy + s*35//100, ox + s*85//100, oy + s*7//10], 210, 330, fill=clr, width=w)
    
    elif name == "search":
        # Magnifying glass
        s = size
        draw.ellipse([ox + s*2//10, oy + s*15//100, ox + s*65//100, oy + s*6//10], outline=clr, width=w)
        draw.line([(ox + s*58//100, oy + s*55//100), (ox + s*8//10, oy + s*8//10)], fill=clr, width=w+1)
    
    elif name == "qr":
        # QR code simplified
        s = size
        # Outer squares
        draw.rectangle([ox + s*15//100, oy + s*15//100, ox + s*4//10, oy + s*4//10], outline=clr, width=w)
        draw.rectangle([ox + s*6//10, oy + s*15//100, ox + s*85//100, oy + s*4//10], outline=clr, width=w)
        draw.rectangle([ox + s*15//100, oy + s*6//10, ox + s*4//10, oy + s*85//100], outline=clr, width=w)
        # Inner dots
        draw.rectangle([ox + s*22//100, oy + s*22//100, ox + s*33//100, oy + s*33//100], fill=clr)
        draw.rectangle([ox + s*67//100, oy + s*22//100, ox + s*78//100, oy + s*33//100], fill=clr)
        draw.rectangle([ox + s*22//100, oy + s*67//100, ox + s*33//100, oy + s*78//100], fill=clr)
        # Random dots
        draw.rectangle([ox + s*5//10, oy + s*5//10, ox + s*6//10, oy + s*6//10], fill=clr)
        draw.rectangle([ox + s*65//100, oy + s*65//100, ox + s*75//100, oy + s*75//100], fill=clr)
    
    elif name == "check" or name == "success":
        # Checkmark in circle
        s = size
        draw.ellipse([ox + s*1//10, oy + s*1//10, ox + s*9//10, oy + s*9//10], outline=clr, width=w)
        draw.line([(ox + s*28//100, oy + s//2), (ox + s*43//100, oy + s*65//100)], fill=clr, width=w+1)
        draw.line([(ox + s*43//100, oy + s*65//100), (ox + s*72//100, oy + s*32//100)], fill=clr, width=w+1)
    
    elif name == "warning" or name == "alert":
        # Triangle with exclamation
        s = size
        draw.polygon([
            (ox + s//2, oy + s*12//100),
            (ox + s*88//100, oy + s*85//100),
            (ox + s*12//100, oy + s*85//100)
        ], outline=clr, width=w)
        draw.line([(ox + s//2, oy + s*35//100), (ox + s//2, oy + s*58//100)], fill=clr, width=w+1)
        draw.ellipse([ox + s*45//100, oy + s*65//100, ox + s*55//100, oy + s*75//100], fill=clr)
    
    elif name == "clock":
        # Clock
        s = size
        draw.ellipse([ox + s*12//100, oy + s*12//100, ox + s*88//100, oy + s*88//100], outline=clr, width=w)
        draw.line([(ox + s//2, oy + s//2), (ox + s//2, oy + s*28//100)], fill=clr, width=w)
        draw.line([(ox + s//2, oy + s//2), (ox + s*68//100, oy + s//2)], fill=clr, width=w)
    
    elif name == "calendar":
        # Calendar
        s = size
        draw.rectangle([ox + s*15//100, oy + s*2//10, ox + s*85//100, oy + s*85//100], outline=clr, width=w)
        draw.line([(ox + s*15//100, oy + s*38//100), (ox + s*85//100, oy + s*38//100)], fill=clr, width=w)
        # Hooks
        draw.line([(ox + s*35//100, oy + s*12//100), (ox + s*35//100, oy + s*28//100)], fill=clr, width=w)
        draw.line([(ox + s*65//100, oy + s*12//100), (ox + s*65//100, oy + s*28//100)], fill=clr, width=w)
        # Dots
        ds = max(3, s*6//100)
        draw.ellipse([ox+s*3//10, oy+s*48//100, ox+s*3//10+ds, oy+s*48//100+ds], fill=clr)
        draw.ellipse([ox+s*48//100, oy+s*48//100, ox+s*48//100+ds, oy+s*48//100+ds], fill=clr)
        draw.ellipse([ox+s*65//100, oy+s*48//100, ox+s*65//100+ds, oy+s*48//100+ds], fill=clr)
    
    elif name == "user":
        # Single person
        s = size
        draw.ellipse([ox + s*3//10, oy + s*1//10, ox + s*7//10, oy + s*45//100], outline=clr, width=w)
        draw.arc([ox + s*15//100, oy + s*5//10, ox + s*85//100, oy + s*95//100], 200, 340, fill=clr, width=w)
    
    elif name == "plus":
        # Plus sign
        s = size
        draw.line([(ox + s//2, oy + s*2//10), (ox + s//2, oy + s*8//10)], fill=clr, width=w+1)
        draw.line([(ox + s*2//10, oy + s//2), (ox + s*8//10, oy + s//2)], fill=clr, width=w+1)
    
    elif name == "bell":
        # Notification bell
        s = size
        draw.arc([ox + s*2//10, oy + s*12//100, ox + s*8//10, oy + s*65//100], 180, 0, fill=clr, width=w)
        draw.line([(ox + s*2//10, oy + s*55//100), (ox + s*15//100, oy + s*72//100)], fill=clr, width=w)
        draw.line([(ox + s*8//10, oy + s*55//100), (ox + s*85//100, oy + s*72//100)], fill=clr, width=w)
        draw.line([(ox + s*12//100, oy + s*72//100), (ox + s*88//100, oy + s*72//100)], fill=clr, width=w)
        draw.ellipse([ox + s*4//10, oy + s*75//100, ox + s*6//10, oy + s*88//100], fill=clr)
    
    elif name == "key":
        # Key
        s = size
        draw.ellipse([ox + s*15//100, oy + s*2//10, ox + s*48//100, oy + s*55//100], outline=clr, width=w)
        draw.line([(ox + s*45//100, oy + s*45//100), (ox + s*82//100, oy + s*82//100)], fill=clr, width=w)
        draw.line([(ox + s*7//10, oy + s*7//10), (ox + s*8//10, oy + s*62//100)], fill=clr, width=w)
    
    elif name == "books" or name == "library":
        # Stack of books
        s = size
        draw.rectangle([ox + s*2//10, oy + s*6//10, ox + s*8//10, oy + s*72//100], fill=clr)
        draw.rectangle([ox + s*18//100, oy + s*45//100, ox + s*82//100, oy + s*57//100], fill=clr)
        draw.rectangle([ox + s*22//100, oy + s*3//10, ox + s*78//100, oy + s*42//100], fill=clr)
        # Spine lines
        draw.line([(ox + s*45//100, oy + s*3//10), (ox + s*45//100, oy + s*42//100)], fill=(255,255,255,180), width=1)
        draw.line([(ox + s*4//10, oy + s*45//100), (ox + s*4//10, oy + s*57//100)], fill=(255,255,255,180), width=1)
    
    elif name == "trending_up":
        # Trending up arrow
        s = size
        draw.line([(ox + s*15//100, oy + s*7//10), (ox + s*4//10, oy + s*45//100)], fill=clr, width=w)
        draw.line([(ox + s*4//10, oy + s*45//100), (ox + s*6//10, oy + s*55//100)], fill=clr, width=w)
        draw.line([(ox + s*6//10, oy + s*55//100), (ox + s*85//100, oy + s*25//100)], fill=clr, width=w)
        # Arrowhead
        draw.polygon([
            (ox + s*85//100, oy + s*25//100),
            (ox + s*72//100, oy + s*22//100),
            (ox + s*78//100, oy + s*35//100)
        ], fill=clr)
    
    elif name == "shield":
        # Shield
        s = size
        draw.polygon([
            (ox + s//2, oy + s*1//10),
            (ox + s*85//100, oy + s*25//100),
            (ox + s*82//100, oy + s*6//10),
            (ox + s//2, oy + s*88//100),
            (ox + s*18//100, oy + s*6//10),
            (ox + s*15//100, oy + s*25//100)
        ], outline=clr, width=w)
        # Check inside
        draw.line([(ox + s*35//100, oy + s//2), (ox + s*45//100, oy + s*62//100)], fill=clr, width=w)
        draw.line([(ox + s*45//100, oy + s*62//100), (ox + s*65//100, oy + s*38//100)], fill=clr, width=w)
    
    elif name == "settings":
        # Gear
        s = size
        # Outer ring approximation with circle + notches
        cx, cy = ox + s//2, oy + s//2
        r_out = s * 38 // 100
        r_in = s * 22 // 100
        draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=clr, width=w)
        # Teeth (simplified as small rectangles)
        import math
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + int(r_in * 0.8 * math.cos(rad))
            y1 = cy + int(r_in * 0.8 * math.sin(rad))
            x2 = cx + int(r_out * math.cos(rad))
            y2 = cy + int(r_out * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=clr, width=w+1)
    
    elif name == "logout":
        # Logout arrow
        s = size
        # Door frame (partial)
        draw.arc([ox + s*1//10, oy + s*1//10, ox + s*6//10, oy + s*9//10], 90, 270, fill=clr, width=w)
        # Arrow
        draw.line([(ox + s*4//10, oy + s//2), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
        draw.line([(ox + s*72//100, oy + s*35//100), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
        draw.line([(ox + s*72//100, oy + s*65//100), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
    
    elif name == "list":
        # List/clipboard
        s = size
        draw.rectangle([ox + s*2//10, oy + s*1//10, ox + s*8//10, oy + s*9//10], outline=clr, width=w)
        # Top handle
        draw.rectangle([ox + s*35//100, oy + s*5//100, ox + s*65//100, oy + s*18//100], outline=clr, width=w)
        # Lines
        draw.line([(ox + s*3//10, oy + s*35//100), (ox + s*7//10, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*3//10, oy + s*5//10), (ox + s*7//10, oy + s*5//10)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*3//10, oy + s*65//100), (ox + s*6//10, oy + s*65//100)], fill=clr, width=max(1, w-1))
    
    elif name == "circle_dot":
        # Status indicator (circle with dot)
        s = size
        draw.ellipse([ox + s*12//100, oy + s*12//100, ox + s*88//100, oy + s*88//100], outline=clr, width=w)
        r = s * 15 // 100
        draw.ellipse([ox + s//2 - r, oy + s//2 - r, ox + s//2 + r, oy + s//2 + r], fill=clr)
    
    elif name == "return":
        # Return/rotate arrow
        s = size
        draw.arc([ox + s*15//100, oy + s*2//10, ox + s*85//100, oy + s*75//100], 30, 330, fill=clr, width=w)
        # Arrowhead
        draw.polygon([
            (ox + s*72//100, oy + s*25//100),
            (ox + s*85//100, oy + s*3//10),
            (ox + s*72//100, oy + s*42//100)
        ], fill=clr)
    
    else:
        # Fallback: filled circle with initial
        s = size
        draw.ellipse([ox + s*1//10, oy + s*1//10, ox + s*9//10, oy + s*9//10], fill=clr)
    
    _icon_cache[key] = img
    return img


def get_ctk_icon(name: str, size: int = 24, color: str = "#FFFFFF", dark_color: str = None) -> 'CTkImage':
    """Returns a CTkImage ready to use in CustomTkinter widgets."""
    import customtkinter as ctk
    
    light_img = _get_icon_image(name, size, color)
    dark_img = _get_icon_image(name, size, dark_color or color)
    
    return ctk.CTkImage(
        light_image=light_img,
        dark_image=dark_img,
        size=(size, size)
    )


def get_badge_icon(name: str, size: int = 40, icon_color: str = "#FFFFFF", bg_color: str = "#4338CA", icon_size_ratio: float = 0.55) -> 'CTkImage':
    """Returns a CTkImage with colored circle background + icon, like Tailwind badge icons.
    Uses supersampling (4x) for smooth antialiased circles."""
    import customtkinter as ctk
    
    # Render at 4x then downscale for smooth edges
    scale = 4
    big = size * scale
    img_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_big)
    
    c = bg_color.lstrip('#')
    r, g, b = int(c[:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    draw.ellipse([2, 2, big - 3, big - 3], fill=(r, g, b, 255))
    
    # Draw icon at scaled size
    icon_s = int(big * icon_size_ratio)
    icon_img = _get_icon_image(name, icon_s, icon_color)
    offset = (big - icon_s) // 2
    img_big.paste(icon_img, (offset, offset), icon_img)
    
    # Downscale with high-quality resampling
    img = img_big.resize((size, size), Image.LANCZOS)
    
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


# Convenience: get all available icon names
AVAILABLE_ICONS = [
    "dashboard", "home", "door", "entrada", "book", "prestamo",
    "chart", "reportes", "users", "usuarios", "search", "qr",
    "check", "success", "warning", "alert", "clock", "calendar",
    "user", "plus", "bell", "key", "books", "library",
    "trending_up", "shield", "settings", "logout", "list",
    "circle_dot", "return"
]
