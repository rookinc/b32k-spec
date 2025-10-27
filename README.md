# Aletheos / B32k Specification

This repository is the **canonical home for the Aletheos.AI Bootloader & B32k** specifications,
schemas, examples, and conformance tests.

## Goals
- Publish a stable, citable spec (with DOI via Zenodo)
- Provide JSON Schemas + examples + test vectors
- Offer a reference validator for CI and implementers
- Track changes via semantic versioning and CHANGELOG

## Quick Start
- The spec lives in `spec/aletheos_b32k_spec.md`
- JSON Schema for packets: `schema/b32k_packet_v1_3.schema.json`
- Test vectors in `examples/`
- Run validation:
  ```bash
  python tools/validate_packet.py examples/B32K_C1110_EYE_PACKET_v1_3.json
  ```

## Versioning
- The spec uses **semver**: MAJOR.MINOR.PATCH
- Breaking changes bump **MAJOR**
- Additions that remain backward compatible bump **MINOR**
- Fixes/clarifications bump **PATCH**

## Citation
See `CITATION.cff` and Zenodo badge (to be added after first release).

---

**Human Anchor:** Scott Allen Cave — ORCID: 0009-0000-0888-4232
