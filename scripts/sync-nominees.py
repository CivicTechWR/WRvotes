#!/usr/bin/env python3
"""
Try to add emails, phone numbers and object IDs to the existing set of
nominees. 

Paul "Worthless" Nijjar, 2018-07-20
"""

import csv, re
import unicodedata
import datetime

SRC_OFFICIAL="./data/Municipal_Elections_Nominees_2018.csv"
SRC_LOCAL="../docs/_data/sync/nominees.csv"

DEST="./data/munged-nominees.csv"

mergedict = {}

# ===== FUNCTIONS ======

def slugify(value):
  """ Normalizes strings. From
  https://stackoverflow.com/questions/5574042/string-slugification-in-python

  Note that this CAN cause collisions if you are using this as a hash
  key (which is what I am doing...)!
  """
  slug = unicodedata.normalize('NFKD', value)
  slug = re.sub(r'[^a-zA-Z0-9]+', '-', slug).strip('-')
  slug = re.sub(r'[-]+', '-', slug)
  slug = slug.lower()

  return slug

# ===== MAIN =======

with open(SRC_OFFICIAL, encoding='utf-8-sig') as official_csv:
    reader_official = csv.DictReader(official_csv)

    for row_o in reader_official:
        # print(row_o['Given_Names'], row_o['Last_Name'])
        row_key = slugify (
          "{} {}".format(row_o['Given_Names'], row_o['Last_Name'])
          ) 
        if row_key in mergedict:
            print("Uh oh! Key \"{}\" is already in dict! "
              "conflict?".format(row_key))
        else:
            mergedict[row_key] = row_o
            mergedict[row_key]['Website'] = None
            mergedict[row_key]['PositionUniqueName'] = None

with open(SRC_LOCAL) as local_csv:
    reader_local = csv.DictReader(local_csv)

    for row_l in reader_local:
        row_key = slugify (
          "{} {}".format(row_l['Given_Names'], row_l['Last_Name'])
          ) 
        
        if row_key not in mergedict:
            print("Uh oh! Local key value \"{}\" "
              "is not in the official open data source. Why?"
              .format(row_key))

        else:
          mergedict[row_key]['Website'] = row_l['Website']
          mergedict[row_key]['PositionUniqueName'] = \
            row_l['PositionUniqueName']

# Try to produce this in a reasonable order?
# Sigh. Why can't people use ISO dates?
mergekeys = sorted(mergedict, 
  key=lambda x: (
                 datetime.datetime.strptime(
                   mergedict[x]['Date_Filed'],
                   '%m/%d/%Y'
                   ),
                 mergedict[x]['Last_Name'],
                ))

#print(mergekeys)

fieldnames = [
  'Date_Filed', 
  'Nominated_Office',
  'Municipality',
  'Ward',
  'Last_Name',
  'Given_Names',
  'Phone1',
  'Email',
  'Website',
  'PositionUniqueName',
 ] 

with open(DEST, 'w', newline='') as out_csv:
    writer = csv.DictWriter(
      out_csv, 
      fieldnames=fieldnames,
      quoting=csv.QUOTE_MINIMAL,
      extrasaction='ignore',
      )


    writer.writeheader()

    for k in mergekeys:
        writer.writerow(mergedict[k])
    



#print(mergedict)


