# Site KB curation and validation

- Always use `linkml-term-validator` when adding or changing term identifiers,
  ontology labels, mappings, bindings, or term-bearing records. Run it on the
  affected data/schema and report any failures or unavailable ontology sources.
  Schema validation alone does not validate ontology terms.
- Keep validation bindings on all `OntologyTerm`-valued fields. Verify that a
  deliberately incorrect label is rejected when changing validation plumbing.
- Preserve verbatim upstream names/IDs in `SourceVariable`; these are source
  evidence, not claims of canonical labels. Validate ontology targets separately.
- Keep facility/site classification separate from ecosystem, habitat, and sample
  material. Do not infer that every research site is a research-station facility.
- Standards-derived candidate properties are not evidence that a particular site
  measures them. Keep candidate profiles separate from actual site declarations.
- Keep ingestion, curated records/crosswalks, and generated output separated as
  documented in README.md. Never hand-edit generated database or HTML output.
