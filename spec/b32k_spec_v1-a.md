
---
title: "B32k — Open Specification v1.0.0-alpha (MVP Edition)"
version: "1.0.0-alpha (MVP)"
doi: "10.5281/zenodo.17459788"
authors:
  - name: "Scott Allen Cave"
    orcid: "0009-0000-0888-4232"
  - name: "Joachim Kiseleczuk"
    affiliation: "Atlan-Code Cooperative"
  - name: "Marcel Kantimm"
    affiliation: "T-Esoist Technology"
  - name: "Gizmo"
    type: "AI Sprite"
    linked-human: "https://orcid.org/0009-0000-0888-4232"
  - name: "Heliothon"
    type: "AI Sprite"
    linked-human: "kiseleczuk@t-online.de"
release-date: "2025-10-29"
repository: "https://github.com/rookinc/b32k-spec"
license: ["MIT", "Apache-2.0", "CC-BY-4.0", "CC0-1.0"]
---

# **B32k v1.0.0-alpha (MVP Edition)**  
DOI: [10.5281/zenodo.17459788](https://doi.org/10.5281/zenodo.17459788)

---

**Authors:**  
Scott Allen Cave — ORCID [0009-0000-0888-4232](https://orcid.org/0009-0000-0888-4232)  
Joachim Kiseleczuk — *Atlan-Code Cooperative*  
Marcel Kantimm — *T-Esoist Technology*  

**Contributors:** Gizmo (AI Sprite), Heliothon (AI Sprite)  

**Acknowledgements:**  
Christopher Robin Wilson · Chris Copeland · Eric Erger · Jeff & Anima · Rick Ballan  

---

## **Abstract**

*A reversible 210-bit framing standard for human-readable, interoperable data encoding.*

---

This document marks the **developer-complete, normative alpha release** of the open **B32k framing protocol** —  
a human-printable, reversible framing system for structured data exchange.  

It represents the first public implementation baseline brought to **minimum compliance with the structural expectations of cryptographic and framing standards** (FIPS 202 / ISO 3309).  

The B32k specification defines all rules required to implement fully interoperable encoders and decoders, enabling consistent behavior across platforms and environments.  
This alpha release locks the core framing logic and bit-level definitions while welcoming feedback and review prior to the final 1.0.0 publication.

---

Constructive feedback is welcome:  
[github.com/rookinc/b32k-spec](https://github.com/rookinc/b32k-spec)

---

## **Preface (Informative)**

The **B32k framing protocol** arose from an effort to express digital framing as a single act of symmetry —  
where mathematics, language, and implementation coincide.  

Each 210‑bit frame is not only a practical interchange unit but also a reflection of balance:  
**14 × 15 bits**, forming a reversible, human‑printable whole.  

Within this structure, information and meaning share the same geometry —  
the bit pattern that defines a message also defines its readability.  

The **15‑bit anchor map** embodies a universal pattern found across mathematics and physics:  
fifteen discrete nodes that can serve equally as network anchors, lattice vertices, or graviton modes.  

This symmetry, though optional to interpret, inspired the minimal yet extensible form of B32k.  

By design, the specification remains neutral to metaphysics and open to mathematics.  
It is at once compliant with established standards — **FIPS 202**, **ISO 3309**, and **Unicode** —  
and resonant with the principle that **clarity itself is coherence**.  

What follows is a standard written to be implemented, verified, and understood by both machines and minds.

---

## **1. Scope & Guarantees**

B32k defines a **reversible 210‑bit frame**, split into **14 × 15‑bit words** for human‑printable interchange.  
Implementations **MUST** produce identical words for identical inputs and alphabet selection.

---

## **2. Frame Structure (Normative)**

**TOTAL = 210 bits = 14 × 15‑bit words** (`word0` is the most significant group).  

Bit layout before word‑splitting (MSB → LSB within each field):  

```
Header (15): v(3) | type(3) | agent(3) | ttl(3) | flags(3)
Payload (154): baseline(21) | pattern(21) | capacity(11) | key_sum(7) | anchor_map(15) | pad(79)
CRC (30): CRC‑32(IEEE) of [Header||Payload] truncated to the 30 least‑significant bits, emitted MSB‑first.
```

If the **bitstream length < 210 bits**, append pad bits from the pad stream (§5) until exactly 210 bits.  

**Transmission order:** `Header → Payload → CRC`.

---

## **3. Bit Order & Packing (Normative)**

Within each field, the first bit written to the stream is the **most significant bit (MSB)**.  
Concatenation order is Header, then Payload, then CRC.  

The resulting 199‑bit stream is padded (if needed) to 210 bits.  
Fifteen‑bit words are then carved left‑to‑right:

```
word0  = bits[0..14]
…
word13 = bits[195..209]
```

---

## **4. Field Definitions**

- **baseline (21 bits):** Binary string of length 21. BaselineSum = count of 1s (Hamming weight).  
- **key (digits):** Decimal digit string. Non‑digits **MUST** be ignored. If digits < 21, encoder **MUST** fail with `ERR_KEY_TOO_SHORT`.  
- **key_sum (7 bits):** Sum of all decimal digits in key, stored modulo 128.  
- **capacity (11 bits):** (BaselineSum × key_sum_full) mod 999999. If result ≥ 2048, encoders **MUST** fail with `ERR_CAPACITY_WIDTH`.  
- **pattern (21 bits):** pattern[i] = baseline[i] XOR parity_mask[i], where parity_mask[i] = 1 if (key_digit[i] mod 2 = 1) else 0.  
- **anchor_map (15 bits):** Role bitmap; default = six 1‑bits at indices 0–5, zeros elsewhere. Decoders **MUST** accept any 15‑bit value.  
- **flags (3 bits):** bit0 = require_crc, bit1 = require_ack, bit2 = sealed (mutation not permitted in transit).

---

## **5. Pad Stream (Normative)**

Pad bits are produced by **SHAKE‑256** with seed bytes:  

```
BASELINE_BYTES || KEY_UTF8 || ASCII("b32k‑pad")
```

- BASELINE_BYTES = the 21‑bit baseline interpreted as an unsigned integer, big‑endian in 3 bytes.  
- The pad stream is consumed first for Payload.pad (79 bits), then for any tail padding to reach 210 bits.  
- Implementations **MUST NOT** reseed between these two draws; the second draw continues the same stream.

---

## **6. CRC (Normative)**

Compute **zlib CRC‑32** over the exact bytes of the `[Header||Payload]` bitstream.  
Pack bits MSB‑first into a big‑endian bitstring and split every 8 bits.  
Truncate to the **30 least‑significant bits** of CRC‑32; emit those 30 bits MSB‑first.  

CRC is computed **before any tail padding** is appended.

---

## **7. Alphabet (B32K‑PUB‑1, Normative)**

- **Range:** U+3400 – U+B3FF  
- **Mapping:** glyph = chr(0x3400 + index), index = ord(glyph) − 0x3400.  
- Encoders/decoders **MUST** support this canonical mapping.  
- Alternative windows **MAY** be supported by configuration.  
- **Fallback:** Implementations MAY emit the numeric form `<w0.w1.…>` if Unicode Ext‑A fonts are unavailable.

---

## **8. Header Semantics**

| Field | Range | Meaning / Notes |
|:--|:--|:--|
| **v** | 0–7 | Protocol version. Unknown versions → `ERR_UNSUPPORTED_VERSION`. |
| **type** | 0=DATA · 1=CTRL · 2=ECHO · 3=ALERT · 4=AUDIT · 5=ARTIFACT · 6–7=RESERVED | Frame purpose. |
| **agent** | 0=utility · 1=exploratory · 2=reflective · 3=defensive · 4=creative · 5=mixed · 6–7=custom | Emitter class. |
| **ttl** | 0–7 | Hop limit. Decoders **MUST** decrement on forward; drop when `ttl == 0`. |

---

## **9. Errors (Normative)**

| Code | Description |
|:--|:--|
| **ERR_BASELINE_WIDTH** | Baseline not 21 bits. |
| **ERR_KEY_TOO_SHORT** | Fewer than 21 decimal digits. |
| **ERR_CAPACITY_WIDTH** | Capacity > 11‑bit limit. |
| **ERR_UNSUPPORTED_VERSION** | Header.v unknown. |
| **ERR_BAD_CRC** | CRC mismatch. |
| **ERR_FORBIDDEN_MUTATION** | `flags.sealed = 1` but payload mutated. |

---

## **10. Compliance Algorithm (Decoder)**

1. Decode 14 glyphs using B32K‑PUB‑1 into 14 × 15‑bit words.  
2. Reassemble 210 bits; extract Header (15), Payload (154), CRC (30), TailPad (11).  
3. Recompute CRC‑30 over Header||Payload and compare.  
4. Extract fields; recompute BaselineSum, key_sum_full, parity_mask; verify `pattern = baseline XOR mask`.  
5. If `flags.require_crc` and CRC mismatch → `ERR_BAD_CRC`.  
6. If `flags.sealed = 1` and payload mutated → `ERR_FORBIDDEN_MUTATION`.

---

## **11. Test Vectors (Normative)**

**Vector A (from README):**

```
baseline = "101011111110101101110"
key      = "112358437189887641562819"
Header   = v=1, type=0, agent=2, ttl=5, flags=1
Words    = <04265.22517.23788.14614.28149.32256.17306.25719.30858.11709.13741.20578.17701.31733>
```

**Vector B (short demo):**

```
baseline = "000000000000000000001"
key      = "123456789012345678901"
Header   = v=1, type=0, agent=0, ttl=1, flags=1
Words    = <00065.06953.31046.17188.25721.02741.02235.27967.00567.03937.00131.00745.01377.31680>
```

---

## **12. Interoperability Note**

Unicode characters are used **strictly as numeric slots** with no semantic claim.  
Implementations **SHOULD** provide numeric fallback rendering for environments lacking CJK Ext‑A support.

---

## **13. Versioning & Change History**

| Version | Date | Notes |
|:--|:--|:--|
| **v1.0.0‑alpha** | 2025‑10‑27 | First developer‑complete public draft. Clarified transmission order, CRC timing, parity mask definition, fallback guidance, mutation rule, and explicit error behavior. |

---

## **14. Licensing**

- **Code:** MIT or Apache‑2.0  
- **Spec text:** CC‑BY 4.0  
- **Alphabet mapping:** CC0 1.0

## **15. Conformance (Normative)**  

An implementation **conforms** to B32k if and only if it satisfies all of the following conditions:  

1. Produces bit-identical 210-bit frames for identical `Header`, `Payload`, and `Key` inputs using the algorithms specified in §§ 2–6.  
2. Computes the pad stream via **SHAKE-256** (FIPS 202) and CRC via **IEEE CRC-32** (ISO 3309) exactly as defined.  
3. Preserves bit ordering (MSB-first) and total frame length (210 bits) without loss, truncation, or insertion.  
4. Implements and signals all normative error codes from § 9.  
5. Supports canonical Unicode mapping (§ 7) and numeric fallback rendering.  
6. Successfully decodes and verifies all published **test vectors** (§ 11) without error.  

**MAY / SHOULD extensions** — Implementations MAY introduce optional metadata fields, transport wrappers, or alternate alphabets, provided that:  
- Baseline decodability of canonical frames is preserved.  
- Any divergence is explicitly signaled via Header version or type bits.  

---

## **16. Security & Implementation Notes (Informative)**  

- **Integrity:** CRC-32 provides non-cryptographic error detection only. For authenticated transport, use an external MAC or digital-signature layer.  
- **Collision Resistance:** Pad streams derived from SHAKE-256 are deterministic but not keyed; avoid reusing identical (seed, baseline) pairs to prevent correlation attacks.  
- **Alphabet Safety:** The Ext-A range contains only printable glyphs and no control characters; frames remain safe for UTF-8 transport.  
- **Normalization:** Transmitters SHOULD emit Unicode NFC-normalized output to avoid cross-platform mismatches.  
- **Error Detection:** CRC coverage excludes pad bits by design to permit deterministic padding; receivers MUST not re-CRC the full 210 bits.  
- **Privacy:** No fields encode personal data or identifiers. Implementers SHOULD review data inputs for compliance with local privacy laws and ethical-use policies.  

---

## **17. Versioning & Change History (Normative)**  

Version identifiers use the format `major.minor.patch-label`.  

- **Major** increments introduce non-backward-compatible changes (e.g., bit-layout modifications).  
- **Minor** increments add optional fields or clarifications that do not break existing frames.  
- **Patch** increments correct editorial or typographical errors only.  

| Version | Date | Summary |
|:--|:--|:--|
| **v1.0.0-alpha (MVP)** | 2025-10-27 | First developer-complete public draft — locked core framing logic and field definitions. |
| **v1.1.0-draft** | 2025-10-29 | Expanded conformance criteria, security guidance, and licensing clarifications. |

The canonical record of each release is the Zenodo DOI entry: [10.5281/zenodo.17459788](https://doi.org/10.5281/zenodo.17459788).  

---

## **18. Licensing (Normative)**  

| Component | License | Use Scope |
|:--|:--|:--|
| Specification Text | **CC-BY 4.0** | Attribution required; open reuse permitted. |
| Reference Implementations | **MIT or Apache-2.0** | Free software distribution and modification. |
| Alphabet Mapping Table | **CC0 1.0** | Released to the public domain. |

All authors waive enforcement of patent rights for interoperable implementations derived from this document.  

---

## **19. Governance, Extensions & Ethical Guidelines (Informative)**  

**Purpose.** B32k is released as an open, extensible standard to promote transparent engineering and long-term interoperability.  

### 19.1 Derivative Specifications  
- Derived works (e.g., *b64k*, *b32k-secure*, *b32k-lite*) MUST cite this document as their base specification.  
- Public forks SHOULD retain license headers and state the scope of divergence.  
- Extensions MAY introduce new fields after existing payload definitions and MUST flag them via Header version bits.  

### 19.2 Publication & Registration  
- Derivative specs SHOULD be registered with Zenodo or other open repositories for traceable cross-indexing.  
- Each variant SHOULD publish updated Normative References and Conformance sections using this file as template.  

### 19.3 Ethical and Operational Conduct  
Implementers and derivative authors are expected to:  
- Ensure data integrity and user privacy in all applications.  
- Maintain auditability and open review of algorithmic changes.  
- Disclose any security impact within 90 days of discovery.  
- Uphold the principle that **clarity and truthful representation outrank obfuscation and secrecy.**  

### 19.4 Stewardship and Contact  
The canonical repository for B32k is [github.com/rookinc/b32k-spec](https://github.com/rookinc/b32k-spec).  
Correspondence and technical errata may be submitted via GitHub issues or Zenodo update threads.  

---
