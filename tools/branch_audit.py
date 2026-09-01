from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET
import json, re, sys, os

ROOT=Path('.')
DOMAIN='https://maqtastudio.com'
AUDIT=Path('audit'); AUDIT.mkdir(exist_ok=True)
errors=[]; warnings=[]; notes=[]

# -------- helpers --------
def attr(tag, name):
    m=re.search(rf'\b{re.escape(name)}=["\']([^"\']*)["\']', tag, re.I)
    return m.group(1) if m else None

def local_target(base, raw):
    if not raw or raw.startswith(('#','mailto:','tel:','javascript:')): return None
    u=urlparse(raw)
    if u.scheme or u.netloc: return None
    p=unquote(u.path)
    if not p: return None
    t=(ROOT/p.lstrip('/')) if p.startswith('/') else (base.parent/p)
    parts=[]
    for x in t.parts:
        if x in ('','.'): continue
        if x=='..':
            if parts: parts.pop()
        else: parts.append(x)
    t=Path(*parts)
    if p.endswith('/'): t=t/'index.html'
    elif not t.suffix: t=t/'index.html'
    return t

def txt_between(text, tag):
    m=re.search(rf'<{tag}\b[^>]*>(.*?)</{tag}>', text, re.I|re.S)
    return re.sub(r'<[^>]+>','',m.group(1)).strip() if m else ''

# -------- root / Netlify routing --------
redir=Path('_redirects').read_text(encoding='utf-8')
if not re.search(r'^/\s+/fr/\s+301!\s*$', redir, re.M): errors.append('Root / is not a forced 301 redirect to /fr/.')
if not re.search(r'^/index\.html\s+/fr/\s+301!\s*$', redir, re.M): warnings.append('/index.html is not force-redirected to /fr/.')
root=Path('index.html').read_text(encoding='utf-8')
if 'noindex,follow' not in root or "window.location.replace('/fr/')" not in root: errors.append('Root index fallback is not a noindex redirect fallback.')

headers=Path('_headers').read_text(encoding='utf-8')
if '/assets/*' in headers and 'immutable' in headers.lower():
    warnings.append('All /assets/* are browser-cached immutable for one year although site.css/site.js are not fingerprinted. This can serve stale CSS/JS after future deploys.')

# -------- sitemap and pages --------
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
tree=ET.parse('sitemap.xml')
locs=[e.text.strip() for e in tree.findall('.//s:loc',ns)]
locset=set(locs)
notes.append(f'Sitemap URLs: {len(locs)}')
if len(locs)!=len(locset): errors.append('Duplicate URLs exist in sitemap.xml.')

titles={}; descriptions={}; html_paths=[]
for lang in ('fr','en','ar'):
    html_paths += sorted(Path(lang).rglob('index.html'))

for p in html_paths:
    text=p.read_text(encoding='utf-8')
    rel='/'+'/'.join(p.parts[:-1])+'/'
    expected=DOMAIN+rel
    title=txt_between(text,'title')
    titles.setdefault(title,[]).append(str(p))
    meta_tags=re.findall(r'<meta\b[^>]*>',text,re.I)
    desc=''
    for t in meta_tags:
        if (attr(t,'name') or '').lower()=='description': desc=attr(t,'content') or ''
    descriptions.setdefault(desc,[]).append(str(p))
    if not title: errors.append(f'{p}: missing title')
    if not desc: errors.append(f'{p}: missing meta description')
    if len(title)>70: warnings.append(f'{p}: long title ({len(title)} chars)')
    if len(desc)>160: warnings.append(f'{p}: long description ({len(desc)} chars)')
    if len(re.findall(r'<h1\b',text,re.I))!=1: errors.append(f'{p}: must contain exactly one H1')

    links=re.findall(r'<link\b[^>]*>',text,re.I)
    canon=[attr(t,'href') for t in links if (attr(t,'rel') or '').lower()=='canonical']
    if canon!=[expected]: errors.append(f'{p}: canonical {canon} != {expected}')
    alts={}
    for t in links:
        if (attr(t,'rel') or '').lower()=='alternate' and attr(t,'hreflang'):
            alts[(attr(t,'hreflang') or '').lower()]=attr(t,'href')
    for h in ('fr','en','ar','x-default'):
        if h not in alts: errors.append(f'{p}: missing hreflang {h}')
        elif alts[h] not in locset: errors.append(f'{p}: hreflang target not in sitemap: {alts[h]}')

    # JSON-LD validity
    ld=re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>',text,re.I|re.S)
    if not ld: errors.append(f'{p}: no JSON-LD')
    for chunk in ld:
        try: json.loads(chunk)
        except Exception as e: errors.append(f'{p}: invalid JSON-LD: {e}')

    # imgs
    for img in re.findall(r'<img\b[^>]*>',text,re.I):
        if attr(img,'alt') is None: errors.append(f'{p}: img missing alt')
        src=attr(img,'src')
        t=local_target(p,src)
        if t and not t.exists(): errors.append(f'{p}: missing image {src}')
    # local references
    for tag in re.findall(r'<(?:a|link|script)\b[^>]*>',text,re.I):
        raw=attr(tag,'href') or attr(tag,'src')
        t=local_target(p,raw)
        if t and not t.exists(): errors.append(f'{p}: broken local reference {raw} -> {t}')

    # project SEO / content quality
    if '/work/' in rel and rel.count('/')==4: # /lang/work/project/
        og=''
        for t in meta_tags:
            if (attr(t,'property') or '').lower()=='og:image': og=attr(t,'content') or ''
        if og.endswith('/assets/og-image.jpg'):
            warnings.append(f'{p}: project page uses generic site OG image instead of its project cover.')
        generic_alt=re.findall(r'alt=["\'][^"\']*(?:application|تطبيق)\s*[12][^"\']*["\']',text,re.I)
        if generic_alt: warnings.append(f'{p}: gallery contains generic numbered ALT text rather than descriptive ALT text.')

