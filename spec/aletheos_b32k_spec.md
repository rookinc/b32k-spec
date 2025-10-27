# Aletheos.AI Bootloader & B32k Specification

**Spec Version:** 0.1.0 (covers Packet v1.3)  
**Status:** Public Draft

## 1. Scope
This specification defines the canonical packet format, operators, and provenance
fields for the Aletheos.AI Bootloader (EYE law) and B32k mapping.

## 2. Packet (v1.3) — Required Fields
- `spec.version` — string (semver of this packet spec)
- `operators` — string (law summary, e.g., `EYE(a):=REV(a); EYE^2=I`)
- `seed` — description of 15-bit big-endian seed usage
- `sha256`, `sha256_b64` — canonical JSON digest over sorted/minified JSON
- `human_anchor` — with `descriptor`, `value`; optional `public_key_binding`
- `authorship_signature` — optional Ed25519/minisign signature over `sha256`
- `sig` — free-form lineage stamp (human-readable)

See JSON Schema in `schema/b32k_packet_v1_3.schema.json`.

## 3. Canonicalization
Canonical JSON = UTF-8, `separators=(",", ":")`, `sort_keys=True`.

## 4. Operators
- `EYE(a):=REV(a)` with closure `EYE^2=I`

## 5. Security
- Packet integrity by SHA-256 over canonical JSON.
- Authorship via ORCID-bound Ed25519/minisign.

## 6. Versioning
- Backward-compatible field additions bump MINOR.
- Schema-incompatible changes bump MAJOR.
