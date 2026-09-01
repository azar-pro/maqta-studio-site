from pathlib import Path
import json
import sys
from playwright.sync_api import sync_playwright

OUT=Path('audit/screenshots'); OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8080'

pages={}
for lang in ('fr','en','ar'):
    for p in sorted(Path(lang).rglob('index.html')):
        route='/'+'/'.join(p.parts[:-1])+'/'
        key='-'.join(p.parts[:-1]) or lang
        pages[key]=route
pages['root-fallback']='/index.html'
pages['404']='/404.html'

# Representative screenshots; every route is still rendered and validated.
screenshot_routes={
    '/fr/','/fr/work/','/fr/services/','/fr/contact/',
    '/fr/work/nawa-cafe/','/fr/work/urban-move/','/fr/work/luna-boutique/','/fr/work/pure-organic/',
    '/en/','/en/work/','/en/services/','/en/contact/',
    '/ar/','/ar/work/','/ar/services/','/ar/contact/','/404.html'
}
viewports={'desktop':{'width':1440,'height':1000},'mobile':{'width':390,'height':844}}
results=[]
failures=[]

with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for mode,vp in viewports.items():
        ctx=browser.new_context(viewport=vp,device_scale_factor=1)
        for name,path in pages.items():
            page=ctx.new_page(); console=[]
            page.on('console',lambda msg,arr=console: arr.append({'type':msg.type,'text':msg.text}) if msg.type=='error' else None)
            page.goto(BASE+path,wait_until='networkidle')
            # Trigger all lazy-loaded images before judging image health.
            page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            page.wait_for_timeout(350)
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_timeout(100)
            data=page.evaluate('''() => ({
              scrollWidth: document.documentElement.scrollWidth,
              clientWidth: document.documentElement.clientWidth,
              scrollHeight: document.documentElement.scrollHeight,
              brokenImages: [...document.images].filter(i=>!i.complete || i.naturalWidth===0).map(i=>i.currentSrc || i.src),
              h1: [...document.querySelectorAll('h1')].map(x=>x.innerText.trim()),
              title: document.title,
              bodyTextLength: document.body.innerText.length,
              finalUrl: location.pathname
            })''')
            data.update({'name':name,'mode':mode,'requestedUrl':path,'consoleErrors':console})
            data['horizontalOverflow']=data['scrollWidth']>data['clientWidth']+1
            if path in screenshot_routes:
                page.screenshot(path=str(OUT/f'{mode}-{name}.png'),full_page=True)
            problems=[]
            if data['horizontalOverflow']: problems.append('horizontal overflow')
            if data['brokenImages']: problems.append('broken images: '+', '.join(data['brokenImages']))
            if data['consoleErrors']: problems.append('console errors')
            if len(data['h1'])!=1: problems.append(f'H1 count={len(data["h1"])}')
            if path=='/index.html' and data['finalUrl']!='/fr/': problems.append('root fallback did not reach /fr/')
            if problems:
                failures.append({'name':name,'mode':mode,'requestedUrl':path,'problems':problems})
            results.append(data)
            page.close()
        ctx.close()
    browser.close()

Path('audit/visual-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
Path('audit/visual-failures.json').write_text(json.dumps(failures,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'ROUTES_TESTED={len(pages)}')
print(f'VIEWPORT_RUNS={len(results)}')
print(f'VISUAL_FAILURES={len(failures)}')
if failures:
    print(json.dumps(failures,ensure_ascii=False,indent=2))
sys.exit(1 if failures else 0)
