#!/usr/bin/env python3

# Grab data files from Google docs

### Sources

TMPDIR='/tmp/01'

sources = {
  'nominees.csv': 'https://docs.google.com/spreadsheets/d/1rsQksqAJjyVzjs9pA49dRij-fC-hwG8nORMmlTx_9_I/export?format=csv&id=1rsQksqAJjyVzjs9pA49dRij-fC-hwG8nORMmlTx_9_I&gid=917247882',
  'events.csv': 'https://docs.google.com/spreadsheets/d/1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw/export?format=csv&id=1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw&gid=103989638',
  'media.csv': 'https://docs.google.com/spreadsheets/d/1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw/export?format=csv&id=1sIfYfey7D72Uyi1NOAxrAFbU6yn9HvIUjINCqYGHwMw&gid=1989058875',
  }


for syncfile in sources:
   print("file: {}, target: {}".format(
           syncfile,
           sources[syncfile],
           ))

"""

# From: https://stackabuse.com/download-files-with-python/

import requests

print('Beginning file download with requests')

url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
r = requests.get(url)

with open('/Users/scott/Downloads/cat3.jpg', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)

"""
