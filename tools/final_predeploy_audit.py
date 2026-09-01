from pathlib import Path
from urllib.parse import urlparse, unquote
from html import unescape
import xml.etree.ElementTree as ET
import json
import re
import sys

ROOT = Path('.')
DOMAIN = 'https://maqtastudio.com'
LANGS = ('fr', 'en', 'ar')
PROJECT_NAMES = ('NAWA CAFÉ', 'URBAN MOVE', 'LUNA BOUTIQUE', 'PURE ORGANIC')

SERVICE_TYPES = {
    'fr': [
        "Design d’identité visuelle", "Design print", "Découpe vinyle",
        "Signalétique de vitrine", "Habillage véhicule", "Création de sites web",
        "Création de sites e-commerce", "Conception d’applications mobiles"
    ],
    'en': [
        "Brand identity design", "Print design", "Vinyl cutting", "Storefront signage",
        "Vehicle graphics", "Website design", "E-commerce design", "Mobile application design"
    ],
    'ar': [
        "تصميم الهوية البصرية", "التصميم والطباعة", "قص الفينيل",
        "لوحات وإشهار الواجهات", "إشهار وتغليف السيارات", "تصميم مواقع الويب",
        "تصميم المتاجر الإلكترونية", "تصميم تطبيقات الهاتف"
    ],
}

CATALOG_NAME = {
    'fr': 'Services MAQTA Studio',
    'en': 'MAQTA Studio Services',
    'ar': 'خدمات MAQTA Studio',
}

STREET = {'fr': 'Rue Benzarte', 'en': 'Rue Benzarte', 'ar': 'شارع بنزرت'}

ALT_REPLACEMENTS = {
    'fr': {
        'Conception de façade et signalétique pour NAWA Café à Fès — projet MAQTA': 'Concept de façade et signalétique pour NAWA Café — MAQTA Studio Fès',
        'Habillage véhicule et marquage adhésif Urban Move au Maroc — projet MAQTA': 'Concept d’habillage véhicule et marquage vinyle Urban Move — MAQTA Studio Maroc',
        'Signalétique de façade et identité visuelle Luna Boutique à Fès — projet MAQTA': 'Concept de signalétique de façade et identité visuelle Luna Boutique — MAQTA Studio Fès',
        'Design de site e-commerce responsive Pure Organic — projet digital MAQTA': 'Concept de site e-commerce responsive Pure Organic — MAQTA Studio Fès',
    },
    'en': {
        'NAWA Café storefront branding and signage design in Fès — MAQTA project': 'NAWA Café storefront branding and signage concept — MAQTA Studio Fès',
        'Urban Move vehicle graphics and vinyl branding in Morocco — MAQTA project': 'Urban Move vehicle graphics and vinyl branding concept — MAQTA Studio Morocco',
        'Luna Boutique storefront signage and brand identity in Fès — MAQTA project': 'Luna Boutique storefront signage and brand identity concept — MAQTA Studio Fès',
        'Pure Organic responsive e-commerce website design — MAQTA digital project': 'Pure Organic responsive e-commerce website concept — MAQTA Studio Fès',
    },
    'ar': {
        'تصميم واجهة وهوية بصرية لمقهى NAWA في فاس — مشروع MAQTA': 'تصميم مفاهيمي لواجهة وهوية مقهى NAWA — استوديو MAQTA فاس',
        'إشهار سيارة وقص فينيل لمشروع Urban Move في المغرب — مشروع MAQTA': 'تصميم مفاهيمي لإشهار سيارة وقص فينيل Urban Move — استوديو MAQTA المغرب',
        'تصميم لوحة وواجهة وهوية Luna Boutique في فاس — مشروع MAQTA': 'تصميم مفاهيمي للوحة وواجهة وهوية Luna Boutique — استوديو MAQTA فاس',
        'تصميم متجر إلكتروني متجاوب Pure Organic — مشروع رقمي من MAQTA': 'تصميم مفاهيمي لمتجر إلكتروني متجاوب Pure Organic — استوديو MAQTA فاس',
    },
}

