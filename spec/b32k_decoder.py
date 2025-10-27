#!/usr/bin/env python3
# b32k_decoder.py — minimal skeleton for decoding a 14-glyph B32k frame

import zlib

BASE = 0x3400

def glyph_to_index(g):
    return ord(g) - BASE

def decode_frame(frame: str):
    assert len(frame) == 14, "Frame must contain 14 glyphs"
    words = [glyph_to_index(g) for g in frame]
    print("Decoded indices:", words)
    # Reassemble bits, check CRC per spec ... (left to implement)
    return words

if __name__ == "__main__":
    demo = "㐅㘑㐔㐞㑤㔂㓺㘲㐧㐲㐫㑆㐭㘥"  # example placeholder
    decode_frame(demo)
