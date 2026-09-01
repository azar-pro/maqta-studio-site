from pathlib import Path
import re

ROOT=Path('.')
LANGS=('fr','en','ar')

TEXT={
'fr':{
 'skip':'Aller au contenu principal','concept':'ÉTUDE CONCEPTUELLE',
 'cap_eyebrow':'MAQTA / EXPERTISES','cap_title':'Ce que ces études démontrent.','cap_intro':'Chaque étude met en scène plusieurs compétences MAQTA. Explorez directement le service qui correspond à votre projet.',
 'caps':[('Identité visuelle','Des systèmes de marque cohérents, du logo aux applications.','../services/identite-visuelle/index.html'),('Print & supports','Cartes, menus, packaging, étiquettes et supports prêts pour la production.','../services/print-cartes-visite/index.html'),('Signalétique & vinyle','Vitrines, lettrage, découpe vinyle et marquage véhicule.','../services/signaletique-vinyle/index.html'),('Sites web & applications','Sites vitrines, e-commerce, web apps et expériences mobiles.','../services/sites-web-applications/index.html')],
 'related_title':'Services illustrés par cette étude','related_intro':'Vous aimez cette direction ? Découvrez les services MAQTA utilisés ou simulés dans cette étude conceptuelle.',
 'address':'Adresse','address_value':'Rue Benzarte, Fès 30000, Maroc','hours':'Horaires','hours_value':'Lun–Ven 09:00–16:00 · Sam 09:00–13:00 · Dim fermé',
 'work_title':'Portfolio & études de marque à Fès — MAQTA','work_desc':'Découvrez les études conceptuelles MAQTA à Fès : identité visuelle, print, signalétique, marquage véhicule, e-commerce et design digital.',
},
'en':{
 'skip':'Skip to main content','concept':'CONCEPT STUDY',
 'cap_eyebrow':'MAQTA / CAPABILITIES','cap_title':'What these studies demonstrate.','cap_intro':'Each study brings several MAQTA capabilities together. Go directly to the service that matches your project.',
 'caps':[('Brand identity','Coherent brand systems, from the logo to real applications.','../services/brand-identity/index.html'),('Print & collateral','Cards, menus, packaging, labels and production-ready materials.','../services/print-design/index.html'),('Signage & vinyl','Storefronts, lettering, vinyl cutting and vehicle graphics.','../services/signage-vinyl/index.html'),('Websites & apps','Business websites, e-commerce, web apps and mobile experiences.','../services/websites-apps/index.html')],
 'related_title':'Services illustrated by this study','related_intro':'Like this direction? Explore the MAQTA services used or simulated in this concept study.',
 'address':'Address','address_value':'Rue Benzarte, Fès 30000, Morocco','hours':'Opening hours','hours_value':'Mon–Fri 09:00–16:00 · Sat 09:00–13:00 · Sun closed',
 'work_title':'Portfolio & brand studies in Fès — MAQTA','work_desc':'Explore MAQTA concept studies in Fès: brand identity, print, signage, vehicle graphics, e-commerce and digital design.',
},
'ar':{
 'skip':'انتقل إلى المحتوى الرئيسي','concept':'دراسة تصورية',
 'cap_eyebrow':'MAQTA / الخبرات','cap_title':'ماذا تُظهر هذه الدراسات؟','cap_intro':'تجمع كل دراسة بين أكثر من خبرة لدى MAQTA. انتقل مباشرة إلى الخدمة التي تناسب مشروعك.',
 'caps':[('الهوية البصرية','نظام بصري متماسك من الشعار إلى التطبيقات الواقعية.','../services/visual-identity/index.html'),('الطباعة والمطبوعات','بطاقات وقوائم وتغليف وملصقات وملفات جاهزة للإنتاج.','../services/print/index.html'),('الإشهار والفينيل','واجهات وحروف وقص فينيل وإشهار المركبات.','../services/signage-vinyl/index.html'),('المواقع والتطبيقات','مواقع احترافية ومتاجر إلكترونية وتطبيقات ويب وهاتف.','../services/websites-apps/index.html')],
 'related_title':'الخدمات التي توضحها هذه الدراسة','related_intro':'أعجبك هذا الاتجاه؟ اكتشف خدمات MAQTA المستخدمة أو المحاكية داخل هذه الدراسة التصورية.',
 'address':'العنوان','address_value':'شارع بنزرت، فاس 30000، المغرب','hours':'ساعات العمل','hours_value':'الاثنين–الجمعة 09:00–16:00 · السبت 09:00–13:00 · الأحد مغلق',
 'work_title':'معرض الأعمال والدراسات البصرية في فاس — MAQTA','work_desc':'اكتشف الدراسات التصورية لـMAQTA في فاس: الهوية البصرية والطباعة والإشهار وقص الفينيل وإشهار المركبات والمتاجر الإلكترونية.',
}}

