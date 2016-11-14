import sys
m = False
for d in sys.stdin.read():
    c = ord(d)
    if c != 0x83:
        d = c ^ 32 if m else c
        sys.stdout.write(chr(d))
        m = False
    else:
        m = True
