# site-kb

Environmental Research Site Knowledge Base — a unified registry of sites across DEIMS/LTER, NEON, ARM, AmeriFlux, and other networks, with harmonized variable/measurement metadata and ontology bindings.

## Setup

```bash
uv sync --group dev
```

## Usage

```bash
# Fetch sites from APIs
just fetch-deims --limit 10
just fetch-neon

# Validate
just validate-db
just validate-terms
```
