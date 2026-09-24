# DEIMS JSON and observed-property investigation

Reviewed 2026-09-22. The findings below describe the original investigation.
Implementation update: DEIMS properties and WKT coordinates are now ingested;
source identities/provenance and directed crosswalk assertions have separate
schema fields. See the repository README for the implemented pipeline.
The [machine-readable coverage audit](deims-api-audit.json) lists the 50 existing
DEIMS records checked, their API URLs, source modification timestamps, and counts.

## Main finding

The existing importer already downloads the rich JSON from
`https://deims.org/api/sites/{UUID}` but ignores
`attributes.focusDesignScale.observedProperties`.

Across all **50 currently imported DEIMS sites**, live responses contained:

- **47 sites** with observed-property entries;
- **1,113 site–property assignments**, representing **248 distinct URIs**;
- no missing labels or URIs among these assignments;
- three empty lists: Estacion Biologica Palo Verde, Las Cruces Biological
  Station, and Estacion Biologica La Selva, all in Costa Rica.

These are metadata declarations, not counts of available time series or guaranteed
current monitoring. This audit is not a survey of the entire DEIMS registry.

| Existing site | Observed-property entries |
| --- | ---: |
| Dinghu Mountain Research of Forest Ecosystem | 169 |
| Yucheng Comprehensive Experiment Station | 154 |
| LTSER-Sabor | 72 |
| Huitong Research Station of Forest Ecosystem | 71 |
| Shennongjia Biodiversity Research Station | 58 |
| Ailao Mountain Research Station | 6 |

For example, [Selhausen's JSON](https://deims.org/api/sites/0a006b69-5134-4c0a-864c-f86c0c61288f)
contains this observed-property object:

```json
{
  "label": "soil heat flux",
  "uri": "http://vocabs.lter-europe.net/EnvThes/22253"
}
```

The same list also includes broad categories such as soil parameter and biological
parameter. Ailao's six entries are broad parameter groups. The
[DEIMS metadata model](https://deims.org/models/?id=site) explicitly describes both
parameters and parameter groups. Do not present every entry as a distinct,
fully specified measurable variable.

## Implications for harmonization

DEIMS already supplies controlled-vocabulary identities through EnvThes. Preserve
those source URIs and labels first; a name-matching step is unnecessary for exact
within-DEIMS identity. Equal URIs establish a shared vocabulary concept, not equal
sampling methods, matrices, units, or interchangeable data series.

Recommended ingestion shape:

1. Preserve source observed-property declarations, their URI, site association,
   source JSON URL/path, and retrieval/source modification dates.
2. Distinguish broad parameter groups from specific properties using verified
   vocabulary metadata or an explicit curated classification. Do not classify
   solely by a label ending in “parameter.”
3. Retain EnvThes as the source vocabulary; use a curated crosswalk for BERVO,
   ENVO, or other preferred terms. Keep source identity separate from the target
   mapping, and distinguish exact, broad, and narrow matches.
4. Leave units, methods, and sampling intervals unset unless independently
   supported. Site-level observed-property objects only supply label and URI.

The current `Variable` class can hold the source URI in `network_variable_id` and
source terms in `additional_terms`, reserving `term` for the harmonized concept.
However, it has no explicit declaration kind (property versus group) or structured
per-claim provenance. Those should be represented before treating the complete
list as harmonized measurements. Alternatively, add a separate source
`observed_properties` collection and populate `variables` only through reviewed
mapping. This avoids making the UI's variable counts misleading.

## Other valuable JSON sections

| JSON path | Available information |
| --- | --- |
| `attributes.geographic` | WKT coordinates and boundaries, country, elevation, area |
| `attributes.general` | Status, establishment/closure years, aliases, related sites, photographs |
| `attributes.affiliation.networks` | Network identities, site codes, verification flags |
| `attributes.contact` | Site managers, operating organizations, ORCID/ROR where supplied |
| `attributes.environmentalCharacteristics` | Habitats, biome, climate summaries and units |
| `attributes.infrastructure` | Facilities, operational schedules, data policies |

A second importer bug emerged: all 50 inspected detail responses have WKT
`POINT (longitude latitude)` coordinates. Our coordinate parser only handles
comma-separated strings, lists, or dictionaries, and does not fall back to detail
coordinates. The API's OpenAPI example also uses WKT for site-list coordinates.
This explains why valid geographic metadata is missing from our imported records.
Climate summary values must not automatically become measured-variable declarations.

## Sensors and documentation drift

The [sensor JSON example](https://deims.org/api/sensors/588b4026-ea1f-4357-ad3e-fabdd7de382c)
works. It links to Obergurgl via `attributes.general.relatedSite` and lists air
humidity and air temperature under `attributes.observation.observedProperty`,
using `property` and `unitOfMeasurement` fields. Both units are `nA` in this
example; do not import that as a real unit. Some method and interval details are
in narrative text rather than structured fields. No related resources were
populated in the 50 site detail responses audited, so following site-level links
alone is not enough to discover all sensors.

The [export documentation](https://deims.org/docs/export.html) still mentions
`/api/datasets`. During this check, that endpoint returned HTTP 200 containing an
`errors` object with internal status 400 and a message that datasets is not a
valid resource type. The documentation's example dataset detail URL returned
404. The live [OpenAPI document](https://deims.org/api) lists sites, activities,
sensors, and individual locations, but not datasets. Validate JSON response shape
and API error payloads, not just HTTP status.

## Suggested implementation order

First fix WKT parsing and add source observed-property ingestion with retained
EnvThes identities and declaration granularity. Refresh the existing 50 records,
validate, and rebuild the browser. Then investigate the EnvThes hierarchy and
crosswalks, followed by sensor/activity enrichment. NEON ingestion remains a
separate task. The audit above does not change imported records or claim that
cross-vocabulary harmonization is already complete.