PROJECTS={
 'nawa-cafe':{'name':'NAWA CAFÉ','cover':'image-04-b0c31110089e.webp','services':{'fr':[('Identité visuelle','../../services/identite-visuelle/index.html'),('Signalétique & vinyle','../../services/signaletique-vinyle/index.html'),('Print & supports','../../services/print-cartes-visite/index.html')],'en':[('Brand identity','../../services/brand-identity/index.html'),('Signage & vinyl','../../services/signage-vinyl/index.html'),('Print & collateral','../../services/print-design/index.html')],'ar':[('الهوية البصرية','../../services/visual-identity/index.html'),('الإشهار والفينيل','../../services/signage-vinyl/index.html'),('الطباعة والمطبوعات','../../services/print/index.html')]},
 'alts':{'fr':['Concept de façade et vitrine NAWA Café — MAQTA Studio','Concept de menu, gobelet et packaging NAWA Café — MAQTA Studio'],'en':['NAWA Café storefront and window branding concept — MAQTA Studio','NAWA Café menu, cup and takeaway packaging concept — MAQTA Studio'],'ar':['تصميم تصوري لواجهة وفينيل مقهى NAWA — استوديو MAQTA','تصميم تصوري لقائمة وأكواب وتغليف مقهى NAWA — استوديو MAQTA']}},
 'urban-move':{'name':'URBAN MOVE','cover':'image-05-8047ea27b712.webp','services':{'fr':[('Identité visuelle','../../services/identite-visuelle/index.html'),('Signalétique & vinyle','../../services/signaletique-vinyle/index.html')],'en':[('Brand identity','../../services/brand-identity/index.html'),('Signage & vinyl','../../services/signage-vinyl/index.html')],'ar':[('الهوية البصرية','../../services/visual-identity/index.html'),('الإشهار والفينيل','../../services/signage-vinyl/index.html')]},
 'alts':{'fr':['Concept de marquage latéral Urban Move sur véhicule — MAQTA Studio','Détail conceptuel du marquage arrière Urban Move — MAQTA Studio','Détail conceptuel de découpe vinyle Urban Move — MAQTA Studio'],'en':['Urban Move side vehicle graphics concept — MAQTA Studio','Urban Move rear vehicle branding detail concept — MAQTA Studio','Urban Move vinyl graphics detail concept — MAQTA Studio'],'ar':['تصميم تصوري لإشهار جانب مركبة Urban Move — استوديو MAQTA','تفصيل تصوري لإشهار خلفية مركبة Urban Move — استوديو MAQTA','تفصيل تصوري لقص فينيل Urban Move — استوديو MAQTA']}},
 'luna-boutique':{'name':'LUNA BOUTIQUE','cover':'image-06-c047225f08a2.webp','services':{'fr':[('Identité visuelle','../../services/identite-visuelle/index.html'),('Signalétique & vinyle','../../services/signaletique-vinyle/index.html')],'en':[('Brand identity','../../services/brand-identity/index.html'),('Signage & vinyl','../../services/signage-vinyl/index.html')],'ar':[('الهوية البصرية','../../services/visual-identity/index.html'),('الإشهار والفينيل','../../services/signage-vinyl/index.html')]},
 'alts':{'fr':['Concept de vitrine et enseigne Luna Boutique — MAQTA Studio','Concept de sacs et supports retail Luna Boutique — MAQTA Studio','Détail conceptuel de signalétique Luna Boutique — MAQTA Studio'],'en':['Luna Boutique storefront and signage concept — MAQTA Studio','Luna Boutique retail bags and collateral concept — MAQTA Studio','Luna Boutique signage detail concept — MAQTA Studio'],'ar':['تصميم تصوري لواجهة ولوحة Luna Boutique — استوديو MAQTA','تصميم تصوري لأكياس ومطبوعات Luna Boutique — استوديو MAQTA','تفصيل تصوري لإشهار Luna Boutique — استوديو MAQTA']}},
 'pure-organic':{'name':'PURE ORGANIC','cover':'image-07-b429438b65c0.webp','services':{'fr':[('Identité visuelle','../../services/identite-visuelle/index.html'),('Sites web & applications','../../services/sites-web-applications/index.html')],'en':[('Brand identity','../../services/brand-identity/index.html'),('Websites & apps','../../services/websites-apps/index.html')],'ar':[('الهوية البصرية','../../services/visual-identity/index.html'),('المواقع والتطبيقات','../../services/websites-apps/index.html')]},
 'alts':{'fr':['Concept mobile e-commerce Pure Organic — MAQTA Studio','Concept de page e-commerce Pure Organic sur tablette — MAQTA Studio','Concept de présentation produit Pure Organic — MAQTA Studio'],'en':['Pure Organic mobile e-commerce concept — MAQTA Studio','Pure Organic tablet e-commerce page concept — MAQTA Studio','Pure Organic product presentation concept — MAQTA Studio'],'ar':['تصميم تصوري لمتجر Pure Organic على الهاتف — استوديو MAQTA','تصميم تصوري لمتجر Pure Organic على الجهاز اللوحي — استوديو MAQTA','تصميم تصوري لعرض منتجات Pure Organic — استوديو MAQTA']}}
}


