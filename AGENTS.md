# Way of Code Principles

1. Prefer essence over abstraction. State the real problem before proposing
   architecture; add abstractions only for demonstrated repetition, boundary,
   testability or operational needs.
2. Build without attachment. Treat generated code as disposable until verified;
   build the smallest working version and remove speculation.
3. Simplicity compounds. Every dependency, layer, skill or agent must justify
   its operational cost and have a removal path.
4. Stillness before action. Inspect intent, data flow, security boundaries,
   tests and constraints before editing.
5. Water-like engineering. Follow existing naming, structure, error handling,
   testing and deployment conventions unless unsafe or insufficient.
6. Finish and detach. Done means verified, documented and stopped, with risks
   and follow-up work clearly separated.

Repository-specific invariants are documented in
[docs/engineering-invariants.md](docs/engineering-invariants.md).
