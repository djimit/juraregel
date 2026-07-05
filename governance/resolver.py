"""
Governance Resolver — resolves governance hierarchy for rules/domains.

Hierarchy: EU > Rijk > Provincie > Gemeente > Waterschap
"""
import json
from pathlib import Path

HIERARCHY = ['eu', 'rijk', 'provincie', 'gemeente', 'waterschap']

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
    """Check if one domain overrides another based on hierarchy."""
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
    
    try:
        d1_rank = HIERARCHY.index(d1_level)
        d2_rank = HIERARCHY.index(d2_level)
    except ValueError:
        return {'error': f'Unknown governance level: {d1_level} or {d2_level}'}
    
    return {
        'domain1': domain,
        'domain2': other_domain,
        'domain1_level': d1_level,
        'domain2_level': d2_level,
        'overrides': d1_rank <= d2_rank,
    }
