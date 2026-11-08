"""Static site generator for ruggierorusso.com (IT + EN)."""
import json, os, re, html, sys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
DOMAIN = 'https://www.ruggierorusso.com'
cat = json.load(open(os.path.join(ROOT, 'catalogo.json'), encoding='utf-8'))
E = html.escape

# shrink logos once
for f, h in (('logo-r.png', 360), ('logo-full.png', 300)):
    p = os.path.join(SITE, 'assets', f); im = Image.open(p)
    if im.height > h:
        im.thumbnail((10000, h), Image.LANCZOS); im.save(p, optimize=True)

FIX = {'Gautier': 'Gaultier', 'Museuem': 'Museum', 'Gautier for Storage Museuem': 'Gaultier for Storage Museum'}
TITLE_FIX = {'4GIVENESS': '4Giveness', 'PERLAROUGE': 'Perlarouge', 'MEJEM': 'Mejem', 'MOYA': 'Moya', 'SCISCI': 'Scisci'}
FEATURED = ['dalila', 'marzia-editorial-02', 'scisci', 'dimensione-danza', 'line-of-light', 'mercii', 'dieci-terre',
            'disclaimer', 'timeless', 'hevo', 'moya', 'shop-art', 'marzia-street', 'vitamina-tu', 'dacabo']
CATS = {'FASHION': ('Fashion', 'Fashion'), 'STILL-LIFE': ('Still-life', 'Still-life'), 'ADVERTISING': ('Advertising', 'Advertising')}

def credits(lines):
    out = []
    for ln in lines:
        for a, b in FIX.items(): ln = ln.replace(a, b)
        m = re.match(r'\s*([A-Za-z &\-]+?)\s*[:;]\s*(.+)$', ln)
        if m: out.append((m.group(1).strip().upper().replace('MAKEUP', 'MAKE-UP'), m.group(2).strip()))
        elif ln.strip(): out.append(('', ln.strip()))
    return out

imgs = sorted(os.listdir(os.path.join(SITE, 'img')))
P = []
for p in cat['progetti']:
    files = [f for f in imgs if re.fullmatch(re.escape(p['s']) + r'-\d\d\.jpg', f)]
    if not files: continue
    sizes = [Image.open(os.path.join(SITE, 'img', f)).size for f in files]
    cover_i = 0
    if p.get('cv') in p['i']: cover_i = p['i'].index(p['cv'])
    P.append(dict(s=p['s'], t=TITLE_FIX.get(p['t'], p['t']), cat=p['cat'], cr=credits(p['cr']),
                  files=list(zip(files, sizes)), cover=files[min(cover_i, len(files) - 1)]))
order = {s: i for i, s in enumerate(FEATURED)}
P.sort(key=lambda x: (order.get(x['s'], 100), cat['progetti'].index(next(c for c in cat['progetti'] if c['s'] == x['s']))))

# ---- Instagram (written by instagram_sync.py) ----
IG = []
igp = os.path.join(ROOT, 'instagram.json')
if os.path.exists(igp):
    IG = [x for x in json.load(open(igp, encoding='utf-8')).get('posts', []) if x.get('files')]
    IG.sort(key=lambda x: x['ts'], reverse=True)
    for post in reversed(IG):
        cap = post.get('caption') or ''
        if '#portfolio' not in cap.lower(): continue
        lines = [l.strip() for l in cap.splitlines() if l.strip()]
        title = re.sub(r'#[\w-]+', '', lines[0]).strip() if lines else ''
        title = title or 'Instagram'
        tags = {t.lower() for t in re.findall(r'#([\w-]+)', cap)}
        c = 'FASHION' if 'fashion' in tags else 'STILL-LIFE' if (tags & {'stilllife', 'still-life', 'stillife'}) else 'ADVERTISING'
        cr = credits([l for l in lines[1:] if re.match(r'\s*[A-Za-z &\-]+\s*:', l)])
        slug = (re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:40] or 'ig') + '-' + post['id'][-5:]
        files = [(f, Image.open(os.path.join(SITE, 'img', f)).size) for f in post['files']]
        P.insert(0, dict(s=slug, t=title, cat=c, cr=cr, files=files, cover=files[0][0]))
print('progetti', len(P), 'foto', sum(len(x['files']) for x in P))

