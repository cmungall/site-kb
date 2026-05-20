## Project-specific recipes. Imported by the main justfile.

# Validate all site YAML files against the schema
validate-db:
  @for f in db/sites/*.yaml; do \
    echo "Validating $f..."; \
    uv run linkml-validate -s src/site_kb/schema/site_kb.yaml -C SiteCollection "$f" || exit 1; \
  done

# Validate a single site file
validate-site FILE:
  uv run linkml-validate -s src/site_kb/schema/site_kb.yaml -C SiteCollection {{FILE}}

# Validate ontology term IDs and labels in the schema
validate-terms-schema *ARGS:
  uv run linkml-term-validator validate-schema src/site_kb/schema/site_kb.yaml -c conf/oak_config.yaml {{ARGS}}

# Validate ontology term IDs and labels in all site data files
validate-terms-data *ARGS:
  @for f in db/sites/*.yaml; do \
    echo "Validating terms in $f..."; \
    uv run linkml-term-validator validate-data "$f" -s src/site_kb/schema/site_kb.yaml -t SiteCollection -c conf/oak_config.yaml {{ARGS}} || exit 1; \
  done

# Validate both schema and data terms
validate-terms *ARGS:
  just validate-terms-schema {{ARGS}}
  just validate-terms-data {{ARGS}}

# Fetch sites from DEIMS API and write to db/sites/
fetch-deims *ARGS:
  uv run python -m site_kb.scripts.fetch_deims {{ARGS}}

# Fetch sites from NEON API and write to db/sites/
fetch-neon *ARGS:
  uv run python -m site_kb.scripts.fetch_neon {{ARGS}}

# Fetch from all sources
fetch-all:
  just fetch-deims
  just fetch-neon

# Run all validations
validate-all: validate-db validate-terms
