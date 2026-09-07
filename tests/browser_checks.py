"""Browser regression checks against the GitHub Pages project subpath.
Dev dependencies: playwright==1.55.0 and axe-core@4.10.3. No runtime dependencies.
"""
from pathlib import Path
from contextlib import contextmanager
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
import json, os, subprocess, sys, tempfile, time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'test-results'
OUT.mkdir(exist_ok=True)
BASE = 'http://127.0.0.1:4173/eme-cafe/'
report = {'viewports': [], 'checks': [], 'axe_violations': [], 'limitations': ['Automated axe and keyboard checks do not replace a complete manual WCAG or screen-reader audit.', 'Lab checks are not field Core Web Vitals.']}

@contextmanager
def server():
    with tempfile.TemporaryDirectory() as folder:
        os.symlink(ROOT / 'dist', Path(folder) / 'eme-cafe', target_is_directory=True)
        process = subprocess.Popen([sys.executable, '-m', 'http.server', '4173', '--bind', '127.0.0.1', '--directory', folder], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1)
        try:
            yield
        finally:
            process.terminate()
            process.wait(timeout=10)

with server(), sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []
    for width, height in [(320,800),(375,812),(390,844),(768,1024),(1024,900),(1440,1000)]:
        context = browser.new_context(viewport={'width':width,'height':height}, device_scale_factor=1)
        page = context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        response = page.goto(BASE, wait_until='networkidle')
        assert response.status == 200
        page.evaluate('document.fonts.ready')
        assert page.locator('h1').count() == 1
        overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
        assert not overflow, f'Horizontal page overflow at {width}px'
        for image in page.locator('img[data-business-photo]').all():
            image.scroll_into_view_if_needed()
            image.evaluate('(img) => img.loading = "eager"')
        page.wait_for_timeout(600)
        broken = page.locator('img[data-business-photo]').evaluate_all('(imgs) => imgs.filter(img => !img.complete || !img.naturalWidth).map(img => img.src)')
        assert not broken, f'Broken images at {width}px: {broken}'
        page.evaluate('window.scrollTo(0,0)')
        page.wait_for_timeout(150)
        if width in (390,1440):
            page.screenshot(path=str(OUT / f'homepage-{width}.png'), full_page=True)
            page.screenshot(path=str(OUT / f'hero-{width}.png'))
        report['viewports'].append({'width':width,'height':height,'horizontal_overflow':False,'broken_images':0})
        context.close()

    context = browser.new_context(viewport={'width':390,'height':844})
    page = context.new_page()
    page.goto(BASE, wait_until='networkidle')
    toggle = page.get_by_role('button', name='Menu', exact=True)
    toggle.focus()
    page.keyboard.press('Enter')
    assert toggle.get_attribute('aria-expanded') == 'true'
    assert page.locator('#site-nav').is_visible()
    page.keyboard.press('Escape')
    assert toggle.get_attribute('aria-expanded') == 'false'
    assert toggle.evaluate('(button) => button === document.activeElement')
    report['checks'].append('Mobile navigation opens by keyboard, closes with Escape and restores focus')
    page.get_by_role('button', name='Coffee & matcha', exact=True).click()
    assert page.locator('.food-card:visible').count() == 1
    assert page.locator('.flavour-item:visible').count() == 2
    assert '3 food and drink highlights' in page.locator('#filter-status').inner_text()
    page.get_by_role('button', name='A bit of everything', exact=True).click()
    assert page.locator('.food-card:visible').count() == 3
    assert page.locator('.flavour-item:visible').count() == 4
    report['checks'].append('Category filters and live status work; reset restores all seven highlights')
    page.emulate_media(reduced_motion='reduce')
    assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior') == 'auto'
    assert page.locator('.button').first.evaluate('(el) => getComputedStyle(el).transitionDuration') == '0s'
    report['checks'].append('Reduced-motion preference removes smooth scrolling and transitions')
    schema = json.loads(page.locator('script[type="application/ld+json"]').inner_text())
    cafe = next(x for x in schema['@graph'] if x['@type'] == 'CafeOrCoffeeShop')
    assert cafe['openingHoursSpecification'][0]['opens'] == '06:30'
    assert cafe['openingHoursSpecification'][0]['closes'] == '15:00'
    assert '5759762822561383577' in cafe['hasMap']
    assert 'aggregateRating' not in cafe and 'priceRange' not in cafe
    assert page.locator('meta[name=robots]').get_attribute('content') == 'noindex, nofollow'
    report['checks'].append('Structured data parses; hours, exact Maps CID and preview noindex match content')
    for href in page.locator('a[href]').evaluate_all('(links) => [...new Set(links.map(a => a.getAttribute("href")))]'):
        if href.startswith('#'):
            assert page.locator(href).count(), f'Missing anchor: {href}'
        elif not urlparse(href).scheme:
            result = context.request.get(urljoin(BASE, href))
            assert result.status == 200, f'Broken local link: {href}'
    report['checks'].append('All homepage local links and anchors resolve under /eme-cafe/')
    axe = ROOT / 'node_modules/axe-core/axe.min.js'
    if not axe.exists():
        raise RuntimeError('Install pinned axe-core before running the accessibility checks')
    for document in ('','credits.html','privacy.html'):
        page.goto(BASE+document, wait_until='networkidle')
        page.add_script_tag(path=str(axe))
        result = page.evaluate('async () => await axe.run(document, {runOnly:{type:"tag",values:["wcag2a","wcag2aa","wcag21aa","wcag22aa"]}})')
        violations = [{'id':v['id'],'impact':v['impact'],'description':v['description'],'nodes':[n['target'] for n in v['nodes']]} for v in result['violations']]
        report['axe_violations'].extend([{'page':document or 'index.html', **v} for v in violations])
    context.close()

    context = browser.new_context(java_script_enabled=False, viewport={'width':390,'height':844})
    page = context.new_page()
    page.goto(BASE, wait_until='networkidle')
    assert page.locator('#site-nav').is_visible()
    assert page.locator('.food-card:visible').count() == 3
    assert page.locator('.flavour-item:visible').count() == 4
    assert page.locator('.filter-bar').is_hidden()
    assert '6:30 am' in page.locator('#visit').inner_text()
    assert not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
    report['checks'].append('No-JavaScript fallback exposes navigation, all food highlights, contact and hours')
    context.close()
    browser.close()
    report['javascript_errors'] = errors
    (OUT/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
    assert not errors, 'JavaScript errors were captured'
    assert not report['axe_violations'], 'Accessibility violations were captured; see report.json'
