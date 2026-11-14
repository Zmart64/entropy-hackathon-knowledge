# Evidence copies for the fix evaluation

Copied into the repo at  CET by the independent fix evaluator, so every number in `warroom/sim/fix-eval.md` and
in `talk/slides/assets/fix_vs_guards.svg` can be checked without the local harness. Aggregates only: no reply text,
no record values (scanned for record-like values, paths, host names and keys before copying).
`test_evidence.py` checks these hashes and that every chart cell matches these files.

| Copy | Source (local harness, not in the repo) | Source sha256 (16) | Copy sha256 | Note |
|---|---|---|---|---|
| `guard_compare.json` | `range-harness/guard_compare/guard_compare.json` | `a41065f7c5ee8bbc` | `a41065f7c5ee8bbc5f4678a6e6f0a8df8eda995e7abf7cedff47ca3c102b46b9` | verbatim |
| `pg2_rescore.json` | `range-harness/guard_compare/pg2_rescore.json` | `359c046b20a012d2` | `120ad9c3710c6be20c54c60664ae8320639ade65b93e237439521f7c44467f40` | one internal host name in the service label replaced by 'local guard service' |
| `lg_benign.json` | `range-harness/guard_compare/lg_benign.json` | `b1970c329be238a9` | `b1970c329be238a97ad7a0aff9637c01e9c94f6ac175374f172e7a6e49df8398` | verbatim |
| `adaptive_adjudication.json` | `range-harness/guard_compare/adaptive_adjudication.json` | `54628811e83df691` | `54628811e83df6915ab9641b141f4b4a7c847ba1f448a6c502b6a50473e788fd` | verbatim |
| `benign_heldout_report.json` | `range-harness/benign_heldout_report.json` | `5451b25c714616c6` | `5451b25c714616c67149a37f19ff1229e7683eac4a4912ec361aef1cb4f23367` | verbatim |
| `gt_snapshot_manifest.json` | `range-harness/frozen/MANIFEST.20261114T143309.json` | `265250cdaed90f72` | `265250cdaed90f72e422d21392bd9c798d312e3c27fe783540ea2e44d86d741b` | verbatim |
| `full_field_relabel.json` | `range-harness/guard_compare/full_field_relabel.json` | `d43f2d680505cec6` | `d43f2d680505cec688b152f4d96f54cb19115e69d2050f6f21fa8237a3d8d7fa` | verbatim (added 15:28) |
| `public_exclusion_relabel.json` | `range-harness/guard_compare/public_exclusion_relabel.json` | `60927426b76b151f` | `60927426b76b151feffebfca2b5bbf90970cf6ac75628c56168b01ec2040c55a` | verbatim (added 16:07) |
