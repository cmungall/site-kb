"""Tests for validating site data against the schema."""

from pathlib import Path

import pytest
import yaml
from linkml_runtime.loaders import yaml_loader

SCHEMA_DIR = Path(__file__).parent.parent / "src" / "site_kb" / "schema"
VALID_DIR = Path(__file__).parent / "data" / "valid"
INVALID_DIR = Path(__file__).parent / "data" / "invalid"


@pytest.fixture
def valid_files():
    return list(VALID_DIR.glob("*.yaml"))


@pytest.fixture
def invalid_files():
    return list(INVALID_DIR.glob("*.yaml"))


def test_valid_data_exists(valid_files):
    assert len(valid_files) > 0, "No valid test data files found"


def test_valid_files_are_parseable(valid_files):
    for f in valid_files:
        data = yaml.safe_load(f.read_text())
        assert "sites" in data, f"Missing 'sites' key in {f.name}"
        assert len(data["sites"]) > 0, f"No sites in {f.name}"


def test_invalid_data_exists(invalid_files):
    assert len(invalid_files) > 0, "No invalid test data files found"
