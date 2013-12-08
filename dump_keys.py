from peylogger import struct_format
from struct import unpack, calcsize
from sys import argv
from sys import stdout

struct_size = calcsize(struct_format)

# xmodmap modifiers
# 0  Key
# 1  Shift+Key
# 2  mode_switch+Key
# 3  mode_switch+Shift+Key
# 4  AltGr+Key
# 5  AltGr+Shift+Key

keymap = {}

with open(argv[2]) as keymapfile:
    for line in keymapfile.readlines():
        line = filter(None, line.strip().split())
        keycode = int(line[1])
        values = line[3:]
        keymap[keycode] = values

with open(argv[1], 'rb') as infile:
    while True:
        chunk = infile.read(struct_size)
        if len(chunk) != struct_size:
            break
        key,pressed,timestamp = unpack(struct_format, chunk)
        if not key in keymap:
            continue
        key_repr = keymap[key][0]
        if pressed:
            if len(key_repr) == 1:
                stdout.write(key_repr)
            elif key_repr == 'space':
                stdout.write(' ')
            elif key_repr == 'Return':
                stdout.write('\n')
            else:
                stdout.write('<{0}>'.format(key_repr))
