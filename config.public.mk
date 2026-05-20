# config.public.mk

# This file is public in git. No sensitive info allowed.

###### schema definition variables, used by justfile

LINKML_SCHEMA_NAME="site_kb"
LINKML_SCHEMA_AUTHOR="Chris Mungall <cjmungall@lbl.gov>"
LINKML_SCHEMA_DESCRIPTION="Environmental Research Site Knowledge Base"
LINKML_SCHEMA_SOURCE_DIR="src/site_kb/schema"

###### linkml generator variables, used by justfile

## gen-project configuration file
LINKML_GENERATORS_CONFIG_YAML=config.yaml

## pass args if gendoc ignores config.yaml (i.e. --no-mergeimports)
LINKML_GENERATORS_DOC_ARGS=

## pass args to workaround genowl rdfs config bug (linkml#1453)
LINKML_GENERATORS_OWL_ARGS=

## pass args to trigger experimental java/typescript generation
LINKML_GENERATORS_JAVA_ARGS=
LINKML_GENERATORS_TYPESCRIPT_ARGS=

## pass args to pydantic generator which isn't supported by gen-project
LINKML_GENERATORS_PYDANTIC_ARGS=
