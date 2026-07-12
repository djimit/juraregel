"""
Governance Resolver — resolves governance hierarchy for rules/domains.

Hierarchy: EU > Rijk > Provincie > Gemeente > Waterschap
"""
import json
from pathlib import Path

def get_repo_root():
    return Path(__file__).parent.parent

def load_registry() -> dict:
    path = get_repo_root() / 'governance' / 'governance-registry.jsonld'
    if not path.exists():
        return {}
    return json.loads(path.read_text())

def resolve_governance(domain: str, location: dict = None) -> dict:
    """Resolve governance for a domain at a specific location."""
    registry = load_registry()
    graph = registry.get('@graph', [])
    
    entry = None
    for e in graph:
        if e.get('domain') == domain:
            entry = e
            break
    
    if not entry:
        return {'error': f'Domain {domain} not in governance registry', 'domain': domain}
    
    result = {
        'domain': domain,
        'governance_level': entry.get('governanceLevel', 'unknown'),
        'legal_basis': entry.get('legalBasis', ''),
        'delegated_to': entry.get('delegatedTo', []),
        'eu_context': entry.get('euLevel', {}),
        'local_variations': [],
    }
    
    if location:
        gemeente = location.get('gemeente')
        provincie = location.get('provincie')
        for variation in entry.get('localVariations', []):
            if variation.get('level') == 'gemeente' and variation.get('scope') == gemeente:
                result['local_variations'].append(variation)
            elif variation.get('level') == 'provincie' and variation.get('scope') == provincie:
                result['local_variations'].append(variation)
    
    return result

def check_override(domain: str, other_domain: str) -> dict:
    """Return evidence for legal conflict analysis; never infer override from level alone."""
    registry = load_registry()
    graph = registry.get('@graph', {})
    
    d1_level = None
    d2_level = None
    for e in graph:
        if e.get('domain') == domain:
            d1_level = e.get('governanceLevel')
        if e.get('domain') == other_domain:
            d2_level = e.get('governanceLevel')
    
    if not d1_level or not d2_level:
        return {'error': 'One or both domains not found'}
    
    return {
        'domain1': domain,
        'domain2': other_domain,
        'domain1_level': d1_level,
        'domain2_level': d2_level,
        'overrides': None,
        'decision': 'requires_legal_analysis',
        'required_factors': [
            'competence', 'jurisdiction', 'lex-superior',
            'lex-specialis', 'lex-posterior', 'validity-and-applicability',
        ],
    }
