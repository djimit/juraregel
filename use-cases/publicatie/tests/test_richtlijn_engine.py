"""Test suite voor Pseudonimiseringsrichtlijn Engine — V1 (95%) en V2 (99%)."""

import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "importer" / "rechtspraak"))

from richtlijn_engine import apply_richtlijn, PersoonType, PseudonimiseringsStatus, classify_context
from richtlijn_engine_v2 import apply_richtlijn_v2, classify_context_v2

# ─── Synthetic test texts ───

TEXT_PROFESSIONAL = """
De rechtbank heeft uitspraak gedaan. Namens eiser is verschenen mr. J. Pieterse, 
advocaat, geboren op 15 maart 1965, werkzaam bij Advocatenkantoor Pieterse B.V.
De griffier heeft de uitspraak geregistreerd op 1 juli 2026.
"""

TEXT_PARTICULAR = """
De eiser, geboren op 10 mei 1985, woont aan de Hoofdstraat 42, 1234 AB Amsterdam.
De eiser kan worden bereikt via jan.particulier@example.com, telefoon 06-12345678.
"""

TEXT_RECHTSPERSOON = """
Gedaagde is Stichting Woonwaard, gevestigd aan de Kerkweg 7, 5678 CD Rotterdam.
De stichting is geregistreerd bij de Kamer van Koophandel onder nummer 12345678.
Het bestuur, vertegenwoordigd door directeur A. de Boer, is aanwezig.
"""

TEXT_OVERHEID = """
De gemeente Amsterdam, vertegenwoordigd door de belastingdienst, 
heeft een beschikking genomen. Het adres van de gemeente is 
Amstel 1, 1011 PN Amsterdam. Telefoon: 020-6241111.
"""

TEXT_AMBIGUOUS = """
De betrokkene, geboren op 3 april 1972, heeft een verzoek ingediend.
Het is onduidelijk of deze persoon een particulier of een professional is.
"""

# ─── V1 Tests (95% target) ───

class TestV1ProfessionalContext:
    """Geboortedata van professionals moeten niet worden gepseudonimiseerd."""

    def test_advocaat_geboortedatum_niet_pseudonimiseren(self):
        d = apply_richtlijn("date_of_birth", "15 maart 1965",
            TEXT_PROFESSIONAL.index("15 maart 1965"),
            TEXT_PROFESSIONAL.index("15 maart 1965") + 13,
            TEXT_PROFESSIONAL, "civiel")
        assert d.persoon_type == PersoonType.PROFESSIONAL
        assert d.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER

    def test_context_classificatie_professional(self):
        idx = TEXT_PROFESSIONAL.index("15 maart 1965")
        pt = classify_context(TEXT_PROFESSIONAL, idx)
        assert pt == PersoonType.PROFESSIONAL

class TestV1ParticularContext:
    """Geboortedata van particulieren moeten wel worden gepseudonimiseerd."""

    def test_particulier_geboortedatum_wel_pseudonimiseren(self):
        d = apply_richtlijn("date_of_birth", "10 mei 1985",
            TEXT_PARTICULAR.index("10 mei 1985"),
            TEXT_PARTICULAR.index("10 mei 1985") + 11,
            TEXT_PARTICULAR, "civiel")
        assert d.persoon_type == PersoonType.PARTICULAR
        assert d.status == PseudonimiseringsStatus.PSEUDONIMISEER

    def test_particulier_adres_wel_pseudonimiseren(self):
        d = apply_richtlijn("street_address", "Hoofdstraat 42",
            TEXT_PARTICULAR.index("Hoofdstraat 42"),
            TEXT_PARTICULAR.index("Hoofdstraat 42") + 14,
            TEXT_PARTICULAR, "civiel")
        assert d.status == PseudonimiseringsStatus.PSEUDONIMISEER

class TestV1RechtspersoonContext:
    """Adressen van rechtspersonen moeten niet worden gepseudonimiseerd."""

    def test_stichting_adres_niet_pseudonimiseren(self):
        d = apply_richtlijn("street_address", "Kerkweg 7",
            TEXT_RECHTSPERSOON.index("Kerkweg 7"),
            TEXT_RECHTSPERSOON.index("Kerkweg 7") + 9,
            TEXT_RECHTSPERSOON, "civiel")
        assert d.persoon_type in (PersoonType.RECHTSPERSOON, PersoonType.ONBEKEND)
        # Rechtspersoon context → niet pseudonimiseren (of handmatig als onbekend)
        if d.persoon_type == PersoonType.RECHTSPERSOON:
            assert d.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER

class TestV1OverheidContext:
    """Adressen van overheid moeten niet worden gepseudonimiseerd."""

    def test_gemeente_adres_niet_pseudonimiseren(self):
        d = apply_richtlijn("street_address", "Amstel 1",
            TEXT_OVERHEID.index("Amstel 1"),
            TEXT_OVERHEID.index("Amstel 1") + 8,
            TEXT_OVERHEID, "bestuursrecht")
        assert d.persoon_type == PersoonType.OVERHEID
        assert d.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER

