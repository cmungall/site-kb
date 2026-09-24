"""Shared definitions never turn applicability into evidence of collection."""
import pytest
import yaml
from site_kb.scripts.build_db import assemble, build_database


def setup_catalog(tmp_path):
    imported, curated = tmp_path / 'imported', tmp_path / 'curated'
    imported.mkdir()
    (curated / 'variables').mkdir(parents=True)
    (tmp_path / 'profiles').mkdir()
    definition = {'id': 'site_kb:temperature', 'name': 'Temperature',
                  'source_variables': [{'source': 'Example', 'source_id': 'temp', 'source_name': 'Temp'}]}
    (curated / 'variables/example.yaml').write_text(yaml.safe_dump({'variable_definitions': [definition]}))
    (imported / 'example.yaml').write_text(yaml.safe_dump({'sites': [{'id': 'site_kb:example', 'name': 'Example'}]}))
    profile = {'name': 'Candidate profile', 'source_url': 'https://example.org/profile', 'source_version': '1',
               'candidates': [{'variable_id': definition['id'], 'source_slot': 'temp', 'category': 'measurement'}]}
    (tmp_path / 'profiles/example.yaml').write_text(yaml.safe_dump({'profiles': [profile]}))
    return imported, curated, definition


def test_profile_does_not_create_site_measurements(tmp_path):
    imported, curated, definition = setup_catalog(tmp_path)
    data = assemble(imported, curated)
    assert data['variable_definitions'] == [definition]
    assert 'variables' not in data['sites'][0]
    assert data['profiles'][0]['candidates'][0]['variable_id'] == definition['id']


def test_resolves_reference_and_preserves_local_evidence(tmp_path):
    imported, curated, definition = setup_catalog(tmp_path)
    path = imported / 'example.yaml'
    record = yaml.safe_load(path.read_text())
    local = {'variable_id': definition['id'], 'evidence': ['https://example.org/study'],
             'method': 'Probe', 'source_variables': [{'source': 'Study', 'source_name': 'water temp'}]}
    record['sites'][0]['variables'] = [local]
    path.write_text(yaml.safe_dump(record));before = path.read_bytes()
    data = assemble(imported, curated)
    variable = data['sites'][0]['variables'][0]
    assert variable['name'] == 'Temperature'
    assert variable['evidence'] == local['evidence']
    assert variable['source_variables'] == definition['source_variables'] + local['source_variables']
    assert data['variable_definitions'] == [definition]
    assert path.read_bytes() == before


@pytest.mark.parametrize('failure', ['site_reference', 'candidate_reference', 'conflicting_name', 'duplicate_definition'])
def test_invalid_catalog_build_preserves_output(tmp_path, failure):
    imported, curated, definition = setup_catalog(tmp_path)
    output = tmp_path / 'built.yaml'
    build_database(imported, curated, output);before = output.read_bytes()
    if failure == 'candidate_reference':
        path = tmp_path / 'profiles/example.yaml'
        path.write_text(path.read_text().replace('site_kb:temperature', 'site_kb:missing'))
    elif failure == 'duplicate_definition':
        (curated / 'variables/duplicate.yaml').write_text(yaml.safe_dump({'variable_definitions': [definition]}))
    else:
        path = imported / 'example.yaml';data = yaml.safe_load(path.read_text())
        variable = {'variable_id': 'site_kb:missing'} if failure == 'site_reference' else {'variable_id': definition['id'], 'name': 'Other'}
        data['sites'][0]['variables'] = [variable];path.write_text(yaml.safe_dump(data))
    with pytest.raises(ValueError):
        build_database(imported, curated, output)
    assert output.read_bytes() == before
