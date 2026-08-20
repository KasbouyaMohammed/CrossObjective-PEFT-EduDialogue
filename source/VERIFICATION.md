# Source package verification

The public source package was independently rechecked before journal submission.

## Verified archive

The files in `source/archive_parts/` reconstruct, through `source/rebuild_source_archive.py`, the audited archive:

```text
dldg_source_code_full.tar.xz
SHA256: bf3a4392ee4ccfe0839fff6c849791eadfdaace53fac7a09fe223b609b9715f6
```

All ten public Base64 chunk files were checked against the locally verified archive by Git blob SHA-1 and byte size. The reconstructed archive is byte-identical to the audited local source archive.

The archive extracts successfully and contains the experiment engine, required shared LoRA/model utilities, Phase-2 launcher, both CPU integrity suites, analysis/regeneration scripts, protocol, environment requirements, and reproducibility documentation.

`SHA256SUMS_SOURCE_FILES.txt` was also checked against the extracted archive; all listed source-file hashes match.

## Rebuild

From the repository root:

```bash
python source/rebuild_source_archive.py
mkdir -p source/reconstructed
tar -xJf source/dldg_source_code_full.tar.xz -C source/reconstructed
```

The rebuild script fails if the chunk set/order or final SHA256 is incorrect.

Verification date: 2026-08-20.
