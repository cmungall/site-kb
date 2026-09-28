# Wastewater expansion: Hong Kong, Nanjing and Nine Springs

Curated 2026-09-23. Nine additional facilities and five primary studies.
Source papers were read through Europe PMC's fullTextXML endpoint. Public
sequencing metadata was checked through ENA's `filereport` API, with the responses
retained in `db/raw/research/wastewater_expansion_ena.json`.
These records register documented properties and study associations, not numerical
observation series or a claim of current monitoring.

## Study and site coverage

| Study | Facilities | Public archive | Scope |
| --- | --- | --- | --- |
| [Che et al., 2019](https://doi.org/10.1186/s40168-019-0663-0) | Sha Tin, Shek Wu Hui, Stanley | PRJNA505617; paper also cites BioSamples SAMN09603371–SAMN09603381 | ARG abundance and genomic location using Illumina and Nanopore sequencing |
| [Effects of operational parameters, 2024](https://doi.org/10.1128/msystems.01333-23) | Sha Tin, Shek Wu Hui, Stanley, Tai Po, Yuen Long, Sai Kung | PRJNA1012295 | 16S profiles and operating covariates, January 2018–January 2019 |
| [Huang et al., 2025](https://doi.org/10.1093/ismejo/wraf058) | The same six Hong Kong plants | PRJNA432264 | Eukaryotic metagenomic profiles, with distinct sampling windows by plant |
| [Long-term antiviral defense study, 2025](https://doi.org/10.1093/ismejo/wraf051) | Dachang and Jiangxinzhou, Nanjing | PRJNA1149857 | Activated-sludge metagenomes, complete defense systems and CRISPR spacers |
| [Stewart et al., 2024](https://doi.org/10.1128/msystems.01188-23) | Nine Springs, Madison, Wisconsin | PRJNA1037153; JGI GOLD Gs0156633 | Four on-site pilot configurations, reduced aeration, nutrients and Accumulibacter |

## What was checked in archive metadata

- **PRJNA1012295:** 222 runs labelled AMPLICON, matching the published aggregate
  74 influent, 74 activated-sludge and 74 effluent samples. The sample titles carry
  the six plant codes. These are not shotgun metagenomes. Sai Kung sampling was
  interrupted after typhoon damage in September 2018.
- **PRJNA505617:** 12 Illumina WGS run records, including repeated BioSamples and
  a mixed-culture library. Twelve runs do not mean twelve independent plant
  samples. The article separately gives the Nanopore-associated BioSample range;
  inspected SAMN09603371 has isolation source `ST_influent`. Nanopore read-run
  accessions were not resolved here. Site coordinates use the paper's named
  sampling locations rather than the broad Hong Kong coordinates in that sample.
- **PRJNA1149857:** 134 WGS runs. The paper partitions these into 69 Dachang and
  65 Jiangxinzhou metagenomes, with four Jiangxinzhou samples excluded by quality
  control. Sampling was monthly from January 2013 through September 2018.
  The inspected sample SAMN43264894 gave Nanjing and coordinates but did not
  establish which plant it represented, so no plant coordinates were inferred.
- **PRJNA432264:** 114 currently returned WGS runs, reused across papers. This
  does not resolve the 2025 paper's entire published inventory. That paper
  describes 143 Sha Tin samples (June 2007–December 2019), one-year series at
  Shek Wu Hui and Stanley, and single samples from the remaining three plants
  on 2018-01-05. It also describes twelve Sha Tin RNA samples (April 2017–March
  2018), but no RNA-labelled run appeared in the queried inventory. The RNA
  dataset is therefore separately marked UNRESOLVED; its study-derived RNA/DNA
  property has paper evidence. RNA observations are not assigned to all six sites.
- **PRJNA1037153:** 13 returned WGS runs, some carrying individual child BioProject
  accessions and PacBio platform metadata. Preserve the queried umbrella project
  separately from the per-run study accession. Full-scale Nine Springs hosts the
  experiments, but the chemistry and genomes belong to pilot trains UCTca, AOia,
  AO-G and AO-FF. The four configurations are not four municipal facilities.

## Variable curation

Seventeen additional shared definitions capture bacterial 16S composition,
temperature, mean cell residence time, hydraulic retention time, sequence-normalized
ARG abundance, ARG genomic context, eukaryotic relative abundance and RNA/DNA
ratios, antiviral defense-system abundance, CRISPR spacer density, filtered total
phosphorus, filtered TKN, filtered nitrate/nitrite nitrogen, pilot dissolved oxygen,
pilot ammonium nitrogen and Accumulibacter relative abundance.

These are local definitions with preserved source wording and paper evidence.
No BERVO equivalence was inferred. Plant declarations carry the relevant assay,
sample compartment, reported units and historical sampling window. RPKM and ARGs
per million base pairs remain sequence-normalized quantities; they are not absolute
concentrations in water. Nine Springs ammonium-sensor declarations apply only to
UCTca/AOia, while dissolved-oxygen sensors apply to all four pilot configurations.
Filtered chemistry is explicitly distinguished from unfiltered total quantities.

The existing Tatlar record also had a prose correction: the named BioSample's
2016-02-03 date agrees with Table S1. It is the *other* Ankara sample group that
has the differing 2016-03-02 date. Its unresolved plant assignment is unchanged.
