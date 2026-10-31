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
    "dark": dict(bg="#0f131a", border="#232a36", ink="#e8ebf0", muted="#8b93a3", faint="#262d3a",
                 accent="#ff5a5f", chip="#161b24"),
    "light": dict(bg="#fbfbf9", border="#e4e4de", ink="#16191f", muted="#5f6673", faint="#e2e2dc",
                  accent="#d1242f", chip="#f1f1ec"),
}

STYLE = """<style>
@keyframes glow{0%,100%{opacity:.3}12%{opacity:1}30%{opacity:.3}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.d{animation:glow 7s ease-in-out infinite}
.caret{animation:blink 1.1s steps(1) infinite}
</style>"""

# 5x7 dot-matrix glyphs for the monogram
GLYPHS = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
}


def svg(h, body, t, frame=True):
    rect = (f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>'
            if frame else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">'
            f'{STYLE}{rect}{body}</svg>')


def text(x, y, s, t, size=15, color="ink", font=SANS, weight=400, anchor="start", spacing=0):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{t.get(color, color)}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def chip_w(s, size=12):
    return len(s) * size * 0.62 + 22


def chip(x, y, s, t, size=12):
    w = chip_w(s, size)
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="6" fill="{t["chip"]}" stroke="{t["border"]}"/>'
            + text(x + w / 2, y + 16, s, t, size, "muted", MONO, anchor="middle")), w


def monogram(x0, y0, t, gap=14, r=4.2, animate=True):
    out = []
    for gi, ch in enumerate("AK"):
        for row, line in enumerate(GLYPHS[ch]):
            for col, c in enumerate(line):
                cx = x0 + (gi * 6 + col) * gap
                cy = y0 + row * gap
                if c == "#":
                    cls = f' class="d" style="animation-delay:{(gi * 6 + col) * 0.12 + row * 0.04:.2f}s"' if animate else ""
                    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t["accent"]}"{cls}/>')
                else:
                    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r * 0.55:.1f}" fill="{t["faint"]}"/>')
    return "".join(out)


def hero(t):
    H = 250
    b = [text(48, 62, "~/armancore", t, 13, "muted", MONO),
         f'<rect class="caret" x="142" y="51" width="8" height="14" fill="{t["accent"]}"/>',
         text(45, 134, "Arman Khan", t, 60, "ink", SANS, 700, spacing=-1.5),
         text(48, 174, "I build the interface people use and the systems behind it.", t, 18, "muted"),
         text(48, 210, "full-stack  ·  javascript  ·  python  ·  sql", t, 12, "muted", MONO, spacing=0.5),
         monogram(708, 76, t)]
    return svg(H, "".join(b), t)


def button(label, t):
    w = int(len(label) * 13 * 0.62 + 54)
    b = (text(18, 27, label, t, 13, "ink", MONO, 600) + text(w - 16, 27, "↗", t, 14, "accent", MONO, anchor="end"))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="44" viewBox="0 0 {w} 44">'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="43" rx="8" fill="{t["bg"]}" stroke="{t["border"]}"/>{b}</svg>')


def heading(num, title, right, t):
    H = 64
    b = [text(2, 40, num, t, 13, "accent", MONO, 700),
         text(38, 41, title, t, 22, "ink", SANS, 700, spacing=-0.3),
         text(898, 40, right, t, 12, "muted", MONO, anchor="end"),
         f'<line x1="0" y1="60" x2="{W}" y2="60" stroke="{t["border"]}"/>']
    return svg(H, "".join(b), t, frame=False)


def project(num, name, lang, lines, tags, t):
    H = 150
    b = [text(32, 46, num, t, 13, "accent", MONO, 700),
         text(72, 47, name, t, 21, "ink", SANS, 700, spacing=-0.3),
         text(868, 46, f"{lang}  ↗", t, 12, "muted", MONO, anchor="end")]
    for i, line in enumerate(lines):
        b.append(text(72, 76 + i * 21, line, t, 15, "muted"))
    x = 72
    for tag in tags:
        c, w = chip(x, 112, tag, t, 11)
        b.append(c)
        x += w + 8
    return svg(H, "".join(b), t)


def stack(t):
    rows = [("frontend", ["React", "Vite", "Tailwind CSS", "TypeScript", "JavaScript"]),
            ("backend", ["Node.js", "Express", "Django REST", "Prisma", "Socket.IO", "JWT auth"]),
            ("databases", ["PostgreSQL", "MS SQL Server", "Redis"]),
            ("mobile", ["Expo"]),
            ("languages", ["JavaScript", "TypeScript", "Python", "Java", "C++"]),
            ("tools", ["Git", "GitHub Actions", "Docker", "ESLint"])]
    b, y = [], 40
    for i, (label, items) in enumerate(rows):
        b.append(text(32, y + 13, label, t, 13, "muted", MONO))
        x = 170
        for it in items:
            if x + chip_w(it) > 868:
                x, y = 170, y + 34
            c, w = chip(x, y - 4, it, t)
            b.append(c)
            x += w + 8
        y += 46
        if i < len(rows) - 1:
            b.append(f'<line x1="32" y1="{y-14}" x2="868" y2="{y-14}" stroke="{t["border"]}"/>')
    return svg(y + 6, "".join(b), t)


def footer(t):
    H = 120
    b = [text(40, 56, "Thanks for stopping by.", t, 22, "ink", SANS, 700, spacing=-0.3),
         text(40, 84, "armankhan.com.np ↗", t, 13, "muted", MONO),
         monogram(760, 39, t, gap=8, r=2.4, animate=False)]
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

BUTTONS = ["portfolio", "linkedin", "instagram", "facebook"]


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for mode, t in THEMES.items():
        files = {"hero": hero(t), "stack": stack(t), "footer": footer(t),
                 "head-work": heading("01", "Selected work", "4 of 13 repos", t),
                 "head-stack": heading("02", "Stack", "", t),
                 "head-commits": heading("03", "Contributions", "last 12 months", t)}
        for p in PROJECTS:
            files[f"work-{p[1].lower().replace(' ', '-')}"] = project(*p, t)
        for label in BUTTONS:
            files[f"btn-{label}"] = button(label, t)
        for name, content in files.items():
            (OUT / f"{name}-{mode}.svg").write_text(content, encoding="utf-8")
    print("built", len(list(OUT.glob("*.svg"))), "files")


if __name__ == "__main__":
    main()