T = {
 'it': dict(lang='it', works='Lavori', studio='ERRE studio', about='Chi sono', contact='Contatti', other='EN',
   tag='Fotografo · Fashion · Still-life · Advertising', avail='Disponibile per nuovi progetti',
   index='Indice lavori', all='Tutti', back='Indice lavori', prev='Progetto precedente', next='Progetto successivo',
   similar='Un progetto simile?', write='Scrivimi', photos='foto', studio_t='Lo studio di Barletta, rinnovato di recente, dove nascono campagne, editoriali e still-life. Set luce professionali e postazione di post-produzione.',
   about_t="Fotografo professionista da oltre vent'anni. Lavoro per brand, agenzie e magazine nella moda, nello still-life e nella pubblicità, in studio e in location, integrando gli strumenti di intelligenza artificiale nel mio flusso di lavoro.",
   clients='Hanno scelto il mio lavoro', project='Hai un progetto?', meta='Ruggiero Russo, fotografo fashion, still-life e advertising a Barletta. Portfolio e ERRE studio.',
   notfound='Pagina non trovata', diary='Diario', follow='Segui su Instagram', home='Torna alla home', close='Chiudi', dir='lavori', open_photo='Apri la foto'),
 'en': dict(lang='en', works='Works', studio='ERRE studio', about='About', contact='Contact', other='IT',
   tag='Photographer · Fashion · Still-life · Advertising', avail='Available for new projects',
   index='Index of works', all='All', back='Index of works', prev='Previous project', next='Next project',
   similar='A similar project?', write='Get in touch', photos='photos', studio_t='My recently renovated studio in Barletta, Italy, where campaigns, editorials and still-life are made. Professional lighting sets and a post-production suite.',
   about_t='Professional photographer for over twenty years. I work for brands, agencies and magazines in fashion, still-life and advertising, in the studio and on location, with AI tools built into my workflow.',
   clients='Clients', project='Have a project?', meta='Ruggiero Russo, fashion, still-life and advertising photographer based in Barletta, Italy. Portfolio and ERRE studio.',
   notfound='Page not found', diary='Diary', follow='Follow on Instagram', home='Back to home', close='Close', dir='works', open_photo='Open photo'),
}
STUDIO_URL = 'https://errestudiobarletta.it/'
def SL(h):
    return h.replace('ERRE studio', f'<a class="sl" href="{STUDIO_URL}" target="_blank" rel="noopener">ERRE studio</a>')

CLIENTS = ['RED Valentino', 'Laura Biagiotti', 'Jean Paul Gaultier', 'Blauer', 'Diadora', 'Umbro', 'Camomilla', 'Pyrex']

def page(lg, depth, title, desc, body, alt_href, og_img, canon):
    t = T[lg]; up = '../' * depth
    return f'''<!doctype html>
<html lang="{lg}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{DOMAIN}/{canon}">
<link rel="alternate" hreflang="{'en' if lg == 'it' else 'it'}" href="{DOMAIN}/{alt_href[1]}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{DOMAIN}/img/{og_img}">
<meta property="og:type" content="website">
<link rel="icon" href="{up}assets/favicon.png">
<link rel="preload" href="{up}assets/rrstencil.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<a class="skip" href="#main">{'Vai al contenuto' if lg == 'it' else 'Skip to content'}</a>
<header class="top">
  <a class="brand" href="{up}{'' if lg == 'it' else 'en/'}index.html"><img src="{up}assets/logo-r.png" alt="" width="37" height="44"><span>Ruggiero Russo</span></a>
  <nav aria-label="Menu">
    <a href="{up}{'' if lg == 'it' else 'en/'}index.html#lavori">{t['works']}</a>
    {f'<a href="{up}{"" if lg == "it" else "en/"}index.html#diario">{t["diary"]}</a>' if IG else ''}
    <a href="{STUDIO_URL}" target="_blank" rel="noopener">{t['studio']}</a>
    <a href="{up}{'' if lg == 'it' else 'en/'}index.html#chi-sono">{t['about']}</a>
    <a href="{up}{'' if lg == 'it' else 'en/'}index.html#contatti">{t['contact']}</a>
    <a class="lang" href="{alt_href[0]}" hreflang="{'en' if lg == 'it' else 'it'}">{t['other']}</a>
  </nav>
</header>
<main id="main">
{body}
</main>
<footer class="foot">
  <img src="{up}assets/logo-full.png" alt="Ruggiero Russo Photography" width="150" height="300" loading="lazy">
  <span class="small">© 2026 Ruggiero Russo · {SL('ERRE studio')} · Barletta (BT) · P.IVA 07989340729</span>
  <span class="links"><a href="https://www.instagram.com/ruggierorussophotography/">Instagram</a><a href="https://www.facebook.com/ruggiero.russo">Facebook</a></span>
</footer>
<div class="lb" hidden aria-modal="true" role="dialog" aria-label="Foto">
  <button class="lb-x" type="button" aria-label="{t['close']}">×</button>
  <button class="lb-p" type="button" aria-label="{t['prev']}">←</button>
  <img alt="">
  <button class="lb-n" type="button" aria-label="{t['next']}">→</button>
  <span class="lb-c"></span>
</div>
<script src="{up}assets/site.js" defer></script>
</body>
</html>
'''

