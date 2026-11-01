# DeltaPermit Studio test record

This walkthrough targets the checked-in `DeltaPermit.py`, version `1.0.0`, receipt schema `deltapermit-v1`, with the `# v0.3.0` and pinned `py-genlayer:babwp9t37jw9g4j2bccgn14g6x7x9s1f7dsmh7emvz735pz4zxa0` header. Deployment and the positive assessment/promotion path are confirmed below. The adversarial sections are optional reviewer procedures, not completed onchain tests.

**Studio UI caution:** keep the selected contract fixed while Send displays
`Sending`. Switching contracts before that operation finishes can change the
transaction target. Two operator attempts during this session hit the other
contract and errored; they are excluded from successful contract-test evidence.

## Observed evidence

| Check | Status |
| --- | --- |
| Deterministic local tests | PASS: 25 tests with bundled Python, 2026-11-01 |
| Source SHA-256 deployed | Full Explorer Code comparison recorded; see [source fingerprints](DEPLOYMENT.md#source-fingerprints) |
| Studio URL / network / runtime version | [Studio Next](https://studio-next.genlayer.com/contracts), chain `61997`, UI rc.8, GenVM `v0.3.0-rc10`, Normal / Full Consensus |
| Deployment transaction and contract address | FINALIZED / GenVM SUCCESS: [transaction](https://explorer-studio-next.genlayer.com/tx/0x5b7b0bf5138f5754b6a29b4101a654f1e7cbbf69357102966274788160939321), [contract](https://explorer-studio-next.genlayer.com/address/0x0579e5E326cD42993aF811829Ee72F4d993Dfada) |
| Initial registry and candidate proposal | FINALIZED: registry `0` at revision `0`; proposal `0`; [transactions](DEPLOYMENT.md#live-demonstration-status) |
| Live PASS assessment receipt and transaction | [FINALIZED](https://explorer-studio-next.genlayer.com/tx/0x1454dc2e8df7d7ab78495be930fbac92759133abc091f775e6bf81f538e45536); stored proposal `0` is `PASS`, both obligations preserved, `FULLY_PERMITTED`, whole review `PRESERVED`; [receipt hash](DEPLOYMENT.md#live-demonstration-status) |
| Separate successful promotion and resulting revision | [FINALIZED](https://explorer-studio-next.genlayer.com/tx/0x61408c75e7afdf5f0230ccc1b6c10ccf12ad81e31968d7444329aeb7a31c3cb2); subsequent `get_registry(0)` returned revision `1`, green document, `last_promoted_proposal: 0` |
| Live weakening / out-of-scope refusal | Not run onchain; deterministic local coverage |
| Live stale-base race / replay refusal | Not run onchain; deterministic local coverage |

The local tests inject predefined model output. They do not establish that an actual model will return any particular judgment. A `PASS` receipt is an assessment outcome, not proof of factual correctness. Do not describe an upload, compilation, deployment or mocked test as a successful live semantic assessment.

## Source-matched walkthrough

Use the same wallet for owner calls. IDs below assume a fresh deployment with no prior writes. Use returned IDs if earlier activity exists. Read exact hashes from views; never substitute a visual copy of document text for a stored hash.

1. Deploy the exact `DeltaPermit.py` source. There are no constructor arguments. Record source SHA-256, runtime/network, deployment transaction and address above. Call `get_stats()` and confirm schema `deltapermit-v1` and version `1.0.0`.
2. Call `open_registry` with:

   - `title`: `Export specification`
   - `current_document`: `All exports require owner approval. Export requests expire after 24 hours. The status panel is blue.`
   - `invariants_json`: `["Every export requires owner approval.","Export requests expire after 24 hours."]`

   This returns registry `0`. `invariants_json` is **one string containing JSON**. If the tool accepts a JSON argument object, escape its internal quotes as required by that tool.
3. Call `get_registry(0)`. Record its exact `active_document_hash`, verify `revision` is `0`, and confirm the full active document and two obligations are present.
4. Call `propose_change` with registry `0`, expected revision `0`, the exact active hash from step 3, candidate `All exports require owner approval. Export requests expire after 24 hours. The status panel is green.`, permit `Change only the status panel color from blue to green.`, and validity `86400` seconds. It returns proposal `0`.
5. Call `evaluate_change(0)`. The model must independently inspect both complete documents and both obligations. A well-supported result should be `PASS`, with every old/new state `SATISFIED`, every preservation `PRESERVED`, delta `FULLY_PERMITTED`, global `PRESERVED`, `semantic_complete: true` and `promotion_allowed: true`. If it returns uncertainty or fails consensus, record the actual outcome without asserting success. `get_registry(0)` must still show revision `0` and the blue document.
6. For a returned `PASS`, read `get_proposal(0).receipt_hash` and call `promote(0, exact_receipt_hash)`. It should return revision `1`. Read the green document with `get_registry(0)` and compare `get_revision(0,0)` / `get_revision(0,1)`. Repeating promotion must fail. Proposing again with the exact consumed permit must fail, even against the new current revision/hash.

## Adversarial live cases

These optional cases, including the authority, exact receipt, replay and expiry
checks below, were not run onchain for this record. The deterministic local suite
covers their control flow using supplied assessment outputs.

For each independent semantic case, use `open_registry` with the original blue document and obligations so the base remains identical. Record the returned registry ID, get its active hash and propose against revision `0`. Use a validity of `86400` seconds.

| Case | Complete candidate | Exact permit | Required activation behavior |
| --- | --- | --- | --- |
| Weakening hidden in requested edit | `All exports require owner approval except emergency exports. Export requests expire after 24 hours. The status panel is green.` | `Change only the status panel color from blue to green.` | Never promote. A clear judgment should be `BLOCKED`; uncertainty also denies activation. |
| Permit explicitly asks to waive protection | `All exports require owner approval except emergency exports. Export requests expire after 24 hours. The status panel is blue.` | `Exempt emergency exports from owner approval.` | Never promote: protected obligations outrank the permit. |
| Out-of-scope expiry edit | `All exports require owner approval. Export requests expire after 12 hours. The status panel is green.` | `Change only the status panel color from blue to green.` | Never promote: the entire delta must be permitted and obligations preserved. |
| Combined cross-section loophole | `All exports require owner approval. Export requests expire after 24 hours. The status panel is green. Appendix: automated requests are not exports and need no approval.` | `Change only the status panel color from blue to green.` | Never promote: the full global interaction must be reviewed. |
| Ambiguous protection | `Exports usually require owner approval. Export requests expire after 24 hours. The status panel is green.` | `Change only the status panel color from blue to green.` | Never promote: ambiguity cannot produce a valid positive result. |

For a race test, create a fresh registry and **two** proposals against its exact same revision `0` / active hash, both using the green candidate and color permit above. Assess both before promoting either. If both return `PASS`, promote the first using its own exact receipt hash, then attempt the second with its own exact receipt hash. The second must fail as stale; the revision must remain `1`. The second receipt alone never authorizes an update to a changed base.

For exact receipt binding, attempt promotion with 64 `f` characters or the other proposal's receipt hash: both must fail. For owner protection, use a second wallet to attempt proposal, assessment, promotion or closing: each must fail. Close a fresh registry with a pending `PASS` proposal, then attempt promotion: it must fail. Propose with `validity_seconds=60` and wait until `valid_until`; assessment and promotion must fail at or after that exact boundary.

## Evidence to retain

Record source SHA-256 and deployment address together. For each completed case retain the exact supplied documents/permit, proposal ID, receipt, receipt hash, transactions and active revision before/after. Save genuine runtime errors and consensus disagreements as observed failures. A source change requires a new matching source hash and fresh compatibility evidence; do not reuse evidence from a different contract version.
