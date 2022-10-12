#!/usr/bin/env python3

import shutil
import argparse
import os
import zipfile
import tempfile

PCVR_KEYWORDS = ["Windows", "PC"]
QUEST_KEYWORDS = ["Quest", "Android"]

platform_is_quest = True

class FileNameHelper:
  
  def __init__(self, path):
    self.path = path.split('/')

  def get_root(self):
    return self.path[0]

  def pop_root(self):
    return self.path.pop(0)

  def __str__(self):
    return '/'.join(self.path)

  def get_package(self):
    """Returns path to extract and package name"""
    last_index = len(self.path) - 1
    if "pallet.json" != self.path[last_index]:
      raise Exception("`pallet.json` not found.")
    
    package_name = self.path[last_index - 1]
    self.path.pop()
    extract_path = '/'.join(self.path)
    # extract_path += '/'

    return extract_path, package_name

def main():
  parser = argparse.ArgumentParser(description='Extract BoneLab Mods.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-q', '--quest', action='store_true', help='Prefer Quest mods.')
  parser.add_argument('-p', '--pcvr', action='store_true', help='Prefer PCVR mods.')
  parser.add_argument('ZipFile', nargs='+', help='Path of a mod zip file.')
  args = parser.parse_args()

  if not (args.quest ^ args.pcvr):
    parser.error('Invalid platform preference.')

  if args.pcvr:
    platform_is_quest = False

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

    if len(palletList) == 0:
      return None # May return somthing in future

    selected_pallet = palletList[0]
    if len(palletList) == 2:
      selected_pallet = resolve_multiple(palletList)
    elif len(palletList) > 2:
      raise Exception("Can not resolve more than two pallets")
    
    package = FileNameHelper(selected_pallet)
    extract_path, package_name = package.get_package()
    
    with tempfile.TemporaryDirectory() as tmppath:
      # archive.extract(extract_path,package_name)
      # archive.extractall(package_name, [extract_path, ])
      for line in archive.namelist():
        if line.startswith(extract_path):
          archive.extract(line, tmppath)      
      shutil.move(tmppath + "/" + extract_path , package_name)

def resolve_multiple(palletList):
  left = FileNameHelper(palletList[0])
  right = FileNameHelper(palletList[1])

  shared_root = ""
  while left.get_root() == right.get_root():
    left.pop_root()
    shared_root += right.pop_root()

  keywords = QUEST_KEYWORDS
  if not platform_is_quest:
    keywords = PCVR_KEYWORDS
  
  for canidate in [left, right]:
    for kwd in keywords:
      if kwd.lower() in canidate.__str__().lower():
        return "%s/%s" % ( shared_root, canidate.__str__() )
  
  return None

if __name__ == '__main__':
  main()
  # input("Press <Enter> to exit.")