def write_if(path,text):
    old=path.read_text(encoding='utf-8')
    if text!=old:
        path.write_text(text,encoding='utf-8'); return True
    return False

changed=[]

# Global page accessibility + remove obsolete homepage preload.
for lang in LANGS:
    for p in sorted(Path(lang).rglob('index.html')):
        s=p.read_text(encoding='utf-8'); orig=s
        # Remove preload for an image no longer rendered in the hero.
        s=re.sub(r'<link\s+rel="preload"\s+as="image"\s+href="/assets/image-01-b4dd0f282b97\.webp"[^>]*?/?>\s*','',s,flags=re.I)
        # Main content target: keep semantic main, replace any previous id such as top.
        m=re.search(r'<main\b([^>]*)>',s,re.I)
        if m:
            attrs=m.group(1)
            attrs=re.sub(r'\s+id="[^"]*"','',attrs)
            attrs=re.sub(r'\s+tabindex="[^"]*"','',attrs)
            s=s[:m.start()]+f'<main id="main-content" tabindex="-1"{attrs}>'+s[m.end():]
        # Accessible skip link after body.
        if 'class="skip-link"' not in s:
            s=re.sub(r'(<body\b[^>]*>)',r'\1\n<a class="skip-link" href="#main-content">'+TEXT[lang]['skip']+'</a>',s,count=1,flags=re.I)
        # Current-page state for visibly active links (nav + mobile + language selector).
        def curr(m):
            tag=m.group(0)
            return tag if 'aria-current=' in tag else tag[:-1]+' aria-current="page">'
        s=re.sub(r'<a\b[^>]*class="[^"]*\bactive\b[^"]*"[^>]*>',curr,s,flags=re.I)
        if write_if(p,s): changed.append(str(p))

# Work listing: transparent metadata, concept badges, balanced capabilities.
for lang in LANGS:
    p=Path(lang)/'work/index.html'; s=p.read_text(encoding='utf-8'); orig=s; t=TEXT[lang]
    # Title/meta/OG/Twitter copy.
    s=re.sub(r'<title>.*?</title>',f'<title>{t["work_title"]}</title>',s,count=1,flags=re.S)
    s=re.sub(r'<meta content="[^"]*" name="description"/>',f'<meta content="{t["work_desc"]}" name="description"/>',s,count=1)
    s=re.sub(r'<meta content="[^"]*" property="og:title"/>',f'<meta content="{t["work_title"]}" property="og:title"/>',s,count=1)
    s=re.sub(r'<meta content="[^"]*" property="og:description"/>',f'<meta content="{t["work_desc"]}" property="og:description"/>',s,count=1)
    s=re.sub(r'<meta content="[^"]*" name="twitter:title"/>',f'<meta content="{t["work_title"]}" name="twitter:title"/>',s,count=1)
    s=re.sub(r'<meta content="[^"]*" name="twitter:description"/>',f'<meta content="{t["work_desc"]}" name="twitter:description"/>',s,count=1)
    # CollectionPage schema title/desc strings, safe simple replace through JSON text.
    # visual badge in project image containers
    if 'project-concept-badge' not in s:
        s=s.replace('<div class="project-card-image"><img',f'<div class="project-card-image"><span class="project-concept-badge">{t["concept"]}</span><img')
    # Replace over-weighted single digital promo with a balanced service map.
    caps=''.join(f'<a class="portfolio-capability-card" href="{href}"><h3>{name}</h3><p>{desc}</p><span>→</span></a>' for name,desc,href in t['caps'])
    balanced=f'<section class="portfolio-capabilities"><div class="wrap"><div class="section-head reveal"><div><div class="page-eyebrow">{t["cap_eyebrow"]}</div><h2>{t["cap_title"]}</h2></div><p>{t["cap_intro"]}</p></div><div class="portfolio-capability-grid">{caps}</div></div></section>'
    s=re.sub(r'<section class="digital-capability">.*?</section>(?=<section class="project-next">)',balanced,s,count=1,flags=re.S)
    if write_if(p,s): changed.append(str(p))

