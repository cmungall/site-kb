"""Resolve shared definitions without inventing site observations from profiles."""
from copy import deepcopy
from pathlib import Path
import yaml


def read_catalog(directory: Path) -> dict:
    definitions = {}
    for path in sorted(directory.glob('*.yaml')):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict) or set(data) != {'variable_definitions'}:
            raise ValueError(f'{path}: expected variable_definitions')
        for definition in data['variable_definitions']:
            identifier = definition.get('id')
            if not identifier or not definition.get('name') or identifier in definitions:
                raise ValueError(f'{path}: missing identity/name or duplicate variable {identifier}')
            definitions[identifier] = definition
    return definitions


def resolve(declaration: dict, definitions: dict) -> dict:
    """Expand identity fields; preserve local provenance and study context."""
    identifier = declaration.get('variable_id')
    if not identifier:
        if not declaration.get('name'):
            raise ValueError('Variable requires a name or variable_id')
        return deepcopy(declaration)
    if identifier not in definitions:
        raise ValueError(f'Unknown variable_id: {identifier}')
    result = deepcopy(definitions[identifier])
    result.pop('id')
    for key, value in declaration.items():
        if key in ('source_variables', 'mappings'):
            result.setdefault(key, [])
            result[key].extend(deepcopy(v) for v in value if v not in result[key])
        elif key in result and result[key] != value:
            raise ValueError(f'{identifier}: declaration conflicts with shared {key}')
        else:
            result[key] = deepcopy(value)
    return result


def read_profiles(directory: Path, definitions: dict) -> list:
    profiles = []
    for path in sorted(directory.glob('*.yaml')):
        data = yaml.safe_load(path.read_text())
        if not isinstance(data, dict) or set(data) != {'profiles'}:
            raise ValueError(f'{path}: expected profiles')
        for profile in data['profiles']:
            for candidate in profile.get('candidates', []):
                identifier = candidate.get('variable_id')
                if identifier not in definitions:
                    raise ValueError(f'{path}: unknown candidate variable_id {identifier}')
            profiles.append(profile)
    return profiles
