from pathlib import Path
import json, re

PAGES = [Path('fr/index.html'), Path('en/index.html'), Path('ar/index.html')]

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
    address['postalCode'] = '30000'

    business['openingHoursSpecification'] = [
        {
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'opens': '09:00',
            'closes': '16:00'
        },
        {
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': 'Saturday',
            'opens': '09:00',
            'closes': '13:00'
        }
    ]

    new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    text = text[:match.start(1)] + new_json + text[match.end(1):]
    path.write_text(text, encoding='utf-8')

print('Updated postal code and opening hours in FR/EN/AR homepage JSON-LD.')