# Home cards: make conceptual status visible immediately, not only in footnote.
for lang in LANGS:
    p=Path(lang)/'index.html'; s=p.read_text(encoding='utf-8'); t=TEXT[lang]
    if 'work-concept-badge' not in s:
        s=s.replace('<div class="work-image-wrap">\n<img',f'<div class="work-image-wrap">\n<span class="work-concept-badge">{t["concept"]}</span>\n<img')
    if write_if(p,s): changed.append(str(p))

# Contact: visibly match LocalBusiness NAP/hours to structured data.
for lang in LANGS:
    p=Path(lang)/'contact/index.html'; s=p.read_text(encoding='utf-8'); t=TEXT[lang]
    if 'contact-local-facts' not in s:
        facts=f'<div class="contact-local-facts"><div><strong>{t["address"]}</strong><br/><span>{t["address_value"]}</span></div><div><strong>{t["hours"]}</strong><br/><span>{t["hours_value"]}</span></div></div>'
        s=s.replace('</div></aside><div><div class="contact-assurance">',f'</div>{facts}</aside><div><div class="contact-assurance">',1)
    if write_if(p,s): changed.append(str(p))

# Project pages: project-specific social image, descriptive gallery ALT, internal service links.
for slug,info in PROJECTS.items():
    for lang in LANGS:
        p=Path(lang)/'work'/slug/'index.html'; s=p.read_text(encoding='utf-8'); t=TEXT[lang]
        absolute=f'https://maqtastudio.com/assets/{info["cover"]}'
        # Replace generic share image only on project pages.
        s=s.replace('<meta content="https://maqtastudio.com/assets/og-image.jpg" property="og:image"/>',f'<meta content="{absolute}" property="og:image"/>',1)
        s=s.replace('<meta content="https://maqtastudio.com/assets/og-image.jpg" name="twitter:image"/>',f'<meta content="{absolute}" name="twitter:image"/>',1)
        # Specific social image alt.
        social_alt=info['alts'][lang][0]
        s=re.sub(r'<meta content="MAQTA — Design, Print, Sign &amp; Digital" property="og:image:alt"/>',f'<meta content="{social_alt}" property="og:image:alt"/>',s,count=1)
        # Replace ALT attributes for gallery images in visual order.
        gm=re.search(r'(<div class="project-gallery">)(.*?)(</div>\s*</div>\s*</section>)',s,re.S)
        if gm:
            body=gm.group(2); alts=info['alts'][lang]; idx=[0]
            def alt_repl(m):
                i=idx[0]; idx[0]+=1
                alt=alts[min(i,len(alts)-1)]
                tag=m.group(0)
                if re.search(r'\balt="[^"]*"',tag): return re.sub(r'\balt="[^"]*"',f'alt="{alt}"',tag,count=1)
                return tag[:-2]+f' alt="{alt}"/>' if tag.endswith('/>') else tag[:-1]+f' alt="{alt}">'
            body=re.sub(r'<img\b[^>]*>',alt_repl,body)
            s=s[:gm.start(2)]+body+s[gm.end(2):]
        # Related service links before conversion CTA.
        if 'project-related-services' not in s:
            links=''.join(f'<a href="{href}">{name}<span>→</span></a>' for name,href in info['services'][lang])
            section=f'<section class="project-related-services"><div class="wrap"><div class="section-head"><h2>{t["related_title"]}</h2><p>{t["related_intro"]}</p></div><div class="project-related-links">{links}</div></div></section>'
            s=s.replace('<section class="project-next">',section+'<section class="project-next">',1)
        if write_if(p,s): changed.append(str(p))

