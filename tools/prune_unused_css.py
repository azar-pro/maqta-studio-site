from pathlib import Path
import json
import re

ROOT=Path('.')
css_path=Path('assets/site.css')
css=css_path.read_text(encoding='utf-8')

used=set()
html_files=(list(Path('fr').rglob('*.html'))+list(Path('en').rglob('*.html'))+list(Path('ar').rglob('*.html'))+[Path('index.html'),Path('404.html')])
for p in html_files:
    text=p.read_text(encoding='utf-8')
    for m in re.finditer(r'class=["\']([^"\']+)["\']',text,re.I): used.update(m.group(1).split())
js=Path('assets/site.js').read_text(encoding='utf-8')
used.update(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)',js))
used.update(re.findall(r'classList\.(?:add|remove|toggle)\(["\']([A-Za-z_][A-Za-z0-9_-]*)',js))
used.update({'active','open','in','reveal'})

def find_matching(text,start):
    depth=0; quote=None; esc=False; in_comment=False; i=start
    while i<len(text):
        ch=text[i]; nxt=text[i+1] if i+1<len(text) else ''
        if in_comment:
            if ch=='*' and nxt=='/': in_comment=False; i+=2; continue
            i+=1; continue
        if quote:
            if esc: esc=False
            elif ch=='\\': esc=True
            elif ch==quote: quote=None
            i+=1; continue
        if ch=='/' and nxt=='*': in_comment=True; i+=2; continue
        if ch in ('"',"'"): quote=ch; i+=1; continue
        if ch=='{': depth+=1
        elif ch=='}':
            depth-=1
            if depth==0:return i
        i+=1
    return -1

def clean_block(text):
    out=[]; i=0; removed=0; kept=0
    while i<len(text):
        quote=None; in_comment=False; esc=False; brace=-1; semi=-1; k=i
        while k<len(text):
            ch=text[k]; nxt=text[k+1] if k+1<len(text) else ''
            if in_comment:
                if ch=='*' and nxt=='/': in_comment=False;k+=2;continue
                k+=1;continue
            if quote:
                if esc:esc=False
                elif ch=='\\':esc=True
                elif ch==quote:quote=None
                k+=1;continue
            if ch=='/' and nxt=='*':in_comment=True;k+=2;continue
            if ch in ('"',"'"):quote=ch;k+=1;continue
            if ch=='{':brace=k;break
            if ch==';':semi=k;break
            k+=1
        if brace<0: out.append(text[i:]);break
        if semi>=0 and semi<brace: out.append(text[i:semi+1]);i=semi+1;continue
        pre=text[i:brace]; end=find_matching(text,brace)
        if end<0: out.append(text[i:]);break
        body=text[brace+1:end]
        stripped=re.sub(r'/\*.*?\*/','',pre,flags=re.S).strip()
        if stripped.startswith('@'):
            name=stripped.split(None,1)[0].lower()
            if name in ('@media','@supports','@layer','@container'):
                cleaned,r,kp=clean_block(body);removed+=r;kept+=kp
                if cleaned.strip():out.append(pre+'{'+cleaned+'}');kept+=1
            else: out.append(pre+'{'+body+'}');kept+=1
        else:
            classes=set(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)',stripped))
            if classes and classes.isdisjoint(used): removed+=1
            else: out.append(pre+'{'+body+'}');kept+=1
        i=end+1
    return ''.join(out),removed,kept

cleaned,removed,kept=clean_block(css)
cleaned=re.sub(r'\n{4,}','\n\n\n',cleaned)
# Contact card is light; local NAP/hours must use dark text for readable contrast.
cleaned=cleaned.replace('.contact-local-facts strong{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:rgba(243,239,230,.62)}','.contact-local-facts strong{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--oxide)}')
cleaned=cleaned.replace('.contact-local-facts span{display:inline-block;margin-top:5px;font-size:13px;line-height:1.55;color:#F3EFE6}','.contact-local-facts span{display:inline-block;margin-top:5px;font-size:13px;line-height:1.55;color:var(--ink)}')
old_bytes=len(css.encode('utf-8'));new_bytes=len(cleaned.encode('utf-8'))
old_imp=css.count('!important');new_imp=cleaned.count('!important')
print(f'CSS_RULES_REMOVED={removed}')
print(f'CSS_RULES_KEPT={kept}')
print(f'CSS_BYTES={old_bytes}->{new_bytes} ({old_bytes-new_bytes} saved)')
print(f'IMPORTANT_COUNT={old_imp}->{new_imp}')
if cleaned!=css: css_path.write_text(cleaned,encoding='utf-8')

