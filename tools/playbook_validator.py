#!/usr/bin/env python3
"""Playbook validator — checks structure and MCP tool references."""
import sys
from pathlib import Path

REQUIRED_SECTIONS = ['Wanneer', 'Stappen', 'Human Escalation', 'Voorbeeld']

def validate_playbook(path: Path) -> list[str]:
    """Validate a single playbook. Returns list of issues."""
    content = path.read_text()
    issues = []
    
    for section in REQUIRED_SECTIONS:
        if f'## {section}' not in content:
            issues.append(f'Missing section: {section}')
    
    # Check MCP tool reference
    if 'juraregel.' not in content:
        issues.append('No MCP tool reference found (juraregel.*)')
    
    return issues

def validate_all(playbooks_dir: str = 'docs/agent-playbooks') -> dict:
    """Validate all playbooks."""
    pb_dir = Path(playbooks_dir)
    if not pb_dir.exists():
        return {'valid': False, 'error': f'Directory {playbooks_dir} not found'}
    
    results = {}
    all_valid = True
    
    for pb_file in sorted(pb_dir.glob('*.md')):
        if pb_file.name == '_template.md':
            continue
        issues = validate_playbook(pb_file)
        results[pb_file.stem] = {'valid': len(issues) == 0, 'issues': issues}
        if issues:
            all_valid = False
    
    return {'valid': all_valid, 'playbooks': results, 'count': len(results)}

if __name__ == '__main__':
    result = validate_all()
    import json
    print(json.dumps(result, indent=2))
    
    if not result['valid']:
        for name, info in result.get('playbooks', {}).items():
            if not info['valid']:
                print(f'  {name}: {info["issues"]}')
    
    sys.exit(0 if result['valid'] else 1)
