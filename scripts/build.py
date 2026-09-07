"""Build the static website. Python 3.10+, standard library only.
Run `python scripts/build.py`, then serve `dist/` using any static web server.
No network access or credentials are needed for ordinary builds.
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import json, re, shutil, gzip

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
e = lambda value: escape(str(value), quote=True)
site = json.loads((ROOT / 'content/site.json').read_text())
images = json.loads((ROOT / 'content/images.json').read_text())
media_file = ROOT / 'public/assets/media/manifest.json'
if not media_file.exists():
    raise SystemExit('Reviewed assets are missing. Run the explicit Import reviewed website assets workflow first.')
media = json.loads(media_file.read_text())
if not site.get('preview', True):
    if not site.get('business_verified', False) or any(x['status'] != 'cleared' for x in images.values()):
        raise SystemExit('Commercial launch blocked: verify business details and clear/replace all photographs first.')
if not site['site_url'].startswith('https://') or not site['site_url'].endswith('/'):
    raise ValueError('site_url must be an HTTPS URL ending with /')
if str(int('4feec9c54545c499', 16)) not in site['maps']:
    raise ValueError('Directions must target the exact place CID from the user-supplied Maps URL')
if DIST.exists():
    shutil.rmtree(DIST)
shutil.copytree(ROOT / 'public', DIST)
for name in ('styles.css', 'app.js'):
    shutil.copy2(ROOT / 'src' / name, DIST / 'assets' / name)

def picture(key: str, sizes: str, eager: bool = False) -> str:
    item, asset = images[key], media[key]
    filename, widths = asset['file'], asset['widths']
    srcset = lambda extension: ', '.join(f'assets/media/{filename}-{width}.{extension} {width}w' for width in widths)
    loading = 'eager' if eager else 'lazy'
    priority = ' fetchpriority="high"' if eager else ''
    return (f'<picture><source type="image/webp" srcset="{srcset("webp")}" sizes="{e(sizes)}">'
            f'<img data-business-photo src="assets/media/{filename}-{widths[-1]}.jpg" '
            f'srcset="{srcset("jpg")}" sizes="{e(sizes)}" width="{asset["width"]}" height="{asset["height"]}" '
            f'alt="{e(item["alt"])}" loading="{loading}" decoding="async"{priority}></picture>')

cards = []
for i, item in enumerate(site['highlights'], 1):
    photo = picture(item['image'], '(max-width: 620px) calc(100vw - 40px), (max-width: 1100px) 30vw, 400px')
    cards.append(f'<article class="food-card" data-category="{e(item["category"])}"><div class="food-image">{photo}<span class="card-number" aria-hidden="true">0{i}</span></div><div class="card-body"><p class="eyebrow">{e(item["label"].upper())}</p><h3>{e(item["name"])}</h3><p>{e(item["description"])}</p><a class="photo-credit" href="credits.html#{e(item["image"])}">Demo photo reference · source & rights ↗</a></div></article>')
more = []
for item in site['more_highlights']:
    more.append(f'<article class="flavour-item" data-category="{e(item["category"])}"><span class="item-spark" aria-hidden="true">✳</span><div><h3>{e(item["name"])}</h3><p>{e(item["note"])}</p></div></article>')
hours = ''.join(f'<div><dt>{e(h["label"])}</dt><dd>{e(h["display"])}</dd></div>' for h in site['hours'])
gallery = []
for key, caption in [('drinks', 'A little colour.'), ('table', 'A little of everything.'), ('cabinet', 'A little temptation.')]:
    photo = picture(key, '(max-width: 620px) 70vw, 420px')
    credit = 'Kat’s Food Diary · gifted visit · demo' if key == 'table' else 'Demo photo reference'
    gallery.append(f'<figure class="gallery-photo">{photo}<figcaption>{caption}<br><a class="photo-credit" href="credits.html#{key}">{e(credit)} ↗</a></figcaption></figure>')

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {'@type': 'WebPage', '@id': site['site_url']+'#webpage', 'url': site['site_url'], 'name': site['title'], 'description': site['description'], 'about': {'@id': site['site_url']+'#cafe'}},
        {'@type': 'CafeOrCoffeeShop', '@id': site['site_url']+'#cafe', 'name': site['name'],
         'telephone': site['phone'], 'email': site['email'], 'hasMap': site['maps'],
         'address': {'@type': 'PostalAddress', 'streetAddress': site['address']['street'], 'addressLocality': site['address']['city'], 'addressRegion': 'Auckland', 'postalCode': site['address']['postal_code'], 'addressCountry': 'NZ'},
         'sameAs': [site['instagram'], site['facebook']],
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in site['hours']]}
    ]
}
values = {key: e(site[key]) for key in ['site_url','title','description','maps','phone','phone_uri','email','instagram','facebook','kitchen']}
values.update({'street': e(site['address']['street']), 'robots': 'noindex, nofollow' if site.get('preview', True) else 'index, follow',
    'schema': json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c'),
    'picture_hero': picture('hero', '(max-width: 620px) calc(100vw - 68px), (max-width: 1100px) 44vw, 560px', True),
    'picture_drinks_small': picture('drinks', '164px'),
    'picture_cabinet': picture('cabinet', '(max-width: 620px) calc(100vw - 70px), 570px'),
    'food_cards': '\n'.join(cards), 'more_highlights': '\n'.join(more), 'hours': hours, 'gallery': '\n'.join(gallery)})
html = (ROOT / 'src/index.html').read_text()
for key, value in values.items():
    html = html.replace('{{'+key+'}}', value)
if re.search(r'\{\{\w+\}\}', html):
    raise ValueError('Unresolved template field in homepage')
(DIST / 'index.html').write_text(html)


def document(title: str, body: str, canonical: str) -> str:
    return f'''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="{values['robots']}"><meta name="theme-color" content="#244633"><title>{e(title)} | Eme’s Cafe preview</title><meta name="description" content="{e(title)} for the Eme’s Cafe website preview."><link rel="canonical" href="{e(site['site_url']+canonical)}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/fonts.css"><link rel="stylesheet" href="assets/styles.css"></head><body><a class="skip-link" href="#main">Skip to content</a><div class="preview-bar"><span>Eme’s Cafe · independent website preview</span><a href="./">Back to the café ↗</a></div><header class="site-header"><div class="container header-inner"><a class="brand" href="./"><span class="brand-name">eme’s<span class="brand-dot">✳</span></span><span class="brand-sub">CAFE · REMUERA</span></a><a class="button button-small button-green" href="./#visit">Find us ↗</a></div></header><main id="main" class="container document-page"><p class="eyebrow">THE SMALL PRINT, CLEARLY</p><h1>{e(title)}</h1>{body}<p style="margin-top:2.5rem"><a class="text-link" href="./">← Back to Eme’s</a></p></main><footer class="site-footer"><div class="container"><p>Independent website preview. Owner verification and image permissions pending.</p><p><a href="credits.html">Photo credits</a> · <a href="privacy.html">Privacy</a></p></div></footer></body></html>'''

credit_sections = []
for key, item in images.items():
    credit_sections.append(f'<section class="credit-card" id="{key}"><span class="status">DEMO ONLY · PERMISSION PENDING</span><h2>{e(item["title"])}</h2><p><strong>Credit:</strong> {e(item["credit"])}</p><p>{e(item["rights"])}</p><p><a href="{e(item["source_page"])}">View the original source ↗</a></p></section>')
credits = ('<div class="notice"><p><strong>This is an independent design preview, not an owner-verified official café website.</strong> The repository owner authorised publishing this preview. Business-owner approval of the details and commercial photo rights are still pending.</p><p>Real photographs are used as clearly identified demo/editorial references. Public availability and owner reposting do not establish a commercial licence. These assets must be licensed or replaced before a commercial launch.</p></div>' + '\n'.join(credit_sections) +
    f'<section id="business-details"><h2>Business information</h2><p>Research checked on 7 September 2026. The address, regular hours and email are drawn from <a href="{e(site["instagram"])}">Eme’s published Instagram profile</a>. The telephone number and food highlights come from the café’s public posts.</p><p><strong>Address discrepancy:</strong> the profile says 13A Shore Road; some public listings say 13 Shore Road. The directions link targets the exact place identifier supplied for Eme’s Cafe.</p><p>The hours are published regular hours, not a real-time opening guarantee. The 2 pm kitchen cutoff is separate from the 3 pm café closing time. Public holidays and special closures need checking directly.</p><p>The food section is a selection of published highlights, not a complete current menu or a promise of today’s availability. No prices, ratings, dietary guarantees, parking, catering, delivery or booking services have been invented.</p></section><section><h2>Fonts and design</h2><p>Fraunces and DM Sans are self-hosted using their Open Font Licences; licence notices are retained with the assets. The typographic wordmark, colours and layout are a proposed design, not a claim to reproduce an official visual identity.</p><p>The social-preview image uses typography and original graphic layout, not permission-pending business photography.</p></section>')
(DIST / 'credits.html').write_text(document('Photo credits & preview notes', credits, 'credits.html'))
privacy = '<p>This page describes the code in this website preview, not the café’s own wider business practices.</p><h2>No forms. No advertising trackers.</h2><p>This preview does not include analytics, advertising scripts, payment processing, newsletter forms or non-essential cookies set by its code. It does not store a visitor profile in local storage.</p><h2>Hosting and external links</h2><p>The static site is hosted through GitHub Pages. Hosting requests are subject to the host’s own privacy practices. Business photographs and fonts are served as local website files; visiting this site does not require a social-media embed or a Google Fonts request.</p><p>Following a Maps, Instagram, Facebook, phone or email link opens the relevant external service. Its own privacy practices apply. A telephone/email link does not send a message automatically.</p><p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement ↗</a></p><h2>Changes before commercial launch</h2><p>Adding analytics, forms, booking or payment tools requires updating this notice to reflect the actual implementation. This preview does not imply that the café has adopted those services.</p>'
(DIST / 'privacy.html').write_text(document('Privacy notes', privacy, 'privacy.html'))
(DIST / '404.html').write_text(f'<!doctype html><html lang="en-NZ"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Eme’s Cafe</title><body style="font-family:Georgia,serif;background:#fbf7ec;color:#244633;padding:10vw"><h1>A little detour.</h1><p>This page could not be found.</p><p><a href="{e(site["site_url"])}">Back to Eme’s Cafe →</a></p></body></html>')
(DIST / '.nojekyll').touch()
# Allow crawling so search engines can observe noindex. robots at a project subpath
# is informative only; page-level noindex is the actual preview safeguard.
(DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\n' + ('' if site.get('preview', True) else f'Sitemap: {site["site_url"]}sitemap.xml\n'))
if not site.get('preview', True):
    (DIST / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{e(site["site_url"])}</loc></url></urlset>')
metrics = {'html_bytes': (DIST/'index.html').stat().st_size, 'css_gzip_bytes': len(gzip.compress((DIST/'assets/styles.css').read_bytes())), 'javascript_gzip_bytes': len(gzip.compress((DIST/'assets/app.js').read_bytes())), 'font_bytes': sum(p.stat().st_size for p in (DIST/'assets/fonts').glob('*.woff2')), 'total_deployment_bytes': sum(p.stat().st_size for p in DIST.rglob('*') if p.is_file()), 'preview': site.get('preview', True)}
(DIST / 'build-info.json').write_text(json.dumps(metrics, indent=2))
print(json.dumps(metrics, indent=2))
print('Built dist/ successfully. All business information is present in the initial HTML.')
