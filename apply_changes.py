import base64, re, os

BASE = r"C:\Users\sharvil khot\nmss-website"
HTML = os.path.join(BASE, "index.html")
MAP_IMG = r"D:\downloads\ChatGPT Image Jul 8, 2026, 12_32_07 PM.png"
MYOSF_IMG = r"D:\downloads\WhatsApp Image 2026-07-09 at 9.01.32 PM.jpeg"

def data_uri(path, mime):
    with open(path, "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b}"

map_uri = data_uri(MAP_IMG, "image/png")
myosf_uri = data_uri(MYOSF_IMG, "image/jpeg")

html = open(HTML, encoding="utf-8").read()

# --- 1) Extract the two existing partner-logo <img> srcs from the nav ---
m = re.search(r'<div class="nav-partner-logos">(.*?)</div>', html, re.S)
imgs = re.findall(r'<img[^>]*>', m.group(1))
stjohns_img = imgs[0]   # St John's
raindrops_img = imgs[1] # Raindrops

# --- 2) Remove the partner-logos block from the nav (keep hamburger) ---
html = html.replace(m.group(0) + "\n    ", "", 1)
assert '<div class="nav-partner-logos">' not in html, "partner logos still in nav"

# --- 3) Replace hero-dots with the map background + scrim layers ---
html = html.replace(
    '<div class="hero-dots"></div>',
    '<div class="hero-map"></div>\n  <div class="hero-scrim"></div>'
)

# --- 4) Insert hero logos row + rebuild eyebrow/heading ---
hero_logos = (
    '  <div class="hero-logos">\n'
    f'    <div class="hero-logo-chip"><img src="{myosf_uri}" alt="Myologie Sans Frontieres"></div>\n'
    f'    <div class="hero-logo-chip">{re.sub(r"^<img", "<img", stjohns_img)}</div>\n'
    f'    <div class="hero-logo-chip">{raindrops_img}</div>\n'
    '  </div>\n'
)
html = html.replace('<div class="hero-content">', hero_logos + '  <div class="hero-content">', 1)

old_head = (
    '<div class="hero-badge"><span class="hero-badge-dot"></span>Inaugural Edition &middot; July 2026</div>\n'
    '    <p class="hero-eyebrow">Indian Neuromuscular Summer School</p>\n'
    '    <h1 class="hero-heading">\n'
    '      Advancing<br>\n'
    '      <em>Neuromuscular</em><br>\n'
    '      Excellence in India\n'
    '    </h1>'
)
new_head = (
    '<div class="hero-badge"><span class="hero-badge-dot"></span>Inaugural Edition &middot; July 2026, Bangalore</div>\n'
    '    <p class="hero-eyebrow">Inaugural Edition &middot; Bangalore, India</p>\n'
    '    <h1 class="hero-heading">\n'
    '      Indian <em>Neuromuscular</em><br>\n'
    '      Summer School\n'
    '    </h1>'
)
assert old_head in html, "hero heading block not found"
html = html.replace(old_head, new_head, 1)

# --- 5) CSS additions ---
css = """
  .hero-map { position: absolute; inset: 0; z-index: 0; background: url('__MAPURI__') no-repeat center right; background-size: cover; }
  .hero-scrim { position: absolute; inset: 0; z-index: 1; background: linear-gradient(90deg, rgba(13,27,42,0.97) 0%, rgba(13,27,42,0.88) 32%, rgba(13,27,42,0.62) 60%, rgba(13,27,42,0.32) 100%); }
  .hero-logos { display: flex; align-items: center; gap: 0.9rem; margin-bottom: 2rem; flex-wrap: wrap; animation: fadeUp 0.8s ease both; }
  .hero-logo-chip { background: #fff; border-radius: 10px; padding: 0.5rem 0.85rem; display: flex; align-items: center; box-shadow: 0 4px 18px rgba(0,0,0,0.22); }
  .hero-logo-chip img { height: 38px; width: auto; object-fit: contain; display: block; }
  .symp-table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; border-radius: 12px; border: 1px solid rgba(16,185,129,0.28); box-shadow: 0 8px 28px rgba(6,95,70,0.07); }
  .symp-table { width: 100%; border-collapse: collapse; min-width: 760px; background: #fff; }
  .symp-table thead th { background: linear-gradient(90deg, #065F46, #10B981); color: #fff; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; padding: 0.85rem 1rem; text-align: left; }
  .symp-table tbody td { padding: 0.9rem 1rem; border-top: 1px solid rgba(16,185,129,0.15); font-size: 0.86rem; color: var(--ink-soft); vertical-align: top; }
  .symp-table tbody tr:nth-child(even) td { background: #F0FDF9; }
  .symp-table tbody tr:hover td { background: #ECFDF5; }
  .symp-table .st-no { font-family: "Space Mono", monospace; font-weight: 700; color: #065F46; text-align: center; width: 56px; }
  .symp-table .st-date { font-weight: 600; color: var(--ink); white-space: nowrap; }
  .symp-table .st-day { color: var(--blue-mid); font-size: 0.78rem; }
  .symp-table .st-time { white-space: nowrap; color: var(--ink-muted); font-size: 0.82rem; }
  .symp-table .st-topic { font-weight: 500; color: var(--ink); }
  .symp-table .st-topic small { display: block; font-weight: 400; color: var(--ink-muted); margin-top: 0.15rem; font-size: 0.76rem; }
"""
css = css.replace("__MAPURI__", map_uri)
html = html.replace("  #schedule { background: var(--cream); }",
                    css + "\n  #schedule { background: var(--cream); }", 1)

# --- 6) Replace the 7-day symposia grid with a horizontal table (no charges) ---
old_days = re.search(r'<div class="tracks-days reveal">.*?</div>\s*</div>\s*</div>', html, re.S)
rows = [
    ("1", "20 July 2026", "Monday",    "9.00 am &ndash; 5.30 pm",  "DMD in Focus", "MDT, Advances &amp; Advocacy"),
    ("2", "21 July 2026", "Tuesday",   "9.00 am &ndash; 5.30 pm",  "Neuromuscular Physiotherapy", "A Cornerstone in NMD"),
    ("3", "22 July 2026", "Wednesday", "10.00 am &ndash; 4.30 pm", "Targets to Therapies &mdash; The Journey of Translational Research", "For Clinicians &amp; Scientists"),
    ("4", "24 July 2026", "Friday",    "8.30 am &ndash; 5.30 pm",  "Challenging Existing Norms in Respiratory Care of Neuromuscular Disorders", ""),
    ("5", "25 July 2026", "Saturday",  "9.00 am &ndash; 5.30 pm",  "SMA in Focus", "MDT, Advances &amp; Advocacy"),
    ("6", "26 July 2026", "Sunday",    "9.00 am &ndash; 5.30 pm",  "Fragmentation to Collaboration", "Multidisciplinary Treatment in Neuromuscular Disorders"),
]
tr = ""
for no, date, day, time, topic, sub in rows:
    subhtml = f"<small>{sub}</small>" if sub else ""
    tr += (f'          <tr><td class="st-no">{no}</td>'
           f'<td class="st-date">{date}</td>'
           f'<td class="st-day">{day}</td>'
           f'<td class="st-time">{time}</td>'
           f'<td class="st-topic">{topic}{subhtml}</td></tr>\n')
new_days = (
    '<div class="tracks-days reveal">\n'
    '      <div class="tracks-days-label">Open Symposia &mdash; Topics &amp; Dates</div>\n'
    '      <div class="symp-table-wrap">\n'
    '        <table class="symp-table">\n'
    '          <thead><tr><th>Sl.No</th><th>Date</th><th>Day</th><th>Timing</th><th>Topic</th></tr></thead>\n'
    '          <tbody>\n'
    + tr +
    '          </tbody>\n'
    '        </table>\n'
    '      </div>\n'
    '    </div>\n'
    '  </div>\n'
    '</div>'
)
assert old_days, "tracks-days block not found"
html = html.replace(old_days.group(0), new_days, 1)

# Fix contradictory "Seven standalone" copy (PDF lists 6 symposia)
html = html.replace("Seven standalone one-day symposia", "Standalone one-day symposia")

open(HTML, "w", encoding="utf-8").write(html)
print("Done. map+myosf embedded; logos moved to hero; heading + symposia table updated.")
