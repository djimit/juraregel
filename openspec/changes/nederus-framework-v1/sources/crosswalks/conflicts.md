# Inter-Framework Conflicts

Known conflicts between frameworks and their resolutions.

## Conflict 1: Incident Reporting Timing

**Frameworks**: NIS2 Art. 23 vs EU AI Act Art. 72

**Description**:
- NIS2 Art. 23 requires preliminary incident notification within **24 hours**
- EU AI Act Art. 72 allows **15 days** for initial serious incident report

**Resolution**: Apply most stringent requirement:
1. **24 hours**: Preliminary notification to national CSIRT (NIS2 compliance)
2. **72 hours**: Incident notification (NIS2 Art. 23(2))
3. **15 days**: Formal report to EU AI Office (EU AI Act Art. 72)
4. **1 month**: Final comprehensive report (NIS2 Art. 23(3))

**Impact on NED-05**: The NED-05 Incident Response control must support all four
timelines. Organizations should implement a single incident response process
that satisfies the most stringent deadline at each stage.

## Conflict 2: Risk Classification

**Frameworks**: EU AI Act Art. 6 vs BIO2 A.5-6

**Description**:
- EU AI Act uses 4-tier classification: prohibited / high-risk / limited / minimal
- BIO2 uses 4-tier classification: baseline / basis-uitgebreid / ernstig / zeer ernstig
- No direct mapping between these classification systems

**Resolution**: No direct mapping. Organizations maintain separate classifications:
- EU AI Act classification for AI-specific compliance (NED-01)
- BIO2 classification for information security compliance (outside NEDERUS scope)

**Impact on NED-01**: NED-01 maps EU AI Act classification only. BIO2 classification
is addressed in the BIO2 crosswalk and remains an organizational responsibility.

## Conflict 3: Provider vs User Obligations

**Frameworks**: EU AI Act Art. 16-20 vs BIO2 A.11

**Description**:
- EU AI Act distinguishes provider, deployer, importer, and distributor obligations
- BIO2 has a single set of controls for "the organization"

**Resolution**: NEDERUS controls are role-agnostic. Organizations must determine
which EU AI Act role(s) they fulfill and apply the relevant articles. NEDERUS
provides the unified control; the organization provides the role mapping.

**Impact on all controls**: Each NEDERUS control description includes the general
obligation. Organizations must supplement with role-specific EU AI Act articles.

## Adding New Conflicts

When you discover a new inter-framework conflict:
1. File an issue with the conflict description
2. Propose a resolution with rationale
3. Maintainer reviews and adds to this document
4. Update relevant crosswalks
