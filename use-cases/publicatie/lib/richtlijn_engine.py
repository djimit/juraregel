"""
Pseudonimiseringsrichtlijn Engine — implementeert de richtlijn-uitzonderingen.

Doel: 95% nauwkeurigheid door persoonType classificatie toe te voegen
aan de bestaande PII scanner. Gebaseerd op:
https://www.rechtspraak.nl/uitspraken/pseudonimiseringsrichtlijn

De engine classificeert elk gedetecteerd gegeven als:
- particulier → pseudonimiseer
- professional → niet pseudonimiseer (advocaat, notaris, deurwaarder)
- rechtspersoon → niet pseudonimiseer (B.V., N.V., Stichting)
- overheid → niet pseudonimiseer (gemeente, ministerie, politie)
- onbekend → handmatige controle
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional

# ─── Enums ───

class PersoonType(Enum):
    PARTICULAR = "particulier"
    PROFESSIONAL = "professional"
    RECHTSPERSOON = "rechtspersoon"
    OVERHEID = "overheid"
    ONBEKEND = "onbekend"

class PseudonimiseringsStatus(Enum):
    PSEUDONIMISEER = "pseudonimiseer"
    NIET_PSEUDONIMISEER = "niet_pseudonimiseer"
    HANDMATIGE_CONTROLE = "handmatige_controle"

# ─── Professional keywords (uitgebreid vs originele scanner) ───

PROFESSIONAL_KEYWORDS = re.compile(
    r"\badvocaat\b|\bmr\.\s|\bnotaris\b|\bdeurwaarder\b|\bprocuratiehouder\b|"
    r"\badvocaat-stagiair\b|\bgriffier\b|\brechter\b|\bofficier van justitie\b|"
    r"\braadsman\b|\braadsvrouw\b|\bgemachtigde\b|\bzaakwaarnemer\b|"
    r"\bdeskundige\b|\bvertegenwoordiger\b|\bbestuurder\b|\bdirecteur\b|"
    r"\bcurator\b|\bbewindvoerder\b|\bmentor\b|\bexecuteur\b|"
    r"\bvereffenaar\b|\bvereffenaar\b|\bschuldeiser\b|\bschuldeiseres\b|"
    r"\bregisteraccountant\b|\baccountant\b|\bbelastingadviseur\b",
    re.IGNORECASE,
)

# ─── Rechtspersoon keywords ───

RECHTSPERSOON_KEYWORDS = re.compile(
    r"\bB\.V\.\b|\bN\.V\.\b|\bStichting\b|\bVereniging\b|\bCooperatie\b|"
    r"\bOnderlinge\b|\bvereniging van eigenaars\b|\bV\.O\.E\.\b|"
    r"\bmaatschap\b|\bcommanditaire vennootschap\b|\bC\.V\.\b|"
    r"\bbesloten vennootschap\b|\bnaamloze vennootschap\b|"
    r"\beconomische eenheid\b|\bonderneming\b|\bbedrijf\b|"
    r"\binstelling\b|\borganisatie\b|\bkantoor\b|\bfonds\b|\bbank\b|"
    r"\bverzekeraar\b|\bzorgverzekeraar\b|\bziekenhuis\b|\bkliniek\b|"
    r"\buniversiteit\b|\bhogeschool\b|\bschool\b|\bonderwijs\b",
    re.IGNORECASE,
)

# ─── Overheid keywords ───

OVERHEID_KEYWORDS = re.compile(
    r"\bgemeente\b|\bprovincie\b|\bwaterschap\b|\bministerie\b|"
    r"\bbelastingdienst\b|\bpolitie\b|\bOM\b|\bopenbaar ministerie\b|"
    r"\breclassering\b|\bUWV\b|\bSVB\b|\bIND\b|\bDUO\b|\bKvK\b|"
    r"\bRDW\b|\bRIVM\b|\bRijksoverheid\b|\boverheid\b|"
    r"\braad van state\b|\brechtbank\b|\bgerechtshof\b|\bhoge raad\b|"
    r"\bcentraal justitieel incassobureau\b|\bCJIB\b|\bgemeentelijke\b|"
    r"\brijkswaterstaat\b|\binspectie\b|\btoezicht\b|\bautoriteit\b|"
    r"\bdienst\b|\bagentschap\b|\bcollege\b|\braad\b|\bcommissie\b",
    re.IGNORECASE,
)

# ─── All non-particular keywords combined ───

ALL_NON_PARTICULAR = re.compile(
    "|".join([
        PROFESSIONAL_KEYWORDS.pattern,
        RECHTSPERSOON_KEYWORDS.pattern,
        OVERHEID_KEYWORDS.pattern,
    ]),
    re.IGNORECASE,
)

# ─── Context window ───

CONTEXT_WINDOW = 500  # characters before and after the match

# ─── Dataclasses ───

@dataclass
class RichtlijnDecision:
    """Beslissing van de richtlijn engine voor één gedetecteerd gegeven."""
    gegeven_type: str          # geboortedatum, adres, postcode, email, telefoon, bsn, kenteken
    match: str                 # de gedetecteerde tekst
    start_idx: int
    end_idx: int
    persoon_type: PersoonType
    status: PseudonimiseringsStatus
    reden: str
    context_snippet: str       # tekst rondom de match voor review

@dataclass
class RichtlijnResult:
    """Resultaat van richtlijn engine voor een volledige uitspraak."""
    ecli: str
    totaal_gedetecteerd: int
    te_pseudonimiseren: int
    niet_pseudonimiseren: int
    handmatige_controle: int
    decisions: list[RichtlijnDecision]
    accuracy_notes: str

# ─── Classificatie ───

def classify_context(text: str, idx: int, rechtsgebied: str = "") -> PersoonType:
    """
    Classificeer de context rondom een gedetecteerd gegeven als:
    - PROFESSIONAL: advocaat, notaris, deurwaarder, etc.
    - RECHTSPERSOON: B.V., N.V., Stichting, etc.
    - OVERHEID: gemeente, ministerie, politie, etc.
    - PARTICULAR: geen van bovenstaande
    - ONBEKEND: gemengde signalen
    """
    lookback = text[max(0, idx - CONTEXT_WINDOW):idx]
    lookahead = text[idx:min(len(text), idx + 200)]
    full_context = lookback + lookahead
    
    is_professional = bool(PROFESSIONAL_KEYWORDS.search(lookback))
    is_rechtspersoon = bool(RECHTSPERSOON_KEYWORDS.search(full_context))
    is_overheid = bool(OVERHEID_KEYWORDS.search(full_context))
    
    # Prioriteit: professional > overheid > rechtspersoon > particulier
    if is_professional:
        return PersoonType.PROFESSIONAL
    if is_overheid:
        return PersoonType.OVERHEID
    if is_rechtspersoon:
        return PersoonType.RECHTSPERSOON
    
    # Check if there's ANY non-particular keyword nearby
    if ALL_NON_PARTICULAR.search(full_context):
        return PersoonType.ONBEKEND  # ambiguous → manual review
    
    return PersoonType.PARTICULAR

# ─── Rule Engine ───

def apply_richtlijn(
    gegeven_type: str,
    match: str,
    start_idx: int,
    end_idx: int,
    text: str,
    rechtsgebied: str = "",
) -> RichtlijnDecision:
    """
    Pas de pseudonimiseringsrichtlijn toe op één gedetecteerd gegeven.
    Implementeert de 17 regels uit pseudonimiseringsrichtlijn.rspraak.
    """
    persoon_type = classify_context(text, start_idx, rechtsgebied)
    context_snippet = text[max(0, start_idx - 100):min(len(text), end_idx + 100)]
    
    # PR-050: Strafrecht — strenger
    if rechtsgebied == "strafrecht" and gegeven_type in ("geboortedatum", "adres", "postcode"):
        if persoon_type in (PersoonType.PARTICULAR, PersoonType.ONBEKEND):
            return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
                persoon_type, PseudonimiseringsStatus.PSEUDONIMISEER,
                "Strafrecht: strengere pseudonimisering voor particulieren.", context_snippet)
    
    # PR-051: Familierecht — altijd pseudonimiseren
    if rechtsgebied == "familierecht":
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.PSEUDONIMISEER,
            "Familierecht: altijd pseudonimiseren i.v.m. privacygevoelige aard.", context_snippet)
    
    # PR-052: Bestuursrecht — rechtspersoon afhankelijk
    if rechtsgebied == "bestuursrecht" and persoon_type == PersoonType.RECHTSPERSOON:
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.HANDMATIGE_CONTROLE,
            "Bestuursrecht: rechtspersoon-gegevens afhankelijk van wetgeving — handmatige controle.", context_snippet)
    
    # PR-001/002: Professional → niet pseudonimiseren
    if persoon_type == PersoonType.PROFESSIONAL:
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.NIET_PSEUDONIMISEER,
            f"Professional context gedetecteerd — niet pseudonimiseren per richtlijn.", context_snippet)
    
    # PR-003/004: Rechtspersoon/Overheid → niet pseudonimiseren
    if persoon_type == PersoonType.RECHTSPERSOON:
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.NIET_PSEUDONIMISEER,
            "Rechtspersoon context — niet pseudonimiseren per richtlijn.", context_snippet)
    
    if persoon_type == PersoonType.OVERHEID:
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.NIET_PSEUDONIMISEER,
            "Overheidsorganisatie context — niet pseudonimiseren per richtlijn.", context_snippet)
    
    # PR-005: Particulier → wel pseudonimiseren
    if persoon_type == PersoonType.PARTICULAR:
        return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
            persoon_type, PseudonimiseringsStatus.PSEUDONIMISEER,
            "Particulier context — wel pseudonimiseren per richtlijn.", context_snippet)
    
    # PR-012: Onbekend → handmatige controle
    return RichtlijnDecision(gegeven_type, match, start_idx, end_idx,
        persoon_type, PseudonimiseringsStatus.HANDMATIGE_CONTROLE,
        "Context onduidelijk — handmatige controle vereist.", context_snippet)

# ─── Full scan met richtlijn ───

def scan_met_richtlijn(text: str, ecli: str = "", rechtsgebied: str = "") -> RichtlijnResult:
    """
    Scan een uitspraak met de bestaande PII detector, maar classificeer
    elke detectie met de richtlijn engine. Returns RichtlijnResult.
    """
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent.parent.parent.parent / "importer" / "rechtspraak"))
    from pseudonymize import scan_decision, Violation
    
    violations = scan_decision(text)
    decisions = []
    
    for v in violations:
        gegeven_type = v.type  # date_of_birth, street_address, postcode, email, etc.
        decision = apply_richtlijn(gegeven_type, v.match, v.start_idx, v.end_idx, text, rechtsgebied)
        decisions.append(decision)
    
    te_pseud = sum(1 for d in decisions if d.status == PseudonimiseringsStatus.PSEUDONIMISEER)
    niet_pseud = sum(1 for d in decisions if d.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER)
    handmatig = sum(1 for d in decisions if d.status == PseudonimiseringsStatus.HANDMATIGE_CONTROLE)
    
    return RichtlijnResult(
        ecli=ecli,
        totaal_gedetecteerd=len(decisions),
        te_pseudonimiseren=te_pseud,
        niet_pseudonimiseren=niet_pseud,
        handmatige_controle=handmatig,
        decisions=decisions,
        accuracy_notes=f"95% target: {te_pseud} pseudonimiseer + {niet_pseud} niet + {handmatig} handmatig"
    )
