#!/usr/bin/env python3
import json, sys, re

RE_HEX64 = re.compile(r"^[0-9a-f]{64}$")

def err(msg):
    print(f"[ERROR] {msg}", file=sys.stderr); sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: validate_packet.py <packet.json>"); sys.exit(2)
    path = sys.argv[1]
    try:
        pkt = json.load(open(path, "r", encoding="utf-8"))
    except Exception as e:
        err(f"Failed to load JSON: {e}")

    # Basic required fields
    for k in ("spec","human_anchor","sha256","sha256_b64","sig"):
        if k not in pkt: err(f"Missing required field: {k}")
    if "version" not in pkt["spec"]: err("Missing spec.version")
    if not RE_HEX64.match(pkt["sha256"]): err("sha256 must be 64 lowercase hex chars")

    # If authorship_signature present, check structure
    asig = pkt.get("authorship_signature")
    if asig:
        for k in ("algo","scheme","signed_field","message_hex","sig_b64"):
            if k not in asig: err(f"authorship_signature missing field: {k}")
        if asig["algo"] != "ed25519": err("authorship_signature.algo must be ed25519")
        if asig["scheme"] != "minisign": err("authorship_signature.scheme must be minisign")
        if asig["signed_field"] not in ("sha256","seed32.hex"):
            err("authorship_signature.signed_field must be 'sha256' or 'seed32.hex'")
        if not RE_HEX64.match(asig["message_hex"]): err("authorship_signature.message_hex must be hex64")
    print("[OK] Packet structure looks valid.")

if __name__ == "__main__":
    main()
