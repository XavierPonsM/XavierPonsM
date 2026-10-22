# Generates the profile banner and project cards (light + dark).
# To add a project: append it to PROJECTS (pick a glyph), run `python assets/generate.py`,
# and add its <picture> block to README.md.
import math, html, os
OUT = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    'light': dict(bg='#f6f8fa', fg='#1f2328', muted='#59636e', faint='#8c959f', accent='#0969da', grid='#eaeef2'),
    'dark':  dict(bg='#161b22', fg='#e6edf3', muted='#9198a1', faint='#6e7681', accent='#4493f8', grid='#1c2128'),
}
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


def wave(x0, y0, w, amp, freq, phase=0, n=240):
    pts = []
    for i in range(n + 1):
        t = i / n
        env = math.sin(math.pi * t) ** 1.5
        pts.append(f"{x0 + w * t:.1f},{y0 + amp * env * math.sin(2 * math.pi * freq * t + phase):.1f}")
    return "M" + " L".join(pts)


def animated_wave(x0, y0, w, amp, freq, phase0, dur, colour, opacity):
    frames = [wave(x0, y0, w, amp, freq, phase0 + 2 * math.pi * k / 16) for k in range(17)]
    return (f'<path d="{frames[0]}" fill="none" stroke="{colour}" stroke-width="2" stroke-opacity="{opacity}">'
            f'<animate attributeName="d" dur="{dur}s" repeatCount="indefinite" values="{";".join(frames)}"/></path>')


def banner(th):
    c = THEMES[th]; W, H = 1200, 260
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for i, (f, a, op, dur) in enumerate([(6, 70, .9, 3.2), (9, 42, .45, 2.3), (4, 90, .25, 4.6)]):
        s.append(animated_wave(660, 130, 500, a, f, i * 1.1, dur, c["accent"], op))
    s.append(f'<text x="40" y="112" font-family="{FONT}" font-size="54" font-weight="700" fill="{c["fg"]}">Xavier Pons Martí</text>')
    s.append(f'<text x="42" y="156" font-family="{FONT}" font-size="22" fill="{c["muted"]}">Telecom engineer · security · things I build</text>')
    s.append(f'<text x="42" y="198" font-family="{MONO}" font-size="16" fill="{c["accent"]}">~/menorca $ ./portfolio --latest</text>')
    s.append('</svg>')
    return "\n".join(s)


def contact(th):
    c = THEMES[th]; W, H = 900, 120; a = c["accent"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
         # small "person + link" line-art glyph
         f'<g transform="translate(30 28)" fill="none" stroke="{a}" stroke-width="2.2">'
         f'<circle cx="32" cy="22" r="10"/><path d="M12 60 C 14 42, 50 42, 52 60"/></g>',
         f'<text x="112" y="52" font-family="{MONO}" font-size="12.5" fill="{c["faint"]}">get in touch</text>',
         f'<text x="112" y="84" font-family="{FONT}" font-size="22" font-weight="700" fill="{c["fg"]}">Let\'s connect on LinkedIn</text>',
         f'<text x="{W-32}" y="76" text-anchor="end" font-family="{MONO}" font-size="15" fill="{a}">linkedin.com/in/xavier-pons-marti  →</text>',
         '</svg>']
    return "\n".join(s)


# ---- small line-art glyphs, one per project -------------------------------------------
def g_radar(c):   # security scanner
    a = c["accent"]
    return (f'<g fill="none" stroke="{a}" stroke-width="2">'
            f'<circle cx="32" cy="32" r="26" stroke-opacity=".3"/><circle cx="32" cy="32" r="17" stroke-opacity=".55"/>'
            f'<circle cx="32" cy="32" r="8"/><path d="M32 32 L52 14"/></g><circle cx="47" cy="22" r="3.5" fill="{a}"/>')

def g_wave(c):    # keyword spotting
    a = c["accent"]; xs = range(6, 60, 6); hs = [6, 14, 26, 40, 30, 46, 22, 12, 6]
    return ''.join(f'<line x1="{x}" y1="{32 - h / 2}" x2="{x}" y2="{32 + h / 2}" stroke="{a}" stroke-width="3" stroke-linecap="round"/>' for x, h in zip(xs, hs))

def g_net(c):     # neural network training
    a = c["accent"]; L = [[14, 32, 50], [20, 44], [32]]; X = [8, 32, 56]; out = []
    for i in range(2):
        for y1 in L[i]:
            for y2 in L[i + 1]:
                out.append(f'<line x1="{X[i]}" y1="{y1}" x2="{X[i+1]}" y2="{y2}" stroke="{a}" stroke-opacity=".4" stroke-width="1.5"/>')
    for i, col in enumerate(L):
        for y in col:
            out.append(f'<circle cx="{X[i]}" cy="{y}" r="5" fill="{c["bg"]}" stroke="{a}" stroke-width="2"/>')
    return ''.join(out)

