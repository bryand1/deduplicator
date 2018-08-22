#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deduplicator

1. Input headlines from command-line
usage: python main.py

2. Input headlines from text file
usage: python main.py /path/to/text/file
"""
import pickle
import sys

import app

if __name__ == '__main__':
    print("\nDeduplicator")
    dedupe = app.Deduplicator()

    if len(sys.argv) == 1:
        _id = 1
        while True:
            headline = input("headline: ")
            dedupe.accept(str(_id), headline)
            dedupe.print_tree()
            _id += 1
    else:
        filepath = sys.argv[1]
        lines = open(filepath).readlines()
        n = len(lines)
        for i in range(n):
            headline = lines[i].strip()
            dedupe.accept(str(i), headline)
            if i == n - 1:
                dedupe.print_tree()
        print('----- Filtered headlines -----')
        dedupe.print_tree(original=False)  # show filtered headlines
        export = dedupe.export()
        with open('./.deduplicator.pkl', 'wb') as fh:
            pickle.dump(export, fh)
