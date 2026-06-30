
# Sistema de Iconos - Biblioteca UMAG
# Genera iconos vectoriales usando Pillow (estilo Lucide/Heroicons)

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
    

    ox, oy = padding, padding

    c = color.lstrip('#')
    r, g, b = int(c[:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    clr = (r, g, b, 255)
    w = max(2, size // 12)
    
    if name == "dashboard" or name == "home":
        s = size
        draw.polygon([
            (ox + s//2, oy + s*2//10),
            (ox + s*2//10, oy + s*5//10),
            (ox + s*8//10, oy + s*5//10)
        ], outline=clr, width=w)
        draw.rectangle([ox + s*3//10, oy + s*5//10, ox + s*7//10, oy + s*8//10], outline=clr, width=w)
        draw.rectangle([ox + s*4//10, oy + s*6//10, ox + s*6//10, oy + s*8//10], fill=clr)
    
    elif name == "door" or name == "entrada":
        s = size
        draw.rectangle([ox + s*3//10, oy + s*2//10, ox + s*7//10, oy + s*8//10], outline=clr, width=w)
        draw.ellipse([ox + s*55//100, oy + s*45//100, ox + s*63//100, oy + s*55//100], fill=clr)
        draw.line([(ox + s*1//10, oy + s//2), (ox + s*3//10, oy + s//2)], fill=clr, width=w)

        draw.polygon([
            (ox + s*25//100, oy + s*4//10),
            (ox + s*35//100, oy + s//2),
            (ox + s*25//100, oy + s*6//10)
        ], fill=clr)
    
    elif name == "book" or name == "prestamo":
        s = size
        draw.rectangle([ox + s*15//100, oy + s*2//10, ox + s//2, oy + s*8//10], outline=clr, width=w)
        draw.rectangle([ox + s//2, oy + s*2//10, ox + s*85//100, oy + s*8//10], outline=clr, width=w)
        draw.line([(ox + s//2, oy + s*15//100), (ox + s//2, oy + s*85//100)], fill=clr, width=w)
        draw.line([(ox + s*25//100, oy + s*35//100), (ox + s*43//100, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*25//100, oy + s*45//100), (ox + s*40//100, oy + s*45//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*25//100, oy + s*55//100), (ox + s*43//100, oy + s*55//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*57//100, oy + s*35//100), (ox + s*75//100, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*57//100, oy + s*45//100), (ox + s*72//100, oy + s*45//100)], fill=clr, width=max(1, w-1))
    
    elif name == "chart" or name == "reportes":
        s = size
        draw.line([(ox + s*2//10, oy + s*2//10), (ox + s*2//10, oy + s*8//10)], fill=clr, width=w)
        draw.line([(ox + s*2//10, oy + s*8//10), (ox + s*85//100, oy + s*8//10)], fill=clr, width=w)
        bw = s * 12 // 100
        draw.rectangle([ox + s*28//100, oy + s*5//10, ox + s*28//100 + bw, oy + s*75//100], fill=clr)
        draw.rectangle([ox + s*45//100, oy + s*3//10, ox + s*45//100 + bw, oy + s*75//100], fill=clr)
        draw.rectangle([ox + s*62//100, oy + s*4//10, ox + s*62//100 + bw, oy + s*75//100], fill=clr)
    
    elif name == "users" or name == "usuarios": 
        s = size   
        draw.ellipse([ox + s*3//10, oy + s*15//100, ox + s*55//100, oy + s*4//10], outline=clr, width=w)
        draw.arc([ox + s*15//100, oy + s*45//100, ox + s*7//10, oy + s*85//100], 200, 340, fill=clr, width=w)
       
        draw.ellipse([ox + s*5//10, oy + s*1//10, ox + s*72//100, oy + s*32//100], outline=clr, width=w)
        draw.arc([ox + s*4//10, oy + s*35//100, ox + s*85//100, oy + s*7//10], 210, 330, fill=clr, width=w)
    
    elif name == "search":
        
        s = size
        draw.ellipse([ox + s*2//10, oy + s*15//100, ox + s*65//100, oy + s*6//10], outline=clr, width=w)
        draw.line([(ox + s*58//100, oy + s*55//100), (ox + s*8//10, oy + s*8//10)], fill=clr, width=w+1)
    
    elif name == "qr":
        # QR code 
        s = size
        draw.rectangle([ox + s*15//100, oy + s*15//100, ox + s*4//10, oy + s*4//10], outline=clr, width=w)
        draw.rectangle([ox + s*6//10, oy + s*15//100, ox + s*85//100, oy + s*4//10], outline=clr, width=w)
        draw.rectangle([ox + s*15//100, oy + s*6//10, ox + s*4//10, oy + s*85//100], outline=clr, width=w)
       
        draw.rectangle([ox + s*22//100, oy + s*22//100, ox + s*33//100, oy + s*33//100], fill=clr)
        draw.rectangle([ox + s*67//100, oy + s*22//100, ox + s*78//100, oy + s*33//100], fill=clr)
        draw.rectangle([ox + s*22//100, oy + s*67//100, ox + s*33//100, oy + s*78//100], fill=clr)
        
        draw.rectangle([ox + s*5//10, oy + s*5//10, ox + s*6//10, oy + s*6//10], fill=clr)
        draw.rectangle([ox + s*65//100, oy + s*65//100, ox + s*75//100, oy + s*75//100], fill=clr)
    
    elif name == "check" or name == "success":
        
        s = size
        draw.ellipse([ox + s*1//10, oy + s*1//10, ox + s*9//10, oy + s*9//10], outline=clr, width=w)
        draw.line([(ox + s*28//100, oy + s//2), (ox + s*43//100, oy + s*65//100)], fill=clr, width=w+1)
        draw.line([(ox + s*43//100, oy + s*65//100), (ox + s*72//100, oy + s*32//100)], fill=clr, width=w+1)
    
    elif name == "warning" or name == "alert":
        
        s = size
        draw.polygon([
            (ox + s//2, oy + s*12//100),
            (ox + s*88//100, oy + s*85//100),
            (ox + s*12//100, oy + s*85//100)
        ], outline=clr, width=w)
        draw.line([(ox + s//2, oy + s*35//100), (ox + s//2, oy + s*58//100)], fill=clr, width=w+1)
        draw.ellipse([ox + s*45//100, oy + s*65//100, ox + s*55//100, oy + s*75//100], fill=clr)
    
    elif name == "clock":
       
        s = size
        draw.ellipse([ox + s*12//100, oy + s*12//100, ox + s*88//100, oy + s*88//100], outline=clr, width=w)
        draw.line([(ox + s//2, oy + s//2), (ox + s//2, oy + s*28//100)], fill=clr, width=w)
        draw.line([(ox + s//2, oy + s//2), (ox + s*68//100, oy + s//2)], fill=clr, width=w)
    
    elif name == "calendar":
        
        s = size
        draw.rectangle([ox + s*15//100, oy + s*2//10, ox + s*85//100, oy + s*85//100], outline=clr, width=w)
        draw.line([(ox + s*15//100, oy + s*38//100), (ox + s*85//100, oy + s*38//100)], fill=clr, width=w)
        
        draw.line([(ox + s*35//100, oy + s*12//100), (ox + s*35//100, oy + s*28//100)], fill=clr, width=w)
        draw.line([(ox + s*65//100, oy + s*12//100), (ox + s*65//100, oy + s*28//100)], fill=clr, width=w)
       
        ds = max(3, s*6//100)
        draw.ellipse([ox+s*3//10, oy+s*48//100, ox+s*3//10+ds, oy+s*48//100+ds], fill=clr)
        draw.ellipse([ox+s*48//100, oy+s*48//100, ox+s*48//100+ds, oy+s*48//100+ds], fill=clr)
        draw.ellipse([ox+s*65//100, oy+s*48//100, ox+s*65//100+ds, oy+s*48//100+ds], fill=clr)
    
    elif name == "user":
       
        s = size
        draw.ellipse([ox + s*3//10, oy + s*1//10, ox + s*7//10, oy + s*45//100], outline=clr, width=w)
        draw.arc([ox + s*15//100, oy + s*5//10, ox + s*85//100, oy + s*95//100], 200, 340, fill=clr, width=w)
    
    elif name == "plus":
        
        s = size
        draw.line([(ox + s//2, oy + s*2//10), (ox + s//2, oy + s*8//10)], fill=clr, width=w+1)
        draw.line([(ox + s*2//10, oy + s//2), (ox + s*8//10, oy + s//2)], fill=clr, width=w+1)
    
    elif name == "bell":
        
        s = size
        draw.arc([ox + s*2//10, oy + s*12//100, ox + s*8//10, oy + s*65//100], 180, 0, fill=clr, width=w)
        draw.line([(ox + s*2//10, oy + s*55//100), (ox + s*15//100, oy + s*72//100)], fill=clr, width=w)
        draw.line([(ox + s*8//10, oy + s*55//100), (ox + s*85//100, oy + s*72//100)], fill=clr, width=w)
        draw.line([(ox + s*12//100, oy + s*72//100), (ox + s*88//100, oy + s*72//100)], fill=clr, width=w)
        draw.ellipse([ox + s*4//10, oy + s*75//100, ox + s*6//10, oy + s*88//100], fill=clr)
    
    elif name == "key":
       
        s = size
        draw.ellipse([ox + s*15//100, oy + s*2//10, ox + s*48//100, oy + s*55//100], outline=clr, width=w)
        draw.line([(ox + s*45//100, oy + s*45//100), (ox + s*82//100, oy + s*82//100)], fill=clr, width=w)
        draw.line([(ox + s*7//10, oy + s*7//10), (ox + s*8//10, oy + s*62//100)], fill=clr, width=w)
    
    elif name == "books" or name == "library":
 
        s = size
        draw.rectangle([ox + s*2//10, oy + s*6//10, ox + s*8//10, oy + s*72//100], fill=clr)
        draw.rectangle([ox + s*18//100, oy + s*45//100, ox + s*82//100, oy + s*57//100], fill=clr)
        draw.rectangle([ox + s*22//100, oy + s*3//10, ox + s*78//100, oy + s*42//100], fill=clr)
        draw.line([(ox + s*45//100, oy + s*3//10), (ox + s*45//100, oy + s*42//100)], fill=(255,255,255,180), width=1)
        draw.line([(ox + s*4//10, oy + s*45//100), (ox + s*4//10, oy + s*57//100)], fill=(255,255,255,180), width=1)
    
    elif name == "trending_up":

        s = size
        draw.line([(ox + s*15//100, oy + s*7//10), (ox + s*4//10, oy + s*45//100)], fill=clr, width=w)
        draw.line([(ox + s*4//10, oy + s*45//100), (ox + s*6//10, oy + s*55//100)], fill=clr, width=w)
        draw.line([(ox + s*6//10, oy + s*55//100), (ox + s*85//100, oy + s*25//100)], fill=clr, width=w)
        draw.polygon([
            (ox + s*85//100, oy + s*25//100),
            (ox + s*72//100, oy + s*22//100),
            (ox + s*78//100, oy + s*35//100)
        ], fill=clr)
    
    elif name == "shield":
        s = size
        draw.polygon([
            (ox + s//2, oy + s*1//10),
            (ox + s*85//100, oy + s*25//100),
            (ox + s*82//100, oy + s*6//10),
            (ox + s//2, oy + s*88//100),
            (ox + s*18//100, oy + s*6//10),
            (ox + s*15//100, oy + s*25//100)
        ], outline=clr, width=w)
        draw.line([(ox + s*35//100, oy + s//2), (ox + s*45//100, oy + s*62//100)], fill=clr, width=w)
        draw.line([(ox + s*45//100, oy + s*62//100), (ox + s*65//100, oy + s*38//100)], fill=clr, width=w)
    
    elif name == "settings":
        s = size
        cx, cy = ox + s//2, oy + s//2
        r_out = s * 38 // 100
        r_in = s * 22 // 100
        draw.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=clr, width=w)
      
        import math
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + int(r_in * 0.8 * math.cos(rad))
            y1 = cy + int(r_in * 0.8 * math.sin(rad))
            x2 = cx + int(r_out * math.cos(rad))
            y2 = cy + int(r_out * math.sin(rad))
            draw.line([(x1, y1), (x2, y2)], fill=clr, width=w+1)
    
    elif name == "logout":
        
        s = size
       
        draw.arc([ox + s*1//10, oy + s*1//10, ox + s*6//10, oy + s*9//10], 90, 270, fill=clr, width=w)
        
        draw.line([(ox + s*4//10, oy + s//2), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
        draw.line([(ox + s*72//100, oy + s*35//100), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
        draw.line([(ox + s*72//100, oy + s*65//100), (ox + s*88//100, oy + s//2)], fill=clr, width=w)
    
    elif name == "list":
       
        s = size
        draw.rectangle([ox + s*2//10, oy + s*1//10, ox + s*8//10, oy + s*9//10], outline=clr, width=w)
      
        draw.rectangle([ox + s*35//100, oy + s*5//100, ox + s*65//100, oy + s*18//100], outline=clr, width=w)
      
        draw.line([(ox + s*3//10, oy + s*35//100), (ox + s*7//10, oy + s*35//100)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*3//10, oy + s*5//10), (ox + s*7//10, oy + s*5//10)], fill=clr, width=max(1, w-1))
        draw.line([(ox + s*3//10, oy + s*65//100), (ox + s*6//10, oy + s*65//100)], fill=clr, width=max(1, w-1))
    
    elif name == "circle_dot":
    
        s = size
        draw.ellipse([ox + s*12//100, oy + s*12//100, ox + s*88//100, oy + s*88//100], outline=clr, width=w)
        r = s * 15 // 100
        draw.ellipse([ox + s//2 - r, oy + s//2 - r, ox + s//2 + r, oy + s//2 + r], fill=clr)
    
    elif name == "return":
    
        s = size
        draw.arc([ox + s*15//100, oy + s*2//10, ox + s*85//100, oy + s*75//100], 30, 330, fill=clr, width=w)
        # Arrowhead
        draw.polygon([
            (ox + s*72//100, oy + s*25//100),
            (ox + s*85//100, oy + s*3//10),
            (ox + s*72//100, oy + s*42//100)
        ], fill=clr)
    
    else:
   
        s = size
        draw.ellipse([ox + s*1//10, oy + s*1//10, ox + s*9//10, oy + s*9//10], fill=clr)
    
    _icon_cache[key] = img
    return img

_ctk_image_cache = {}

def get_ctk_icon(name, size=24, color="#FFFFFF", dark_color=None):
    import customtkinter as ctk
    key = f"ctk_{name}_{size}_{color}_{dark_color}"
    if key in _ctk_image_cache:
        return _ctk_image_cache[key]
    light_img = _get_icon_image(name, size, color)
    dark_img  = _get_icon_image(name, size, dark_color or color)
    result = ctk.CTkImage(light_image=light_img, dark_image=dark_img, size=(size, size))
    _ctk_image_cache[key] = result
    return result


# Cache de badges 
_badge_icon_cache = {}

def get_badge_icon(name: str, size: int = 40, icon_color: str = "#FFFFFF", bg_color: str = "#4338CA", icon_size_ratio: float = 0.55) -> 'CTkImage':
    """Returns a CTkImage with colored circle background + icon, like Tailwind badge icons.
    Uses supersampling (4x) for smooth antialiased circles.
    Resultado cacheado por (name, size, icon_color, bg_color, icon_size_ratio)."""
    import customtkinter as ctk

    key = f"badge_{name}_{size}_{icon_color}_{bg_color}_{icon_size_ratio}"
    if key in _badge_icon_cache:
        return _badge_icon_cache[key]


    scale = 4
    big = size * scale
    img_big = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img_big)
    
    c = bg_color.lstrip('#')
    r, g, b = int(c[:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    draw.ellipse([2, 2, big - 3, big - 3], fill=(r, g, b, 255))
    

    icon_s = int(big * icon_size_ratio)
    icon_img = _get_icon_image(name, icon_s, icon_color)
    offset = (big - icon_s) // 2
    img_big.paste(icon_img, (offset, offset), icon_img)
    

    img = img_big.resize((size, size), Image.LANCZOS)

    result = ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))
    _badge_icon_cache[key] = result
    return result


# Iconos
AVAILABLE_ICONS = [
    "dashboard", "home", "door", "entrada", "book", "prestamo",
    "chart", "reportes", "users", "usuarios", "search", "qr",
    "check", "success", "warning", "alert", "clock", "calendar",
    "user", "plus", "bell", "key", "books", "library",
    "trending_up", "shield", "settings", "logout", "list",
    "circle_dot", "return"
]