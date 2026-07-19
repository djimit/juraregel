#!/bin/bash
# JuraRegel Gemeente Starter Kit
# Start een volledige compliance-pilot voor uw gemeente

echo "=========================================="
echo "  JuraRegel Gemeente Starter Kit v4.1.0"
echo "=========================================="
echo ""

# Stap 1: Registreer organisatie
echo "[1/5] Organisatie registreren..."
curl -X POST http://localhost:8527/v1/cloud/organisations \
  -d "name=Gemeente Voorbeeld" \
  -d "contact_email=ict@gemeente-voorbeeld.nl" \
  -d "plan=pro"

# Stap 2: Start BIA
echo "[2/5] Business Impact Analyse..."
curl -X POST http://localhost:8524/v1/bia-biv-dpia/calculate \
  -H "X-API-Key: JOUW_API_KEY" \
  -d '{"procesNaam":"Belastingheffing","impactNiveau":"kritiek","hersteltijd":4}'

# Stap 3: Check DPIA verplichting
echo "[3/5] DPIA check..."
curl -X POST http://localhost:8525/v1/dpia-generator/calculate \
  -H "X-API-Key: JOUW_API_KEY" \
  -d '{"dpiaVerplicht":"ja","dpiaUitgevoerd":"nee"}'

# Stap 4: Genereer advies
echo "[4/5] AI-Adviser analyse..."
curl -X POST http://localhost:8527/v1/cloud/organisations/ORG_ID/compliance \
  -H "X-API-Key: JOUW_API_KEY"

# Stap 5: Toon dashboard
echo "[5/5] Dashboard openen..."
echo "Open http://localhost:8527/dashboard voor het executive dashboard"

echo ""
echo "=========================================="
echo "  Pilot gestart! Volg de stappen in de"
echo "  documentatie voor volledige implementatie."
echo "=========================================="
