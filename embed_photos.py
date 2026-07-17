import base64, re, os, sys

BASE = r"C:\Users\sharvil khot\nmss-website"
IMG_DIR = os.path.join(BASE, "drive-download-20260702T155905Z-3-001")
HTML = os.path.join(BASE, "index.html")

# card-name (exact text WITHOUT prefix) -> image filename
MAP = {
    "Andoni Urtizberea": "Andoni urtizberea.png",
    "Urvi Desai": "Urvi desai.jpg",
    "Volker Straub": "Volker straub.jpg",
    "Annemieke Aartsma-Rus": "Annemieke.jpg",
    "Sanjeev Nandedkar": "Sanjeev Nandekar.jpg",
    "Edoardo Malfatti": "Eduardo Malfatti.jpg",
    "Kumaran Deiva": "DEIVA Kumaran-06ce9c8f.jpg",
    "Umapathi": "Umapathi.jpg",
    "Nalini Atchayaram": "Nalini.jpg",
    "Vineeth Jaison": "Vineeth jaison.jpg",
    "Satish Khadilkar": "Dr. Satish Khadilkar.webp",
    "V Vishwanathan": "Viswanathan.jpg",
    "Gayathri": "Gayathri.jpg",
    "Anita Mahadevan": "Anita Mahadevan.jpg",
    "Meenakshi Bhat": "Meenakshi Bhat.jpg",
    "Renu Suthar": "Renu-Suthar.jpg",
    "Umesh Kalane": "Umesh Kalane.jpg",
    "Radhika Manohar": "Radhika Manohar.jpg",
    "Kushnuma Mansukhani": "Khushnuma.jpg",
    "Ilin Kinimi": "Ilin.jpg_",
}

def mime_for(fn):
    l = fn.lower()
    if l.endswith(".png"): return "image/png"
    if l.endswith(".webp"): return "image/webp"
    return "image/jpeg"  # jpg, jpeg, jpg_

def data_uri(fn):
    p = os.path.join(IMG_DIR, fn)
    with open(p, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime_for(fn)};base64,{b}"

with open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

# 1) Normalise all faculty-card-name prefixes to "Dr. "
def fix_prefix(m):
    inner = m.group(1)
    inner = re.sub(r'^(?:Prof\.|Ms\.|Dr\.)\s*', '', inner)
    return f'<div class="faculty-card-name">Dr. {inner}</div>'

html, npref = re.subn(r'<div class="faculty-card-name">(.*?)</div>', fix_prefix, html)
print(f"Prefix normalised on {npref} cards")

# 2) Inject photos. Match each full card block and replace the avatar initials.
inserted = []
missing = []
for name, fn in MAP.items():
    uri = data_uri(fn)
    # find the card block containing this name; replace its avatar div contents
    pat = re.compile(
        r'(<div class="faculty-card"><div class="faculty-avatar">)([^<]*)(</div><div class="faculty-card-name">Dr\. '
        + re.escape(name) + r'</div>)'
    )
    newhtml, n = pat.subn(lambda m: m.group(1) + f'<img src="{uri}" alt="Dr. {name}" loading="lazy">' + m.group(3), html)
    if n == 1:
        html = newhtml
        inserted.append(name)
    else:
        missing.append((name, n))

# 3) CSS: make avatar render an embedded img nicely
css_anchor = '.faculty-avatar { width: 52px; height: 52px; border-radius: 50%;'
if css_anchor in html and '.faculty-avatar img' not in html:
    add = ('.faculty-avatar { overflow: hidden; }\n'
           '  .faculty-avatar img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block; }\n  ')
    html = html.replace(css_anchor, add + css_anchor, 1)
    print("CSS rule added")
else:
    print("CSS rule NOT added (anchor missing or already present)")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nInserted photos ({len(inserted)}):")
for n in inserted: print("  +", n)
if missing:
    print(f"\nFAILED matches ({len(missing)}):")
    for n, c in missing: print(f"  ! {n} (matched {c})")
