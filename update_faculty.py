# -*- coding: utf-8 -*-
import base64, io, os

BASE = r"C:\Users\sharvil khot\nmss-website"
IMG_DIR = os.path.join(BASE, "drive-download-20260717T122424Z-1-001")
HTML = os.path.join(BASE, "index.html")

def mime_for(fn):
    l = fn.lower()
    if l.endswith(".png"): return "image/png"
    if l.endswith(".webp"): return "image/webp"
    return "image/jpeg"

def data_uri(fn):
    with open(os.path.join(IMG_DIR, fn), "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (mime_for(fn), b)

def card(name, fn, typ):
    return ('        <div class="faculty-card"><div class="faculty-avatar">'
            '<img src="%s" alt="Dr. %s" loading="lazy"></div>'
            '<div class="faculty-card-name">Dr. %s</div>'
            '<div class="faculty-card-type">%s</div></div>'
            % (data_uri(fn), name, name, typ))

with io.open(HTML, "r", encoding="utf-8") as f:
    html = f.read()

# 1) Remove the two faculty cards
remove = [
    '        <div class="faculty-card"><div class="faculty-avatar">VV</div><div class="faculty-card-name">Dr. Vinitha Varghese</div><div class="faculty-card-type">National</div></div>\n',
    '        <div class="faculty-card"><div class="faculty-avatar">LB</div><div class="faculty-card-name">Dr. Lokesh Bathala</div><div class="faculty-card-type">National</div></div>\n',
]
for r in remove:
    assert r in html, "remove target not found: " + r[:70]
    html = html.replace(r, "", 1)

# 2) Add Elaine Chan to International panel (before its grid close)
intl_anchor = '\n      </div>\n    </div>\n    <div id="panel-natl"'
assert intl_anchor in html
html = html.replace(intl_anchor,
                    "\n" + card("Elaine Chan", "Elaine Chan.jpg", "International") + intl_anchor, 1)

# 3) Add Denis Xavier + Sonnappa to National panel (before its grid close)
natl_start = html.index('id="panel-natl"')
grid_close = html.index('\n      </div>\n    </div>', natl_start)  # natl grid + panel close
add_natl = ("\n" + card("Denis Xavier", "denis-xavier-photo.png", "National")
            + "\n" + card("Sonnappa", "Sonnappa.png", "National"))
html = html[:grid_close] + add_natl + html[grid_close:]

with io.open(HTML, "w", encoding="utf-8") as f:
    f.write(html)
print("Removed 2, added 3 faculty cards.")
