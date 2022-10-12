#!/usr/bin/env bash

for file in _batch/*.zip
do
  python mod_extractor.py -q $file
done