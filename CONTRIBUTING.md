# Bijdragen aan JuraRegel

## Nieuwe Use Case Toevoegen

### 1. Maak de structuur
```
use-cases/<jouw-domein>/
├── regelspraak/
│   ├── begrippen.rspraak
│   └── regels-2025.rspraak
├── jrem/exports/
│   └── <domein>-2025.1.json
├── api/
│   └── app.py
├── lib/ (optioneel — parser)
└── tests/
    └── test_<domein>.py
```

### 2. Schrijf RegelSpraak
```
begrip maatregelId: "Unieke identificatie." type: tekst.
begrip compliant: "Voldoet?" waarden: ja, nee, onbekend.

regel UC-001 "Naam van je regel":
  als maatregelId is "UC-001"
  en implementatie is "ja"
  dan is compliant ja
  en is categorie "jouw-categorie".
```

### 3. Maak JREM export
Valideer: `python3 shared/validate.py --schema shared/jrem-schema.json --instance use-cases/<domein>/jrem/exports/*.json`

### 4. Maak Rule API
```python
from api_base import create_app
app = create_app("<domein>", jrem_path, <port>)
```

### 5. Schrijf tests
Minimaal: TestHealth, TestCheck, TestJREMValidation, TestIdempotentie, TestInputValidatie.

### 6. Run CI
```bash
bash ci/run-gates.sh use-cases/<domein>/
```

### 7. Submit PR
- Alle tests groen
- Alle CI gates PASS
- JREM export valideert
- Bronverwijzingen aanwezig per regel
