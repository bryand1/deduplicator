#!/usr/bin/env python
# -*- coding: utf-8 -*-
import app

print("\nDeduplicator")
d = app.Deduplicator()

while True:
    _id = input("uniqueid: ")
    headline = input("headline: ")
    d.accept(_id, headline)