LD_RE = re.compile(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', re.I | re.S)


def loc_to_file(loc: str) -> Path:
    p = unquote(urlparse(loc).path).strip('/')
    return Path(p) / 'index.html'


def business_fields(lang: str):
    service_types = SERVICE_TYPES[lang]
    return {
        '@type': ['ProfessionalService', 'Organization'],
        '@id': f'{DOMAIN}/#organization',
        'name': 'MAQTA Studio',
        'alternateName': 'MAQTA',
        'url': f'{DOMAIN}/',
        'telephone': '+212639879506',
        'image': f'{DOMAIN}/assets/og-image.jpg',
        'logo': f'{DOMAIN}/assets/image-02-cad96d8d4eb4.png',
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': STREET[lang],
            'addressLocality': 'Fès',
            'addressRegion': 'Fès-Meknès',
            'postalCode': '30000',
            'addressCountry': 'MA',
        },
        'areaServed': [
            {'@type': 'City', 'name': 'Fès'},
            {'@type': 'AdministrativeArea', 'name': 'Fès-Meknès'},
            {'@type': 'Country', 'name': 'Morocco'},
        ],
        'serviceType': service_types,
        'sameAs': ['https://www.instagram.com/maqta_studio/'],
        'contactPoint': {
            '@type': 'ContactPoint',
            'telephone': '+212639879506',
            'contactType': 'customer service',
            'areaServed': 'MA',
            'availableLanguage': ['Arabic', 'French', 'English'],
        },
        'hasOfferCatalog': {
            '@type': 'OfferCatalog',
            'name': CATALOG_NAME[lang],
            'itemListElement': [
                {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}}
                for n in service_types
            ],
        },
        'openingHoursSpecification': [
            {
                '@type': 'OpeningHoursSpecification',
                'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens': '09:00', 'closes': '16:00'
            },
            {
                '@type': 'OpeningHoursSpecification',
                'dayOfWeek': 'Saturday',
                'opens': '09:00', 'closes': '13:00'
            },
        ],
    }


def find_org(data):
    if isinstance(data, dict):
        if data.get('@id') == f'{DOMAIN}/#organization':
            return data
        graph = data.get('@graph')
        if isinstance(graph, list):
            for node in graph:
                if isinstance(node, dict) and node.get('@id') == f'{DOMAIN}/#organization':
                    return node
    return None


def patch_schema(path: Path, text: str, lang: str):
    matches = list(LD_RE.finditer(text))
    if not matches:
        raise RuntimeError(f'No JSON-LD found: {path}')
    for m in matches:
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        org = find_org(data)
        if org is None:
            continue
        org.clear()
        org.update(business_fields(lang))
        encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        return text[:m.start(1)] + encoded + text[m.end(1):]
    raise RuntimeError(f'Organization schema node not found: {path}')


def patch_file(path: Path, lang: str):
    text = path.read_text(encoding='utf-8')
    original = text
    text = patch_schema(path, text, lang)

    for old, new in ALT_REPLACEMENTS[lang].items():
        text = text.replace(old, new)

    if path == Path(lang) / 'work' / 'index.html':
        for name in PROJECT_NAMES:
            text = text.replace(f'<h3>{name}</h3>', f'<div class="project-card-title">{name}</div>')

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False


def attr_value(tag_text: str, attr: str):
    m = re.search(rf'\b{re.escape(attr)}=["\']([^"\']*)["\']', tag_text, re.I)
    return unescape(m.group(1)) if m else None


def resolve_local(base_file: Path, raw: str):
    if not raw or raw.startswith('#'):
        return None
    parsed = urlparse(unescape(raw))
    if parsed.scheme or parsed.netloc:
        return None
    p = unquote(parsed.path)
    if not p:
        return None
    if p.startswith('/'):
        target = Path(p.lstrip('/'))
    else:
        target = base_file.parent / p
    # Normalize without requiring existence yet.
    parts = []
    for part in target.parts:
        if part in ('', '.'):
            continue
        if part == '..':
            if parts:
                parts.pop()
        else:
            parts.append(part)
    target = Path(*parts)
    if p.endswith('/'):
        target = target / 'index.html'
    elif not target.suffix and not target.exists():
        target = target / 'index.html'
    return target