def g_route(c):   # pollution-aware routing
    a = c["accent"]
    return (f'<path d="M8 52 C 20 52, 18 30, 32 30 S 44 10, 56 12" fill="none" stroke="{a}" stroke-width="2.5" stroke-dasharray="5 4"/>'
            f'<circle cx="8" cy="52" r="4.5" fill="{a}"/><circle cx="56" cy="12" r="4.5" fill="none" stroke="{a}" stroke-width="2.5"/>'
            f'<circle cx="40" cy="44" r="9" fill="{a}" fill-opacity=".15"/><circle cx="20" cy="18" r="7" fill="{a}" fill-opacity=".15"/>')

def g_donut(c):   # personal finance
    a = c["accent"]; r = 22; C = 2 * math.pi * r
    return (f'<circle cx="32" cy="32" r="{r}" fill="none" stroke="{a}" stroke-opacity=".2" stroke-width="9"/>'
            f'<circle cx="32" cy="32" r="{r}" fill="none" stroke="{a}" stroke-width="9" stroke-dasharray="{C*.62:.1f} {C:.1f}" transform="rotate(-90 32 32)"/>')

def g_pwm(c):     # class-D / signal processing
    a = c["accent"]
    sq = "M4 46 H12 V18 H20 V46 H24 V18 H36 V46 H40 V18 H44 V46 H52 V18 H60"
    sine = "M4 32 " + " ".join(f"L{4 + i*2} {32 - 12*math.sin(i*2*math.pi/28):.1f}" for i in range(1, 29))
    return (f'<path d="{sq}" fill="none" stroke="{a}" stroke-opacity=".35" stroke-width="1.8"/>'
            f'<path d="{sine}" fill="none" stroke="{a}" stroke-width="2.5"/>')


PROJECTS = [
    ('wp-vuln-scanner', 'security', g_radar,
     'WordPress exposure scanner: fingerprints the stack, maps versions to CVEs and writes an HTML risk report.',
     ['Python', 'NVD', 'CVSS']),
    ('ges_iavoz', 'embedded ML', g_wave,
     'Real-time keyword spotting on an ESP32-S3. 97.2% accuracy, 0.05 false positives per hour.',
     ['C++', 'ESP-IDF', 'TFLite Micro']),
    ('tfg-kws-training', 'machine learning', g_net,
     'Training pipeline for the thesis model: MobileNetV2 transfer learning and int8 quantization.',
     ['Python', 'TensorFlow']),
    ('air-quality-forecasting', 'data · backend', g_route,
     'NO₂ forecasting with LSTMs and low-pollution route planning over OpenStreetMap.',
     ['Python', 'Keras', 'Flask']),
    ('mi-cartera', 'web app', g_donut,
     'Offline-first personal finance PWA with bank-statement import and receipt OCR.',
     ['JavaScript', 'PWA']),
    ('matlab-signal-processing', 'signal processing', g_pwm,
     'Class-D amplifier simulation and sound-card distortion and frequency-response measurements.',
     ['MATLAB']),
]


def wrap(t, n):
    out, line = [], ''
    for w in t.split():
        if len(line) + len(w) + 1 > n:
            out.append(line); line = w
        else:
            line = (line + ' ' + w).strip()
    out.append(line)
    return out


def card(p, th):
    name, cat, glyph, desc, tags = p
    c = THEMES[th]; W, H = 440, 200
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>',
         f'<g transform="translate(352 24)">{glyph(c)}</g>',
         f'<text x="28" y="44" font-family="{MONO}" font-size="12.5" fill="{c["faint"]}">{html.escape(cat)}</text>',
         f'<text x="28" y="78" font-family="{FONT}" font-size="22" font-weight="700" fill="{c["fg"]}">{html.escape(name)}</text>']
    for i, l in enumerate(wrap(desc, 50)[:3]):
        s.append(f'<text x="28" y="{108 + i * 21}" font-family="{FONT}" font-size="14.5" fill="{c["muted"]}">{html.escape(l)}</text>')
    s.append(f'<text x="28" y="176" font-family="{MONO}" font-size="12.5" fill="{c["accent"]}">{html.escape("  ·  ".join(tags))}</text>')
    s.append('</svg>')
    return "\n".join(s)


if __name__ == '__main__':
    for th in THEMES:
        open(f'{OUT}/banner-{th}.svg', 'w').write(banner(th))
        open(f'{OUT}/contact-{th}.svg', 'w').write(contact(th))
        for p in PROJECTS:
            open(f'{OUT}/card-{p[0]}-{th}.svg', 'w').write(card(p, th))
    print('ok')
