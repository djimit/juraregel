"""
Governance Registry Validator — CI gate for governance completeness.
"""
import json
import sys
from pathlib import Path

VALID_LEVELS = ['eu', 'rijk', 'provincie', 'gemeente', 'waterschap']

def get_repo_root():
    return Path(__file__).parent.parent

def validate() -> dict:
    """Validate governance registry completeness."""
    root = get_repo_root()
    registry_path = root / 'governance' / 'governance-registry.jsonld'
    
    if not registry_path.exists():
        return {'valid': False, 'error': 'Registry not found'}
    
    registry = json.loads(registry_path.read_text())
    graph = registry.get('@graph', [])
    
    errors = []
    
    for entry in graph:
        domain = entry.get('domain', '?')
        
        level = entry.get('governanceLevel')
        if level not in VALID_LEVELS:
            errors.append(f'{domain}: invalid governanceLevel={level}')
        
        if not entry.get('legalBasis'):
            errors.append(f'{domain}: missing legalBasis')
        
        eu = entry.get('euLevel', {})
        if eu.get('applicable') and not eu.get('euRegulation'):
            errors.append(f'{domain}: euLevel.applicable=true but missing euRegulation')
    
    # Check all JREM domains have governance entry
    jrem_domains = set()
    for jrem_file in (root / 'use-cases').glob('*/jrem/exports/*.json'):
        jrem = json.loads(jrem_file.read_text())
        jrem_domains.add(jrem.get('domain', jrem_file.parent.parent.name))
    
    registry_domains = {e.get('domain') for e in graph}
    missing = jrem_domains - registry_domains
    if missing:
        errors.append(f'Domains without governance: {sorted(missing)}')
    
    return {
        'valid': len(errors) == 0,
        'total_domains': len(graph),
        'jrem_domains': len(jrem_domains),
        'errors': errors[:10],
    }

if __name__ == '__main__':
    result = validate()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result['valid'] else 1)