def audit_page(path: Path, loc: str, sitemap_locs: set, errors: list, warnings: list):
    text = path.read_text(encoding='utf-8')
    lang = path.parts[0]

    # Title / meta description.
    tm = re.search(r'<title>(.*?)</title>', text, re.I | re.S)
    if not tm:
        errors.append(f'{path}: missing title')
        title = ''
    else:
        title = unescape(re.sub(r'<[^>]+>', '', tm.group(1))).strip()

    metas = re.findall(r'<meta\b[^>]*>', text, re.I)
    desc = None
    for tag in metas:
        if (attr_value(tag, 'name') or '').lower() == 'description':
            desc = attr_value(tag, 'content') or ''
            break
    if desc is None:
        errors.append(f'{path}: missing meta description')
        desc = ''

    if path in [Path('fr/index.html'), Path('en/index.html'), Path('ar/index.html')]:
        if len(title) >= 60:
            errors.append(f'{path}: homepage title is {len(title)} chars (must be <60)')
        if len(desc) >= 155:
            errors.append(f'{path}: homepage description is {len(desc)} chars (must be <155)')
    else:
        if len(title) > 70:
            warnings.append(f'{path}: long title ({len(title)} chars)')
        if len(desc) > 160:
            warnings.append(f'{path}: long description ({len(desc)} chars)')

    # Canonical and hreflang.
    links = re.findall(r'<link\b[^>]*>', text, re.I)
    canonicals = []
    alternates = {}
    for tag in links:
        rel = (attr_value(tag, 'rel') or '').lower()
        href = attr_value(tag, 'href')
        if rel == 'canonical' and href:
            canonicals.append(href)
        if rel == 'alternate':
            hl = attr_value(tag, 'hreflang')
            if hl and href:
                alternates[hl.lower()] = href
    if canonicals != [loc]:
        errors.append(f'{path}: canonical mismatch {canonicals!r} != {loc}')
    for hl in ('fr', 'en', 'ar', 'x-default'):
        if hl not in alternates:
            errors.append(f'{path}: missing hreflang {hl}')
        elif alternates[hl] not in sitemap_locs:
            errors.append(f'{path}: hreflang {hl} target not in sitemap: {alternates[hl]}')

    # Heading structure.
    h1_count = len(re.findall(r'<h1\b', text, re.I))
    if h1_count != 1:
        errors.append(f'{path}: expected exactly one H1, found {h1_count}')
    if path in [Path(x) / 'index.html' for x in LANGS] or path in [Path(x) / 'work' / 'index.html' for x in LANGS]:
        for name in PROJECT_NAMES:
            if re.search(rf'<h[23]\b[^>]*>\s*{re.escape(name)}\s*</h[23]>', text, re.I):
                errors.append(f'{path}: project name still used as H2/H3: {name}')

    # Images: alt required; local src/srcset targets must exist.
    for tag in re.findall(r'<img\b[^>]*>', text, re.I):
        if attr_value(tag, 'alt') is None:
            errors.append(f'{path}: image missing alt attribute: {tag[:100]}')
        src = attr_value(tag, 'src')
        target = resolve_local(path, src) if src else None
        if target is not None and not target.exists():
            errors.append(f'{path}: missing image/script asset {src} -> {target}')
        srcset = attr_value(tag, 'srcset')
        if srcset:
            for item in srcset.split(','):
                candidate = item.strip().split()[0]
                target = resolve_local(path, candidate)
                if target is not None and not target.exists():
                    errors.append(f'{path}: missing srcset asset {candidate} -> {target}')

    # Internal href/src targets.
    for tag in re.findall(r'<(?:a|link|script)\b[^>]*>', text, re.I):
        raw = attr_value(tag, 'href') or attr_value(tag, 'src')
        target = resolve_local(path, raw) if raw else None
        if target is not None and not target.exists():
            errors.append(f'{path}: broken local reference {raw} -> {target}')

    # Structured data consistency.
    org = None
    parsed_any = False
    for m in LD_RE.finditer(text):
        try:
            data = json.loads(m.group(1))
            parsed_any = True
        except json.JSONDecodeError as exc:
            errors.append(f'{path}: invalid JSON-LD: {exc}')
            continue
        org = org or find_org(data)
    if not parsed_any:
        errors.append(f'{path}: no valid JSON-LD')
    if org is None:
        errors.append(f'{path}: organization schema missing')
    else:
        expected = business_fields(lang)
        for key in ('name', 'alternateName', 'url', 'telephone', 'address', 'openingHoursSpecification'):
            if org.get(key) != expected.get(key):
                errors.append(f'{path}: organization schema mismatch for {key}')

    if 'Rue Bizerte' in text:
        errors.append(f'{path}: obsolete misspelling Rue Bizerte remains')


