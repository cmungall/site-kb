# BERVO integration

Implemented 2026-09-23 after inspecting `~/repos/nmdc-sfas-brcs` at commit
`11492b0f0f173f57ef79390eb121f6af96d0e439`.

## Patterns reused

The reference project represents BERVO annotations as identifier/label objects,
preserves mapping predicates and notes in its SSSOM/profile pipeline, validates
terms with linkml-term-validator, and generates a grouped BERVO variable index
that also identifies unmapped variables. The relevant implementations are
`schemas/generate_profiles.py` (`slot_mappings`), `schemas/generate_variables.py`
(`build_variable_view`), and its OAK validator configuration.

Site KB already has attributed crosswalks with EXACT, CLOSE, BROAD, NARROW and
RELATED relations. Those remain the source of truth; a second `bervo_term` field
and a duplicate SSSOM authoring layer were not needed. Unlike the reference
project's default predicate selection, each crosswalk here explicitly names its
relation. Term existence does not establish mapping correctness.

## Reproducible ontology source

BERVO is pinned to upstream commit
`23b551635d42614ec09a5670866d714007039011`, reporting release `2026-09-03`:

https://github.com/bioepic-data/bervo/blob/23b551635d42614ec09a5670866d714007039011/bervo.obo

`prepare_term_sources.py` verifies its SHA-256 and normalizes the OBO serialization
from `bervo:BERVO_…` to `BERVO:…` for the local OAK adapter. This preserves labels,
definitions and hierarchy; validation never derives labels from the mappings it
is checking. The schema and browser use the actual term IRI namespace
`https://w3id.org/bervo/BERVO_`. The reference project's June label cache contains
older capitalization, so its labels were not copied into the current mappings.
The source URL/checksum is recorded in `cache/ontologies/sources.json`.

## First reviewed crosswalk set

`db/curated/variable_mappings/bervo.yaml` contains 17 assertions:

- Six local catalog definitions: pH, conductivity, salinity and turbidity have
  exact property mappings; water/treatment temperature maps to broader Temperature.
- Three MIxS source fields: `ph`, `temp` and `salinity` map to the corresponding
  properties. Their original MIxS term identifiers and submission constraints are
  preserved. Candidate fields remain separate from site observations.
- Eight DEIMS/EnvThes declarations: air temperature, soil pH, soil temperature,
  water temperature, lake temperature, conductivity, water salinity and specific
  conductivity. Live EnvThes definitions could not be retrieved, so the mappings
  explicitly record that limitation. Five are provisional CLOSE matches based on
  preserved source labels and target definitions; the three aquatic-context
  matches use BROAD. No DEIMS exact equivalence is asserted.

`source: site-kb` plus a catalog `source_id` targets a local definition directly,
without adding fabricated upstream identities to `source_variables`. Mapping
assertions propagate to site references. Four exact Moroccan chemistry matches
also have explicitly curated primary BERVO terms; applying a crosswalk never
chooses or overwrites a primary term automatically.

Wastewater COD/BOD, hydraulic/sludge retention times, filtered nutrient quantities
and sequence-derived resistome/phage metrics remain unmapped in this pass.
A chemical entity such as nitrate is not interchangeable with its concentration,
and soil-specific model variables are not generic wastewater measurements.

## Browser and validation

The Variables & profiles page groups catalog definitions and site declarations
by BERVO target, retaining each mapping relation. Broader-group membership does
not make two variables equivalent. `data/bervo.json` exports the same view with
coverage counts and unmapped catalog definitions. Site counts are counts of
recorded declarations, not independent samples or harmonized numerical values.

The standard `just site` pipeline checks the schema, profiles, crosswalk file,
and assembled data with linkml-term-validator. Regression tests cover local-ID
mapping inheritance, relation-preserving grouping, the w3id links, and deliberate
rejection of an incorrect BERVO label by the validator.
