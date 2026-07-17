# -*- coding: utf-8 -*-
import base64, io, os, re
import fitz  # PyMuPDF
from PIL import Image, ImageChops

BASE = r"C:\Users\sharvil khot\nmss-website"
SRC = os.path.join(BASE, "sponser logo")
HTML = os.path.join(BASE, "index.html")

def load_pdf(fn, zoom=4, crop_top=0.0):
    doc = fitz.open(os.path.join(SRC, fn))
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
    if crop_top:
        w, h = im.size
        im = im.crop((0, int(h * crop_top), w, h))
    return im

def load_svg(fn, zoom=5):
    doc = fitz.open(os.path.join(SRC, fn))
    pix = doc[0].get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    return Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")

def load_img(fn):
    return Image.open(os.path.join(SRC, fn)).convert("RGBA")

def trim(im, tol=18, pad_ratio=0.04):
    a = im.split()[3]
    if a.getextrema()[0] < 245:            # genuine transparency -> trim by alpha
        bbox = a.getbbox()
    else:                                  # solid bg -> trim by corner colour
        rgb = im.convert("RGB")
        bg = rgb.getpixel((0, 0))
        diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg))
        mask = diff.convert("L").point(lambda p: 255 if p > tol else 0)
        bbox = mask.getbbox()
    if bbox:
        w, h = im.size
        pad = int(min(w, h) * pad_ratio)
        bbox = (max(0, bbox[0]-pad), max(0, bbox[1]-pad),
                min(w, bbox[2]+pad), min(h, bbox[3]+pad))
        im = im.crop(bbox)
    return im

def fit(im, max_h=150, max_w=380):
    w, h = im.size
    s = min(max_h/h, max_w/w)
    if s < 1:
        im = im.resize((max(1, int(w*s)), max(1, int(h*s))), Image.LANCZOS)
    return im

def has_alpha(im):
    return im.split()[3].getextrema()[0] < 245

def data_uri(im):
    im = trim(im)
    im = fit(im)
    buf = io.BytesIO()
    if has_alpha(im):
        im.save(buf, "PNG", optimize=True)
        mime = "image/png"
    else:
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im.convert("RGB"), mask=im.split()[3])
        bg.save(buf, "JPEG", quality=88, optimize=True)
        mime = "image/jpeg"
    b = base64.b64encode(buf.getvalue()).decode("ascii")
    print("  %-14s %6.1f KB  %s" % (mime.split("/")[1], len(b)/1024, im.size))
    return "data:%s;base64,%s" % (mime, b)

print("Processing logos...")
uris = {}
print("Natco");        uris["natco"]   = data_uri(load_img("Hygeia Logo Final jpg.jpg.jpeg"))
print("Intas");        uris["intas"]   = data_uri(load_img("WhatsApp Image 2026-07-17 at 12.20.31 PM.jpeg"))
print("Novartis");     uris["novartis"]= data_uri(load_svg("Logo with purpose Warm Black RGB.svg"))
print("Jain");         uris["jain"]    = data_uri(load_img("WhatsApp Image 2026-07-17 at 12.20.34 PM.jpeg"))
print("Roche");        uris["roche"]   = data_uri(load_pdf("Roche_Logo_Blue_CMYK (1).pdf", crop_top=0.16))
print("Consilience");  uris["consil"]  = data_uri(load_img("logo (1).png"))
print("Jokaan");       uris["jokaan"]  = data_uri(load_pdf("JOKAAN Final_c.pdf"))
print("ImpactGuru");   uris["impact"]  = data_uri(load_pdf("impact guru logo (1) (4).pdf"))

def card(uri, alt):
    return ('<div class="spon-card"><div class="spon-slot filled">'
            '<img src="%s" alt="%s" loading="lazy"></div></div>' % (uri, alt))

def card2(u1, a1, u2, a2):
    return ('<div class="spon-card"><div class="spon-slot filled two">'
            '<img src="%s" alt="%s" loading="lazy">'
            '<img src="%s" alt="%s" loading="lazy"></div></div>' % (u1, a1, u2, a2))

def placeholder(label):
    return ('<div class="spon-card"><div class="spon-slot"><span>%s</span></div></div>' % label)

grid = "\n".join([
    '    <div class="sponsors-grid reveal">',
    "      " + card(uris["natco"], "Natco"),
    "      " + card(uris["intas"], "Intas"),
    "      " + card(uris["novartis"], "Novartis"),
    "      " + card(uris["jain"], "Jain Foundation"),
    "      " + placeholder("Breas &amp; Biome"),
    "      " + card(uris["roche"], "Roche"),
    "      " + placeholder("Sun Pharma"),
    "      " + card2(uris["consil"], "Consilience Consultants", uris["jokaan"], "Jokaan"),
    '    </div>',
    '    <div class="sponsors-below reveal">',
    "      " + card(uris["impact"], "ImpactGuru"),
    '    </div>',
])

with io.open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

start = html.index('<div class="sponsors-grid reveal">')
sec_end = html.index('</section>', start)
wrap_close = html.rindex('</div>', start, sec_end)   # the content-wrapper </div>
new_html = html[:start] + grid.lstrip() + "\n  " + html[wrap_close:]

# --- CSS additions ---
css_anchor = '  .spon-label { font-size: 0.7rem; font-weight: 600; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.08em; }'
if css_anchor in new_html and '.spon-slot.filled' not in new_html:
    add = (css_anchor + "\n"
        '  .spon-slot.filled { border: 1px solid rgba(77,184,232,0.18); background: #fff; padding: 0.7rem 1rem; }\n'
        '  .spon-slot img { max-height: 62px; max-width: 100%; object-fit: contain; display: block; }\n'
        '  .spon-slot.two { gap: 0.9rem; }\n'
        '  .spon-slot.two img { max-height: 46px; max-width: 44%; }\n'
        '  .sponsors-below { display: flex; justify-content: center; margin-top: 1.6rem; }\n'
        '  .sponsors-below .spon-card { width: 200px; }')
    new_html = new_html.replace(css_anchor, add, 1)
    print("CSS added")
else:
    print("CSS NOT added (anchor missing or already present)")

with io.open(HTML, "w", encoding="utf-8") as f:
    f.write(new_html)
print("index.html updated")
