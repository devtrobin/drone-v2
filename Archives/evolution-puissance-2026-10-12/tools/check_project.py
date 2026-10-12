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


def is_project_file(path):
    return not set(path.relative_to(ROOT).parts) & {
        '.git', '.venv', '__pycache__', 'secrets', 'temp', 'tmp', '.ruff_cache'
    }


def check():
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    pages = sorted(path for path in ROOT.rglob('*.md') if is_project_file(path))
    for page in pages:
        text = page.read_text(encoding='utf8')
        relative = page.relative_to(ROOT)
        for number, line in enumerate(text.splitlines(), 1):
            url_reference = re.fullmatch(r'\[[^\]]+\]:\s*https?://\S+', line)
            require(len(line) <= 100 or url_reference,
                    f'{relative}:{number}: line over 100 characters')
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
        if not is_project_file(path) or path.name == 'robot.local.json':
            continue
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

    profiles = json.loads((ROOT/'Sources/fiches-techniques.json').read_text(encoding='utf8'))
    pdf_report = json.loads((ROOT/'Validation/resultats/fiches-pdf.json').read_text(encoding='utf8'))
    pdf_records = {record['slug']: record for record in pdf_report['documents']}
    slugs = {component['slug'] for component in components}
    require(set(profiles['profiles']) == set(pdf_records) == slugs,
            'PDF profiles and report must cover the 19 purchase lots')
    require({path.stem for path in (ROOT/'Composants').glob('*/*.pdf')} == slugs,
            'Expected one final PDF per component')
    require(not list((ROOT/'output/pdf').glob('*.pdf')), 'Old central PDF copies must be removed')
    estimation_index = json.loads((ROOT/'Sources/estimations-dimensions.json').read_text(encoding='utf8'))
    indexed_estimates = {item['slug']: item for item in estimation_index['components']}
    require(set(indexed_estimates) == slugs, 'Dimension index must cover all 19 components')
    for component in components:
        slug = component['slug']
        record = pdf_records[slug]
        collected = json.loads((ROOT/'Composants'/slug/'documentation.json').read_text(encoding='utf8'))
        require(collected['purchase_page'] == component['purchase_url'],
                f'{slug}: documentary purchase source differs')
        require(record['file'] == f'Composants/{slug}/{slug}.pdf', f'{slug}: unexpected PDF path')
        dimensions_path = ROOT/'Composants'/slug/'dimensions.json'
        dimensions = json.loads(dimensions_path.read_text(encoding='utf8'))
        require(dimensions['published_dimensions'] == profiles['profiles'][slug]['dimensions'],
                f'{slug}: documented dimensions differ from PDF profile')
        require(record['dimensions_sha256'] == hashlib.sha256(dimensions_path.read_bytes()).hexdigest(),
                f'{slug}: PDF dimension estimates need regeneration')
        require(record['dimension_estimates'] == len(dimensions['estimates']),
                f'{slug}: PDF estimate count differs')
        require(indexed_estimates[slug]['estimate_count'] == len(dimensions['estimates']),
                f'{slug}: dimension index count differs')
        require(indexed_estimates[slug]['file'] == str(dimensions_path.relative_to(ROOT)),
                f'{slug}: dimension index path differs')
        require(collected['dimensions_file'] == str(dimensions_path.relative_to(ROOT)),
                f'{slug}: documentary dimension path differs')
        require(collected['dimension_comparison_sources'] == dimensions['comparison_sources'],
                f'{slug}: comparison sources differ between registers')
        for estimate in dimensions['estimates']:
            require(estimate['unit'] == 'mm' and not estimate['physically_measured'],
                    f'{slug}: estimates must remain distinguished from physical measurements')
            require(len(estimate['nominal_mm']) == len(estimate['ranges_mm']) == len(estimate['axes']),
                    f'{slug}: dimension axes and ranges differ')
            require(all(0 < low <= value <= high for value, (low, high)
                        in zip(estimate['nominal_mm'], estimate['ranges_mm'])),
                    f'{slug}: estimate outside its stated range')
        for photo in dimensions['photo_evidence']:
            path = (ROOT/photo['file']).resolve()
            require(path.is_relative_to(ROOT) and path.is_file(),
                    f'{slug}: estimate photo evidence missing')
            if path.is_relative_to(ROOT) and path.is_file():
                require(hashlib.sha256(path.read_bytes()).hexdigest() == photo['sha256'],
                        f'{slug}: estimate photo changed')
        require(record['missing_text'] == [], f'{slug}: missing content in PDF')
        selected = profiles['profiles'][slug]['selected']
        require(record['photos_selected'] == len(selected), f'{slug}: PDF photo count differs')
        require(record['photos_downloaded'] == len(collected['photos']),
                f'{slug}: collected photo count differs')
        for index, photo in enumerate(collected['photos'], 1):
            require(photo['selected_for_pdf'] == (index in selected),
                    f'{slug}: gallery selection differs at photo {index}')
        for source in [record] + collected['photos'] + collected['documents']:
            path = (ROOT/source['file']).resolve()
            require(path.is_relative_to(ROOT) and path.is_file(),
                    f'{slug}: documentary file missing or outside project')
            if path.is_relative_to(ROOT) and path.is_file():
                require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'],
                        f'{slug}: documentary file changed: {source["file"]}')

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
    def amount(values):
        return sum((Decimal(str(c['total_eur'])) for c in values), Decimal('0'))
    # Keep validating the archived V5 evidence without confusing it with current purchases.
    budget = data.get('reference_budget', data['budget'])
    supplements = data['assembly_supplements']
    require(len(supplements) == 4, 'Expected four grouped fixture purchase lots')
    fixture_sources = json.loads((ROOT/'Sources/fixations-amazon.json').read_text(encoding='utf8'))
    require(fixture_sources['products'] == supplements and not fixture_sources['orders_placed'],
            'Fixture purchase evidence differs or purchases falsely recorded')
    for item in supplements:
        require(urlparse(item['purchase_url']).hostname == 'www.amazon.fr'
                and item['purchase_url'].endswith('/dp/' + item['asin']),
                'Fixture purchases must link to exact Amazon France products')
        require(Decimal(str(item['lot_price_eur'])) * item['order_lots']
                == Decimal(str(item['total_eur'])) and item['total_eur'] > 0,
                'Fixture lot total incorrect')
        require(item['procurement_state'] == 'non acheté' and not item['hardware_verified'],
                'Fixture purchase/physical status must remain unverified')
    covered = {mid for item in supplements for mid in item['covers_missing_ids']}
    covered |= {item['missing_id'] for item in data['existing_lot_uses']}
    require(covered == {f'M{i:02d}' for i in range(1, 10)}, 'Missing fixture not covered')
    require(all(item['additional_cost_eur'] == 0
                and set(item['reference_slugs']) <= slugs for item in data['existing_lot_uses']),
            'Existing fixture supplies must reference already budgeted lots')
    extra_total = amount(supplements)
    active_total = amount(components) + extra_total
    expected = {
        'main_components_eur': amount(c for c in components if c['category'] == 'principal'),
        'base_supplies_eur': amount(c for c in components if c['category'] == 'fourniture'),
        'supplies_eur': amount(c for c in components if c['category'] == 'fourniture') + extra_total,
        'assembly_supplements_eur': extra_total,
        'material_without_lighting_eur': active_total,
        'reference_material_total_eur': amount(components),
        'conditional_lots_eur': amount(conditional),
        'base_subtotal_before_conditional_lots_eur': amount(c for c in components if not c['conditional']),
        'subtotal_before_conditional_lots_eur': active_total - amount(conditional),
        'amazon_material_eur': amount(c for c in components if c not in outside) + extra_total,
        'outside_amazon_pi_eur': amount(outside),
        'excess_eur': active_total - Decimal(str(budget['ceiling_eur'])),
    }
    for key, value in expected.items():
        require(Decimal(str(budget[key])) == value, f'Budget {key}: incorrect total')
    require(budget['ceiling_met'] == (active_total <= Decimal(str(budget['ceiling_eur']))),
            'Budget ceiling status differs from total')
    purchase_text = (ROOT/'Sources/listeAchat-avant-puissance.md').read_text(encoding='utf8')
    rows = re.findall(r'^\| \[.*?\]\[achat-\d+\] \| ([\d,]+) € \|$', purchase_text, re.M)
    require([Decimal(price.replace(',', '.')) for price in rows]
            == [Decimal(str(c['total_eur'])) for c in components],
            'Purchase Markdown prices differ from achats.json')
    fixture_rows = re.findall(r'^\| \[.*?\]\[fix-\d+\] \| .*? \| ([\d,]+) € \|$',
                              purchase_text, re.M)
    require([Decimal(price.replace(',', '.')) for price in fixture_rows]
            == [Decimal(str(c['total_eur'])) for c in supplements],
            'Purchase Markdown fixture prices differ from achats.json')
    require(Decimal(str(fixture_sources['additional_cost_eur'])) == extra_total
            and Decimal(str(fixture_sources['total_material_eur'])) == active_total,
            'Fixture price evidence total differs from active budget')
    current = data['active_components']
    power_sources = json.loads((ROOT/'Sources/motorisation-puissance.json').read_text())
    removed = set(data['removed_from_active'])
    expected_active = [dict(c) for c in components if c['slug'] not in removed] + supplements
    expected_active += power_sources['products']
    require({c['slug'] for c in current} == {c['slug'] for c in expected_active}
            and len(current) == len({c['slug'] for c in current}),
            'Active purchase coverage differs or contains duplicate lots')
    for item in current:
        expected_item = next(c for c in expected_active if c['slug'] == item['slug'])
        for key in ['asin', 'purchase_url', 'lot_price_eur', 'order_lots', 'total_eur']:
            require(item[key] == expected_item[key], f'{item["slug"]}: active {key} differs')
        require(Decimal(str(item['lot_price_eur'])) * item['order_lots']
                == Decimal(str(item['total_eur'])), 'Active lot total incorrect')
        require(item['procurement_state'] == 'non acheté' and not item['conditional'],
                'Active procurement status incorrect')
        require((ROOT/item['component_file']).exists(), 'Active component sheet missing')
    for item in power_sources['products']:
        path = ROOT/'Composants'/item['slug']/'sources.json'
        require(json.loads(path.read_text()) == item, 'Power component evidence differs')
    require(not power_sources['orders_placed'] and not power_sources['selection_complete'],
            'Unconfirmed power design must not be represented as purchased or fully qualified')
    current_outside = [c for c in current if urlparse(c['purchase_url']).hostname != 'www.amazon.fr']
    require(len(current_outside) == 1 and current_outside[0]['slug'] == 'raspberry-pi-zero-2-w',
            'Only the active Pi purchase may be outside Amazon')
    current_total = amount(current)
    current_budget = data['budget']
    for key, value in {
        'material_without_lighting_eur': current_total,
        'amazon_material_eur': current_total - amount(current_outside),
        'outside_amazon_pi_eur': amount(current_outside),
        'excess_eur': current_total - Decimal(str(current_budget['ceiling_eur'])),
        'previous_total_eur': active_total,
        'removed_lots_eur': amount(c for c in components if c['slug'] in removed),
        'new_lots_eur': amount(power_sources['products']),
        'increase_eur': current_total - active_total,
        'main_components_eur': amount(c for c in current if c['category'] == 'principal'),
        'supplies_eur': amount(c for c in current if c['category'] == 'fourniture'),
    }.items():
        require(Decimal(str(current_budget[key])) == value, f'Active budget {key} differs')
    require(current_budget['ceiling_met'] == (current_total <= Decimal('150')),
            'Active ceiling status incorrect')
    current_rows = re.findall(r'^\| \[.*?\]\[actif-\d+\] \| ([\d,]+) € \|$',
                             (ROOT/'listeAchat.md').read_text(), re.M)
    require([Decimal(p.replace(',', '.')) for p in current_rows]
            == [Decimal(str(c['total_eur'])) for c in current], 'Active Markdown prices differ')
    power_profile = json.loads((ROOT/'Logiciel/config/robot.puissance.example.json').read_text())
    require(power_profile['driver'] == 'md13s' and power_profile['hardware_confirmed'] is False
            and power_profile['pins'] == {'left_pwm': 17, 'left_dir': 27,
                                          'right_pwm': 22, 'right_dir': 23},
            'Power profile differs from MD13S wiring or falsely confirms hardware')
    power_prediction = json.loads((ROOT/'Validation/resultats/performance-puissance.json').read_text())
    require(not power_prediction['hardware_verified'], 'Power predictions are not physical tests')
    for source in power_prediction['sources']:
        require(hashlib.sha256((ROOT/source['file']).read_bytes()).hexdigest() == source['sha256'],
                'Power prediction input changed; recalculate')
    for script in list((ROOT/'tools').rglob('*.py')) + list((ROOT/'Logiciel').rglob('*.py')):
        if not is_project_file(script):
            continue
        ast.parse(script.read_text(encoding='utf8'), filename=str(script))
    config = json.loads((ROOT/'Logiciel/config/robot.example.json').read_text(encoding='utf8'))
    require(config['hardware_confirmed'] is False, 'Example GPIO must stay unconfirmed')
    require(config['pins'] == {'left_forward': 17, 'left_reverse': 27,
                              'right_forward': 22, 'right_reverse': 23, 'sleep': 24},
            'Example GPIO differs from documented wiring')
    cad_report = json.loads((ROOT/'Validation/resultats/modeles-step.json').read_text(encoding='utf8'))
    cad_records = {record['slug']: record for record in cad_report['models']}
    expected_steps = {f'Composants/{slug}/{slug}.step' for slug in slugs}
    actual_steps = {str(path.relative_to(ROOT)) for path in ROOT.rglob('*.step')
                    if is_project_file(path)}
    require(set(cad_records) == slugs and cad_report['count'] == 19,
            'STEP report must cover all 19 component folders')
    expected_assemblies = {'Assemblage/drone-v2.step', 'Assemblage/atelier-v2.step'}
    require(actual_steps == expected_steps | expected_assemblies,
            'Expected 19 component STEP files and the two assembly views')
    require(cad_report['unit'] == 'mm' and not cad_report['hardware_measured'],
            'STEP models must remain millimetre placement models without physical validation')
    require(cad_report['visual_review']['status'] == 'terminée'
            and cad_report['visual_review']['count'] == 19, 'STEP visual review incomplete')
    for slug in slugs:
        record = cad_records[slug]
        path = ROOT/record['file']
        require(record['file'] == f'Composants/{slug}/{slug}.step', f'{slug}: STEP path differs')
        meta = json.loads((ROOT/record['metadata_file']).read_text(encoding='utf8'))
        require(meta['unit'] == 'mm' and not meta['hardware_measured']
                and not meta['vendor_native_cad'], f'{slug}: misleading CAD provenance')
        require(meta['additional_assumptions'] and meta['representation'],
                f'{slug}: missing CAD assumptions / representation')
        require(meta['validation'] == record['validation'], f'{slug}: CAD validation differs')
        require(record['validation']['reimport_valid']
                and record['validation']['all_solids_valid']
                and record['validation']['solids'] > 0
                and record['validation']['relative_volume_error'] < 1e-7
                and record['validation']['bbox_error_mm'] < 1e-5,
                f'{slug}: invalid CAD import report')
        require(path.is_file(), f'{slug}: STEP file missing')
        if path.is_file():
            require(hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256']
                    == meta['sha256'], f'{slug}: STEP changed after validation')
            step_text = path.read_text(encoding='utf8')
            require(step_text.startswith('ISO-10303-21;')
                    and step_text.rstrip().endswith('END-ISO-10303-21;')
                    and 'MANIFOLD_SOLID_BREP' in step_text
                    and 'SI_UNIT(.MILLI.,.METRE.)' in step_text,
                    f'{slug}: incomplete STEP / incorrect unit')
        for source in meta['sources'] + [meta['preview']]:
            source_path = (ROOT/source['file']).resolve()
            require(source_path.is_relative_to(ROOT) and source_path.is_file(),
                    f'{slug}: CAD source missing or outside project')
            if source_path.is_relative_to(ROOT) and source_path.is_file():
                require(hashlib.sha256(source_path.read_bytes()).hexdigest() == source['sha256'],
                        f'{slug}: CAD input or preview changed; regenerate model')
    assembly = json.loads((ROOT/'Assemblage/verification.json').read_text(encoding='utf8'))
    require(not assembly['hardware_measured'], 'CAD assembly is not physically measured')
    coverage = assembly['coverage']
    require(set(coverage['onboard']) | set(coverage['offboard']) == slugs
            and not set(coverage['onboard']) & set(coverage['offboard'])
            and len(coverage['onboard']) == 13 and len(coverage['offboard']) == 6
            and coverage['reference_lots'] == 19, 'Assembly must account for all 19 lots')
    require(assembly['collisions']['interferences'] == [], 'Unresolved assembly interference')
    require(assembly['optical_clearance']['obstructions'] == [], 'Camera field obstructed')
    require(assembly['visual_review']['status'] == 'terminée'
            and assembly['visual_review']['count'] == 5, 'Assembly visual review incomplete')
    for key, filename in [('robot','Assemblage/drone-v2.step'),
                          ('workshop','Assemblage/atelier-v2.step')]:
        record = assembly[key]
        require(record['file'] == filename and record['unit'] == 'mm',
                f'{key}: incorrect assembly path / unit')
        require(record['reimport_valid'] and record['named_assembly_reimport_valid']
                and record['solids'] >= record['named_parts'] > 0
                and record['relative_volume_error'] < 1e-7
                and record['bbox_error_mm'] < 1e-5, f'{key}: assembly reimport failed')
        require((ROOT/filename).is_file(), f'{key}: assembly missing')
        if (ROOT/filename).is_file():
            require(hashlib.sha256((ROOT/filename).read_bytes()).hexdigest() == record['sha256'],
                    f'{key}: assembly changed after validation')
    require(len(assembly['sources']) == 19 and len(assembly['previews']) == 5,
            'Expected 19 assembly sources and 5 rendered views')
    sources = (assembly['sources'] + assembly['generator_sources']
               + assembly['additional_sources'] + assembly['previews'])
    for source in sources:
        path = (ROOT/source['file']).resolve()
        require(path.is_relative_to(ROOT) and path.is_file(), 'Assembly source missing')
        if path.is_relative_to(ROOT) and path.is_file():
            require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'],
                    f'Assembly source or preview changed: {source["file"]}')
        if 'metadata_file' in source:
            require(hashlib.sha256((ROOT/source['metadata_file']).read_bytes()).hexdigest()
                    == source['metadata_sha256'], 'Assembly component metadata changed')
    extras = json.loads((ROOT/'Assemblage/composants-manquants.json').read_text(encoding='utf8'))
    require(not extras['hardware_verified'] and extras['additional_cost_eur'] is None
            and extras['final_budget_eur'] is None and not extras['included_in_V5_budget'],
            'Unpriced assembly extras must not be represented as purchased or budgeted')
    require(len(extras['items']) == 9 and all(item['unit_price_eur'] is None
            and item['procurement_state'] == 'non acheté' for item in extras['items']),
            'Expected nine proposed fixture types, without invented prices or purchases')
    # Historical geometric BOM remains intact; current procurement is in achats.json.
    performance = json.loads((ROOT/'Validation/resultats/performance.json').read_text())
    require(not performance['hardware_verified'], 'Performance predictions are not physical tests')
    for source in performance['sources']:
        path = (ROOT/source['file']).resolve()
        require(path.is_relative_to(ROOT) and path.is_file(), 'Performance input missing')
        if path.is_relative_to(ROOT) and path.is_file():
            require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'],
                    'Performance input changed; recalculate')
    assumed = json.loads((ROOT/'Mecanique/hypotheses-performance.json').read_text())
    require(not assumed['hardware_measured'] and assumed['configured_max_duty'] == config['max_duty'],
            'Performance must use current duty and keep assumptions unmeasured')
    if errors:
        print('\n'.join(errors))
        return 1
    print(f'OK : {len(pages)} documents Markdown, liens locaux, tableaux et syntaxe Python.')
    print('OK : 19 lots issus de V5, provenance, fiches et sources JSON cohérentes.')
    print('OK : Pi seul hors Amazon ; compléments historiques archivés ; pas de PCB sur mesure.')
    print(f'OK : archive 257,03 € ; panier actif {current_total} €, plafond 150 € non atteint.')
    print('OK : 19 PDF, sélection des galeries et empreintes des documents sources.')
    print('OK : 19 STEP en mm, hypothèses, sources, réimport CAO et aperçu de chaque modèle.')
    print('OK : robot et atelier STEP, 19 lots couverts, 5 vues, interférences et champ caméra.')
    print('OK : hypothèses de performance, sources et limite PWM cohérentes ; aucun essai physique.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(check())
    except (KeyError, ValueError, OSError, TypeError) as error:
        print(f'Échec de vérification : {error}', file=sys.stderr)
        sys.exit(1)
