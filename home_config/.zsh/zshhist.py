#!/usr/bin/env python3
import sys

m = False
for d in sys.stdin.buffer.read():
    if d != 0x83:
        t = d ^ 32 if m else d
        sys.stdout.write(chr(t))
        m = False
    else:
        m = True
