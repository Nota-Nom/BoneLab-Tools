#!/usr/bin/env python3

# Copyright 2022 Nota-Nom

# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import argparse
import os
import zipfile
import tempfile

def main():
  parser = argparse.ArgumentParser(description='Determines a BoneLab mod\'s intended platform.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('ZipFile', nargs='+', help='Path of a mod zip file.')
  args = parser.parse_args()

  for path in args.ZipFile:
    if os.path.isfile(path):
      process_zip(path)
      
def process_zip(path):
  print('Processing [%s]...' % path)
  with zipfile.ZipFile(path, mode="r") as archive:
    palletList = []
    for line in archive.namelist():
      if "pallet.json" in line:
        palletList.append(line)
        with tempfile.TemporaryDirectory() as tmppath:
          # archive.extract(extract_path,package_name)
          archive.extractall(tmppath)
          for path, dirnames, filenames in os.walk(tmppath):
            for pname in filenames:
              if pname.startswith("catalog_") and pname.endswith(".json"):
                with open(os.path.join(path, pname), mode='r') as jsonfile:
                  for jsonline in jsonfile:
                    # is the string ".RuntimeModsPath}/" in the file?
                    if ".RuntimeModsPath}/" in jsonline:
                      print("QUEST")
                      break
                    # is the string ".RuntimeModsPath}\\" in the file?
                    if ".RuntimeModsPath}\\\\" in jsonline:
                      print("PCVR")
                      break

if __name__ == '__main__':
  main()
  # input("Press <Enter> to exit.")