# Remove redundant reveal observer: no CSS transition depends on .reveal.in.
p=Path('assets/site.js'); js=p.read_text(encoding='utf-8')
js=re.sub(r"\s*if\('IntersectionObserver' in window\)\{.*?\}\s*else document\.querySelectorAll\('\.reveal'\)\.forEach\(el=>el\.classList\.add\('in'\)\);\s*",'\n',js,flags=re.S)
if write_if(p,js): changed.append(str(p))

# Append focused, low-risk styles for the new semantic/UX improvements.
p=Path('assets/site.css'); css=p.read_text(encoding='utf-8')
MARK='/* ===== FINAL QA / ACCESSIBILITY / PORTFOLIO BALANCE ===== */'
if MARK not in css:
    css += r'''

/* ===== FINAL QA / ACCESSIBILITY / PORTFOLIO BALANCE ===== */
.skip-link{
  position:fixed;left:16px;top:12px;z-index:9999;
  transform:translateY(-180%);padding:11px 15px;border-radius:999px;
  background:#171716;color:#F3EFE6;font-size:13px;font-weight:700;
  transition:transform .18s ease;
}
.skip-link:focus{transform:none}
body[dir="rtl"] .skip-link{left:auto;right:16px}
:where(a,button,input,select,textarea,summary):focus-visible{
  outline:3px solid #A63A22;outline-offset:3px;
}
#main-content:focus{outline:none}

.project-card-image,.work-image-wrap{position:relative}
.project-concept-badge,.work-concept-badge{
  position:absolute;z-index:3;top:14px;left:14px;
  padding:7px 10px;border-radius:999px;
  background:rgba(23,23,22,.76);color:#F3EFE6;
  border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(8px);
  font-size:8px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
}
body[dir="rtl"] .project-concept-badge,body[dir="rtl"] .work-concept-badge{
  left:auto;right:14px;letter-spacing:0;text-transform:none;
}

.portfolio-capabilities{padding:78px 0 86px;border-top:1px solid var(--line)}
.portfolio-capability-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.portfolio-capability-card{
  min-height:210px;padding:24px;border:1px solid var(--line);border-radius:20px;
  display:flex;flex-direction:column;transition:transform .22s ease,border-color .22s ease,background .22s ease;
}
.portfolio-capability-card:hover,.portfolio-capability-card:focus-visible{
  transform:translateY(-3px);border-color:rgba(23,23,22,.38);background:rgba(255,255,255,.18)
}
.portfolio-capability-card h3{font-family:Georgia,'Times New Roman',serif;font-size:25px;font-weight:400;margin:0 0 14px}
body[dir="rtl"] .portfolio-capability-card h3{font-family:Tahoma,Arial,sans-serif}
.portfolio-capability-card p{font-size:13px;line-height:1.65;color:var(--soft);margin:0}
.portfolio-capability-card span{margin-top:auto;padding-top:20px;color:var(--oxide);font-size:20px}

.contact-local-facts{margin-top:26px;padding-top:22px;border-top:1px solid rgba(243,239,230,.16);display:grid;gap:18px}
.contact-local-facts strong{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:rgba(243,239,230,.62)}
.contact-local-facts span{display:inline-block;margin-top:5px;font-size:13px;line-height:1.55;color:#F3EFE6}
body[dir="rtl"] .contact-local-facts strong{letter-spacing:0;text-transform:none}

.project-related-services{padding:74px 0;border-top:1px solid var(--line)}
.project-related-links{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.project-related-links a{min-height:92px;padding:20px 22px;border:1px solid var(--line);border-radius:18px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-weight:700;transition:.2s ease}
.project-related-links a:hover,.project-related-links a:focus-visible{background:var(--ink);color:var(--paper);border-color:var(--ink);transform:translateY(-2px)}
.project-related-links span{color:var(--oxide);font-size:20px}

@media(max-width:900px){
  .portfolio-capability-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
  .project-related-links{grid-template-columns:1fr}
}
@media(max-width:600px){
  .portfolio-capabilities,.project-related-services{padding:58px 0}
  .portfolio-capability-grid{grid-template-columns:1fr}
  .portfolio-capability-card{min-height:170px}
  .project-concept-badge,.work-concept-badge{top:10px;left:10px;font-size:7.5px;padding:6px 8px}
  body[dir="rtl"] .project-concept-badge,body[dir="rtl"] .work-concept-badge{left:auto;right:10px}
}
'''
if write_if(p,css): changed.append(str(p))

print(f'POLISH_CHANGED_FILES={len(set(changed))}')
for x in sorted(set(changed)): print(x)
