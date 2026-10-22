# Generates the profile banner and project cards (light + dark).
# To add a project: append it to PROJECTS, run `python assets/generate.py`, and add its card to README.md.
import math, html
import os
OUT=os.path.dirname(os.path.abspath(__file__))
THEMES={
 'light':dict(bg='#ffffff',fg='#1f2328',muted='#59636e',line='#d1d9e0',chip='#f6f8fa',grid='#eef1f4'),
 'dark': dict(bg='#0d1117',fg='#e6edf3',muted='#9198a1',line='#30363d',chip='#161b22',grid='#161b22'),
}
FONT="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

def wave(x0,y0,w,amp,freq,phase=0,n=240):
    pts=[]
    for i in range(n+1):
        x=x0+w*i/n; t=i/n
        env=math.sin(math.pi*t)**1.5
        y=y0+amp*env*math.sin(2*math.pi*freq*t+phase)
        pts.append(f"{x:.1f},{y:.1f}")
    return "M"+" L".join(pts)

def banner(th):
    c=THEMES[th]; W,H=1200,280
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<rect width="{W}" height="{H}" rx="16" fill="{c["bg"]}" stroke="{c["line"]}"/>']
    # grid
    for x in range(40,W,40): s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{c["grid"]}" stroke-width="1"/>')
    for y in range(40,H,40): s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{c["grid"]}" stroke-width="1"/>')
    # waves on the right
    cols=['#2f81f7','#3fb950','#a371f7']
    for i,(col,f,a) in enumerate(zip(cols,[6,9,4],[60,38,80])):
        s.append(f'<path d="{wave(700,140,460,a,f,i*1.1)}" fill="none" stroke="{col}" stroke-width="2.2" stroke-opacity="{0.85-0.15*i}"/>')
    s.append(f'<rect x="56" y="64" width="6" height="150" rx="3" fill="#2f81f7"/>')
    s.append(f'<text x="84" y="118" font-family="{FONT}" font-size="52" font-weight="700" fill="{c["fg"]}">Xavier Pons Martí</text>')
    s.append(f'<text x="86" y="162" font-family="{FONT}" font-size="22" fill="{c["muted"]}">Cybersecurity · Telecommunications · Things I build</text>')
    s.append(f'<text x="86" y="204" font-family="{MONO}" font-size="16" fill="#2f81f7">~/barcelona $ ./portfolio --latest</text>')
    s.append('</svg>'); return "\n".join(s)

PROJECTS=[
 ('wp-vuln-scanner','Security','#f85149','WordPress exposure scanner: fingerprints the stack, maps versions to CVEs and writes an HTML risk report.',['Python','NVD','CVSS']),
 ('ges_iavoz','Embedded ML','#2f81f7','Real-time keyword spotting on an ESP32-S3. 97.2% accuracy, 0.05 false positives per hour.',['C++','ESP-IDF','TFLite Micro']),
 ('tfg-kws-training','Machine learning','#a371f7','Training pipeline for the thesis model: MobileNetV2 transfer learning and int8 quantization.',['Python','TensorFlow']),
 ('air-quality-forecasting','Data & backend','#3fb950','NO₂ forecasting with LSTMs and low-pollution route planning over OpenStreetMap.',['Python','Keras','Flask']),
 ('mi-cartera','Web app','#d29922','Offline-first personal finance PWA with bank-statement import and receipt OCR.',['JavaScript','PWA']),
 ('matlab-signal-processing','Signal processing','#db61a2','Class-D amplifier simulation and sound-card distortion and frequency-response measurements.',['MATLAB']),
]
def wrap(t,n):
    out=[];line=''
    for w in t.split():
        if len(line)+len(w)+1>n: out.append(line); line=w
        else: line=(line+' '+w).strip()
    out.append(line); return out

def card(p,th):
    name,cat,col,desc,tags=p; c=THEMES[th]; W,H=440,210
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
       f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>',
       f'<clipPath id="c"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12"/></clipPath><rect clip-path="url(#c)" x="0" y="0" width="{W}" height="5" fill="{col}"/>',
       f'<circle cx="30" cy="38" r="5" fill="{col}"/>',
       f'<text x="44" y="43" font-family="{FONT}" font-size="13" font-weight="600" fill="{col}" letter-spacing="0.6">{html.escape(cat.upper())}</text>',
       f'<text x="24" y="80" font-family="{FONT}" font-size="22" font-weight="700" fill="{c["fg"]}">{html.escape(name)}</text>']
    for i,l in enumerate(wrap(desc,52)[:3]):
        s.append(f'<text x="24" y="{110+i*21}" font-family="{FONT}" font-size="14.5" fill="{c["muted"]}">{html.escape(l)}</text>')
    x=24
    for t in tags:
        w=len(t)*7.6+20
        s.append(f'<rect x="{x}" y="166" width="{w:.0f}" height="24" rx="12" fill="{c["chip"]}" stroke="{c["line"]}"/>')
        s.append(f'<text x="{x+w/2:.0f}" y="182" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{c["fg"]}">{html.escape(t)}</text>')
        x+=w+8
    s.append('</svg>'); return "\n".join(s)

for th in THEMES:
    open(f'{OUT}/banner-{th}.svg','w').write(banner(th))
    for p in PROJECTS: open(f'{OUT}/card-{p[0]}-{th}.svg','w').write(card(p,th))
print('ok')
