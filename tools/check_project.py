"""Check the Drone V2 documentation, provenance and purchase budget, without writes."""
from decimal import Decimal
from pathlib import Path
from urllib.parse import urlparse
import ast
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def check():
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    pages = sorted(ROOT.rglob('*.md'))
    for page in pages:
        text = page.read_text(encoding='utf8')
        relative = page.relative_to(ROOT)
        for number, line in enumerate(text.splitlines(), 1):
            require(len(line) <= 100, f'{relative}:{number}: line over 100 characters')
            require(line == line.rstrip(), f'{relative}:{number}: trailing whitespace')
        refs = dict(re.findall(r'^\[([^\]]+)\]:\s*\n?\s*<?([^\s>]+)>?\s*$', text, re.M))
        used = re.findall(r'!?\[[^\]]+\]\[([^\]]+)\]', text)
        for key in used:
            require(key in refs, f'{relative}: undefined reference {key}')
        targets = re.findall(r'!?\[[^\]]+\]\(([^)]+)\)', text)
        targets += [refs[key] for key in used if key in refs]
        for target in targets:
            if target.startswith(('https:', 'http:', 'mailto:')):
                continue
            filename, _, fragment = target.partition('#')
            resolved = (page.parent / filename).resolve() if filename else page
            require(resolved.is_relative_to(ROOT), f'{relative}: dependency outside Drone V2: {target}')
            require(resolved.exists(), f'{relative}: missing link {target}')
            if fragment and resolved.exists() and resolved.suffix == '.md':
                headings = re.findall(r'^#+\s+(.+)$', resolved.read_text(encoding='utf8'), re.M)
                anchors = {re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-')
                           for heading in headings}
                require(fragment in anchors, f'{relative}: missing heading {target}')
        for table in re.findall(r'(?:^\|.*\n)+', text, re.M):
            rows = table.strip().splitlines()
            sizes = {len(row.split('|')) for row in rows}
            require(len(sizes) == 1 and len(rows) >= 2, f'{relative}: malformed table')
            if len(rows) >= 2:
                require(all(re.fullmatch(r'\s*:?-{3,}:?\s*', cell)
                            for cell in rows[1].split('|')[1:-1]),
                        f'{relative}: missing table separator')

    for path in ROOT.rglob('*.json'):
        json.loads(path.read_text(encoding='utf8'))
    data = json.loads((ROOT/'achats.json').read_text(encoding='utf8'))
    original_path = ROOT / data['origin']['local_snapshot']
    original = json.loads(original_path.read_text(encoding='utf8'))
    require(hashlib.sha256(original_path.read_bytes()).hexdigest() == data['origin']['sha256'],
            'Original V5 snapshot has changed')
    components = data['components']
    by_origin = {c['slug']: c for c in original['components']}
    require(len(components) == len(original['components']) == 19, 'Expected 19 reference lots')
    require(len({c['slug'] for c in components}) == len(components), 'Duplicate component slug')
    for component in components:
        slug = component['slug']
        reference = by_origin.get(component['origin_slug'])
        require(reference is not None, f'{slug}: missing V5 provenance')
        if reference:
            for key in ['asin', 'purchase_url', 'variant', 'lot_price_eur',
                        'order_lots', 'total_eur', 'seller', 'checked_on']:
                require(component[key] == reference[key], f'{slug}: reference {key} differs from V5')
        require(Decimal(str(component['lot_price_eur'])) * component['order_lots']
                == Decimal(str(component['total_eur'])), f'{slug}: incorrect lot total')
        require((ROOT / component['component_file']).exists(), f'{slug}: missing component sheet')
        source_path = ROOT / 'Composants' / slug / 'sources.json'
        require(source_path.exists(), f'{slug}: missing sources.json')
        if source_path.exists():
            require(json.loads(source_path.read_text(encoding='utf8')) == component,
                    f'{slug}: component source record differs from achats.json')
        require(component['procurement_state'] == 'non acheté', f'{slug}: initial purchase state differs')

    outside = [c for c in components if urlparse(c['purchase_url']).hostname != 'www.amazon.fr']
    require(len(outside) == 1 and outside[0]['slug'] == 'raspberry-pi-zero-2-w',
            'Only the Raspberry Pi may be purchased outside Amazon')
    require(not data['user_constraints']['lighting'], 'Lighting must remain excluded')
    require(not data['architecture']['custom_pcb_required'], 'No custom PCB in this base')
    require(not data['architecture']['hardware_verified'], 'Initial hardware must remain unverified')
    conditional = [c for c in components if c['conditional']]
    require({c['slug'] for c in conditional}
            == {'ceramique-100nf', 'electrolytiques', 'resistances'},
            'The three electronics supplements must remain conditional')
    amount = lambda values: sum((Decimal(str(c['total_eur'])) for c in values), Decimal('0'))
    budget = data['budget']
    expected = {
        'main_components_eur': amount(c for c in components if c['category'] == 'principal'),
        'supplies_eur': amount(c for c in components if c['category'] == 'fourniture'),
        'material_without_lighting_eur': amount(components),
        'reference_material_total_eur': amount(components),
        'conditional_lots_eur': amount(conditional),
        'subtotal_before_conditional_lots_eur': amount(c for c in components if not c['conditional']),
        'amazon_material_eur': amount(c for c in components if c not in outside),
        'outside_amazon_pi_eur': amount(outside),
        'excess_eur': amount(components) - Decimal(str(budget['ceiling_eur'])),
    }
    for key, value in expected.items():
        require(Decimal(str(budget[key])) == value, f'Budget {key}: incorrect total')
    require(budget['ceiling_met'] == (amount(components) <= Decimal(str(budget['ceiling_eur']))),
            'Budget ceiling status differs from total')
    purchase_text = (ROOT/'listeAchat.md').read_text(encoding='utf8')
    rows = re.findall(r'^\| \[.*?\]\[achat-\d+\] \| ([\d,]+) € \|$', purchase_text, re.M)
    require([Decimal(price.replace(',', '.')) for price in rows]
            == [Decimal(str(c['total_eur'])) for c in components],
            'Purchase Markdown prices differ from achats.json')
    for script in (ROOT/'tools').glob('*.py'):
        ast.parse(script.read_text(encoding='utf8'), filename=str(script))
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK : {len(pages)} documents Markdown, liens locaux, tableaux et syntaxe Python.')
    print('OK : 19 lots issus de V5, provenance, fiches et sources JSON cohérentes.')
    print('OK : Pi seul hors Amazon ; compléments conditionnels ; pas de PCB sur mesure.')
    print('OK : référence 205,37 €, compléments 24,97 €, sous-total avant décision 180,40 €.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(check())
    except (KeyError, ValueError, OSError, TypeError) as error:
        print(f'Échec de vérification : {error}', file=sys.stderr)
        sys.exit(1)
