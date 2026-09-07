"""Research-only public image collection; never used by the production build.
No authentication, cookies, or hidden endpoints are used. Failed pages are skipped.
References must be visually verified and rights-reviewed before selection.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import re, json, html

OUT = Path('references')
OUT.mkdir(exist_ok=True)
SOURCES = {
    'facebook': 'https://www.facebook.com/p/Emescafeakl-61568487993875/',
    'blueberry': 'https://www.facebook.com/61568487993875/posts/122154617126616266/',
    'lemon8': 'https://www.lemon8-app.com/@kain.kat/7545374036445446674?region=nz',
    'instagram': 'https://www.instagram.com/emescafe.akl/',
}

def download(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=25) as response:
        return response.read(12_000_000)

candidates=[]
for source, url in SOURCES.items():
    try:
        raw=download(url).decode('utf-8')
        (OUT / (source+'.html')).write_text(raw)
        decoded=html.unescape(raw.replace('\\u002F','/').replace('\\/','/').replace('\\u0026','&'))
        urls=re.findall(r'https://[^\s\"<>]+',decoded)
        allowed=('cdninstagram.com','fbcdn.net','byteimg.com','lemon8cdn.com','tiktokcdn.com')
        urls=[u.rstrip('\\') for u in dict.fromkeys(urls) if any(host in u for host in allowed)]
        for u in urls[:35]:
            if not any(ext in u for ext in ('.mp4','.js','.css')):
                candidates.append({'source':source,'source_page':url,'url':u})
        print(source, 'public page bytes:',len(raw),'image candidates:',len(urls))
    except Exception as exc:
        print(source,'unavailable:',exc)

def save(pair):
    number,item=pair
    try:
        data=download(item['url'])
        if data.startswith(b'\x89PNG') or data.startswith(b'\xff\xd8') or data[:4]==b'RIFF':
            ext='png' if data.startswith(b'\x89PNG') else ('webp' if data[:4]==b'RIFF' else 'jpg')
            name=f'{number:02d}-{item["source"]}.{ext}'
            (OUT/name).write_bytes(data)
            item['file']=name
    except Exception as exc:
        item['error']=str(exc)
    return item
with ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(save,enumerate(candidates)))
(OUT/'references.json').write_text(json.dumps(results,indent=2))
print('Downloaded',sum('file' in item for item in results),'candidate images. All rights pending.')