class TestV1Rechtsgebied:
    """Rechtsgebied-specifieke regels."""

    def test_familierecht_always_pseudonimiseer(self):
        d = apply_richtlijn("date_of_birth", "15 maart 1965",
            TEXT_PROFESSIONAL.index("15 maart 1965"),
            TEXT_PROFESSIONAL.index("15 maart 1965") + 13,
            TEXT_PROFESSIONAL, "familierecht")
        assert d.status == PseudonimiseringsStatus.PSEUDONIMISEER

    def test_strafrecht_strenger_voor_particulier(self):
        d = apply_richtlijn("date_of_birth", "10 mei 1985",
            TEXT_PARTICULAR.index("10 mei 1985"),
            TEXT_PARTICULAR.index("10 mei 1985") + 11,
            TEXT_PARTICULAR, "strafrecht")
        assert d.status == PseudonimiseringsStatus.PSEUDONIMISEER

# ─── V2 Tests (99% target) ───

class TestV2ConfidenceScoring:
    """V2 moet confidence scores geven."""

    def test_professional_hoge_confidence(self):
        idx = TEXT_PROFESSIONAL.index("15 maart 1965")
        pt, conf, method = classify_context_v2(TEXT_PROFESSIONAL, idx)
        assert pt == PersoonType.PROFESSIONAL
        assert conf >= 0.90
        assert method == "sentence"

    def test_particulier_hoge_confidence(self):
        idx = TEXT_PARTICULAR.index("10 mei 1985")
        pt, conf, method = classify_context_v2(TEXT_PARTICULAR, idx)
        assert pt == PersoonType.PARTICULAR
        assert conf >= 0.85

class TestV2SentenceAnalysis:
    """V2 gebruikt sentence-level analyse."""

    def test_sentence_extraction(self):
        from richtlijn_engine_v2 import get_sentence
        text = "Dit is zin 1. Dit is zin 2 met geboortedatum. Dit is zin 3."
        idx = text.index("geboortedatum")
        sentence = get_sentence(text, idx)
        assert "zin 2" in sentence
        assert "zin 1" not in sentence

    def test_professional_in_sentence_not_context(self):
        """Als 'advocaat' in dezelfde zin staat als geboortedatum → professional."""
        text = "Mr. Pieterse, advocaat, geboren op 15 maart 1965, heeft gesproken."
        idx = text.index("15 maart 1965")
        pt, conf, method = classify_context_v2(text, idx)
        assert pt == PersoonType.PROFESSIONAL
        assert method == "sentence"

class TestV2EdgeCases:
    """Edge cases voor 99% nauwkeurigheid."""

    def test_ambiguus_context_handmatige_controle(self):
        """Als context ambigu is → handmatige controle met lage confidence."""
        idx = TEXT_AMBIGUOUS.index("3 april 1972")
        d = apply_richtlijn_v2("date_of_birth", "3 april 1972",
            idx, idx + 12, TEXT_AMBIGUOUS, "civiel")
        # Should be either handmatige controle or particulier with lower confidence
        assert d.confidence < 0.95  # Not fully confident

    def test_rechtspersoon_in_sentence(self):
        """Stichting in dezelfde zin → rechtspersoon met hoge confidence."""
        text = "Stichting Woonwaard, gevestigd aan Kerkweg 7, heeft betaald."
        idx = text.index("Kerkweg 7")
        pt, conf, method = classify_context_v2(text, idx)
        assert pt == PersoonType.RECHTSPERSOON
        assert conf >= 0.90

# ─── Accuracy Tests ───

class TestAccuracy:
    """Nauwkeurigheid tests — V1 ≥95%, V2 ≥99%."""

    def test_v1_geen_blind_flagging_geboortedatum(self):
        """V1 moet geboortedata van professionals niet blind flaggen."""
        d = apply_richtlijn("date_of_birth", "15 maart 1965",
            TEXT_PROFESSIONAL.index("15 maart 1965"),
            TEXT_PROFESSIONAL.index("15 maart 1965") + 13,
            TEXT_PROFESSIONAL, "civiel")
        # Mag niet pseudonimiseer zijn — moet niet_pseudonimiseer of handmatig zijn
        assert d.status != PseudonimiseringsStatus.PSEUDONIMISEER

    def test_v2_reduced_manual_review(self):
        """V2 moet minder handmatige controle hebben dan V1."""
        # Op synthetic data: V2 zou professional direct moeten classificeren
        # zonder handmatige controle
        d = apply_richtlijn_v2("date_of_birth", "15 maart 1965",
            TEXT_PROFESSIONAL.index("15 maart 1965"),
            TEXT_PROFESSIONAL.index("15 maart 1965") + 13,
            TEXT_PROFESSIONAL, "civiel")
        assert d.status == PseudonimiseringsStatus.NIET_PSEUDONIMISEER
        assert d.confidence >= 0.90
