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


def deims_to_site(summary: dict, detail: dict) -> dict:
    """Convert DEIMS API response to site-kb Site format."""
    site_id = summary.get("id", {}).get("suffix", "")
    title = summary.get("title", "Unknown")

    # Extract coordinates
    coords = summary.get("coordinates", "").split(",") if summary.get("coordinates") else []
    lat = float(coords[1].strip()) if len(coords) >= 2 else None
    lon = float(coords[0].strip()) if len(coords) >= 2 else None

    location = {}
    if lat is not None:
        location["latitude"] = lat
        location["longitude"] = lon

    # Extract country from detail
    geo = detail.get("attributes", {}).get("geographic", {})
    if geo.get("country"):
        location["country"] = geo["country"]
    if geo.get("elevation", {}).get("avg"):
        location["elevation_meters"] = float(geo["elevation"]["avg"])

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
    general = detail.get("attributes", {}).get("general", {})
    if general.get("abstract"):
        site["description"] = general["abstract"]

    # Extract ecosystem from environmental characteristics
    env_chars = detail.get("attributes", {}).get("environmentalCharacteristics", {})
    if env_chars and env_chars.get("biogeographicalRegion"):
        site["notes"] = f"Biogeographical region: {env_chars['biogeographicalRegion']}"

    site["status"] = "ACTIVE"

    return site


@app.command()
def main(
    limit: int = typer.Option(0, help="Limit number of sites to fetch (0 = all)"),
    output_dir: Path = typer.Option(OUTPUT_DIR, help="Output directory"),
    detail: bool = typer.Option(True, help="Fetch detailed metadata for each site"),
    summary_only: bool = typer.Option(False, help="Print summary statistics only"),
):
    """Fetch sites from DEIMS-SDR API."""
    output_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("Fetching DEIMS site list...")
    sites = fetch_site_list()
    typer.echo(f"Found {len(sites)} sites")

    if limit > 0:
        sites = sites[:limit]

    if summary_only:
        typer.echo(f"Total sites: {len(sites)}")
        return

    for i, summary in enumerate(sites):
        title = summary.get("title", "Unknown")
        site_id = summary.get("id", {}).get("suffix", "")
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
