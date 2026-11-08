"""Downloads the latest Instagram posts into site/img/ig and writes instagram.json.

Needs the environment variable IG_TOKEN (Instagram API with Instagram Login, long-lived token).
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
MAX_POSTS = 60

token = os.environ.get('IG_TOKEN', '').strip()
if not token:
    sys.exit('IG_TOKEN mancante: aggiungilo nei Secrets del repository.')

def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()

def api(path, **params):
    params['access_token'] = token
    return json.loads(get(f'{API}/{path}?{urllib.parse.urlencode(params)}'))

def save(url, dest):
    if os.path.exists(dest): return True
    try:
        im = Image.open(io.BytesIO(get(url))).convert('RGB')
    except Exception as e:
        print('  salto immagine:', e); return False
    im.thumbnail((1600, 1600), Image.LANCZOS)
    im.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)
    return True

os.makedirs(OUT, exist_ok=True)
posts, url = [], None
data = api('me/media', fields=FIELDS, limit=50)
while True:
    posts += data.get('data', [])
    nxt = data.get('paging', {}).get('next')
    if len(posts) >= MAX_POSTS or not nxt: break
    data = json.loads(get(nxt))
posts = posts[:MAX_POSTS]

out = []
for p in posts:
    items = p.get('children', {}).get('data') or [p]
    files = []
    for k, it in enumerate(items, 1):
        src = it.get('thumbnail_url') if it.get('media_type') == 'VIDEO' else it.get('media_url')
        if not src: continue
        name = f"{p['id']}-{k:02d}.jpg"
        if save(src, os.path.join(OUT, name)): files.append('ig/' + name)
    out.append(dict(id=p['id'], caption=p.get('caption', ''), permalink=p.get('permalink', ''),
                    ts=p.get('timestamp', ''), type=p.get('media_type', ''), files=files))

json.dump({'posts': out}, open(DB, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('post Instagram:', len(out))
