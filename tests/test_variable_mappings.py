"""Crosswalks are attributed assertions; ingestion must not invent equivalence."""
from copy import deepcopy
import yaml
import pytest

from site_kb.scripts.build_db import assemble
from site_kb.scripts.variable_mappings import read_mappings


def example_mapping():
    # Intentionally synthetic BERVO target: tests exercise structure, not ontology truth.
    return {'source': 'DEIMS', 'source_id': 'http://example.org/property',
            'source_name': 'Original label',
            'target': {'id': 'BERVO:9999999', 'label': 'Synthetic test concept'},
            'relation': 'BROAD', 'origin': 'CURATED',
            'evidence': ['https://example.org/review/1'], 'attributed_to': 'Test curator'}


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data))


def test_shared_crosswalk_survives_refresh_and_preserves_source_assertions(tmp_path):
    imported, curated = tmp_path / 'imported', tmp_path / 'curated'
    upstream = {**example_mapping(), 'origin': 'SOURCE', 'relation': 'CLOSE'}
    variable = {'name': 'Original label', 'declaration_kind': 'UNSPECIFIED',
                'source_variables': [{'source': 'DEIMS', 'source_id': 'http://example.org/property', 'source_name': 'Original label'}],
                'mappings': [upstream]}
    records = [{'id': 'site_kb:a', 'name': 'A', 'variables': [deepcopy(variable)]},
               {'id': 'site_kb:b', 'name': 'B', 'variables': [deepcopy(variable)]}]
    write(imported / 'sites.yaml', {'sites': records})
    write(curated / 'variable_mappings/test.yaml', {'mappings': [example_mapping()]})
    for name in ['Original label', 'Refreshed upstream label']:
        records[0]['variables'][0]['source_variables'][0]['source_name'] = name
        write(imported / 'sites.yaml', {'sites': records})
        result = assemble(imported, curated)
        for site in result['sites']:
            v = site['variables'][0]
            assert v['mappings'] == [upstream, example_mapping()]
            assert 'term' not in v
            assert v['declaration_kind'] == 'UNSPECIFIED'
        assert result['sites'][0]['variables'][0]['source_variables'][0]['source_name'] == name
    write(curated / 'overrides/a.yaml', {'sites': [{'id': 'site_kb:a', 'variables': [{'name': 'Site-specific declaration'}]}]})
    assert assemble(imported, curated)['sites'][0]['variables'] == [{'name': 'Site-specific declaration'}]


def test_mapping_match_requires_both_source_and_id(tmp_path):
    imported, curated = tmp_path / 'imported', tmp_path / 'curated'
    write(imported / 'a.yaml', {'sites': [{'id': 'site_kb:a', 'name': 'A', 'variables': [
        {'name': 'x', 'source_variables': [{'source': 'NEON', 'source_id': 'http://example.org/property', 'source_name': 'x'}]}]}]})
    write(curated / 'variable_mappings/test.yaml', {'mappings': [example_mapping()]})
    assert 'mappings' not in assemble(imported, curated)['sites'][0]['variables'][0]


@pytest.mark.parametrize('field,value', [('evidence', []), ('relation', 'SAME'), ('origin', 'GUESSED'), ('source_id', None)])
def test_invalid_crosswalk_rejected(tmp_path, field, value):
    mapping = example_mapping()
    mapping[field] = value
    write(tmp_path / 'test.yaml', {'mappings': [mapping]})
    with pytest.raises(ValueError):
        read_mappings(tmp_path)


def test_conflicting_relations_in_same_mapping_origin_rejected(tmp_path):
    write(tmp_path / 'test.yaml', {'mappings': [example_mapping(), {**example_mapping(), 'relation': 'EXACT'}]})
    with pytest.raises(ValueError, match='conflicting'):
        read_mappings(tmp_path)


@pytest.fixture(scope='module')
def mapping_schema():
    import json
    from pathlib import Path
    from linkml.generators.jsonschemagen import JsonSchemaGenerator
    schema = Path(__file__).parents[1] / 'src/site_kb/schema/site_kb.yaml'
    return json.loads(JsonSchemaGenerator(str(schema), top_class='VariableMappingCollection').serialize())


def test_schema_accepts_attributed_source_and_curated_crosswalks(mapping_schema):
    import jsonschema
    jsonschema.validate({'mappings': [example_mapping(), {**example_mapping(), 'origin': 'SOURCE', 'relation': 'CLOSE'}]}, mapping_schema)


def test_schema_requires_evidence_and_valid_relation(mapping_schema):
    import jsonschema
    for edit in ({'evidence': []}, {'relation': 'SAME'}, {'target': {'id': 'BERVO:9999999'}}):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate({'mappings': [{**example_mapping(), **edit}]}, mapping_schema)
