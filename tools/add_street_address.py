from pathlib import Path
import json, re

PAGES = [Path('fr/index.html'), Path('en/index.html'), Path('ar/index.html')]

street_by_lang = {
    'fr': 'Rue Bizerte',
    'en': 'Rue Bizerte',
    'ar': 'شارع بنزرت',
}

for path in PAGES:
    text = path.read_text(encoding='utf-8')
    match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S)
    if not match:
        raise SystemExit(f'JSON-LD not found: {path}')

    data = json.loads(match.group(1))
    graph = data.get('@graph', [])
    business = next((node for node in graph if isinstance(node, dict) and node.get('@id') == 'https://maqtastudio.com/#organization'), None)
    if business is None:
        raise SystemExit(f'Business node not found: {path}')

    address = business.setdefault('address', {'@type': 'PostalAddress'})
    lang = path.parts[0]
    address['streetAddress'] = street_by_lang[lang]
    address['postalCode'] = '30000'
    address['addressLocality'] = 'Fès'
    address['addressRegion'] = 'Fès-Meknès'
    address['addressCountry'] = 'MA'

    new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    text = text[:match.start(1)] + new_json + text[match.end(1):]
    path.write_text(text, encoding='utf-8')

print('Added Rue Bizerte / شارع بنزرت to LocalBusiness schema.')
# Trigger workflow after workflow file exists.
