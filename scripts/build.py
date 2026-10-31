"""Builds the profile README's SVG cards (light + dark) into assets/.

Run: python scripts/build.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 900

SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0f1526", border="#1f2a44", ink="#e9edf5", muted="#8a94ab", faint="#2a3550",
                 accent="#ff4d6a", blue="#6a8dff", chip="#16203a",
                 far="#18223d", mid="#1f2c50", near="#283a6a", snow="#dfe6f7"),
    "light": dict(bg="#f8f6f1", border="#e3dfd4", ink="#151a2c", muted="#5e667d", faint="#d9d5ca",
                  accent="#c8102e", blue="#1f4fbf", chip="#efece4",
                  far="#e1e5ef", mid="#c9d2e6", near="#aab8d8", snow="#ffffff"),
}
FLAGS = ["#2f6fe0", "#f4f4f4", "#d7263d", "#2a9d55", "#f2c230"]

STYLE = """<style>
@keyframes sway{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.f{transform-box:fill-box;transform-origin:50% 0;animation:sway 3.2s ease-in-out infinite}
</style>"""


def svg(h, body, t):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">'
            f'{STYLE}<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="18" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            f'{body}</svg>')


def text(x, y, s, t, size=15, color="ink", font=SANS, weight=400, anchor="start", spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{t.get(color, color)}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def flags(x0, y0, cx, cy, x1, y1, n, t, size=(20, 26)):
    out = [f'<path d="M{x0},{y0} Q{cx},{cy} {x1},{y1}" fill="none" stroke="{t["muted"]}" stroke-width="1.2"/>']
    for i in range(n):
        u = (i + 0.5) / n
        px = (1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u ** 2 * x1
        py = (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u ** 2 * y1
        c = FLAGS[i % 5]
        stroke = f' stroke="{t["faint"]}"' if c == "#f4f4f4" else ""
        w, h = size
        out.append(f'<g class="f" style="animation-delay:-{i * 0.37:.2f}s">'
                   f'<rect x="{px - w / 2:.1f}" y="{py:.1f}" width="{w}" height="{h}" rx="1.5" fill="{c}" opacity="0.92"{stroke}/></g>')
    return "".join(out)


def ridge(pts, h, fill):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts) + f" V{h} H0 Z"
    return f'<path d="{d}" fill="{fill}"/>'


def snowcaps(pts, peaks, t):
    out = []
    for i in peaks:
        (lx, ly), (px, py), (rx, ry) = pts[i - 1], pts[i], pts[i + 1]
        a = (px + (lx - px) * 0.28, py + (ly - py) * 0.28)
        b = (px + (rx - px) * 0.28, py + (ry - py) * 0.28)
        m = ((a[0] + b[0]) / 2, max(a[1], b[1]) - 3)
        out.append(f'<polygon points="{px},{py} {b[0]:.1f},{b[1]:.1f} {m[0]+4:.1f},{m[1]:.1f} {m[0]-3:.1f},{m[1]+3:.1f} {a[0]:.1f},{a[1]:.1f}" fill="{t["snow"]}" opacity="0.85"/>')
    return "".join(out)


def chip_w(s, size=12):
    return len(s) * size * 0.62 + 22


def chip(x, y, s, t, size=12):
    w = chip_w(s, size)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{t["chip"]}" stroke="{t["border"]}"/>'
            + text(x + w / 2, y + 16, s, t, size, "muted", MONO, anchor="middle")), w


def hero(t):
    H = 420
    far = [(0, 320), (90, 300), (170, 312), (250, 288), (330, 300), (420, 262), (500, 280), (580, 236),
           (650, 262), (720, 214), (790, 250), (860, 226), (900, 240)]
    mid = [(0, 352), (100, 334), (190, 346), (280, 318), (360, 338), (450, 306), (540, 330), (620, 292),
           (700, 318), (780, 296), (860, 322), (900, 310)]
    near = [(0, 392), (110, 372), (210, 386), (300, 360), (400, 380), (490, 350), (580, 372), (670, 338),
            (760, 362), (840, 346), (900, 358)]
    trail = "M60,406 L170,394 L250,382 L330,372 L420,354 L500,338 L580,320 L640,288 L690,252 L720,216"
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17"/></clipPath><g clip-path="url(#c)">',
         ridge(far, H, t["far"]), snowcaps(far, [7, 9, 11], t), ridge(mid, H, t["mid"]), ridge(near, H, t["near"]),
         f'<path d="{trail}" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>',
         f'<circle r="5" fill="{t["accent"]}"><animateMotion dur="9s" repeatCount="indefinite" path="{trail}"/>'
         f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.9;1" dur="9s" repeatCount="indefinite"/></circle>',
         f'<circle cx="60" cy="406" r="4" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>',
         text(72, 404, "DAMAK", t, 11, "ink", MONO, 600, spacing=1),
         f'<circle cx="330" cy="372" r="4" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>',
         text(342, 370, "KATHMANDU · 2024", t, 11, "ink", MONO, 600, spacing=1),
         f'<line x1="720" y1="216" x2="720" y2="186" stroke="{t["ink"]}" stroke-width="1.5"/>',
         f'<polygon points="720,186 742,192 720,198" fill="{t["accent"]}"/>',
         text(708, 192, "NEXT", t, 11, "accent", MONO, 700, anchor="end", spacing=1.5),
         text(708, 207, "internship / junior role", t, 11, "ink", MONO, anchor="end"),
         flags(540, -4, 720, 78, 904, 6, 11, t),
         "</g>",
         text(48, 64, "27.7172° N · 85.3240° E", t, 12, "muted", MONO, spacing=1.5),
         text(46, 136, "Arman Khan", t, 64, "ink", SANS, 700, spacing=-1.5),
         text(48, 178, "Full-stack developer. I build the interface", t, 20, "muted"),
         text(48, 205, "people use and the systems behind it.", t, 20, "muted"),
         f'<rect x="48" y="226" width="246" height="30" rx="15" fill="{t["chip"]}" stroke="{t["border"]}"/>',
         f'<circle cx="66" cy="241" r="4" fill="{t["accent"]}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>',
         text(78, 246, "currently building TriLearn", t, 12, "ink", MONO),
         ]
    return svg(H, "".join(b), t)


def button(label, color, t):
    w = int(len(label) * 13 * 0.62 + 64)
    b = (f'<rect x="10" y="10" width="7" height="24" rx="2" fill="{color}"' +
         (f' stroke="{t["faint"]}"' if color == "#f4f4f4" else "") + "/>" +
         text(28, 27, label, t, 13, "ink", MONO, 600) + text(w - 14, 27, "↗", t, 14, "accent", MONO, anchor="end"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44">'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="43" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>{b}</svg>')


def contours(cx, cy, t):
    out = []
    for i, (rx, ry) in enumerate([(26, 12), (48, 22), (72, 33), (98, 44)]):
        out.append(f'<ellipse cx="{cx + i * 4}" cy="{cy - i}" rx="{rx}" ry="{ry}" transform="rotate(-8 {cx} {cy})" '
                   f'fill="none" stroke="{t["faint"]}" stroke-width="1"/>')
    return "".join(out)


def heading(num, kicker, title, right, t):
    H = 96
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17"/></clipPath><g clip-path="url(#c)">',
         contours(800, 50, t), "</g>",
         text(40, 40, f"{num} — {kicker}", t, 12, "accent", MONO, 700, spacing=2),
         text(40, 72, title, t, 26, "ink", SANS, 700, spacing=-0.5),
         text(860, 72, right, t, 12, "muted", MONO, anchor="end")]
    return svg(H, "".join(b), t)


def project(num, name, lang, lines, tags, t, first=False, last=False):
    H = 168
    b = [f'<line x1="44" y1="{84 if first else 0}" x2="44" y2="{84 if last else H}" stroke="{t["accent"]}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>',
         f'<circle cx="44" cy="84" r="16" fill="{t["bg"]}" stroke="{t["accent"]}" stroke-width="2"/>',
         text(44, 88, num, t, 11, "accent", MONO, 700, anchor="middle"),
         f'<rect x="80.5" y="8.5" width="811" height="151" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
         text(108, 50, name, t, 22, "ink", SANS, 700, spacing=-0.3),
         text(862, 50, f"{lang}  ↗", t, 12, "muted", MONO, anchor="end")]
    for i, line in enumerate(lines):
        b.append(text(108, 78 + i * 21, line, t, 15, "muted"))
    x = 108
    for tag in tags:
        c, w = chip(x, 120, tag, t, 11)
        b.append(c)
        x += w + 8
    # project cards sit on the page background, so no outer frame
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'{"".join(b)}</svg>')


def stack(t):
    rows = [("frontend", ["React", "Vite", "Tailwind CSS", "TypeScript", "JavaScript"]),
            ("backend", ["Node.js", "Express", "Django REST", "Prisma", "Socket.IO", "JWT auth"]),
            ("data", ["PostgreSQL", "Redis"]),
            ("mobile", ["Expo", "React Native"]),
            ("languages", ["JavaScript", "TypeScript", "Python", "Java", "C++"]),
            ("tools", ["Git", "GitHub Actions", "Docker", "ESLint"])]
    b, y = [], 112
    for label, items in rows:
        b.append(f'<rect x="40" y="{y}" width="16" height="16" rx="4" fill="none" stroke="{t["accent"]}" stroke-width="1.6"/>'
                 f'<path d="M44,{y+8} l3,3 l6,-7" fill="none" stroke="{t["accent"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(text(68, y + 13, label, t, 13, "ink", MONO, 600))
        x = 200
        for it in items:
            if x + chip_w(it) > 864:
                x, y = 200, y + 34
            c, w = chip(x, y - 4, it, t)
            b.append(c)
            x += w + 8
        y += 46
        b.append(f'<line x1="40" y1="{y-14}" x2="860" y2="{y-14}" stroke="{t["border"]}" stroke-dasharray="3 5"/>')
    H = y + 14
    head = [f'<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17"/></clipPath><g clip-path="url(#c)">',
            contours(800, 50, t), "</g>",
            text(40, 40, "02 — PACKING LIST", t, 12, "accent", MONO, 700, spacing=2),
            text(40, 72, "What I carry up the mountain", t, 26, "ink", SANS, 700, spacing=-0.5)]
    return svg(H, "".join(head + b), t)


def footer(t):
    H = 230
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17"/></clipPath><g clip-path="url(#c)">',
         flags(-10, 14, 450, 96, 910, 14, 24, t, (22, 28)),
         ridge([(0, 214), (120, 196), (220, 206), (330, 184), (450, 200), (560, 178), (680, 198), (790, 186), (900, 202)], H, t["far"]),
         "</g>",
         text(450, 134, "Let's build something.", t, 32, "ink", SANS, 700, "middle", -0.5),
         text(450, 166, "open to internships & junior roles  ·  armankhan.com.np ↗", t, 13, "muted", MONO, anchor="middle")]
    return svg(H, "".join(b), t)


PROJECTS = [
    ("01", "TriLearn", "JavaScript",
     ["Self-hosted college management system: admissions, QR attendance,",
      "marks, assignments, real-time notices and a student mobile app."],
     ["React 19", "Express 5", "PostgreSQL", "Redis", "Socket.IO", "Expo", "Docker"]),
    ("02", "Sajilo Bus Ticket", "Python",
     ["Bus booking with a Django REST API and a React frontend. Safe seat",
      "holds, eSewa payments and printable QR tickets."],
     ["Django REST", "React", "PostgreSQL", "JWT", "eSewa"]),
    ("03", "Nepal Patra", "JavaScript",
     ["A Nepal-focused news aggregator with categories, search,",
      "bookmarks and a system-aware dark mode."],
     ["React", "Vite", "Axios", "Tailwind CSS"]),
    ("04", "VibeTyper", "JavaScript",
     ["A modern, interactive typing speed test."],
     ["React 19", "Vite", "Tailwind CSS"]),
]

BUTTONS = [("portfolio", "#2f6fe0"), ("linkedin", "#f4f4f4"), ("instagram", "#d7263d"), ("facebook", "#2a9d55")]


def main():
    OUT.mkdir(exist_ok=True)
    for mode, t in THEMES.items():
        files = {"hero": hero(t), "stack": stack(t), "footer": footer(t),
                 "work-head": heading("01", "SUMMITS", "Things I've built", "4 of 13 repos", t),
                 "trail-head": heading("03", "TRAIL LOG", "A year of commits", "updated every 12h", t)}
        for i, p in enumerate(PROJECTS):
            files[f"work-{p[1].lower().replace(' ', '-')}"] = project(*p, t, first=i == 0, last=i == len(PROJECTS) - 1)
        for label, color in BUTTONS:
            files[f"btn-{label}"] = button(label, color, t)
        for name, content in files.items():
            (OUT / f"{name}-{mode}.svg").write_text(content, encoding="utf-8")
    print("built", len(list(OUT.glob("*.svg"))), "files")


if __name__ == "__main__":
    main()
