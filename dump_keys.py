from peylogger import struct_format
from struct import unpack, calcsize

def get_keymap(filename):
    keymap = {}
    # xmodmap modifiers
    # 0  Key
    # 1  Shift+Key
    # 2  mode_switch+Key
    # 3  mode_switch+Shift+Key
    # 4  AltGr+Key
    # 5  AltGr+Shift+Key

    with open(filename) as keymapfile:
        for line in keymapfile.readlines():
            line = filter(None, line.strip().split())
            keycode = int(line[1])
            values = line[3:]
            keymap[keycode] = values
    return keymap

def parse_keys(peyfilename, keymap, outfile):
    struct_size = calcsize(struct_format)
    with open(peyfilename, 'rb') as infile:
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
                    outfile.write(key_repr)
                elif key_repr == 'space':
                    outfile.write(' ')
                elif key_repr == 'Return':
                    outfile.write('\n')
                else:
                    outfile.write('<{0}>'.format(key_repr))

def argparser():
    import argparse
    from sys import stdout
    argp = argparse.ArgumentParser(description='peylogger keydumper')
    argp.add_argument('-o', '--output'
                     ,help      = 'Output file - default is STDOUT'
                     ,metavar   = 'FILE'
                     ,default   = stdout
                     ,type      = argparse.FileType('w')
                     )
    argp.add_argument('peylog'
                     ,metavar   = '[peylog file]'
                     ,help      = 'output file of peylogger.py'
                     )
    argp.add_argument('keymap'
                     ,metavar   = '[keymap file]'
                     ,help      = 'xmodmap keymap file - run `xmodmap -pke > your.keymap` to create keymaps'
                     )
    return vars(argp.parse_args())



def main():
    args = argparser()
    keymap = get_keymap(args['keymap'])
    parse_keys(args['peylog'], keymap, args['output'])


if __name__ == '__main__':
    main()
