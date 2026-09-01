from pathlib import Path
import json
from playwright.sync_api import sync_playwright

OUT=Path('audit/screenshots'); OUT.mkdir(parents=True,exist_ok=True)
BASE='http://127.0.0.1:8080'
pages={
 'fr-home':'/fr/','fr-work':'/fr/work/','fr-services':'/fr/services/','fr-contact':'/fr/contact/',
 'fr-nawa':'/fr/work/nawa-cafe/','fr-pure':'/fr/work/pure-organic/',
 'en-home':'/en/','en-work':'/en/work/','en-services':'/en/services/','en-contact':'/en/contact/',
 'ar-home':'/ar/','ar-work':'/ar/work/','ar-services':'/ar/services/','ar-contact':'/ar/contact/'
}
viewports={'desktop':{'width':1440,'height':1000},'mobile':{'width':390,'height':844}}
results=[]
with sync_playwright() as pw:
    browser=pw.chromium.launch()
    for mode,vp in viewports.items():
        ctx=browser.new_context(viewport=vp,device_scale_factor=1)
        for name,path in pages.items():
            page=ctx.new_page(); console=[]
            page.on('console',lambda msg,arr=console: arr.append({'type':msg.type,'text':msg.text}) if msg.type=='error' else None)
            page.goto(BASE+path,wait_until='networkidle')
            page.wait_for_timeout(300)
            data=page.evaluate('''() => ({
              scrollWidth: document.documentElement.scrollWidth,
              clientWidth: document.documentElement.clientWidth,
              scrollHeight: document.documentElement.scrollHeight,
              brokenImages: [...document.images].filter(i=>!i.complete || i.naturalWidth===0).map(i=>i.src),
              h1: [...document.querySelectorAll('h1')].map(x=>x.innerText.trim()),
              title: document.title,
              bodyTextLength: document.body.innerText.length
            })''')
            data.update({'name':name,'mode':mode,'url':path,'consoleErrors':console})
            data['horizontalOverflow']=data['scrollWidth']>data['clientWidth']+1
            page.screenshot(path=str(OUT/f'{mode}-{name}.png'),full_page=True)
            results.append(data)
            page.close()
        ctx.close()
    browser.close()
Path('audit/visual-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
