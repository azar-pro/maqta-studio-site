from pathlib import Path
import json, re

for path in [Path('fr/index.html'), Path('en/index.html'), Path('ar/index.html')]:
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
    if path.parts[0] in ('fr','en'):
        address['streetAddress'] = 'Rue Benzarte'
    else:
        address['streetAddress'] = 'شارع بنزرت'
    new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    text = text[:match.start(1)] + new_json + text[match.end(1):]
    path.write_text(text, encoding='utf-8')

print('Corrected Rue Benzarte spelling in FR/EN; Arabic unchanged.')
