# DeltaPermit deployment record

## Confirmed deployment

Observed on **2026-11-01** in GenLayer Studio Next, using Normal / Full Consensus.
The deployment reached **FINALIZED** and the Explorer reported **GenVM SUCCESS**.
The constructor takes no arguments. The deployment used transaction value 0 GEN;
network fees are separate.

| Field | Observed value |
| --- | --- |
| Contract | [0x0579e5E326cD42993aF811829Ee72F4d993Dfada](https://explorer-studio-next.genlayer.com/address/0x0579e5E326cD42993aF811829Ee72F4d993Dfada) |
| Deployment transaction | [0x5b7b0bf5138f5754b6a29b4101a654f1e7cbbf69357102966274788160939321](https://explorer-studio-next.genlayer.com/tx/0x5b7b0bf5138f5754b6a29b4101a654f1e7cbbf69357102966274788160939321) |
| Studio | [Studio Next](https://studio-next.genlayer.com/contracts), UI release candidate rc.8 |
| RPC | `https://studio-next.genlayer.com/api` |
| Chain ID | `61997` |
| GenVM executor | `v0.3.0-rc10` |
| Contract version / receipt schema | `1.0.0` / `deltapermit-v1` |
| Python runner | `py-genlayer:babwp9t37jw9g4j2bccgn14g6x7x9s1f7dsmh7emvz735pz4zxa0` |

## Runtime compatibility

The source uses the two-line `# v0.3.0` / pinned `Depends` header. The runner pin
comes from the exact executor commit
[`2e094c6fdd7fb3b620706a2d20845e004fb6d298`](https://github.com/genlayerlabs/genvm-executor/blob/2e094c6fdd7fb3b620706a2d20845e004fb6d298/runners/support/versions/current.nix),
bundled by GenVM Manager `v0.6.0-rc10`. Its published `py-genlayer` SRI hash is
`sha256-WpfLJ0M8uJgSQlsZCoSQN0/U5C87c0id1N/OMtvk/1Q=`; the runner ID above is
that hash encoded as GVM32.

The rc10 executor uses GVM32 runner IDs. An obsolete or uninstalled pin can surface
as `invalid_contract runner malformed`, as shown by its
[runner-resolution code](https://github.com/genlayerlabs/genvm-executor/blob/2e094c6fdd7fb3b620706a2d20845e004fb6d298/executor/src/rt/supervisor/actions.rs).
Changing the dependency pin preserved this contract's storage, consensus and public
method APIs. A read-only schema check of the official Hello World source with this
pin succeeded before the contract deployment. The deployment result above supplies
the contract's own runtime compatibility evidence.

## Source fingerprints

| Fingerprint | SHA-256 |
| --- | --- |
| Local `DeltaPermit.py`, exact UTF-8 file | `e4b02b8fba7f13b6a1dac14f681ef2733cadc8b7a22cd2ccb97a9ec793e5331d` |
| Local source and full Explorer Code view, normalized | `a962589800e2385e48a41af44f491b2c2e01f8afa78ab371b4dbde7c31a715ba` |

The full Explorer Code tab's text and the local UTF-8 source were each normalized
by replacing CRLF with LF and trimming leading/trailing whitespace, including the
terminal newline. Internal whitespace was preserved. Their normalized text and
SHA-256 hashes matched. The exact local file hash differs because the comparison
trims boundary whitespace; this establishes normalized source equality, not raw
byte equality between the file and Explorer rendering.

## Live demonstration status

| Check | Observed status |
| --- | --- |
| Deployment and runtime execution | PASS: FINALIZED / GenVM SUCCESS |
| Initial registry | FINALIZED: registry `0`, active revision `0` |
| Safe color-change proposal | FINALIZED: proposal `0` |
| Safe color change receives a semantic `PASS` | PASS: assessment FINALIZED; stored proposal `0` reports `PASS` |
| Separate promotion activates revision 1 | PASS: promotion FINALIZED; `get_registry(0)` returned revision `1` and the green document |
| Weakening or out-of-scope refusal | Not run onchain; deterministic local coverage |
| Stale-base race / replay refusal | Not run onchain; deterministic local coverage |

The demo uses the complete export specification, two protected obligations and
color-change permit in [STUDIO-TEST.md](STUDIO-TEST.md). The 25 deterministic local
tests use supplied model outputs and remain separate from live-model and network
evidence. The optional adversarial, authority, expiry and replay walkthroughs were
not run onchain for this record.

Observed setup transactions:

- `open_registry`: [0x95144849a75b34a75f4a979def6f11bfd4e3c77719ca1e2c4309705d1fa5849b](https://explorer-studio-next.genlayer.com/tx/0x95144849a75b34a75f4a979def6f11bfd4e3c77719ca1e2c4309705d1fa5849b), FINALIZED; registry `0`, revision `0`.
- `propose_change`: [0xb47c1d382766de9bebca10660438f1db27eca889b75fc1afcdc41ced18e6488d](https://explorer-studio-next.genlayer.com/tx/0xb47c1d382766de9bebca10660438f1db27eca889b75fc1afcdc41ced18e6488d), FINALIZED; proposal `0`.
- `evaluate_change(0)`: [0x1454dc2e8df7d7ab78495be930fbac92759133abc091f775e6bf81f538e45536](https://explorer-studio-next.genlayer.com/tx/0x1454dc2e8df7d7ab78495be930fbac92759133abc091f775e6bf81f538e45536), FINALIZED. `get_proposal(0)` reported `PASS`, `promotion_allowed: true`, `semantic_complete: true`, and `prompt_truncated: false`. Both obligation rows reported `SATISFIED` for the old and candidate documents and `PRESERVED` for preservation. The overall fields were `FULLY_PERMITTED` and `PRESERVED`.

The accepted assessment's stored receipt hash is
`74d83f8cb278557d5f855faa9085992b3957d09a21614e2ba5d4b43d9599956a`.

Separate `promote(0, receipt_hash)` transaction
[0x61408c75e7afdf5f0230ccc1b6c10ccf12ad81e31968d7444329aeb7a31c3cb2](https://explorer-studio-next.genlayer.com/tx/0x61408c75e7afdf5f0230ccc1b6c10ccf12ad81e31968d7444329aeb7a31c3cb2)
was observed **FINALIZED**. A subsequent `get_registry(0)` returned revision `1`,
`last_promoted_proposal: 0`, and:

```text
All exports require owner approval. Export requests expire after 24 hours. The status panel is green.
```

The active document hash was
`f63e2b958434292ae8d9961bb0db1d2491f3b719962b1237aaf775ca5ee6ba64`.
Revision `0` had been observed with the blue document before promotion. These
observations demonstrate this example's distinct assessment and activation steps;
they do not establish semantic accuracy for other inputs.
