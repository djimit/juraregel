# Autonomous Question Ledger

Questions are resolved here instead of interrupting the build. `resolved` means
an engineering default was selected; it does not mean legal approval.

| ID | Question | Resolution | Evidence | Status |
|---|---|---|---|---|
| Q-001 | Where should the first demo run? | Reuse the existing GitHub Pages playground. | `.github/workflows/pages.yml` already deploys `playground/`. | resolved |
| Q-002 | Should the profile get a calculate route? | No. Keep `catalog_only`; build a separate evidence-completeness demo. | Existing profile contract and `409 catalog_only` tests. | resolved |
| Q-003 | Should OpenMythos scores determine admission? | No. Preserve individual findings as evidence; hard stops cannot be compensated by scores. | JAI-009 and live deployment-block results. | resolved |
| Q-004 | Can Djimitflo logs prove meaningful human oversight? | No. They prove events and authority boundaries; substantive review remains a human gate. | Current trace/eval capability boundary. | resolved |
| Q-005 | Must LongCat be a runtime dependency? | No. The bundle accepts provider-neutral run evidence; a LongCat adapter can be added independently. | LongCat works outside Ollama; current OpenMythos adapter is not robust for its thinking response. | resolved |
| Q-006 | Is a new evidence database needed? | No. Generate deterministic static JSON and reuse existing stores by reference. | Three synthetic scenarios and a read-only demo need no mutable store. | resolved |
| Q-007 | May autonomous checks approve legal evidence? | No. They may mark evidence observed or failed; only the final human decision can admit. | JREM `manualReviewRequired=true` for every control. | resolved |
| Q-008 | Should Djimit.nl be changed now? | No. Deliver a portable GitHub Pages artifact and documented link/embed/fetch contract. | User allowed Djimit.nl **or Git**; Git is the existing lower-cost path. | resolved |
| Q-009 | Can the static demo be visually accepted autonomously? | No browser instance was exposed in this session. Validate generation, DOM-safety assertions and HTTP delivery now; defer visual acceptance to the publication gate. | In-app browser inventory was empty; local HTTP returned 200 for page and JSON. | final gate |

## Routing Rule

New questions follow this order:

1. repository and current runtime truth;
2. official source register;
3. OpenMythos behavioural evidence;
4. Djimitflo execution evidence;
5. Wiki/Knowledge as discovery support;
6. defer to a final human gate when the answer changes legal authority,
   publication, liability or production scope.