def home(lg):
    t = T[lg]; up = '' if lg == 'it' else '../'; d = t['dir']
    hero = []
    for s in ('dalila', 'marzia-editorial-02', 'dimensione-danza'):
        x = next(p for p in P if p['s'] == s)
        hero.append(f'<a href="{d}/{s}.html"><img src="{up}img/{x["cover"]}" alt="{E(x["t"])}" width="800" height="1200"><span class="cap">{E(x["t"])} · {CATS[x["cat"]][0 if lg == "it" else 1]}</span></a>')
    rows = []
    for i, x in enumerate(P, 1):
        rows.append(f'<li data-cat="{x["cat"]}" data-img="{up}img/{x["cover"]}"><a href="{d}/{x["s"]}.html"><span class="n">{i:02d}</span><span class="t">{E(x["t"])}</span><span class="c">{CATS[x["cat"]][0]}</span></a></li>')
    chips = ''.join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "ALL" else "false"}">{v}</button>' for k, v in
                    [('ALL', t['all'])] + [(k, v[0]) for k, v in CATS.items()])
    first = P[0]
    diary = ''
    if IG:
        cells = ''.join(f'<a href="{E(x["permalink"])}" target="_blank" rel="noopener"><img src="{up}img/{x["files"][0]}" alt="{E((x.get("caption") or "Instagram").splitlines()[0][:90])}" loading="lazy" width="600" height="600"></a>' for x in IG[:12])
        diary = f'<section id="diario" class="diary"><div class="bar"><h2>{t["diary"]}</h2><a class="ul" href="https://www.instagram.com/ruggierorussophotography/" target="_blank" rel="noopener">{t["follow"]} →</a></div><div class="dgrid">{cells}</div></section>'
    body = f'''<section class="intro">
  <img class="mark" src="{up}assets/logo-r.png" alt="" width="250" height="300">
  <div>
    <h1>Ruggiero<br>Russo</h1>
    <p class="meta"><span>{t['tag']}</span><span class="red">● {t['avail']}</span></p>
  </div>
</section>
<section class="hero">{''.join(hero)}</section>
<section id="lavori" class="works">
  <div class="bar"><h2>{t['index']} <span class="count">({len(P)})</span></h2><div class="chips" role="group">{chips}</div></div>
  <div class="split">
    <ol class="list">{''.join(rows)}</ol>
    <figure class="preview" aria-hidden="true"><img src="{up}img/{first['cover']}" alt="" width="800" height="1200"></figure>
  </div>
</section>
{diary}
<section id="studio" class="studio">
  <img src="{up}img/line-of-light-01.jpg" alt="ERRE studio" loading="lazy" width="800" height="1200">
  <div><h2><a href="{STUDIO_URL}" target="_blank" rel="noopener">ERRE<br>studio</a></h2><p>{t['studio_t']}</p><a class="ul" href="{STUDIO_URL}" target="_blank" rel="noopener">errestudiobarletta.it →</a></div>
</section>
<section id="chi-sono" class="about">
  <h2>{t['about']}</h2><p>{t['about_t']}</p>
</section>
<section class="clients"><p class="label">{t['clients']}</p><div>{''.join(f'<span>{E(c)}</span>' for c in CLIENTS)}</div></section>
<section id="contatti" class="contact">
  <p class="label">{t['project']}</p>
  <a class="mail" href="mailto:info@ruggierorusso.com">info<span class="at">@</span>ruggierorusso.com</a>
  <p class="addr">{SL('ERRE studio')} · Barletta (BT), {'Italia' if lg == 'it' else 'Italy'}</p>
</section>'''
    alt = ('en/index.html', 'en/') if lg == 'it' else ('../index.html', '')
    canon = '' if lg == 'it' else 'en/'
    return page(lg, 0 if lg == 'it' else 1, 'Ruggiero Russo · Photography', t['meta'], body, alt, first['cover'], canon)

