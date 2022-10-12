#!/usr/bin/env bash

for file in _batch/*.zip
do
  python mod_extractor.py -p $file
done