#!/usr/bin/env python3
import argparse
import csv
import sys
from datetime import datetime, date
import requests

BASE_URL = "https://data.vinnova.se/api/projekt/"

def parse_date(datestr: str) -> date:
    """Parsa YYYY-MM-DD till date-objekt, med enkel felhantering."""
    try:
        return date.fromisoformat(datestr)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Ogiltigt datumformat: {datestr}, använd YYYY-MM-DD")

def fetch_projects(from_date: date):
    """
    Hämtar alla projekt som ändrats från och med from_date.
    Vinnovas API: /api/projekt/YYYY-MM-DD
    """
    url = BASE_URL + from_date.isoformat()
    print(f"Hämtar projekt från Vinnova: {url}", file=sys.stderr)
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, list):
        raise RuntimeError("Oväntat svar från API: förväntade en lista")
    print(f"  → fick {len(data)} projekt totalt", file=sys.stderr)
    return data

def filter_beviljade_in_interval(projects, from_date: date | None, to_date: date | None):
    """
    Filtrera:
      - BeviljatBidrag > 0
      - ProjektStart inom [from_date, to_date] om de anges
    """
    result = []
    for p in projects:
        # 1) Beviljat bidrag
        bidrag = p.get("BeviljatBidrag") or 0
        if bidrag <= 0:
            continue

        # 2) ProjektStart: format "YYYY-MM-DDTHH:MM:SS"
        ps_raw = p.get("ProjektStart")
        if not ps_raw:
            # Saknar startdatum → hoppa över eller inkludera, här väljer vi överhoppning
            continue

        try:
            ps_date = date.fromisoformat(ps_raw[:10])
        except ValueError:
            # Konstigt datumformat → hoppa
            continue

        if from_date and ps_date < from_date:
            continue
        if to_date and ps_date > to_date:
            continue

        result.append(p)

    print(f"  → efter filtrering: {len(result)} beviljade projekt i intervallet", file=sys.stderr)
    return result

def save_to_csv(projects, filename: str):
    """
    Spara ett urval fält till CSV.
    Lägg till fler fält vid behov.
    """
    if not projects:
        print("Inga projekt att spara.", file=sys.stderr)
        return

    fields = [
        "Diarienummer",
        "Ärenderubrik",
        "ÄrenderubrikEngelska",
        "BeviljatBidrag",
        "ProjektStart",
        "ProjektSlut",
        "Status",
        "KoordinatorOrg",
        "KoordinatorArb",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for p in projects:
            row = {field: p.get(field, "") for field in fields}
            writer.writerow(row)

    print(f"Sparade {len(projects)} projekt till {filename}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(
        description="Hämta beviljade Vinnova-projekt via öppna API:t och filtrera på datumintervall."
    )
    parser.add_argument(
        "--from-date",
        type=parse_date,
        help="Hämta projekt ändrade från och med detta datum (YYYY-MM-DD). "
             "Används även som nedre gräns för ProjektStart. (default: 2000-01-01)",
        default=date(2000, 1, 1),
    )
    parser.add_argument(
        "--to-date",
        type=parse_date,
        help="Övre gräns för ProjektStart (YYYY-MM-DD). Om utelämnas: ingen övre gräns.",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="vinnova_beviljade_projekt.csv",
        help="Filnamn för CSV-utdata (default: vinnova_beviljade_projekt.csv)",
    )

    args = parser.parse_args()

    try:
        projects = fetch_projects(args.from_date)
    except Exception as e:
        print(f"Fel vid hämtning från API: {e}", file=sys.stderr)
        sys.exit(1)

    filtered = filter_beviljade_in_interval(projects, args.from_date, args.to_date)
    save_to_csv(filtered, args.output)

if __name__ == "__main__":
    main()