def project(lg, i):
    t = T[lg]; x = P[i]; d = t['dir']; depth = 1 if lg == 'it' else 2; up = '../' * depth
    prv, nxt = P[i - 1], P[(i + 1) % len(P)]
    cr = ''.join(f'<div><dt>{E(k) if k else "&nbsp;"}</dt><dd>{SL(E(v))}</dd></div>' for k, v in x['cr'])
    gal = ''.join(f'<a href="{up}img/{f}" data-i="{k}"><img src="{up}img/{f}" alt="{E(x["t"])} – {k + 1}" width="{w}" height="{h}" loading="{"eager" if k < 2 else "lazy"}"></a>'
                  for k, (f, (w, h)) in enumerate(x['files']))
    body = f'''<section class="phead">
  <a class="back" href="../{'' if lg == 'it' else ''}index.html#lavori">← {t['back']}</a>
  <div class="ptitle"><h1>{E(x['t'])}</h1><span class="red">{CATS[x['cat']][0]} · {i + 1:02d} / {len(P)}</span></div>
  {f'<dl class="credits">{cr}</dl>' if cr else ''}
</section>
<section class="gallery">{gal}</section>
<p class="note">{len(x['files'])} {t['photos']}</p>
<nav class="pn" aria-label="{t['works']}">
  <a href="{prv['s']}.html"><span class="label">← {t['prev']}</span><span class="pt">{E(prv['t'])}</span></a>
  <a class="r" href="{nxt['s']}.html"><span class="label">{t['next']} →</span><span class="pt">{E(nxt['t'])}</span></a>
</nav>
<section class="contact small-c"><p class="label">{t['similar']}</p><a class="mail" href="mailto:info@ruggierorusso.com?subject={E(x['t'])}">info<span class="at">@</span>ruggierorusso.com</a></section>'''
    other = T['en' if lg == 'it' else 'it']['dir']
    alt = ((f'../en/{other}/{x["s"]}.html', f'en/{other}/{x["s"]}.html') if lg == 'it'
           else (f'../../{other}/{x["s"]}.html', f'{other}/{x["s"]}.html'))
    canon = f'{d}/{x["s"]}.html' if lg == 'it' else f'en/{d}/{x["s"]}.html'
    desc = f'{x["t"]} – ' + ', '.join(v for k, v in x['cr'][:3]) + ' · Ruggiero Russo Photography'
    return page(lg, depth, f'{x["t"]} · Ruggiero Russo', desc, body, alt, x['cover'], canon)

def w(rel, s):
    p = os.path.join(SITE, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(s)

w('index.html', home('it')); w('en/index.html', home('en'))
for i in range(len(P)):
    w(f'lavori/{P[i]["s"]}.html', project('it', i)); w(f'en/works/{P[i]["s"]}.html', project('en', i))
nf = f'<section class="nf"><h1>404</h1><p>{T["it"]["notfound"]} · {T["en"]["notfound"]}</p><a class="ul" href="/index.html">{T["it"]["home"]}</a></section>'
w('404.html', page('it', 0, '404 · Ruggiero Russo', T['it']['notfound'], nf, ('en/index.html', 'en/'), P[0]['cover'], '404.html').replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/'))
urls = [''] + ['en/'] + [f'lavori/{x["s"]}.html' for x in P] + [f'en/works/{x["s"]}.html' for x in P]
w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
w('_redirects', '/portfolio-item/:slug/  /lavori/:slug.html  301\n/portfolio/  /#lavori  301\n')
print('ok')
