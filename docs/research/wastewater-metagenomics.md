# Wastewater sites with sequencing and chemistry

Research date: 2026-09-23. All facilities are classified with ENVO:00002043
(wastewater treatment plant); canonical labels are checked by linkml-term-validator.
The records register measured/analyzed properties, not numerical observation series.

## Seed: Türkiye reanalysis

[Kurt 2026, DOI 10.3390/antibiotics15080795](https://pmc.ncbi.nlm.nih.gov/articles/PMC13509523/)
reanalyzes ten sequencing runs labelled Ankara and Hatay. The full JATS and
supplement were retrieved through Europe PMC:

- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13509523/fullTextXML
- https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13509523/supplementaryFiles

The supplement contains `antibiotics-15-00795-s001.zip`; `Table S1.xlsx`, Sayfa1,
A1:R11 contains the ten run accessions, study accessions, places, dates and assay
metadata. Names and accession joins were checked against the ENA browser XML
and portal `filereport` APIs. The extracted API responses are retained in
`db/raw/research/turkiye_seed_ena.json` with retrieval date and source endpoints.
Extracted supplement cells and the original workbook SHA-256 are retained in
`db/raw/research/turkiye_seed_table_s1.json`.

| Run(s) | ENA sample | Plant resolution |
| --- | --- | --- |
| ERR2592273, ERR1713395, ERR1726009 | SAMEA4527663 | Explicitly named Tatlar Wastewater Treatment Plant |
| ERR2607547 | SAMEA4700868 | Ankara lead; no explicit plant-name attribute |
| ERR2607548 | SAMEA4700869 | Ankara lead; no explicit plant-name attribute |
| ERR2607549 | SAMEA4700870 | Ankara lead; no explicit plant-name attribute |
| ERR4678594 | SAMEA7426294 | Hatay lead; unresolved facility |
| ERR14141077 | SAMEA117579351 | Hatay lead; unresolved facility |
| ERR14149368 | SAMEA117579518 | Hatay lead; unresolved facility |
| ERR14173499 | SAMEA117579663 | Hatay lead; unresolved facility |

Tatlar is added using the explicit name in
[SAMEA4527663](https://www.ebi.ac.uk/ena/browser/view/SAMEA4527663).
Its three runs share one BioSample, not three independently documented biological
samples. The other accession group has distinct sample IDs but biological
independence is not established. The paper's aggregate ARG/MAG counts must not be
assigned to a plant or treated as a count of independent samples.

The named sample records 2016-02-03 and coordinates 39.9334 N, 32.8597 E.
The other Ankara sample group records 2016-03-02 and 39.8983889 N, 32.4536389 E.
Supplement S1 uses Excel serial 42403 for all six Ankara rows (2016-02-03).
These discrepancies are unresolved; facility coordinates and assignment of the
other three runs are deliberately omitted. Hatay's city/region label and rounded
coordinates do not establish a unique treatment plant.

## Aalborg West, Denmark

[BioProject PRJEB67571](https://www.ncbi.nlm.nih.gov/bioproject/1249737)
deposits metagenomic and transcriptomic data. Its description distinguishes
39 full-scale-plant transcriptomic samples from 140 batch-experiment samples;
these cannot all be treated as direct plant observations.

[BioSample SAMEA115986499](https://www.ebi.ac.uk/ena/browser/view/SAMEA115986499)
is MAG AalW_0078, derived from metagenome ERS16511554. Its aeration-tank provenance,
2021-11-02 date, and coordinates support the site record. Completeness and
contamination scores are registered as genome-quality properties with explicit
sample context. The recorded completeness is 88.15%, illustrating why a project's
“high quality” wording must not be transformed into an assumed >=90% threshold.
Upstream environmental term strings are not copied as validated canonical labels.

## Six Moroccan plants with chemistry and targeted sequencing

[Wardi et al. 2024](https://doi.org/10.1038/s41598-024-76773-4)
identifies M’ZAR, AOURIR, ANZA, DRARGA, TIZNIT and AIT BAHA (Table 1),
with influent/effluent chemistry in Table 3. These are six distinct plant records.
The manuscript methods use Ion AmpliSeq Pan-Bacterial panels: targeted species,
ARG loci and 16S profiling, **not untargeted shotgun sequencing**.
The data-availability statement offers data on request, without public read
accessions. Each record carries this distinction.

Thirteen reported chemistry variables are registered with study units/methods:
pH, temperature, dissolved oxygen, conductivity, salinity, turbidity, COD, calcium,
total hardness, magnesium, TAC, chlorides and antimony. Targeted ARG and 16S
profiles are broad parameter groups. Sampling was February and July 2020 except
AIT BAHA, sampled only in February because of July maintenance. Treatment types
are source-reported study context, not assertions about current operation.
No numerical values or inferred removals have been imported.

## Additional leads

[Chen et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11471163/)
names plants at Liptovský Mikuláš (SVLI), Kysucké Nové Mesto (SVKY) and Komárno
(SVKO), with paired influent/effluent resistome, mobilome and virulome analyses.
The reported SRA identifier SUB14264437 is a submission identifier, not a verified
public BioProject/run accession. These remain leads pending accession and
supplementary site metadata resolution. Taiwan sites are identified only by
codes ZN, WS and FS in the main text; no facility identities were invented.
