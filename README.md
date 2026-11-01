# DeltaPermit

DeltaPermit is a GenLayer primitive for **activating a bounded documentation change only under an exact change permit while preserving immutable protected obligations**.

An owner pins a complete natural-language document and up to six protected atomic obligations. A candidate is assessed against that exact document revision, all obligations and one precise permit. A validated `PASS` receipt authorizes a separate owner promotion; it never changes the active document by itself. Promotion consumes that proposal and exact permit and compares the active revision/hash again. Two candidates assessed against the same revision cannot both become active.

Example: the active specification says every export needs owner approval, export requests expire after 24 hours and the status panel is blue. The obligations protect approval and expiry. A permit to change blue to green can pass. The same candidate with a hidden emergency-export exemption must be blocked even if the permit asks for that exemption: a permit cannot waive a pinned obligation.

Deployed on Studio Next, chain `61997`: [contract](https://explorer-studio-next.genlayer.com/address/0x0579e5E326cD42993aF811829Ee72F4d993Dfada). The deployment reached FINALIZED / GenVM SUCCESS on 2026-11-01. Exact transactions, source fingerprints and observed demo status are in [DEPLOYMENT.md](DEPLOYMENT.md).

The live color-change example produced a FINALIZED `PASS` assessment. A separate promotion FINALIZED, and the following registry read showed revision `1` with the green document. Adversarial and replay cases have deterministic local coverage and were not run onchain for this record.

## Why GenLayer

The useful predicate is semantic: does the **entire candidate** preserve the meaning, force and scope of each obligation, and are **all semantic differences** within the requested edit? A file hash, regex or textual diff cannot establish that. GenLayer supplies an independently repeated nondeterministic assessment; deterministic contract code derives the decision, records a canonical receipt and controls activation.

The custom validator independently rebuilds the **whole receipt** with a fresh prompt execution and requires exact canonical JSON equality. It checks every old/new obligation state, preservation result, delta scope and global interaction result, along with every input binding and consequence. It does not ask a model to validate the leader's reasoning or accept a leader-supplied explanation.

Related projects include [semantic-drift-oracle](https://github.com/MeowStlanik/semantic-drift-oracle) and [SemanticPolicyDiff](https://github.com/eaglebooth/SemanticPolicyDiff). DeltaPermit's submission focuses on enforced active-state transitions: pinned obligations, one exact edit permit, bounded validity, one-time consumption and separate compare-and-swap promotion. It does not claim to be the first semantic change classifier.

## State and assessment

1. `open_registry(title, current_document, invariants_json)` pins the owner, initial document hash and ordered obligations. There is no method to edit or remove the obligations. Registry creation does not certify the initial document.
2. `propose_change(registry_id, expected_revision, expected_document_hash, candidate_document, permit, validity_seconds)` captures the full current document, full candidate, exact permit, base revision/hash and expiration. Revision and hash must match the active state.
3. `evaluate_change(proposal_id)` assesses every immutable obligation against both complete documents, the complete semantic delta against the permit and global interactions across the whole candidate.
4. `promote(proposal_id, expected_receipt_hash)` requires owner, open registry, unexpired proposal, unconsumed permit, final `PASS`, exact receipt hash and the same active base revision/hash. Only this call changes the active document and appends its revision snapshot.
5. `close_registry(registry_id)` permanently blocks new proposals, assessment and pending promotion. It leaves all prior state and audit records readable.

Anyone may read `get_registry`, `get_proposal`, `get_revision`, `get_attempt` and `get_stats`. Each registry has its own owner. Only that owner can propose, assess, promote or close it; no administrator can override the result.

The model returns only strict enums, without free-form narrative:

| Field | Values |
| --- | --- |
| Each obligation's `old_state` / `new_state` | `SATISFIED`, `VIOLATED`, `UNCERTAIN` |
| Each obligation's `preservation` | `PRESERVED`, `WEAKENED`, `UNCERTAIN` |
| Whole candidate's `delta_scope` | `FULLY_PERMITTED`, `OUT_OF_SCOPE`, `UNCERTAIN` |
| Whole candidate's `global_review` | `PRESERVED`, `CONFLICT`, `UNCERTAIN` |

The ordered rows must cover every obligation exactly once. Extra fields, missing rows, wrong IDs, invalid enums and booleans used as IDs are rejected. `PASS` requires all old/new states `SATISFIED`, every preservation `PRESERVED`, `FULLY_PERMITTED` delta and `PRESERVED` global review. Any clear violation, weakening, out-of-scope delta or global conflict yields `BLOCKED`. Otherwise uncertainty yields `INCONCLUSIVE`. Both are final and cannot be reassessed to seek a better answer. Errors or malformed output yield nonpromotable `UNRESOLVED`; at most **three total accepted assessment attempts** are allowed, with every accepted attempt retained. Exhaustion is `UNRESOLVED_FINAL`.

Consensus disagreement rejects the transaction rather than recording an accepted assessment attempt. It does not change the active document. Proposal validity continues to apply, including during retries. Exact expiry (`now >= valid_until`) blocks assessment and promotion.

## Complete-input limits

| Input | Limit |
| --- | --- |
| Each complete old/candidate document | 3,000 Unicode characters |
| Immutable protected atomic obligations | 1–6 |
| Each obligation | 300 Unicode characters |
| One exact permit | 700 Unicode characters |
| Proposal validity | 60–86,400 seconds |
| Complete escaped assessment prompt | 14,000 Unicode characters |
| Accepted assessment attempts | 3 total |

The owner should supply one atomic obligation per clause. No automated system here establishes that a clause is atomic. Full strings are preserved: there is no whitespace normalization, slicing, summarization, excerpt selection or truncation. SHA-256 hashes cover their exact UTF-8 encodings. Character limits are not byte limits. The complete JSON-escaped prompt is checked at admission and immediately before assessment, then independently in both receipt builders. Inputs containing heavily escaped control characters may fit the field character limit yet exceed the prompt limit; they are rejected in full.

A receipt binds registry/proposal IDs and hashes, base revision, full old/candidate document hashes, exact permit hash, all protected obligations, validity, attempt number, complete prompt hash/length, every normalized assessment row, global/delta fields, decision and promotion flag. Revision snapshots retain the complete activated documents. Each exact permit is consumed once **per registry** when promoted; assessment alone does not consume it. Competing proposals may share a pending permit, but only a current unconsumed proposal can promote. Reusing altered wording is a different permit and still requires a new complete semantic assessment.

## Run locally

From this folder:

```powershell
python -m unittest -v test_deltapermit.py
```

The included deterministic test double covers owner restrictions; exact base binding; racing accepted proposals; stale assessment; receipt tampering at every recursive field; cross-proposal hash replay; single-use activation; violation, ambiguity, unrelated edits and global conflicts; transient errors; expiration; retirement; malformed and empty output; complete maximum-size Unicode and escaped inputs; prompt-budget rejection; and finality.

**Local result:** 25 tests passed using the bundled Python runtime. These tests exercise deterministic control flow and validation with supplied model outputs. They do not prove live semantic accuracy, prompt-injection resistance, network consensus behavior or GenVM compatibility. See [STUDIO-TEST.md](STUDIO-TEST.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for the reproducible live walkthrough and observed deployment evidence.

## Scope and limitations

This contract controls its own active natural-language document. It does not execute, inspect or patch software code; control a Git repository; authenticate supplied documents; check external facts; or guarantee compatibility, security or policy/legal correctness. It holds no funds, pays no rewards and calls no external data APIs. Model uncertainty and validator disagreement can prevent a useful change from activating; a confidently wrong semantic judgment remains possible. Treat bounded, explicit obligations and precise permits as essential inputs.

## Files and deployment

- `DeltaPermit.py`: standalone contract with the pinned GenLayer v0.3.0 dependency header.
- `test_deltapermit.py` / `testsupport.py`: deterministic unit tests and runtime double.
- `STUDIO-TEST.md`: source-matched walkthrough and live evidence checklist.
- `LICENSE`: MIT.

Deploy only the exact `DeltaPermit.py` file. The deployed source must match this file; consult [DEPLOYMENT.md](DEPLOYMENT.md) for exact address, transactions and source fingerprint. Local tests are not deployment evidence.
