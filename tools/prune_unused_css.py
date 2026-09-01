from pathlib import Path
import re

ROOT=Path('.')
css_path=Path('assets/site.css')
css=css_path.read_text(encoding='utf-8')

# Static site: collect every class present in real HTML plus JS class/selectors.
used=set()
for p in list(Path('fr').rglob('*.html'))+list(Path('en').rglob('*.html'))+list(Path('ar').rglob('*.html'))+[Path('index.html')]:
    text=p.read_text(encoding='utf-8')
    for m in re.finditer(r'class=["\']([^"\']+)["\']',text,re.I):
        used.update(m.group(1).split())
js=Path('assets/site.js').read_text(encoding='utf-8')
used.update(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)',js))
used.update(re.findall(r'classList\.(?:add|remove|toggle)\(["\']([A-Za-z_][A-Za-z0-9_-]*)',js))
# Safety whitelist for common runtime/state classes.
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
        # preserve whitespace/comments before next rule
        j=i
        # find next top-level '{' or ';' for at-rule without block
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
        if brace<0:
            out.append(text[i:]);break
        if semi>=0 and semi<brace:
            out.append(text[i:semi+1]);i=semi+1;continue
        pre=text[i:brace]
        end=find_matching(text,brace)
        if end<0:
            out.append(text[i:]);break
        body=text[brace+1:end]
        stripped=re.sub(r'/\*.*?\*/','',pre,flags=re.S).strip()
        if stripped.startswith('@'):
            name=stripped.split(None,1)[0].lower()
            if name in ('@media','@supports','@layer','@container'):
                cleaned,r,kp=clean_block(body);removed+=r;kept+=kp
                # Keep surrounding at-rule if content still has a qualified/at rule.
                if cleaned.strip():out.append(pre+'{'+cleaned+'}');kept+=1
            else:
                out.append(pre+'{'+body+'}');kept+=1
        else:
            classes=set(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)',stripped))
            # Conservative removal: only if the rule references classes and NONE exist anywhere in real site content.
            if classes and classes.isdisjoint(used):
                removed+=1
            else:
                out.append(pre+'{'+body+'}');kept+=1
        i=end+1
    return ''.join(out),removed,kept

cleaned,removed,kept=clean_block(css)
# Normalize excessive blank lines only; do not minify, to keep maintainability.
cleaned=re.sub(r'\n{4,}','\n\n\n',cleaned)
old_bytes=len(css.encode('utf-8'));new_bytes=len(cleaned.encode('utf-8'))
old_imp=css.count('!important');new_imp=cleaned.count('!important')
print(f'CSS_RULES_REMOVED={removed}')
print(f'CSS_RULES_KEPT={kept}')
print(f'CSS_BYTES={old_bytes}->{new_bytes} ({old_bytes-new_bytes} saved)')
print(f'IMPORTANT_COUNT={old_imp}->{new_imp}')
if cleaned!=css:
    css_path.write_text(cleaned,encoding='utf-8')
