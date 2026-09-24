# MIxS candidates for wastewater treatment sites

Reviewed 2026-09-23 against MIxS 7.0.1, commit
`0bc3c221b4a368ed7939d9a1fe4cbd8f407a221b`. The machine-readable
[candidate profiles](../../db/profiles/wastewater_sludge.yaml) preserve source
fields, IDs, definitions, ranges, cardinality flags, and preferred-unit annotations.
They are **not evidence of measurements at ROPEC**.

## Which extensions apply?

- **WastewaterSludge** is the primary environmental extension for wastewater and
  sludge samples. Its 40 explicitly listed fields include measurements, process
  descriptions, and sample/study metadata. Our profile captures those fields;
  it is not a complete MIxS checklist or submission schema.
- **Water** supplies useful additional aqueous chemistry metadata. We selected
  eight supplemental candidates: ammonium, nitrite, dissolved oxygen, conductivity,
  redox potential, dissolved organic carbon, organic carbon, and dissolved inorganic
  nitrogen. Suitability depends on the actual influent, effluent, or receiving-water
  sample and measurement definition.
- **Sediment** is relevant to receiving-water sediment studies. It should not be
  used to assert that treatment sludge is sediment.
- **BuiltEnvironment** is relevant to surfaces and indoor environments within a
  facility, rather than a replacement for wastewater/sludge metadata.

The supplied name `WastewaterSludgeInterface` is not a class in the reviewed MIxS
source. The environmental extension is `WastewaterSludge`; an interface name may
come from a generated or downstream submission schema. Keep that schema/version
separate from the MIxS identity.

Sources: [WastewaterSludge](https://genomicsstandardsconsortium.github.io/mixs/0016013/),
[Water](https://genomicsstandardsconsortium.github.io/mixs/0016014/),
[Sediment](https://genomicsstandardsconsortium.github.io/mixs/0016011/),
[BuiltEnvironment](https://genomicsstandardsconsortium.github.io/mixs/0016001/),
and the [pinned source schema](https://github.com/GenomicsStandardsConsortium/mixs/blob/0bc3c221b4a368ed7939d9a1fe4cbd8f407a221b/src/mixs/schema/mixs.yaml).

## Priorities for treatment-plant curation

| Area | Candidate fields | Interpretation |
| --- | --- | --- |
| Treatment performance | `biochem_oxygen_dem`, `chem_oxygen_dem`, `efficiency_percent` | BOD, COD, and digester volatile-solids removal are distinct measurements. |
| Solids and residence time | `suspend_solids`, `sludge_retent_time`, `inorg_particles`, `org_particles` | Preserve sample stage, matrix, and analytical method. Sludge residence time is not hydraulic residence time. |
| Nutrients and chemistry | `nitrate`, `phosphate`, `tot_nitro`, `tot_phosphate`, `ph`, `alkalinity`, `temp`, `salinity`, `sodium` | Retain analyte distinctions; do not silently equate total phosphate with total phosphorus. |
| Process and facility context | `pre_treatment`, `primary_treatment`, `secondary_treatment`, `tertiary_treatment`, `reactor_type` | These describe treatment processes/equipment rather than concentrations. |
| Influent origin | `sewage_type`, `wastewater_type`, `indust_eff_percent` | Facility/wastewater categories and industrial fraction; not removal efficiency. |
| Sample handling | `samp_store_dur`, `samp_store_temp`, `samp_store_loc`, `samp_vol_we_dna_ext` | Metadata about the sample and extraction, not permanent site attributes. |

A useful future observation model should attach measured values to sampling point
(influent, primary sludge, reactor, effluent), matrix, time, method, unit, and source.
The current variable declarations describe what is reported as observed; they are
not a time-series observation schema.

## The efficiency example needs an explicit unit caveat

`efficiency_percent` has ID **MIXS:0000657**. It specifically concerns the percentage
of volatile solids removed in an anaerobic digester. The reviewed extension makes
it optional and single-valued, with a string range and a structured value/unit
pattern. That string range describes submission encoding, not the physical
quantity's data type or sampling frequency.

The source's `Preferred_unit` is **micromole per liter**, inconsistent with its
percentage definition. The profile preserves that annotation as source evidence,
flags the inconsistency, and assigns no normalized unit or BERVO equivalence.
Resolve the upstream issue before treating the annotation as a canonical unit.
[Source term page](https://genomicsstandardsconsortium.github.io/mixs/0000657/).

The pinned RDF uses `rdfs:label = efficiency_percent`; the human-facing title is
“efficiency percent.” Candidate `OntologyTerm.label` follows the canonical RDF
label so term validation checks a real, independently retrieved source. The
correct MIxS namespace is `https://w3id.org/mixs/`, not an OBO-style `MIXS_` PURL.

## High-level ENVO classification

Previously the schema had ecosystem annotations and network-specific free-text
site types, but no high-level ontology classification of the record. `Site.site_type`
now represents the kind of physical facility/site. ROPEC is annotated as
**ENVO:00002043 — wastewater treatment plant**, independently of `ecosystem_terms`.
The term is validated against ENVO release 2026-06-26.

Observation is a role a treatment plant can also serve; these are not necessarily
mutually exclusive kinds. Do not classify every DEIMS or NEON entry as a built
research station merely because research happens there. Finer habitat/ecosystem
annotations remain in `ecosystem_terms`; sample material belongs with sample
metadata, not as the physical facility's type.
[ENVO release](https://github.com/EnvironmentOntology/envo/releases/tag/v2026-06-26).

## Term validation

All `OntologyTerm`-valued fields now have explicit bindings so
`linkml-term-validator` checks both existence and labels, including nested mapping
targets and candidate profiles. Earlier invocations without those bindings could
succeed without inspecting nested IDs/labels. Regression tests verify rejection of
wrong IDs and wrong labels.

`just validate-terms` prepares pinned, checksum-verified ENVO, MIxS, and SKOS sources.
The SQLite download endpoint was unavailable in this environment; ENVO uses its
upstream OBO release, while MIxS and SKOS use reproducible label indexes projected
from upstream RDF. Those indexes validate identities and labels, not hierarchy,
scientific equivalence, or unit consistency. They are generated from the source
standards, never from the candidate annotations being validated.

`just site` and the Pages workflow now run term validation as well as structural
validation. The standing rule is recorded in `AGENTS.md`. Source-variable labels
remain verbatim provenance rather than canonical-label assertions.
