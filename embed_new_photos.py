# -*- coding: utf-8 -*-
import base64, re, os

BASE = r"C:\Users\sharvil khot\nmss-website"
IMG_DIR = os.path.join(BASE, "drive-download-20260717T122424Z-1-001")
HTML = os.path.join(BASE, "index.html")

# faculty-card-name (WITHOUT "Dr. " prefix, exactly as in HTML) -> image filename
MAP = {
    "Joanne Ng": "Joanne Ng.jpg",
    "Ramya R Babu": "Ramya Babu.jpg",
    "Victoria Selby": "Vic Selby.jpg",
    "V Y Vishnu": "Vishnu VY.jpg",
    "Sruthi Nair": "Sruthi Nair.jpg",
    "Gauri Krishna": "Gauri Krishna.png",
    "Suma Uday": "Dr. Suma Uday.jpg",
    "Saravanan Palaniappan": "Saravanan palaniappan.png",
    "Ann Agnes Mathew": "Ann Agnes Mathew_.jpg",
}

def mime_for(fn):
    l = fn.lower()
    if l.endswith(".png"): return "image/png"
    if l.endswith(".webp"): return "image/webp"
    return "image/jpeg"

def data_uri(fn):
    with open(os.path.join(IMG_DIR, fn), "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (mime_for(fn), b)

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

inserted, failed = [], []
for name, fn in MAP.items():
    uri = data_uri(fn)
    # avatar content (initials or existing img) -> new img, keyed by the card name div
    pat = re.compile(
        r'(<div class="faculty-avatar">)[^<]*(</div><div class="faculty-card-name">Dr\. '
        + re.escape(name) + r'</div>)')
    img = '<img src="%s" alt="Dr. %s" loading="lazy">' % (uri, name)
    newhtml, n = pat.subn(lambda m: m.group(1) + img + m.group(2), html, count=1)
    if n == 1:
        html = newhtml
        inserted.append(name)
    else:
        failed.append((name, n))

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)

print("Inserted (%d):" % len(inserted))
for n in inserted: print("  +", n)
if failed:
    print("FAILED (%d):" % len(failed))
    for n, c in failed: print("  !", n, "matched", c)
