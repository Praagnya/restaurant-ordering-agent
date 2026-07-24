#!/usr/bin/env python3
"""Parse a restaurant menu PDF into MenuItem schema and save to data/menu.json.

Usage:
    python scripts/parse_menu.py path/to/menu.pdf
    python scripts/parse_menu.py path/to/menu.pdf --output data/menu.json
    python scripts/parse_menu.py path/to/menu.pdf --show-intermediate
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from anthropic import Anthropic

from app.services.menu_parser.pdf_extractor import extract_menu_from_pdf
from app.services.menu_parser.schema_converter import convert_to_menu_items


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Parse a restaurant menu PDF into MenuItem JSON")
    parser.add_argument("pdf_path", help="Path to the menu PDF file")
    parser.add_argument("--output", default="data/menu.json", help="Output path (default: data/menu.json)")
    parser.add_argument("--show-intermediate", action="store_true", help="Print raw Claude extraction before converting")
    args = parser.parse_args()

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    print(f"Extracting menu from {args.pdf_path}...")
    intermediate = extract_menu_from_pdf(args.pdf_path, client)

    if args.show_intermediate:
        print("\n--- Intermediate extraction ---")
        print(json.dumps(intermediate, indent=2))
        print("--- End intermediate ---\n")

    items = convert_to_menu_items(intermediate)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps([item.model_dump() for item in items], indent=2))

    section_count = len(intermediate.get("sections", []))
    print(f"Parsed {len(items)} items across {section_count} sections → {output_path}")
    print()
    for item in items[:5]:
        print(f"  {item.name:<30} ${item.price_cents / 100:.2f}")
    if len(items) > 5:
        print(f"  ... and {len(items) - 5} more")


if __name__ == "__main__":
    main()
