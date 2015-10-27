#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse, os, sys
from lipsync_tools import LipsSyncor

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fname", help = "path to the wav file to be processed.", dest = "fname")

def main(args):
    fname = args.fname
    _, ext = os.path.splitext(fname)
    assert ext == ".wav", "Only support wav files."

    fname = os.path.abspath(fname)
    syncor = LipsSyncor(fname)

    params = syncor.get_sync_params()
    print params.tolist()

if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
