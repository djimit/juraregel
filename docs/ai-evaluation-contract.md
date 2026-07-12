# AI/ML evaluation contract

LLM extraction and PII classification produce review proposals, never legal approval.

Every evaluation dataset must record corpus version/hash, annotation guideline version,
two independent annotators, adjudication status, model/provider/version, prompt hash,
and prediction timestamp. Raw personal data must not be written to audit metadata.

Release reports must include per-label TP/FP/FN, micro precision/recall/F1, abstention,
and results split by legal domain. PII releases additionally report the false-negative
rate for every identifier class. A release gate may only be set after an independently
annotated gold set exists; until then all results remain `evaluation-pending`.

Run `python tools/evaluate_predictions.py dataset.jsonl` for the dependency-free baseline.
