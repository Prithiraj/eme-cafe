"""Explicit asset import, not part of ordinary deployment.

Downloads only the reviewed URLs in content/images.json. Commits optimised local
copies so the live site and subsequent builds do not depend on expiring social URLs.
All current business photographs are labelled permission-pending demo references.
"""
from __future__ import annotations
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
from PIL import Image, ImageOps, ImageDraw, ImageFont
import hashlib, io, json, re, time

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'public/assets'
MEDIA = ASSETS / 'media'
MEDIA.mkdir(parents=True, exist_ok=True)
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}

def fetch(url: str) -> bytes:
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS asset URLs are accepted')
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=HEADERS), timeout=40) as response:
                payload = response.read(16_000_001)
            if len(payload) > 16_000_000:
                raise ValueError('Asset exceeds the 16 MB import limit')
            return payload
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)
    raise RuntimeError('Download failed')

sources = json.loads((ROOT / 'content/images.json').read_text())
manifest = {}
register = ['# Photography and asset register', '', 'Reviewed: 7 September 2026. **All business photography below is demo-only, permission pending.**', '', 'Owner publication is not proof of photographer ownership. Obtain permission or replace before commercial launch. No imagery is generated or substituted from an unrelated café.', '']
for key, item in sources.items():
    payload = fetch(item['download_url'])
    digest = hashlib.sha256(payload).hexdigest()
    with Image.open(io.BytesIO(payload)) as original:
        original.load()
        image = ImageOps.exif_transpose(original).convert('RGB')
    if image.width < 300 or image.height < 300:
        raise ValueError(f'{key}: source is too small for a business photograph')
    widths = sorted(set([w for w in (320, 480, 768, 1200) if w < image.width] + [min(image.width, 1200)]))
    for width in widths:
        height = round(image.height * width / image.width)
        resized = image.resize((width, height), Image.Resampling.LANCZOS)
        resized.save(MEDIA / f'{item["file"]}-{width}.webp', 'WEBP', quality=81, method=6)
        resized.save(MEDIA / f'{item["file"]}-{width}.jpg', 'JPEG', quality=83, optimize=True, progressive=True)
    manifest[key] = {'file': item['file'], 'width': image.width, 'height': image.height, 'widths': widths, 'source_sha256': digest}
    register += [f'## {item["title"]} (`{key}`)', '', f'- **Source:** {item["source_page"]}', f'- **Credit:** {item["credit"]}', f'- **Status:** {item["status"]}; {item["rights"]}', f'- **Original dimensions:** {image.width} × {image.height}', f'- **Source SHA-256:** `{digest}`', f'- **Local variants:** `public/assets/media/{item["file"]}-*`', '- **Processing:** proportionate resize, EXIF orientation, metadata stripped, WebP/JPEG compression. No invented ingredients, removed watermarks or altered people.', '']
(MEDIA / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(ROOT / 'docs').mkdir(exist_ok=True)
(ROOT / 'docs/ASSET_REGISTER.md').write_text('\n'.join(register))

# Self-host Latin font subsets. Runtime does not contact Google Fonts.
font_dir = ASSETS / 'fonts'
font_dir.mkdir(exist_ok=True)
css_parts = []
for family, query, slug in [('DM Sans', 'DM+Sans:wght@400..700', 'dm-sans'), ('Fraunces', 'Fraunces:opsz,wght@9..144,400..700', 'fraunces')]:
    css = fetch('https://fonts.googleapis.com/css2?family=' + query + '&display=swap').decode()
    blocks = re.findall(r'/\*\s*latin\s*\*/\s*(@font-face\s*\{[^}]+\})', css)
    if not blocks:
        raise RuntimeError(f'Expected Latin WOFF2 font subset for {family}')
    for i, block in enumerate(blocks):
        remote = re.search(r'url\((https://[^)]+)\)', block).group(1)
        payload = fetch(remote)
        if payload[:4] != b'wOF2':
            raise ValueError(f'Expected WOFF2 data for {family}')
        filename = f'{slug}-{i}.woff2'
        (font_dir / filename).write_bytes(payload)
        css_parts.append(block.replace(remote, 'fonts/' + filename))
    ofl = fetch('https://raw.githubusercontent.com/google/fonts/main/ofl/' + ('dmsans' if slug == 'dm-sans' else 'fraunces') + '/OFL.txt')
    (font_dir / (slug + '-OFL.txt')).write_bytes(ofl)
(ASSETS / 'fonts.css').write_text('\n'.join(css_parts) + '\n')

# A typography-only social card: no rights-pending business photo in OG previews.
card = Image.new('RGB', (1200, 630), '#FBF7EC')
draw = ImageDraw.Draw(card)
try:
    serif = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 120)
    sans = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
    small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)
except OSError:
    serif, sans, small = ImageFont.load_default(size=120), ImageFont.load_default(size=28), ImageFont.load_default(size=22)
draw.rectangle((0, 0, 1200, 20), fill='#244633')
draw.ellipse((915, 85, 1135, 305), fill='#F1BFCB')
draw.ellipse((1010, 255, 1160, 405), fill='#F4D875')
draw.text((75, 85), 'SHORE ROAD / REMUERA', font=small, fill='#244633')
draw.text((65, 170), 'Eme’s Cafe', font=serif, fill='#244633')
draw.text((75, 350), 'Good mornings. Better brunch.', font=sans, fill='#963D53')
draw.rectangle((0, 520, 1200, 630), fill='#244633')
draw.text((75, 556), 'WEBSITE PREVIEW · OWNER APPROVAL PENDING', font=small, fill='#FBF7EC')
card.save(ASSETS / 'social-preview.png', optimize=True)
(ASSETS / 'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#244633"/><text x="31" y="47" text-anchor="middle" font-family="Georgia,serif" font-size="57" fill="#FBF7EC">e</text><circle cx="49" cy="15" r="6" fill="#F1BFCB"/></svg>')
print('Imported', len(manifest), 'visually reviewed photos; local variants and font subsets ready.')
