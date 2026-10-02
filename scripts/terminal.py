# Generates assets/terminal.svg — edit `script` below, then run: python3 scripts/terminal.py
from html import escape
W, CH, FS, LH = 900, 9, 15, 28   # width, char width, font size, line height
X0, Y0 = 28, 78
BG, BAR = "#0d1117", "#161b22"
PROMPT = "alex@github:~$ "
script = [
    ("whoami", ["Victor Alexandre (Alex) · Software Engineer — Backend / Fullstack"]),
    ("cat stack.txt", ["TypeScript · Go · Node.js / Deno · Kafka · PostgreSQL · Swift"]),
    ("cat now.txt", ["building NoteCast Editor — native macOS Markdown editor (Swift/AppKit)"]),
]
TYPE, PAUSE = 0.055, 0.45
css, body = [], []
t, y, n = 0.6, Y0, 0

def text(x, y, s, fill, extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" textLength="{len(s)*CH}" '
            f'lengthAdjust="spacingAndGlyphs"{extra}>{escape(s)}</text>')

def prompt(y):
    return (f'<text x="{X0}" y="{y}" textLength="{len(PROMPT)*CH}" lengthAdjust="spacingAndGlyphs">'
            f'<tspan fill="#b579f9">alex@github</tspan><tspan fill="#8b949e">:</tspan>'
            f'<tspan fill="#00bfbf">~</tspan><tspan fill="#8b949e">$ </tspan></text>')

def show(cls, at):
    css.append(f".{cls}{{animation:show 0s {at:.2f}s both}}")

for cmd, outs in script:
    n += 1
    cx = X0 + len(PROMPT) * CH
    dur = len(cmd) * TYPE
    body.append(f'<g class="l{n}">{prompt(y)}{text(cx, y, cmd, "#e6edf3")}'
                f'<g class="t{n}"><rect class="c{n}" x="{cx}" y="{y-FS+2}" width="{CH}" height="{FS+3}" fill="#00bfbf"/>'
                f'<rect x="{cx+CH}" y="{y-FS-2}" width="{len(cmd)*CH+20}" height="{FS+8}" fill="{BG}"/></g></g>')
    show(f"l{n}", t)
    css.append(f".t{n}{{animation:type{n} {dur:.2f}s steps({len(cmd)}) {t:.2f}s both}}"
               f"@keyframes type{n}{{to{{transform:translateX({len(cmd)*CH}px)}}}}")
    t += dur + 0.2
    css.append(f".c{n}{{animation:hide 0s {t:.2f}s both}}")
    for o in outs:
        n += 1; y += LH
        body.append(f'<g class="l{n}">{text(X0, y, o, "#c9d1d9")}</g>')
        show(f"l{n}", t)
    t += PAUSE; y += LH + 6

n += 1
cx = X0 + len(PROMPT) * CH
body.append(f'<g class="l{n}">{prompt(y)}<rect class="blink" x="{cx}" y="{y-FS+2}" width="{CH}" height="{FS+3}" fill="#00bfbf"/></g>')
show(f"l{n}", t)
H = y + 30

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: Victor Alexandre, Software Engineer, Backend / Fullstack">
<style>
text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace;font-size:{FS}px;white-space:pre}}
@keyframes show{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes hide{{to{{opacity:0}}}}
@keyframes blink{{50%{{opacity:0}}}}
.blink{{animation:blink 1s step-end infinite}}
{chr(10).join(css)}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}" stroke="#30363d"/>
<path d="M1 13a12 12 0 0 1 12-12h{W-26}a12 12 0 0 1 12 12v23H1z" fill="{BAR}"/>
<line x1="1" y1="36" x2="{W-1}" y2="36" stroke="#30363d"/>
<circle cx="24" cy="18.5" r="6" fill="#ff5f57"/><circle cx="44" cy="18.5" r="6" fill="#febc2e"/><circle cx="64" cy="18.5" r="6" fill="#28c840"/>
<text x="{W/2}" y="23" fill="#8b949e" text-anchor="middle" style="font-size:13px">alex — zsh</text>
{chr(10).join(body)}
</svg>'''
open("assets/terminal.svg", "w").write(svg)
print(H, round(t, 2), "s")
