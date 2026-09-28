from site_kb.scripts.bervo_view import build_bervo_view
from site_kb.scripts.render_site import term


def test_bervo_index_retains_broader_relation_and_does_not_create_observations():
    target = {'id': 'BERVO:8000133', 'label': 'Temperature'}
    candidate = {'id': 'site_kb:water-temp', 'name': 'Water temperature',
                 'mappings': [{'target': target, 'relation': 'BROAD'}]}
    data = {'variable_definitions': [candidate, {'id': 'site_kb:arg', 'name': 'ARG abundance'}],
            'sites': [{'id': 'site_kb:s', 'name': 'Site'}]}
    result = build_bervo_view(data)
    assert result['summary']['mapped_catalog_definition_count'] == 1
    assert result['summary']['mapped_site_declaration_count'] == 0
    assert result['groups'][0]['definitions'][0]['relation'] == 'BROAD'
    assert result['groups'][0]['site_declarations'] == []
    assert result['unmapped_catalog_definitions'] == [{'id': 'site_kb:arg', 'name': 'ARG abundance'}]
    assert 'variables' not in data['sites'][0]


def test_bervo_links_follow_upstream_w3id_namespace():
    html = term({'id': 'BERVO:8000133', 'label': 'Temperature'})
    assert 'https://w3id.org/bervo/BERVO_8000133' in html
    assert 'purl.obolibrary.org' not in html
