# Robert O. Pickard Environmental Centre (ROPEC)

Researched 2026-09-21. Site record: [wwtp_robert_o_pickard.yaml](../../db/curated/sites/wwtp_robert_o_pickard.yaml).

ROPEC is Ottawa's municipal wastewater treatment plant and a documented
environmental sampling site. “Ottawa wastewater treatment plant” refers here
to ROPEC; the Gatineau plant across the river is a separate facility, even when
both appear in the same study.

## Facility and treatment

The City dates the facility to 1962, originally named Green's Creek Pollution
Control Centre. Expansion in 1988–1993 introduced biological secondary
treatment; dechlorination was added in 2013. The site occupies 67 hectares in
eastern Ottawa and returns treated wastewater to the Ottawa River.
[City facility history](https://ottawa.ca/en/living-ottawa/drinking-water-stormwater-and-wastewater/wastewater-and-sewers/wastewater-collection-and-treatment/ottawas-wastewater-treatment-plant).

The address is 800 Green Creek Drive, Ottawa, Ontario, Canada.
[City address reference](https://app06.ottawa.ca/calendar/ottawa/citycouncil/pdc/2005/05-24/ACS2005-PWS-UTL-0017.htm).

Treatment comprises screening and grit removal, primary settling, biological
secondary treatment, iron-assisted phosphorus removal, and sodium-hypochlorite
disinfection. The City's performance table distinguishes **545 million L/day
average capacity** from **436 million L/day actual average flow in 2019**.
These are different quantities; 436 is not a verified present-day flow.
[City treatment overview](https://ottawa.ca/en/living-ottawa/drinking-water-stormwater-and-wastewater/wastewater-and-sewers/wastewater-collection-and-treatment/wastewater-treatment).

## Research and measurements

| Evidence | Sample or measurement | Relevance |
| --- | --- | --- |
| [SARS-CoV-2 surveillance study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9444583/) | Primary clarified sludge; SARS-CoV-2 and PMMoV RT-qPCR | Ottawa sampling started April 8, 2020, with daily collection from September 10, 2020 during the study. |
| [Influenza surveillance study](https://pmc.ncbi.nlm.nih.gov/articles/PMC9493155/) | Daily 24-hour composite primary sludge; influenza A/B RNA, February–May 2022 | Distinguishes plant-level sampling from separate neighbourhood sewer sites. |
| [RSV surveillance study](https://pmc.ncbi.nlm.nih.gov/articles/PMC10566629/) | Daily composite primary sludge; RSV and PMMoV RT-qPCR, August 2022–March 2023 | Connects environmental signals with pediatric seasonal surveillance. |
| [SARS-CoV-2 genomic-method study](https://pubs.acs.org/doi/10.1021/acsestwater.5c00142) | Thirty paired influent/primary-sludge composites across three campaigns in 2022–2023 | Supports recording distinct sampling matrices within one facility. |
| [Acinetobacter study](https://journals.asm.org/doi/10.1128/spectrum.01509-24) | Thirty samples spanning pre-chlorination, chlorination, and dechlorination stages | Extends research coverage beyond respiratory-virus surveillance to treatment-stage microbiology. |

The influenza study estimated 910,000 people served at that time. Catchment
population estimates should retain their source and period rather than become
an undated site constant. The study's neighbourhood manholes must not be
merged into ROPEC's physical location.
[Study site descriptions](https://pmc.ncbi.nlm.nih.gov/articles/PMC9493155/).

## Current reporting and data access

[Ottawa Public Health](https://www.ottawapublichealth.ca/statistics-and-reports/infectious-diseases-and-outbreaks/)
directs readers to the [613COVID wastewater dashboard](https://613covid.ca/wastewater/).
At review, that dashboard reported samples through September 6, 2026 and a
September 9 update. It states that surveillance continues through Ottawa Public
Health and the University of Ottawa's Delatolla group after provincial funding
ended July 31, 2024. Its influenza and RSV schedules vary seasonally. A plot's
update frequency should not be used as the sample collection frequency.

The dashboard links methods and data-access information. This research pass
verified the reporting page, but did not download a time series or establish
its reuse license or a stable machine-readable endpoint.

## Knowledge-base representation and remaining gaps

The initial record uses the existing Site schema, with published measurements
and sources in variable descriptions and notes. No external network membership
is inferred from a dashboard or paper. Coordinates and ontology mappings remain
unverified; the record omits them. The year 1962 is retained in notes because
the schema's `established` field requires a full date.

For broader wastewater coverage, useful schema extensions would separate
facility type, treatment stages, sampling points and matrices, sewershed,
population served with observation year, design capacity versus observed flow,
and per-claim provenance. These are proposals, not schema changes in this pass.
An authoritative geospatial record, current operational report, and verified
dataset identifiers are the next metadata targets.
