peylogger
=========

A tiny linux X11 keylogger implemented in python

### Usage

`peylogger.py -o your_output_file.peylog` saves the timestamped keydown and keyup events.

`dump_keys.py` is an example logfile parser/analyzer.

Peylogger captures pure keyboard events, so keymap information is required to extract the pressed characters.
`xmodmap -pke` lists the current keymap table.


### License

The project is licensed under MIT license.