def audit_contact_forms(errors: list):
    checks = {
        'fr': ('landing', 'e-commerce', 'web app', 'application mobile'),
        'en': ('landing', 'e-commerce', 'web app', 'mobile'),
        'ar': ('موقع', 'متجر', 'تطبيق'),
    }
    for lang, needles in checks.items():
        path = Path(lang) / 'contact' / 'index.html'
        text = path.read_text(encoding='utf-8').lower()
        m = re.search(r'<select\b[^>]*id=["\']project-type["\'][^>]*>(.*?)</select>', text, re.I | re.S)
        if not m:
            errors.append(f'{path}: project type selector missing')
            continue
        body = unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).lower()
        option_count = len(re.findall(r'<option\b', m.group(1), re.I))
        if option_count < 9:
            errors.append(f'{path}: too few project type options ({option_count})')
        for needle in needles:
            if needle.lower() not in body:
                errors.append(f'{path}: missing digital project option containing {needle!r}')


def main():
    sitemap = ET.parse('sitemap.xml')
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [el.text.strip() for el in sitemap.findall('.//sm:loc', ns) if el.text]
    if len(locs) != len(set(locs)):
        raise SystemExit('Duplicate URLs found in sitemap')
    sitemap_locs = set(locs)

    changed = []
    errors = []
    warnings = []

    if len(locs) != 39:
        errors.append(f'Sitemap URL count is {len(locs)}, expected 39')

    page_map = {}
    for loc in locs:
        path = loc_to_file(loc)
        page_map[loc] = path
        if not path.exists():
            errors.append(f'Sitemap URL missing file: {loc} -> {path}')
            continue
        if path.parts[0] not in LANGS:
            errors.append(f'Unexpected sitemap language path: {path}')
            continue
        try:
            if patch_file(path, path.parts[0]):
                changed.append(path)
        except Exception as exc:
            errors.append(f'{path}: patch failed: {exc}')

    # Preserve visual parity after demoting project names from heading tags on work listing pages.
    css_path = Path('assets/site.css')
    css = css_path.read_text(encoding='utf-8')
    marker = '/* MAQTA SEO project-card semantic-title parity */'
    if marker not in css:
        css += "\n\n" + marker + "\n.project-card-copy .project-card-title{font-family:Georgia,'Times New Roman',serif;font-weight:400;font-size:30px;margin:0 0 8px;letter-spacing:-.02em}\n"
        css_path.write_text(css, encoding='utf-8')
        changed.append(css_path)

    # Audit every sitemap page after patching.
    for loc, path in page_map.items():
        if path.exists():
            audit_page(path, loc, sitemap_locs, errors, warnings)

    # Confirm all language HTML pages are represented in sitemap, unless explicitly noindex.
    sitemap_files = set(page_map.values())
    for lang in LANGS:
        for path in Path(lang).rglob('*.html'):
            if path not in sitemap_files:
                text = path.read_text(encoding='utf-8')
                if re.search(r'<meta\b[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', text, re.I):
                    continue
                warnings.append(f'Indexable HTML page not in sitemap: {path}')

    audit_contact_forms(errors)

    # Dedicated web/app service pages must exist and be in sitemap.
    required_web = {
        Path('fr/services/sites-web-applications/index.html'): f'{DOMAIN}/fr/services/sites-web-applications/',
        Path('en/services/websites-apps/index.html'): f'{DOMAIN}/en/services/websites-apps/',
        Path('ar/services/websites-apps/index.html'): f'{DOMAIN}/ar/services/websites-apps/',
    }
    for path, loc in required_web.items():
        if not path.exists():
            errors.append(f'Missing dedicated web/apps service page: {path}')
        if loc not in sitemap_locs:
            errors.append(f'Web/apps service URL missing from sitemap: {loc}')

    robots = Path('robots.txt').read_text(encoding='utf-8')
    if f'Sitemap: {DOMAIN}/sitemap.xml' not in robots or 'Allow: /' not in robots:
        errors.append('robots.txt is missing Allow:/ or sitemap declaration')

    redirects = Path('_redirects').read_text(encoding='utf-8')
    if not re.search(r'^/\s+/fr/\s+301\s*$', redirects, re.M):
        errors.append('Root 301 redirect to /fr/ missing from _redirects')

    # Human-readable audit result.
    print(f'SITEMAP_URLS={len(locs)}')
    print(f'PATCHED_FILES={len(set(changed))}')
    print(f'WARNINGS={len(warnings)}')
    for w in warnings:
        print('WARNING:', w)
    print(f'ERRORS={len(errors)}')
    for e in errors:
        print('ERROR:', e)

    if errors:
        sys.exit(1)

    print('FINAL_PREDEPLOY_AUDIT=PASS')


if __name__ == '__main__':
    main()
