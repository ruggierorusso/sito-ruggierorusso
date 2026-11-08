"""Downloads all Instagram posts into site/img/ig and writes instagram.json.

Needs the environment variable IG_TOKEN: either an Instagram Login token (graph.instagram.com)
or a Facebook/Unified Login system-user token (graph.facebook.com, never expires).
Run by .github/workflows/instagram.yml once a day; build.py then turns the posts into the
"Diario" grid and, for captions containing #portfolio, into full project pages.
"""
import json, os, sys, io, urllib.request, urllib.parse
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'site', 'img', 'ig')
DB = os.path.join(ROOT, 'instagram.json')
API = 'https://graph.instagram.com'
FIELDS = 'id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,children{media_type,media_url,thumbnail_url}'
MAX_POSTS = 2000  # in pratica: tutti i post

token = os.environ.get('IG_TOKEN', '').strip()
if not token:
    sys.exit('IG_TOKEN mancante: aggiungilo nei Secrets del repository.')

def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()

IG_USER_ID = os.environ.get('IG_USER_ID', '17841400928920314').strip()
FB_API = 'https://graph.facebook.com/v21.0'

def api(path, **params):
    params['access_token'] = token
    return json.loads(get(f'{API}/{path}?{urllib.parse.urlencode(params)}'))

def first_page():
    # token Instagram Login (inizia con IG...) oppure token Facebook / Unified Login
    global API
    if token.startswith('IG'):
        return api('me/media', fields=FIELDS, limit=50)
    API = FB_API
    return api(f'{IG_USER_ID}/media', fields=FIELDS, limit=50)

def save(url, dest, size):
    if os.path.exists(dest): return True
    try:
        im = Image.open(io.BytesIO(get(url))).convert('RGB')
    except Exception as e:
        print('  salto immagine:', e); return False
    im.thumbnail((size, size), Image.LANCZOS)
    im.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)
    return True

os.makedirs(OUT, exist_ok=True)
posts, url = [], None
data = first_page()
while True:
    posts += data.get('data', [])
    nxt = data.get('paging', {}).get('next')
    if len(posts) >= MAX_POSTS or not nxt: break
    data = json.loads(get(nxt))
posts = posts[:MAX_POSTS]

out = []
for p in posts:
    items = p.get('children', {}).get('data') or [p]
    # per il Diario basta la copertina; i post #portfolio diventano pagine progetto e servono tutte le foto
    portfolio = '#portfolio' in (p.get('caption') or '').lower()
    if not portfolio: items = items[:1]
    files = []
    for k, it in enumerate(items, 1):
        src = it.get('thumbnail_url') if it.get('media_type') == 'VIDEO' else it.get('media_url')
        if not src: continue
        name = f"{p['id']}-{k:02d}.jpg"
        if save(src, os.path.join(OUT, name), 1600 if portfolio else 1080): files.append('ig/' + name)
    out.append(dict(id=p['id'], caption=p.get('caption', ''), permalink=p.get('permalink', ''),
                    ts=p.get('timestamp', ''), type=p.get('media_type', ''), files=files))

# rimuove le immagini di post cancellati da Instagram
keep = {f[3:] for x in out for f in x['files']}
for f in os.listdir(OUT):
    if f not in keep: os.remove(os.path.join(OUT, f))

json.dump({'posts': out}, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('post Instagram:', len(out))
