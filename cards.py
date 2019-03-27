#!/usr/bin/env python3

import argparse
import os
import filecmp
import subprocess
import shutil
import sys
import platform
import typing
import json
import re
from enum import Enum

def svg_to_png(svg, png, id, dpi):
    subprocess.check_output(['inkscape', svg, '-e', png, '-i', id, '-d', dpi])

def get(name, o):
    if name in o:
        return o[name]
    else:
        print('missing ', name)
        return None

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    cwd = os.getcwd()

    parser = argparse.ArgumentParser(description='aur helper tool')
    parser.add_argument('cmd', help='json cmd file')
    args = parser.parse_args()
    cmd = []
    with open(args.cmd, 'r') as f:
        cmd = json.load(f)

    for c in cmd:
        svg = get('svg', c)
        dpi = get('dpi', c)
        sub = get('sub', c)
        if svg is None:
            return
        if dpi is None:
            return
        if sub is None:
            return
        for d in dpi:
            for s in sub:
                id = get('id', s)
                png = get('png', s)
                if id is None:
                    return
                if png is None:
                    return
                dpi_str = str(d)+'dpi'
                print(dpi_str, png)
                png = os.path.join(cwd, dpi_str, png + '.png')
                ensure_dir(png)
                svg_to_png(svg, png, id, str(d))



if __name__ == "__main__":
    main()

