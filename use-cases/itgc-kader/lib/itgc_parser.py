#!/usr/bin/env python3
"""Deterministische extractie van het officiële ADR ITGC-kader naar JREM.

De parser gebruikt alleen de Python-standaardbibliotheek. Hij leest de XLSX
rechtstreeks uit de door ADR gepubliceerde ZIP en interpreteert geen inhoud met
een taalmodel.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile


SOURCE_URL = (
    "https://www.auditdienstrijk.nl/site/binaries/site-content/collections/"
    "documents/2026/maart/17/itgc-kader/adr-itgc-kader-v1-1.zip"
)
SOURCE_ZIP_SHA256 = "9b50fc02cb03c6a505a0c9d939853afbcd3d71eaa330c62349e9152d61d0af17"
SOURCE_XLSX_SHA256 = "bff440bd16fd8f6a03892b0a96d0e5e4c9b4eb6ae86da177b1d9d1f006188a7e"
SOURCE_TITLE = "ADR ITGC-kader v1.1"
CONTROL_ID = re.compile(r"^[A-Z]\d\.\d+$")
CRITERION_ID = re.compile(r"^([A-Z]\d\.\d+\.\d+)[: ]")
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "docrel": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pkgrel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def clean(value: str | None) -> str:
    return "\n".join(line.rstrip() for line in (value or "").strip().splitlines()).strip()


def read_source(source_zip: Path) -> bytes:
    archive = source_zip.read_bytes()
    if sha256(archive) != SOURCE_ZIP_SHA256:
        raise ValueError("De bron-ZIP wijkt af van de vastgelegde ADR SHA-256")
    with ZipFile(BytesIO(archive)) as outer:
        names = [name for name in outer.namelist() if name.lower().endswith(".xlsx")]
        if len(names) != 1:
            raise ValueError("De ADR ZIP moet exact één XLSX bevatten")
        workbook = outer.read(names[0])
    if sha256(workbook) != SOURCE_XLSX_SHA256:
        raise ValueError("De XLSX wijkt af van de vastgelegde ADR SHA-256")
    return workbook


def workbook_rows(workbook: bytes) -> dict[str, list[dict[str, str]]]:
    """Lees werkbladen als rijen met kolomletter -> celtekst."""
    with ZipFile(BytesIO(workbook)) as xlsx:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in xlsx.namelist():
            root = ET.fromstring(xlsx.read("xl/sharedStrings.xml"))
            for item in root.findall("main:si", NS):
                shared.append("".join(node.text or "" for node in item.iter(f"{{{NS['main']}}}t")))

        workbook_xml = ET.fromstring(xlsx.read("xl/workbook.xml"))
        rels_xml = ET.fromstring(xlsx.read("xl/_rels/workbook.xml.rels"))
        targets = {item.attrib["Id"]: item.attrib["Target"] for item in rels_xml}
        sheets: dict[str, list[dict[str, str]]] = {}

        sheet_nodes = workbook_xml.find("main:sheets", NS)
        if sheet_nodes is None:
            raise ValueError("Werkmap bevat geen werkbladen")
        for sheet in sheet_nodes:
            name = sheet.attrib["name"]
            relation_id = sheet.attrib[f"{{{NS['docrel']}}}id"]
            target = targets[relation_id].lstrip("/")
            path = target if target.startswith("xl/") else f"xl/{target}"
            sheet_xml = ET.fromstring(xlsx.read(path))
            rows: list[dict[str, str]] = []
            for row in sheet_xml.findall(".//main:sheetData/main:row", NS):
                values: dict[str, str] = {}
                for cell in row.findall("main:c", NS):
                    column = re.match(r"[A-Z]+", cell.attrib["r"])
                    if column is None:
                        continue
                    cell_type = cell.attrib.get("t")
                    value = cell.find("main:v", NS)
                    if cell_type == "inlineStr":
                        text = "".join(
                            node.text or "" for node in cell.iter(f"{{{NS['main']}}}t")
                        )
                    elif value is None or value.text is None:
                        text = ""
                    elif cell_type == "s":
                        text = shared[int(value.text)]
                    elif cell_type == "e":
                        text = ""
                    else:
                        text = value.text
                    if clean(text):
                        values[column.group()] = clean(text)
                rows.append(values)
            sheets[name] = rows
        return sheets


def parse_overview(rows: list[dict[str, str]]) -> dict[str, dict]:
    overview: dict[str, dict] = {}
    context = {"process": "", "objective": "", "risk": ""}
    for row in rows:
        control_id = row.get("F", "")
        if not CONTROL_ID.fullmatch(control_id):
            continue
        for column, key in (("C", "process"), ("D", "objective"), ("E", "risk")):
            if row.get(column):
                context[key] = row[column]
        overview[control_id] = {
            **context,
            "biv": [label for column, label in (("H", "B"), ("I", "I"), ("J", "V")) if row.get(column)],
            "audience": row.get("K", ""),
        }
    return overview


def reference_lines(value: str) -> list[str]:
    return [line.strip() for line in value.splitlines() if line.strip()]


def parse_controls(sheets: dict[str, list[dict[str, str]]]) -> list[dict]:
    overview = parse_overview(sheets["Beheerprocessen overzicht"])
    controls: list[dict] = []

    for sheet_name, rows in sheets.items():
        if not rows or not any(row.get("B") == "ID" and row.get("F") == "Testcriteria" for row in rows):
            continue
        current: dict | None = None
        for row in rows:
            candidate = row.get("B", "")
            if CONTROL_ID.fullmatch(candidate):
                current = {
                    "id": candidate,
                    "title": row.get("C", ""),
                    "measure": row.get("D", ""),
                    "elaboration": row.get("E", ""),
                    "worksheet": sheet_name,
                    "overview": overview[candidate],
                    "testCriteria": [],
                }
                controls.append(current)

            criterion = row.get("F", "")
            if current is None or not criterion:
                continue
            match = CRITERION_ID.match(criterion)
            if match is None:
                raise ValueError(f"Toetsingscriterium zonder herkenbaar ID in {sheet_name}: {criterion[:80]}")
            current["testCriteria"].append(
                {
                    "id": match.group(1),
                    "text": criterion,
                    "type": row.get("G", ""),
                    "references": reference_lines(row.get("H", "")),
                }
            )

    ids = [control["id"] for control in controls]
    criterion_ids = [item["id"] for control in controls for item in control["testCriteria"]]
    if len(ids) != 48 or len(set(ids)) != 48:
        raise ValueError(f"Verwacht 48 unieke beheersmaatregelen, gevonden {len(set(ids))}")
    if len(criterion_ids) != 147 or len(set(criterion_ids)) != 147:
        raise ValueError(f"Verwacht 147 unieke toetsingscriteria, gevonden {len(set(criterion_ids))}")
    return controls


def build_jrem(source_zip: Path) -> dict:
    controls = parse_controls(workbook_rows(read_source(source_zip)))
    rules = []
    for control in controls:
        rules.append(
            {
                "ruleId": f"ITGC-{control['id']}",
                "name": control["title"],
                "priority": 100,
                "legalStatus": "conventie",
                "sourceRefs": [
                    {
                        "type": "standaard",
                        "title": SOURCE_TITLE,
                        "section": control["id"],
                        "url": SOURCE_URL,
                        "bronVersie": "2026-05-12",
                        "bronDatum": "2026-05-12",
                    }
                ],
                "conditions": {},
                "outcome": {
                    "category": f"itgc_{control['id'].split('.')[0].lower()}",
                    "confidence": "deterministic",
                    "manualReviewRequired": True,
                    "manualReviewReason": "Catalogusrecord; organisatiebewijs en auditoroordeel ontbreken.",
                    "assessmentStatus": "insufficient_evidence",
                    "itgc": control,
                },
            }
        )

    return {
        "schemaVersion": "1.1.0",
        "ruleSetId": "adr-itgc-kader",
        "version": "2026.1",
        "validFrom": "2026-05-12",
        "validUntil": None,
        "jurisdiction": "NL",
        "governanceLevel": "rijk",
        "domain": "itgc-kader",
        "procedureType": "itgc-kader",
        "conflictResolution": "first-match",
        "maturityLevel": "L1-poc",
        "approval": {
            "type": "self",
            "reviewer": "JuraRegel maintainer",
            "role": "technische bronextractie",
            "date": "2026-07-16",
            "scope": "Bronintegriteit, structuur en cataloguscontract; geen auditor- of juridisch oordeel.",
            "limitations": [
                "Geen organisatiebewijs beoordeeld.",
                "Geen onafhankelijke inhoudelijke review.",
                "ADR vermeldt dat aan het kader geen rechten kunnen worden ontleend.",
                "Leveranciersmanagement (L1) is in versie 1.1 niet opgenomen.",
            ],
        },
        "rules": rules,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    data = build_jrem(args.source_zip)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    criteria = sum(len(rule["outcome"]["itgc"]["testCriteria"]) for rule in data["rules"])
    print(f"Gegenereerd: {len(data['rules'])} maatregelen, {criteria} toetsingscriteria")


if __name__ == "__main__":
    main()
