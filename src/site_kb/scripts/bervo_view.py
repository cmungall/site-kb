"""A BERVO browsing index, retaining mapping relationships and measurement scope."""


def assertions(variable):
    result = [m for m in variable.get('mappings', []) if m['target']['id'].startswith('BERVO:')]
    primary = variable.get('term', {})
    if primary.get('id', '').startswith('BERVO:') and not any(m['target']['id'] == primary['id'] for m in result):
        result = result + [{'target': primary, 'relation': 'PRIMARY'}]
    return result


def build_bervo_view(collection):
    groups = {}
    unmapped = []
    mapped_declarations = 0
    declaration_count = 0

    def group(mapping):
        target = mapping['target']
        return groups.setdefault(target['id'], {'term': target, 'definitions': [], 'site_declarations': []})

    for definition in collection.get('variable_definitions', []):
        mappings = assertions(definition)
        if not mappings:
            unmapped.append({'id': definition['id'], 'name': definition['name']})
        for mapping in mappings:
            entry = {'id': definition['id'], 'name': definition['name'], 'relation': mapping['relation']}
            if entry not in group(mapping)['definitions']:
                group(mapping)['definitions'].append(entry)
    for site in collection['sites']:
        for index, variable in enumerate(site.get('variables', [])):
            declaration_count += 1
            mappings = assertions(variable)
            mapped_declarations += bool(mappings)
            for mapping in mappings:
                entry = {'site_id': site['id'], 'site_name': site['name'], 'variable_name': variable['name'],
                         'declaration_index': index, 'relation': mapping['relation']}
                if entry not in group(mapping)['site_declarations']:
                    group(mapping)['site_declarations'].append(entry)
    count = len(collection.get('variable_definitions', []))
    return {'summary': {'catalog_definition_count': count, 'mapped_catalog_definition_count': count - len(unmapped),
                        'site_declaration_count': declaration_count, 'mapped_site_declaration_count': mapped_declarations,
                        'bervo_term_count': len(groups)},
            'groups': sorted(groups.values(), key=lambda g: g['term']['label'].casefold()),
            'unmapped_catalog_definitions': sorted(unmapped, key=lambda v: v['name'].casefold())}
