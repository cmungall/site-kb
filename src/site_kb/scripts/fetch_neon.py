"""Fetch site metadata from the NEON API and write to db/imported/neon/."""

from pathlib import Path

import httpx
import typer
import yaml

NEON_API = "https://data.neonscience.org/api/v0"
OUTPUT_DIR = Path("db/imported/neon")

app = typer.Typer()


def fetch_sites() -> list[dict]:
    """Fetch all NEON sites."""
    resp = httpx.get(f"{NEON_API}/sites", timeout=60)
    resp.raise_for_status()
    return resp.json()["data"]


def neon_to_site(neon_site: dict) -> dict:
    """Convert NEON API site to site-kb Site format."""
    code = neon_site["siteCode"]
    name = neon_site["siteName"]

    site = {
        "id": f"site_kb:neon-{code.lower()}",
        "name": name,
        "location": {
            "latitude": neon_site["siteLatitude"],
            "longitude": neon_site["siteLongitude"],
            "country": "United States",
            "state_province": neon_site.get("stateName"),
        },
        "network_registrations": [
            {
                "network": "NEON",
                "network_id": code,
                "network_url": f"https://www.neonscience.org/field-sites/{code.lower()}",
                "name": name,
                "site_type": neon_site.get("siteType"),
            }
        ],
        "status": "ACTIVE",
    }

    # Add DEIMS cross-reference if available
    deims_id = neon_site.get("deimsId")
    if deims_id:
        # Extract UUID from the DEIMS URL
        deims_uuid = deims_id.rstrip("/").split("/")[-1]
        site["network_registrations"].append(
            {
                "network": "DEIMS",
                "network_id": deims_uuid,
                "network_url": deims_id,
            }
        )

    # Domain info as notes
    domain_code = neon_site.get("domainCode", "")
    domain_name = neon_site.get("domainName", "")
    if domain_code:
        site["notes"] = f"NEON Domain: {domain_code} ({domain_name})"

    return site


@app.command()
def main(
    output_dir: Path = typer.Option(OUTPUT_DIR, help="Output directory"),
    summary_only: bool = typer.Option(False, help="Print summary statistics only"),
):
    """Fetch sites from NEON API."""
    output_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("Fetching NEON sites...")
    neon_sites = fetch_sites()
    typer.echo(f"Found {len(neon_sites)} sites")

    if summary_only:
        for s in neon_sites:
            typer.echo(f"  {s['siteCode']}: {s['siteName']} ({s.get('siteType', '?')})")
        return

    for site_data in neon_sites:
        site = neon_to_site(site_data)
        collection = {"sites": [site]}

        code = site_data["siteCode"].lower()
        filename = f"neon_{code}.yaml"
        filepath = output_dir / filename
        filepath.write_text(yaml.dump(collection, default_flow_style=False, allow_unicode=True, sort_keys=False))

    typer.echo(f"Wrote {len(neon_sites)} site files to {output_dir}")


if __name__ == "__main__":
    app()
