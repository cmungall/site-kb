"""Tests for DEIMS API mapping helpers."""

from site_kb.scripts.fetch_deims import deims_to_site


def test_deims_list_country_without_coordinates_does_not_emit_location():
    site = deims_to_site(
        {
            "id": {"suffix": "90e55d56-fb0a-44c3-aeb6-c750d0eeefc4"},
            "title": "Changshu Agro-Ecological Experimental Station - China",
        },
        {
            "attributes": {
                "geographic": {
                    "country": ["China"],
                    "elevation": {"avg": "3"},
                }
            }
        },
    )

    assert "location" not in site
    assert "DEIMS country: China" in site["notes"]
    assert "DEIMS average elevation: 3 m" in site["notes"]


def test_deims_coordinates_emit_schema_compatible_location():
    site = deims_to_site(
        {
            "id": {"suffix": "abc"},
            "title": "Example Site",
            "coordinates": "120.6984,31.5497",
        },
        {
            "attributes": {
                "geographic": {
                    "country": ["China"],
                    "elevation": {"avg": "3"},
                }
            }
        },
    )

    assert site["location"] == {
        "latitude": 31.5497,
        "longitude": 120.6984,
        "country": "China",
        "elevation_meters": 3.0,
    }


def test_deims_mapper_normalizes_scalar_and_list_detail_fields():
    site = deims_to_site(
        {
            "id": "abc",
            "title": None,
            "coordinates": {"lat": "45.0", "lng": "-122.0"},
        },
        {
            "attributes": {
                "general": {"abstract": ["First sentence.", "Second sentence."]},
                "geographic": {
                    "country": "United States",
                    "elevation": "42",
                },
                "environmentalCharacteristics": {
                    "biogeographicalRegion": ["Region A", "Region B"],
                },
            }
        },
    )

    assert site["id"] == "site_kb:deims-unknown"
    assert site["network_registrations"][0]["network_id"] == "abc"
    assert site["description"] == "First sentence., Second sentence."
    assert site["location"]["elevation_meters"] == 42.0
    assert site["notes"] == "Biogeographical region: Region A, Region B"
