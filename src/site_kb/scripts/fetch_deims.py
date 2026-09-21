"""Fetch site metadata from the DEIMS-SDR API and write to db/sites/."""

from pathlib import Path

import httpx
import typer
import yaml

DEIMS_API = "https://deims.org/api"
OUTPUT_DIR = Path("db/sites")

app = typer.Typer()


def sanitize_filename(name: str) -> str:
    """Convert a site name to a safe filename."""
    safe = name.lower()
    safe = "".join(c if c.isalnum() or c in " -_" else "" for c in safe)
    safe = safe.strip().replace(" ", "_")
    return safe[:80]


def fetch_site_list() -> list[dict]:
    """Fetch the list of all DEIMS sites."""
    resp = httpx.get(f"{DEIMS_API}/sites", timeout=60)
    resp.raise_for_status()
    return resp.json()


def fetch_site_detail(resource_id: str) -> dict:
    """Fetch detailed metadata for a single DEIMS site."""
    resp = httpx.get(f"{DEIMS_API}/sites/{resource_id}", timeout=30)
    resp.raise_for_status()
    return resp.json()


def _as_text(value: object) -> str | None:
    """Normalize DEIMS scalar/list values to a schema-compatible string."""
    if value is None:
        return None
    if isinstance(value, list):
        parts = [str(v).strip() for v in value if v is not None and str(v).strip()]
        return ", ".join(parts) if parts else None
    text = str(value).strip()
    return text or None


def _as_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_coordinates(value: object) -> tuple[float | None, float | None]:
    """Return latitude and longitude from common DEIMS coordinate shapes."""
    if not value:
        return None, None
    if isinstance(value, str):
        coords = [part.strip() for part in value.split(",")]
        if len(coords) >= 2:
            return _as_float(coords[1]), _as_float(coords[0])
    if isinstance(value, dict):
        lat = _as_float(value.get("latitude") or value.get("lat"))
        lon = _as_float(value.get("longitude") or value.get("lon") or value.get("lng"))
        return lat, lon
    if isinstance(value, (list, tuple)) and len(value) >= 2:
        return _as_float(value[1]), _as_float(value[0])
    return None, None


def _as_dict(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _site_id_from_summary(summary: dict) -> str:
    id_value = summary.get("id")
    if isinstance(id_value, dict):
        return _as_text(id_value.get("suffix") or id_value.get("id")) or ""
    return _as_text(id_value) or ""


def _elevation_from_geographic(geo: dict) -> float | None:
    elevation = geo.get("elevation")
    if isinstance(elevation, dict):
        return _as_float(elevation.get("avg") or elevation.get("mean") or elevation.get("value"))
    return _as_float(elevation)


def deims_to_site(summary: dict, detail: dict) -> dict:
    """Convert DEIMS API response to site-kb Site format."""
    title = _as_text(summary.get("title")) or "Unknown"
    site_id = _site_id_from_summary(summary) or sanitize_filename(title)

    # Extract coordinates
    lat, lon = _parse_coordinates(summary.get("coordinates"))

    location = {}
    if lat is not None and lon is not None:
        location["latitude"] = lat
        location["longitude"] = lon

    # Extract country from detail
    attributes = _as_dict(detail.get("attributes"))
    geo = _as_dict(attributes.get("geographic"))
    country = _as_text(geo.get("country"))
    if location and country:
        location["country"] = country
    elevation = _elevation_from_geographic(geo)
    if location and elevation is not None:
        location["elevation_meters"] = elevation

    site = {
        "id": f"site_kb:deims-{sanitize_filename(title)}",
        "name": title,
        "network_registrations": [
            {
                "network": "DEIMS",
                "network_id": site_id,
                "network_url": f"https://deims.org/{site_id}",
                "name": title,
            }
        ],
    }

    if location:
        site["location"] = location

    # Extract description
    general = _as_dict(attributes.get("general"))
    abstract = _as_text(general.get("abstract"))
    if abstract:
        site["description"] = abstract

    # Extract ecosystem from environmental characteristics
    env_chars = _as_dict(attributes.get("environmentalCharacteristics"))
    notes = []
    biogeographical_region = _as_text(env_chars.get("biogeographicalRegion"))
    if biogeographical_region:
        notes.append(f"Biogeographical region: {biogeographical_region}")
    if not location:
        if country:
            notes.append(f"DEIMS country: {country}")
        if elevation is not None:
            notes.append(f"DEIMS average elevation: {elevation:g} m")
    if notes:
        site["notes"] = "; ".join(notes)

    site["status"] = "ACTIVE"

    return site


@app.command()
def main(
    limit: int = typer.Option(0, help="Limit number of sites to fetch (0 = all)"),
    offset: int = typer.Option(0, help="Number of sites to skip before applying limit"),
    output_dir: Path = typer.Option(OUTPUT_DIR, help="Output directory"),
    detail: bool = typer.Option(True, help="Fetch detailed metadata for each site"),
    summary_only: bool = typer.Option(False, help="Print summary statistics only"),
):
    """Fetch sites from DEIMS-SDR API."""
    output_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("Fetching DEIMS site list...")
    sites = fetch_site_list()
    typer.echo(f"Found {len(sites)} sites")

    if offset > 0:
        sites = sites[offset:]
    if limit > 0:
        sites = sites[:limit]

    if summary_only:
        typer.echo(f"Total sites: {len(sites)}")
        return

    for i, summary in enumerate(sites):
        title = _as_text(summary.get("title")) or "Unknown"
        site_id = _site_id_from_summary(summary)
        typer.echo(f"[{i+1}/{len(sites)}] {title}")

        detail_data = {}
        if detail and site_id:
            detail_data = fetch_site_detail(site_id)

        site = deims_to_site(summary, detail_data)
        collection = {"sites": [site]}

        filename = f"deims_{sanitize_filename(title)}.yaml"
        filepath = output_dir / filename
        filepath.write_text(yaml.dump(collection, default_flow_style=False, allow_unicode=True, sort_keys=False))

    typer.echo(f"Wrote {len(sites)} site files to {output_dir}")


if __name__ == "__main__":
    app()
