from dataclasses import dataclass


SUPPORTED_STTR_MAJOR = "3.0"


def _norm(value: str) -> str:
    return " ".join((value or "").casefold().split())


@dataclass
class STTRPreflightRequest:
    packageId: str


def _version_fit(version: str, supported_versions: list[str] | tuple[str, ...]) -> bool:
    return any((version or "").startswith(supported) for supported in supported_versions)


def check_sttr_package(
    req: STTRPreflightRequest,
    packages: list[dict],
    supported_versions: list[str] | tuple[str, ...] | None = None,
) -> dict:
    supported_versions = supported_versions or (SUPPORTED_STTR_MAJOR,)
    package_id = _norm(req.packageId)
    package = next((item for item in packages if item.get("packageId") == package_id), None)

    if not package:
        return {
            "packageFound": False,
            "sttrVersionFit": False,
            "imtrVersionFit": False,
            "rtrVersionFit": False,
            "jremMappingFit": False,
            "manualReviewRequired": True,
            "manualReviewReason": "Toepasbare-regelbestand niet gevonden.",
            "appliedRules": ["STTR-008"],
            "sourceRefs": [],
        }

    applied = ["STTR-001"]
    issues = list(package.get("issues", []))
    sttr_fit = _version_fit(package.get("sttrVersion", ""), supported_versions)
    imtr_fit = _version_fit(package.get("imtrVersion", ""), supported_versions)
    rtr_fit = bool(package.get("rtrVersion"))
    mapped_rule_ids = package.get("jremMapping", {}).get("mappedRuleIds", [])
    mapping_fit = bool(mapped_rule_ids)

    if sttr_fit:
        applied.append("STTR-002")
    else:
        applied.append("STTR-006")
        issues.append("STTR-versie past niet bij actuele ondersteunde versie.")

    if not imtr_fit:
        issues.append("IMTR-versie ontbreekt of past niet bij ondersteunde versies.")

    if rtr_fit:
        applied.append("STTR-003")
    else:
        issues.append("RTR-versie ontbreekt.")

    if mapping_fit:
        applied.append("STTR-004")
    else:
        applied.append("STTR-007")
        issues.append("JREM mapping ontbreekt.")

    if not issues and package.get("status") == "valid":
        applied.append("STTR-005")

    return {
        "packageFound": True,
        "packageId": package.get("packageLabel"),
        "sttrVersionFit": sttr_fit,
        "imtrVersionFit": imtr_fit,
        "rtrVersionFit": rtr_fit,
        "jremMappingFit": mapping_fit,
        "mappedRuleIds": mapped_rule_ids,
        "manualReviewRequired": bool(issues),
        "manualReviewReason": "; ".join(dict.fromkeys(issues)),
        "appliedRules": list(dict.fromkeys(applied)),
        "sourceRefs": package.get("sourceRefs", []),
    }