# pages in sitemap must exist
for loc in locs:
    path=urlparse(loc).path.strip('/')
    fp=Path(path)/'index.html'
    if not fp.exists(): errors.append(f'Sitemap URL missing file: {loc}')

# duplicate metadata (same-language duplicates are suspicious; cross-language may be intentional only if brand names)
for title,paths in titles.items():
    langs={Path(x).parts[0] for x in paths}
    if title and len(paths)>1 and len(langs)==1: warnings.append(f'Duplicate title in same language: {title} -> {paths}')
for d,paths in descriptions.items():
    langs={Path(x).parts[0] for x in paths}
    if d and len(paths)>1 and len(langs)==1: warnings.append(f'Duplicate description in same language -> {paths}')

# -------- CSS/code quality stats --------
css=Path('assets/site.css').read_text(encoding='utf-8')
js=Path('assets/site.js').read_text(encoding='utf-8')
notes.append(f'CSS bytes: {len(css.encode("utf-8")):,}')
notes.append(f'JS bytes: {len(js.encode("utf-8")):,}')
notes.append(f'CSS !important count: {css.count("!important")}')
version_comments=re.findall(r'V\d+',css)
notes.append(f'Legacy version markers in CSS: {len(version_comments)} ({", ".join(sorted(set(version_comments)))})')
if css.count('!important')>40: warnings.append(f'CSS uses {css.count("!important")} !important declarations; stylesheet has accumulated override layers and should be consolidated carefully.')
if len(version_comments)>5: warnings.append('Stylesheet contains many historical version override sections; this increases regression risk and maintenance cost.')
if "classList.add('in')" in js and '.reveal.in' not in css:
    warnings.append("IntersectionObserver adds class 'in' but CSS has no .reveal.in rule; observer work is currently redundant.")

# class reference rough audit
content='\n'.join(p.read_text(encoding='utf-8') for p in html_paths)+js
css_classes=set(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)',css))
used_classes=set()
for m in re.finditer(r'class=["\']([^"\']+)["\']',content): used_classes.update(m.group(1).split())
unused=sorted(css_classes-used_classes)
notes.append(f'CSS classes: {len(css_classes)}; no static HTML/JS reference: {len(unused)}')
notes.append('Sample unreferenced CSS classes: '+', '.join(unused[:80]))

# asset sizes and unreferenced assets
all_asset_files=[p for p in Path('assets').iterdir() if p.is_file()]
refs='\n'.join(p.read_text(encoding='utf-8') for p in html_paths+[Path('index.html')])+css+js
unused_assets=[p.name for p in all_asset_files if p.name not in refs and p.name not in ('site.css','site.js')]
notes.append(f'Assets: {len(all_asset_files)}; apparently unreferenced: {len(unused_assets)}')
if unused_assets: notes.append('Unreferenced asset candidates: '+', '.join(unused_assets))
large=sorted([(p.stat().st_size,p.name) for p in all_asset_files],reverse=True)[:15]
notes.append('Largest assets: '+', '.join(f'{n}={s/1024:.0f}KB' for s,n in large))

# -------- report --------
report=[]
report.append('MAQTA BRANCH STATIC AUDIT')
report.append('='*34)
report += ['','ERRORS'] + ([f'- {x}' for x in errors] or ['- none'])
report += ['','WARNINGS'] + ([f'- {x}' for x in warnings] or ['- none'])
report += ['','NOTES'] + [f'- {x}' for x in notes]
Path('audit/site-audit.txt').write_text('\n'.join(report),encoding='utf-8')
print('\n'.join(report))
# Do not fail on warnings; fail only on structural errors.
sys.exit(1 if errors else 0)