portfolio_meta={
    'fr':('Portfolio & études de marque à Fès — MAQTA','Découvrez les études conceptuelles MAQTA à Fès : identité visuelle, print, signalétique, marquage véhicule, e-commerce et design digital.'),
    'en':('Portfolio & brand studies in Fès — MAQTA','Explore MAQTA concept studies in Fès: brand identity, print, signage, vehicle graphics, e-commerce and digital design.'),
    'ar':('معرض الأعمال والدراسات البصرية في فاس — MAQTA','اكتشف الدراسات التصورية لـMAQTA في فاس: الهوية البصرية والطباعة والإشهار وقص الفينيل وإشهار المركبات والمتاجر الإلكترونية.')
}
for lang,(name,description) in portfolio_meta.items():
    p=Path(lang)/'work/index.html'; text=p.read_text(encoding='utf-8')
    m=re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)',text,re.S)
    if not m: raise SystemExit(f'Missing JSON-LD in {p}')
    data=json.loads(m.group(2)); found=False
    for node in data.get('@graph',[]):
        if node.get('@type')=='CollectionPage': node['name']=name; node['description']=description; found=True
    if not found: raise SystemExit(f'Missing CollectionPage node in {p}')
    compact=json.dumps(data,ensure_ascii=False,separators=(',',':'))
    updated=text[:m.start(2)]+compact+text[m.end(2):]
    if updated!=text: p.write_text(updated,encoding='utf-8'); print(f'SCHEMA_SYNCED={p}')

covers={'nawa-cafe':'image-04-b0c31110089e','urban-move':'image-05-8047ea27b712','luna-boutique':'image-06-c047225f08a2','pure-organic':'image-07-b429438b65c0'}
for lang in ('fr','en','ar'):
    listing=Path(lang)/'work/index.html'; text=listing.read_text(encoding='utf-8')
    for slug,stem in covers.items():
        src=f'../../assets/{stem}.webp'; pattern=rf'<img([^>]*?)\s+src="{re.escape(src)}"([^>]*)/?>'
        def listing_img(m,stem=stem,src=src):
            attrs=(m.group(1)+m.group(2)).strip()
            attrs=re.sub(r'\s*(?:width|height|decoding|srcset|sizes)="[^"]*"','',attrs).strip().rstrip('/').strip()
            return f'<img {attrs} decoding="async" width="1448" height="1086" srcset="../../assets/{stem}-640.webp 640w, ../../assets/{stem}-960.webp 960w, ../../assets/{stem}.webp 1448w" sizes="(max-width: 760px) calc(100vw - 36px), (max-width: 1160px) calc(50vw - 42px), 548px" src="{src}"/>'
        text=re.sub(pattern,listing_img,text,count=1)
    listing.write_text(text,encoding='utf-8')

    for slug,stem in covers.items():
        p=Path(lang)/'work'/slug/'index.html'; text=p.read_text(encoding='utf-8')
        src=f'../../../assets/{stem}.webp'; pattern=rf'(<div class="project-cover">)<img([^>]*?)\s+src="{re.escape(src)}"([^>]*)/?>'
        def cover_img(m,stem=stem,src=src):
            attrs=(m.group(2)+m.group(3)).strip()
            attrs=re.sub(r'\s*(?:width|height|decoding|fetchpriority|srcset|sizes)="[^"]*"','',attrs).strip().rstrip('/').strip()
            return m.group(1)+f'<img {attrs} decoding="async" fetchpriority="high" width="1448" height="1086" srcset="../../../assets/{stem}-640.webp 640w, ../../../assets/{stem}-960.webp 960w, ../../../assets/{stem}.webp 1448w" sizes="(max-width: 760px) calc(100vw - 36px), 1110px" src="{src}"/>'
        text=re.sub(pattern,cover_img,text,count=1)
        p.write_text(text,encoding='utf-8')
