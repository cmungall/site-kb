"""Prepare pinned upstream sources for reproducible linkml-term-validator checks."""
from pathlib import Path
import hashlib
import json

import httpx
from rdflib import Graph, RDFS

CACHE = Path('cache/ontologies')
MIXS_COMMIT = '0bc3c221b4a368ed7939d9a1fe4cbd8f407a221b'
SOURCES = {
    'envo.obo': 'https://raw.githubusercontent.com/EnvironmentOntology/envo/v2026-06-26/envo.obo',
    'mixs.owl.ttl': f'https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/{MIXS_COMMIT}/project/owl/mixs.owl.ttl',
    'mixs.yaml': f'https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/{MIXS_COMMIT}/src/mixs/schema/mixs.yaml',
    'skos.rdf': 'https://www.w3.org/2009/08/skos-reference/skos.rdf',
}
CHECKSUMS = {
    'envo.obo': '7f5a6580d1b59166da07a54f9aa907a76f86079b7082e089192f04df91fd7d5b',
    'mixs.owl.ttl': '817d8993b54ffa256da2cc177322d48859557d3565834ae1e4ab165a1078b23e',
    'mixs.yaml': '4e7755dc52227d1c9f1abe7ebe2852054bcf8085edf997d6b85c54e59968c329',
    'skos.rdf': 'e79633b8d0564816cee8a99f5c9acf9a0e6fc7257c7209acd684ecad53a89dd6',
}


def prepare():
    CACHE.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for filename, url in SOURCES.items():
        destination = CACHE / filename
        if not destination.exists():
            response = httpx.get(url, follow_redirects=True, timeout=90)
            response.raise_for_status()
            destination.write_bytes(response.content)
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        if digest != CHECKSUMS[filename]:
            raise ValueError(f'Checksum mismatch for {destination}; inspect or remove the cache before retrying')
        manifest[filename] = {'url': url, 'sha256': digest}
    # MIxS terms are RDF properties as well as classes, with w3id rather than
    # OBO PURLs. A label-only OBO projection lets OAK validate both consistently.
    # Labels come from pinned upstream RDF, never from candidate data being checked.
    graph = Graph().parse(CACHE / 'mixs.owl.ttl', format='turtle')
    labels = sorted((str(subject).replace('https://w3id.org/mixs/', 'MIXS:'), str(label))
                    for subject, label in graph.subject_objects(RDFS.label)
                    if str(subject).startswith('https://w3id.org/mixs/'))
    lines = ['format-version: 1.2', 'ontology: mixs-labels', '']
    for identifier, label in labels:
        lines.extend(['[Term]', f'id: {identifier}', f'name: {label}', ''])
    (CACHE / 'mixs-labels.obo').write_text('\n'.join(lines))
    skos = Graph().parse(CACHE / 'skos.rdf', format='xml')
    skos_lines = ['format-version: 1.2', 'ontology: skos-labels', '']
    for subject, label in sorted(skos.subject_objects(RDFS.label)):
        if label.language == 'en' and str(subject).startswith('http://www.w3.org/2004/02/skos/core#'):
            identifier = str(subject).replace('http://www.w3.org/2004/02/skos/core#', 'skos:')
            skos_lines.extend(['[Term]', f'id: {identifier}', f'name: {label}', ''])
    (CACHE / 'skos-labels.obo').write_text('\n'.join(skos_lines))
    (CACHE / 'sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Prepared ENVO, SKOS, and {len(labels)} MIxS canonical labels from pinned upstream sources.')


if __name__ == '__main__':
    prepare()
